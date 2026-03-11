# Textual Cellular Automata (TSCA)

A high-dimensional engine for modeling literary transformations using **Semantic Cellular Automata**.

This tool treats textual works (drama, fiction, poetry) as initial states and simulates their evolution through semantic rewrite rules. It was originally developed as part of the **NADJA** "Absolute Reality" engine to observe the transformation and "decay" of rhetorical motifs.

## Core Concepts

- **Text Cells:** Discrete units of text (lines, stanzas, paragraphs) with genre-aware metadata.
- **Semantic Fingerprints:** Multichannel state vectors representing Lakoff frames, sentiment, and structural markers.
- **Semantic CA:** Rules that govern how a cell's state changes based on its own state and its local neighborhood (context).
- **Rule Induction:** Tools to "learn" transformation rules from aligned source/target corpora (e.g., translating between different "voices" or genres).

## Features

- **Lakoff Taxonomy Integration:** Grounded in Conceptual Metaphor Theory, Frame Semantics, and Moral Foundations.
- **Induction Engine:** Automatically extract rewrite rules from aligned textual examples.
- **Multichannel Analytics:** Measure frame contagion rates, diversity, and compatibility across simulation runs.
- **Genre-Aware:** Native support for Drama, Fiction, Poetry, and Hybrid forms.

## Installation

```bash
pip install .
```

## Usage

### Running a Simulation

```python
from text_ca import run_minimal_text_ca, DEFAULT_TEXT_CA_RULES

# Define initial states (list of TextCellState objects)
initial_states = [...] 

# Run CA for 5 iterations
run_record = run_minimal_text_ca(initial_states, DEFAULT_TEXT_CA_RULES, iterations=5)

print(f"Final state iteration: {run_record.iteration_count}")
```

### Inducing Rules from a Corpus

```python
from text_ca import load_corpus_jsonl, induce_rules_from_corpus

# Load aligned source/target corpus
corpus = load_corpus_jsonl("path/to/corpus.jsonl")

# Induce rules
rules = induce_rules_from_corpus(corpus)

for rule in rules:
    print(f"Induced Rule: {rule.name}")
```

## Philosophical Note: The Mirror

In the NADJA ecosystem, this tool serves as **The Mirror**. It allows us to observe how rhetoric breaks down or evolves when stripped of its "Absolute Reality" grounding. By observing the "convulsive beauty" of these transformations, we gain insight into the internal mechanics of narrative itself.

## License

MIT
