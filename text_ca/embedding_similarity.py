"""
Embedding-Based Semantic Similarity for Textual Cellular Automata

This module provides tools for computing semantic similarity between textual 
cellular automaton states using high-dimensional embeddings. Traditional 
CA systems rely on exact string matching or simple edit distances, which 
fail when cells express similar ideas using different words ("market falls"
vs "equities decline"). 

By representing each cell's text as a 768-dimensional vector via 
nomic-embed-text (served through Ollama), we can compute cosine similarities 
to detect semantic adjacency. This enables:

- Neighborhood influence based on meaning rather than syntax
- Detection of conceptual clusters in CA state space
- Measurement of semantic drift over time steps
- Quantification of semantic diversity via entropy

Mathematically:
    - Cosine similarity: sim(a,b) = (a·b) / (||a|| ||b||)
    - Compatibility score: soft thresholded similarity
    - Clustering: greedy grouping above threshold
    - Drift: L2 distance between embedding trajectories
    - Entropy: Shannon entropy of similarity histogram bins
"""

import numpy as np
import json
import urllib.request
from typing import List, Set, Dict, Any, Optional
from urllib.error import URLError


def embed_text(text: str, ollama_url: str = 'http://localhost:11434/api/embeddings') -> np.ndarray:
    """
    Fetch embedding vector for input text using Ollama API.
    
    Args:
        text: Input text to embed
        ollama_url: URL endpoint for Ollama embeddings API
        
    Returns:
        768-dimensional embedding vector as numpy array
        
    Raises:
        URLError: If API request fails
    """
    data = {
        "model": "nomic-embed-text",
        "prompt": text
    }
    
    req = urllib.request.Request(
        ollama_url,
        data=json.dumps(data).encode('utf-8'),
        headers={'Content-Type': 'application/json'}
    )
    
    try:
        with urllib.request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            embedding = np.array(result['embedding'], dtype=np.float64)
            return embedding
    except URLError as e:
        raise URLError(f"Failed to get embedding from {ollama_url}: {e}")


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    """
    Compute cosine similarity between two vectors.
    
    Args:
        a: First vector (768-dim)
        b: Second vector (768-dim)
        
    Returns:
        Cosine similarity value in range [-1, 1]
    """
    # Normalize vectors
    norm_a = np.linalg.norm(a)
    norm_b = np.linalg.norm(b)
    
    if norm_a == 0 or norm_b == 0:
        return 0.0
    
    similarity = np.dot(a, b) / (norm_a * norm_b)
    return float(similarity)


def compute_neighborhood_similarity_matrix(cell_embeddings: np.ndarray) -> np.ndarray:
    """
    Compute pairwise cosine similarity matrix for all cell embeddings.
    
    Args:
        cell_embeddings: Array of shape (N, 768) containing embeddings
        
    Returns:
        Symmetric similarity matrix of shape (N, N)
    """
    n_cells = cell_embeddings.shape[0]
    similarity_matrix = np.zeros((n_cells, n_cells), dtype=np.float64)
    
    # Normalize all embeddings once
    norms = np.linalg.norm(cell_embeddings, axis=1, keepdims=True)
    normalized_embeddings = cell_embeddings / np.where(norms == 0, 1, norms)
    
    # Compute all pairwise similarities efficiently
    similarity_matrix = np.dot(normalized_embeddings, normalized_embeddings.T)
    
    return similarity_matrix


def semantic_compatibility(cell_a_embedding: np.ndarray, 
                          cell_b_embedding: np.ndarray, 
                          threshold: float = 0.7) -> float:
    """
    Compute soft semantic compatibility score between two cells.
    
    Uses sigmoid-like transformation of cosine similarity to produce
    smooth compatibility values that decay around the threshold.
    
    Args:
        cell_a_embedding: First cell embedding (768-dim)
        cell_b_embedding: Second cell embedding (768-dim)
        threshold: Compatibility threshold for meaningful similarity
        
    Returns:
        Compatibility score in range [0, 1]
    """
    sim = cosine_similarity(cell_a_embedding, cell_b_embedding)
    # Smooth sigmoid-like transition around threshold
    compatibility = 1.0 / (1.0 + np.exp(-10 * (sim - threshold)))
    return float(compatibility)


def detect_semantic_clusters(embeddings: np.ndarray, threshold: float = 0.8) -> List[Set[int]]:
    """
    Identify groups of semantically similar cells using greedy clustering.
    
    Each cluster contains cells mutually above similarity threshold.
    Greedy approach: process embeddings in order, assign to first qualifying cluster.
    
    Args:
        embeddings: Array of shape (N, 768) containing embeddings
        threshold: Minimum similarity for cluster membership
        
    Returns:
        List of sets, each containing indices of clustered cells
    """
    n_embeddings = embeddings.shape[0]
    clusters: List[Set[int]] = []
    assigned: Set[int] = set()
    
    # Precompute similarity matrix for efficiency
    similarity_matrix = compute_neighborhood_similarity_matrix(embeddings)
    
    for i in range(n_embeddings):
        if i in assigned:
            continue
            
        # Start new cluster with current embedding
        current_cluster: Set[int] = {i}
        assigned.add(i)
        
        # Check remaining embeddings for cluster membership
        for j in range(i + 1, n_embeddings):
            if j in assigned:
                continue
                
            # Check if j is compatible with all members of current cluster
            is_compatible = True
            for member_idx in current_cluster:
                if similarity_matrix[j, member_idx] < threshold:
                    is_compatible = False
                    break
                    
            if is_compatible:
                current_cluster.add(j)
                assigned.add(j)
                
        clusters.append(current_cluster)
        
    return clusters


def compute_semantic_drift(trajectory_embeddings: List[np.ndarray]) -> np.ndarray:
    """
    Measure semantic change across time steps in cellular automaton evolution.
    
    For each cell, computes cumulative L2 distance between consecutive embeddings.
    
    Args:
        trajectory_embeddings: List of arrays, each of shape (N, 768),
                               representing embeddings at each time step
                               
    Returns:
        Array of shape (N,) with total semantic drift per cell
    """
    if len(trajectory_embeddings) < 2:
        return np.array([0.0])
        
    n_cells = trajectory_embeddings[0].shape[0]
    drift_per_cell = np.zeros(n_cells, dtype=np.float64)
    
    # Compare consecutive time steps
    for t in range(len(trajectory_embeddings) - 1):
        emb_t0 = trajectory_embeddings[t]
        emb_t1 = trajectory_embeddings[t + 1]
        
        # Ensure consistent number of cells
        min_cells = min(emb_t0.shape[0], emb_t1.shape[0])
        for i in range(min_cells):
            diff = emb_t1[i] - emb_t0[i]
            distance = np.linalg.norm(diff)
            drift_per_cell[i] += distance
            
    return drift_per_cell


def semantic_entropy(embeddings: np.ndarray) -> float:
    """
    Calculate entropy of semantic similarity distribution.
    
    Discretizes cosine similarities into histogram bins and computes
    Shannon entropy to quantify diversity of semantic relationships.
    
    Args:
        embeddings: Array of shape (N, 768) containing embeddings
        
    Returns:
        Entropy value (higher means more diverse semantic relationships)
    """
    if embeddings.shape[0] < 2:
        return 0.0
        
    similarity_matrix = compute_neighborhood_similarity_matrix(embeddings)
    
    # Extract upper triangle (excluding diagonal) for unique pairwise sims
    triu_indices = np.triu_indices_from(similarity_matrix, k=1)
    similarities = similarity_matrix[triu_indices]
    
    # Discretize similarities into histogram bins
    bins = np.linspace(-1.0, 1.0, num=51)  # 50 bins
    hist_counts, _ = np.histogram(similarities, bins=bins)
    
    # Convert counts to probability distribution
    total_pairs = len(similarities)
    if total_pairs == 0:
        return 0.0
        
    probabilities = hist_counts.astype(np.float64) / total_pairs
    
    # Compute Shannon entropy
    # Avoid log(0) by filtering out zero probabilities
    nonzero_probs = probabilities[probabilities > 0]
    entropy = -np.sum(nonzero_probs * np.log2(nonzero_probs))
    
    return float(entropy)


if __name__ == "__main__":
    # Demo functionality with mock embeddings
    print("Demo: Semantic similarity analysis for Textual CA")
    
    # Create mock embeddings (normalized for realistic cosine sims)
    np.random.seed(42)
    n_cells = 5
    dim = 768
    mock_embeddings = []
    for i in range(n_cells):
        vec = np.random.randn(dim)
        vec /= np.linalg.norm(vec)
        mock_embeddings.append(vec)
    mock_embeddings = np.array(mock_embeddings)
    
    # Compute similarity matrix
    sim_matrix = compute_neighborhood_similarity_matrix(mock_embeddings)
    print("\nSimilarity Matrix:")
    print(sim_matrix.round(3))
    
    # Find semantic clusters
    clusters = detect_semantic_clusters(mock_embeddings, threshold=0.3)
    print(f"\nSemantic Clusters (threshold=0.3): {clusters}")
    
    # Test semantic compatibility
    comp_score = semantic_compatibility(mock_embeddings[0], mock_embeddings[1])
    print(f"\nCompatibility Score (cells 0,1): {comp_score:.3f}")
    
    # Simulate semantic drift
    trajectory = [
        mock_embeddings,
        mock_embeddings + np.random.normal(0, 0.1, size=(n_cells, dim)),
        mock_embeddings + np.random.normal(0, 0.2, size=(n_cells, dim))
    ]
    drift = compute_semantic_drift(trajectory)
    print(f"\nSemantic Drift per Cell: {drift.round(3)}")
    
    # Compute semantic entropy
    entropy = semantic_entropy(mock_embeddings)
    print(f"\nSemantic Entropy: {entropy:.3f}")
