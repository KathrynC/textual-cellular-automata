"""Lakoff taxonomy integration for financial semantic CA.
Implements George Lakoff's conceptual metaphor theory, frame semantics,
moral foundations theory, and prototype theory for financial domain mappings.

Reference frameworks:
- Conceptual Metaphor Theory (Lakoff & Johnson, 1980)
- Frame Semantics (Fillmore, 1982; Lakoff, 1987)
- Moral Foundations Theory (Haidt, 2012; Lakoff influence)
- Prototype Theory (Rosch, 1975; Lakoff application)
"""

from enum import Enum
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, field

# ============================================================================
# Lakoff Taxonomy Enums
# ============================================================================

class LakoffCategory(Enum):
    """Seven core categories of the Lakoff taxonomy for financial CA."""
    CONCEPTUAL_METAPHOR = "CONCEPTUAL_METAPHOR"  # Deep cognitive metaphors
    FRAME_SEMANTICS = "FRAME_SEMANTICS"          # Semantic frames structuring understanding
    MORAL_FOUNDATIONS = "MORAL_FOUNDATIONS"      # Moral/intuitive foundations
    EMOTIONAL_FRAMES = "EMOTIONAL_FRAMES"        # Emotion-based frames
    FINANCIAL_SPECIFIC = "FINANCIAL_SPECIFIC"    # Finance-domain specific frames
    SYSTEM_VULNERABILITY = "SYSTEM_VULNERABILITY"  # System vulnerability patterns
    VISUAL_DESIGN = "VISUAL_DESIGN"              # Visual design principles


class LakoffIcon(Enum):
    """Icon representations for each category (approximate Unicode)."""
    CONCEPTUAL_METAPHOR = "⎔"     # Hexagon for structured thought
    FRAME_SEMANTICS = "⎈"         # Gear for semantic machinery
    MORAL_FOUNDATIONS = "⚖"       # Scales for moral balance
    EMOTIONAL_FRAMES = "❤"        # Heart for emotions
    FINANCIAL_SPECIFIC = "₿"      # Currency symbol for finance
    SYSTEM_VULNERABILITY = "⚠"    # Warning sign for vulnerabilities
    VISUAL_DESIGN = "🎨"          # Artist palette for design


class AttractorType(Enum):
    """Types of dynamical attractors for financial regimes."""
    FIXED_POINT = "FIXED_POINT"           # Stable equilibrium
    LIMIT_CYCLE = "LIMIT_CYCLE"           # Periodic oscillation
    STRANGE_ATTRACTOR = "STRANGE_ATTRACTOR"  # Chaotic attractor
    NONE = "NONE"                         # No attractor (transient)
    MULTIPLE = "MULTIPLE"                 # Multiple coexisting attractors


class DynamicalSignature(Enum):
    """Characteristic dynamical behavior signatures."""
    FIXED_POINT = "FIXED_POINT"           # Stable, steady-state
    PERIODIC = "PERIODIC"                 # Regular oscillations
    CHAOTIC = "CHAOTIC"                   # Sensitive dependence, unpredictability
    TRANSIENT = "TRANSIENT"               # Temporary, decaying
    EXPLOSIVE = "EXPLOSIVE"               # Growing without bound
    DAMPED = "DAMPED"                     # Decaying oscillations to equilibrium


# ============================================================================
# Lakoff Frame Elements
# ============================================================================

@dataclass(frozen=True)
class LakoffFrame:
    """One Lakoff frame with financial mappings."""
    id: str  # e.g., "DECEPTION", "BALANCE", "CASCADE"
    name: str
    category: LakoffCategory
    description: str
    # Lakoff theoretical grounding
    theoretical_source: str  # "CMT", "Frame", "MFT", "Emotion", "Finance"
    prototype_centrality: float  # 0-1, typicality for financial markets
    # Financial domain mappings
    financial_keywords: Tuple[str, ...] = field(default_factory=tuple)
    ca_rule_triggers: Tuple[str, ...] = field(default_factory=tuple)
    ca_state_indicators: Tuple[str, ...] = field(default_factory=tuple)
    # Relationships to other frames
    opposite_frame: Optional[str] = None
    commonly_cooccurs: Tuple[str, ...] = field(default_factory=tuple)
    # Dynamical systems signatures (Beer-inspired)
    attractor_type: AttractorType = AttractorType.NONE
    basin_width: float = 0.5  # 0-1, width of attractor basin
    bifurcation_sensitivity: float = 0.5  # 0-1, sensitivity to parameter changes
    dynamical_signature: DynamicalSignature = DynamicalSignature.FIXED_POINT
    regime_transition_probability: float = 0.1  # 0-1, probability of transitioning to other regimes
    # Additional financial dynamics
    volatility_multiplier: float = 1.0  # Multiplier effect on volatility
    liquidity_impact: float = 0.0  # -1 to +1, impact on liquidity
    correlation_effect: float = 0.0  # -1 to +1, effect on cross-asset correlations
    # Visual representation
    icon_variant: Optional[str] = None
    
    @property
    def icon(self) -> str:
        """Icon representation with optional variant."""
        base_icon = LakoffIcon[self.category.name].value
        if self.icon_variant:
            return f"{base_icon}{self.icon_variant}"
        return base_icon


# ============================================================================
# CONCEPTUAL METAPHORS (Deep cognitive mappings)
# ============================================================================

CONCEPTUAL_METAPHOR_FRAMES = [
    LakoffFrame(
        id="CONTAINER",
        name="Container",
        category=LakoffCategory.CONCEPTUAL_METAPHOR,
        description="Markets as bounded spaces with inside/outside; positions as contained objects",
        theoretical_source="CMT",
        prototype_centrality=0.9,
        financial_keywords=("portfolio", "allocation", "in_out", "boundary", "containment"),
        ca_rule_triggers=("liquidity:adequate", "portfolio_value:moderate"),
        ca_state_indicators=("volatility:calm", "regime:steady"),
        opposite_frame="FLOW",
        commonly_cooccurs=("BALANCE", "LIMIT"),
        icon_variant="📦"
    ),
    LakoffFrame(
        id="JOURNEY",
        name="Journey",
        category=LakoffCategory.CONCEPTUAL_METAPHOR,
        description="Investing as a path with direction, progress, obstacles, and destinations",
        theoretical_source="CMT",
        prototype_centrality=0.8,
        financial_keywords=("trend", "momentum", "path", "destination", "progress"),
        ca_rule_triggers=("momentum:positive", "regime:bull"),
        ca_state_indicators=("momentum:strong", "portfolio_value:growth"),
        opposite_frame="STASIS",
        commonly_cooccurs=("GROWTH", "FORCE", "ATTRACTION"),
        icon_variant="🗺"
    ),
    LakoffFrame(
        id="FORCE",
        name="Force",
        category=LakoffCategory.CONCEPTUAL_METAPHOR,
        description="Market moves as physical forces: pushes, pulls, resistance, momentum",
        theoretical_source="CMT",
        prototype_centrality=0.7,
        financial_keywords=("momentum", "pressure", "resistance", "push", "pull"),
        ca_rule_triggers=("volatility:high", "leverage_ratio:high"),
        ca_state_indicators=("momentum:strong", "volatility:high"),
        opposite_frame="BALANCE",
        commonly_cooccurs=("AMPLIFICATION", "CASCADE", "PRESSURE"),
        icon_variant="⚡"
    ),
    LakoffFrame(
        id="BALANCE",
        name="Balance",
        category=LakoffCategory.CONCEPTUAL_METAPHOR,
        description="Markets seeking equilibrium; symmetry, fairness, proper proportions",
        theoretical_source="CMT",
        prototype_centrality=0.6,
        financial_keywords=("equilibrium", "fair_value", "mean_reversion", "symmetry"),
        ca_rule_triggers=("volatility:calm", "regime:steady"),
        ca_state_indicators=("momentum:neutral", "volatility:calm"),
        opposite_frame="IMBALANCE",
        commonly_cooccurs=("STASIS", "EQUILIBRIUM", "FAIRNESS"),
        icon_variant="⚖"
    ),
    LakoffFrame(
        id="WAR",
        name="War",
        category=LakoffCategory.CONCEPTUAL_METAPHOR,
        description="Trading as battle: attacks, defenses, strategies, winners/losers",
        theoretical_source="CMT",
        prototype_centrality=0.4,
        financial_keywords=("battle", "attack", "defense", "strategy", "winner", "loser"),
        ca_rule_triggers=("volatility:high", "regime:crisis"),
        ca_state_indicators=("volatility:extreme", "regime:crisis"),
        opposite_frame="COOPERATION",
        commonly_cooccurs=("CONFLICT", "DOMINATION", "COMPETITION"),
        icon_variant="⚔"
    ),
    LakoffFrame(
        id="GAME",
        name="Game",
        category=LakoffCategory.CONCEPTUAL_METAPHOR,
        description="Markets as game with rules, players, strategies, scores, outcomes",
        theoretical_source="CMT",
        prototype_centrality=0.5,
        financial_keywords=("game", "player", "strategy", "score", "outcome", "rules"),
        ca_rule_triggers=("regime:bull", "volatility:moderate"),
        ca_state_indicators=("momentum:positive", "regime:bull"),
        opposite_frame="SERIOUS_BUSINESS",
        commonly_cooccurs=("COMPETITION", "STRATEGY", "OUTCOME"),
        icon_variant="🎮"
    ),
    LakoffFrame(
        id="FLOW",
        name="Flow",
        category=LakoffCategory.CONCEPTUAL_METAPHOR,
        description="Capital as fluid: liquidity, currents, floods, droughts, circulation",
        theoretical_source="CMT",
        prototype_centrality=0.7,
        financial_keywords=("liquidity", "flow", "current", "flood", "drought", "circulation"),
        ca_rule_triggers=("liquidity:excess", "liquidity:critical"),
        ca_state_indicators=("liquidity:excess", "liquidity:critical"),
        opposite_frame="CONTAINER",
        commonly_cooccurs=("LIQUIDITY", "MOVEMENT", "CIRCULATION"),
        icon_variant="🌊"
    ),
    LakoffFrame(
        id="MACHINE",
        name="Machine",
        category=LakoffCategory.CONCEPTUAL_METAPHOR,
        description="Markets as mechanical systems: inputs, outputs, levers, breakdowns",
        theoretical_source="CMT",
        prototype_centrality=0.5,
        financial_keywords=("mechanism", "lever", "input", "output", "breakdown", "repair"),
        ca_rule_triggers=("leverage_ratio:extreme", "volatility:extreme"),
        ca_state_indicators=("leverage_ratio:extreme", "regime:crisis"),
        opposite_frame="ORGANISM",
        commonly_cooccurs=("AMPLIFICATION", "BREAKDOWN", "REPAIR"),
        icon_variant="⚙"
    ),
    LakoffFrame(
        id="ORGANISM",
        name="Organism",
        category=LakoffCategory.CONCEPTUAL_METAPHOR,
        description="Markets as living systems: growth, health, sickness, healing, death",
        theoretical_source="CMT",
        prototype_centrality=0.6,
        financial_keywords=("growth", "health", "sickness", "healing", "death", "vitality"),
        ca_rule_triggers=("regime:recovery", "portfolio_value:distressed"),
        ca_state_indicators=("regime:recovery", "portfolio_value:robust"),
        opposite_frame="MACHINE",
        commonly_cooccurs=("GROWTH", "HEALING", "DECAY"),
        icon_variant="🌱"
    ),
]


# ============================================================================
# FRAME SEMANTICS (Structuring understanding of situations)
# ============================================================================

FRAME_SEMANTICS_FRAMES = [
    LakoffFrame(
        id="CAUSATION",
        name="Causation",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Understanding events through cause-effect relationships",
        theoretical_source="Frame",
        prototype_centrality=0.8,
        financial_keywords=("cause", "effect", "trigger", "result", "because"),
        ca_rule_triggers=("regime:transition", "volatility:spike"),
        ca_state_indicators=("momentum:change", "volatility:change"),
        opposite_frame="RANDOMNESS",
        commonly_cooccurs=("FORCE", "CHANGE", "EFFECT"),
        icon_variant="⇨"
    ),
    LakoffFrame(
        id="CHANGE",
        name="Change",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Focus on transformation from one state to another",
        theoretical_source="Frame",
        prototype_centrality=0.7,
        financial_keywords=("change", "transform", "become", "transition", "evolution"),
        ca_rule_triggers=("regime:transition", "momentum:change"),
        ca_state_indicators=("regime:transition", "momentum:change"),
        opposite_frame="STASIS",
        commonly_cooccurs=("JOURNEY", "TRANSFORMATION", "EVOLUTION"),
        icon_variant="🔄"
    ),
    LakoffFrame(
        id="STATE",
        name="State",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Focus on stable conditions and properties",
        theoretical_source="Frame",
        prototype_centrality=0.6,
        financial_keywords=("state", "condition", "property", "stable", "static"),
        ca_rule_triggers=("volatility:calm", "regime:steady"),
        ca_state_indicators=("volatility:calm", "momentum:neutral"),
        opposite_frame="CHANGE",
        commonly_cooccurs=("STASIS", "BALANCE", "EQUILIBRIUM"),
        icon_variant="⏸"
    ),
    LakoffFrame(
        id="PROCESS",
        name="Process",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Focus on ongoing activities and procedures",
        theoretical_source="Frame",
        prototype_centrality=0.7,
        financial_keywords=("process", "procedure", "activity", "ongoing", "flow"),
        ca_rule_triggers=("momentum:positive", "volatility:moderate"),
        ca_state_indicators=("momentum:positive", "portfolio_value:growth"),
        opposite_frame="EVENT",
        commonly_cooccurs=("FLOW", "JOURNEY", "ACTIVITY"),
        icon_variant="⏩"
    ),
    LakoffFrame(
        id="EVENT",
        name="Event",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Focus on discrete occurrences with clear boundaries",
        theoretical_source="Frame",
        prototype_centrality=0.5,
        financial_keywords=("event", "occurrence", "happening", "discrete", "boundary"),
        ca_rule_triggers=("volatility:spike", "regime:break"),
        ca_state_indicators=("volatility:spike", "regime:break"),
        opposite_frame="PROCESS",
        commonly_cooccurs=("SHOCK", "BREAK", "OCCURRENCE"),
        icon_variant="❗"
    ),
    LakoffFrame(
        id="COMPARISON",
        name="Comparison",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Understanding through similarity/difference relations",
        theoretical_source="Frame",
        prototype_centrality=0.6,
        financial_keywords=("compare", "similar", "different", "relative", "benchmark"),
        ca_rule_triggers=("momentum:relative", "volatility:relative"),
        ca_state_indicators=("momentum:neutral", "volatility:moderate"),
        opposite_frame="ABSOLUTE",
        commonly_cooccurs=("BALANCE", "RELATIVE", "BENCHMARK"),
        icon_variant="⇔"
    ),
    LakoffFrame(
        id="POSSESSION",
        name="Possession",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Understanding through ownership and control relations",
        theoretical_source="Frame",
        prototype_centrality=0.7,
        financial_keywords=("own", "control", "possess", "belong", "property"),
        ca_rule_triggers=("portfolio_value:high", "leverage_ratio:low"),
        ca_state_indicators=("portfolio_value:surplus", "leverage_ratio:conservative"),
        opposite_frame="LOSS",
        commonly_cooccurs=("OWNERSHIP", "CONTROL", "PROPERTY"),
        icon_variant="🤲"
    ),
    LakoffFrame(
        id="LOSS",
        name="Loss",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Understanding through deprivation and absence",
        theoretical_source="Frame",
        prototype_centrality=0.3,
        financial_keywords=("loss", "deprivation", "absence", "lack", "deficit"),
        ca_rule_triggers=("portfolio_value:distressed", "regime:crisis"),
        ca_state_indicators=("portfolio_value:distressed", "regime:crisis"),
        opposite_frame="POSSESSION",
        commonly_cooccurs=("DEPRIVATION", "ABSENCE", "DEFICIT"),
        icon_variant="💔"
    ),
    LakoffFrame(
        id="POWER_ASYMMETRY",
        name="Power Asymmetry",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Asymmetric power relations where influence flows more from high-power agents to low-power agents",
        theoretical_source="Frame",
        prototype_centrality=0.5,
        financial_keywords=("power", "asymmetry", "influence", "hierarchy", "dominance"),
        ca_rule_triggers=("trust:low", "institutional_quality:low"),
        ca_state_indicators=("trust:low", "institutional_quality:low"),
        opposite_frame=None,
        commonly_cooccurs=("AUTHORITY", "DOMINATION", "COERCION"),
        icon_variant="⚖"
    ),
    LakoffFrame(
        id="CENTRALIZATION",
        name="Centralization",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Connectivity concentrated around central nodes; neighborhood limited to hierarchical proximity",
        theoretical_source="Frame",
        prototype_centrality=0.4,
        financial_keywords=("centralization", "hierarchy", "hub", "core", "periphery"),
        ca_rule_triggers=("correlation:high", "herding:high"),
        ca_state_indicators=("correlation:high", "herding:high"),
        opposite_frame=None,
        commonly_cooccurs=("AUTHORITY", "LOYALTY", "GROUP"),
        icon_variant="🎯"
    ),
    LakoffFrame(
        id="OPACITY",
        name="Opacity",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Information obscurity; neighbors' states are less observable, reducing influence weight",
        theoretical_source="Frame",
        prototype_centrality=0.3,
        financial_keywords=("opacity", "obscurity", "hidden", "unobservable", "uncertainty"),
        ca_rule_triggers=("transparency:low", "trust:low"),
        ca_state_indicators=("transparency:low", "trust:low"),
        opposite_frame="TRANSPARENCY",
        commonly_cooccurs=("DECEPTION", "SECRECY", "UNCERTAINTY"),
        icon_variant="🌫"
    ),
    LakoffFrame(
        id="ASSUMPTION_VIOLATION",
        name="Assumption Violation",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Violation of idealized cognitive model (ICM) assumptions; pattern assumptions break down",
        theoretical_source="Frame",
        prototype_centrality=0.2,
        financial_keywords=("assumption_violation", "model_breakdown", "assumption_failure", "icm_violation"),
        ca_rule_triggers=("trust:low", "transparency:low"),
        ca_state_indicators=("trust:low", "transparency:low"),
        opposite_frame=None,
        commonly_cooccurs=("DECEPTION", "BREAKDOWN", "UNCERTAINTY"),
        icon_variant="⚠"
    ),
    LakoffFrame(
        id="MODEL_BREAKDOWN",
        name="Model Breakdown",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Complete failure of cognitive model; predictive relationships collapse",
        theoretical_source="Frame",
        prototype_centrality=0.1,
        financial_keywords=("model_breakdown", "predictive_failure", "cognitive_collapse", "framework_failure"),
        ca_rule_triggers=("trust:critical", "transparency:critical"),
        ca_state_indicators=("trust:critical", "transparency:critical"),
        opposite_frame="MODEL_COHERENCE",
        commonly_cooccurs=("DECEPTION", "ASSUMPTION_VIOLATION", "BREAKDOWN"),
        icon_variant="💥"
    ),
    LakoffFrame(
        id="MODEL_COHERENCE",
        name="Model Coherence",
        category=LakoffCategory.FRAME_SEMANTICS,
        description="Cognitive model assumptions hold; predictive relationships remain reliable",
        theoretical_source="Frame",
        prototype_centrality=0.7,
        financial_keywords=("model_coherence", "predictive_accuracy", "assumption_holding", "framework_stable"),
        ca_rule_triggers=("trust:high", "transparency:high"),
        ca_state_indicators=("trust:high", "transparency:high"),
        opposite_frame="MODEL_BREAKDOWN",
        commonly_cooccurs=("TRANSPARENCY", "INTEGRITY", "STABILITY"),
        icon_variant="🔮"
    ),
]


# ============================================================================
# MORAL FOUNDATIONS (Intuitive ethical frames)
# ============================================================================

MORAL_FOUNDATIONS_FRAMES = [
    LakoffFrame(
        id="AUTHORITY",
        name="Authority",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Respect for hierarchy, leadership, tradition, and legitimate authority",
        theoretical_source="MFT",
        prototype_centrality=0.5,
        financial_keywords=("authority", "hierarchy", "leadership", "tradition", "legitimate"),
        ca_rule_triggers=("regime:stable", "volatility:low"),
        ca_state_indicators=("regime:stable", "volatility:calm"),
        opposite_frame="SUBVERSION",
        commonly_cooccurs=("ORDER", "LEGITIMACY", "HIERARCHY"),
        icon_variant="👑"
    ),
    LakoffFrame(
        id="SUBVERSION",
        name="Subversion",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Challenge to authority, hierarchy, and established order",
        theoretical_source="MFT",
        prototype_centrality=0.3,
        financial_keywords=("subversion", "rebellion", "challenge", "disruption", "revolution"),
        ca_rule_triggers=("regime:transition", "volatility:high"),
        ca_state_indicators=("regime:transition", "volatility:high"),
        opposite_frame="AUTHORITY",
        commonly_cooccurs=("DISRUPTION", "CHANGE", "REVOLUTION"),
        icon_variant="⚒"
    ),
    LakoffFrame(
        id="FAIRNESS",
        name="Fairness",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Justice, equality, proportionality, and cheating detection",
        theoretical_source="MFT",
        prototype_centrality=0.7,
        financial_keywords=("fair", "just", "equal", "proportional", "cheating"),
        ca_rule_triggers=("credit_spread:normal", "volatility:moderate"),
        ca_state_indicators=("credit_spread:normal", "volatility:moderate"),
        opposite_frame="UNFAIRNESS",
        commonly_cooccurs=("JUSTICE", "EQUITY", "BALANCE"),
        icon_variant="⚖"
    ),
    LakoffFrame(
        id="UNFAIRNESS",
        name="Unfairness",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Injustice, inequality, cheating, exploitation",
        theoretical_source="MFT",
        prototype_centrality=0.3,
        financial_keywords=("unfair", "unjust", "inequality", "cheat", "exploit"),
        ca_rule_triggers=("credit_spread:wide", "regime:crisis"),
        ca_state_indicators=("credit_spread:wide", "regime:crisis"),
        opposite_frame="FAIRNESS",
        commonly_cooccurs=("DECEPTION", "EXPLOITATION", "CORRUPTION"),
        icon_variant="⚡"
    ),
    LakoffFrame(
        id="LOYALTY",
        name="Loyalty",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Group allegiance, patriotism, teamwork, betrayal detection",
        theoretical_source="MFT",
        prototype_centrality=0.4,
        financial_keywords=("loyalty", "allegiance", "team", "betrayal", "group"),
        ca_rule_triggers=("correlation:high", "herding:high"),
        ca_state_indicators=("correlation:high", "herding:high"),
        opposite_frame="BETRAYAL",
        commonly_cooccurs=("GROUP", "ALLEGIANCE", "TEAM"),
        icon_variant="🤝"
    ),
    LakoffFrame(
        id="BETRAYAL",
        name="Betrayal",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Treachery, disloyalty, defection, backstabbing",
        theoretical_source="MFT",
        prototype_centrality=0.2,
        financial_keywords=("betrayal", "treachery", "disloyal", "defect", "backstab"),
        ca_rule_triggers=("correlation:break", "trust:low"),
        ca_state_indicators=("correlation:break", "trust:low"),
        opposite_frame="LOYALTY",
        commonly_cooccurs=("DECEPTION", "TREACHERY", "DISLOYALTY"),
        icon_variant="🗡"
    ),
    LakoffFrame(
        id="CARE",
        name="Care",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Nurturance, protection, harm prevention, compassion",
        theoretical_source="MFT",
        prototype_centrality=0.6,
        financial_keywords=("care", "protect", "nurture", "compassion", "harm_prevent"),
        ca_rule_triggers=("regime:recovery", "liquidity:adequate"),
        ca_state_indicators=("regime:recovery", "liquidity:adequate"),
        opposite_frame="HARM",
        commonly_cooccurs=("PROTECTION", "NURTURANCE", "COMPASSION"),
        icon_variant="🛡"
    ),
    LakoffFrame(
        id="HARM",
        name="Harm",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Cruelty, violence, suffering, destruction",
        theoretical_source="MFT",
        prototype_centrality=0.2,
        financial_keywords=("harm", "cruel", "violent", "suffer", "destroy"),
        ca_rule_triggers=("regime:crisis", "portfolio_value:distressed"),
        ca_state_indicators=("regime:crisis", "portfolio_value:distressed"),
        opposite_frame="CARE",
        commonly_cooccurs=("VIOLENCE", "DESTRUCTION", "SUFFERING"),
        icon_variant="💀"
    ),
    LakoffFrame(
        id="SANCTITY",
        name="Sanctity",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Purity, cleanliness, pollution, degradation, sacredness",
        theoretical_source="MFT",
        prototype_centrality=0.3,
        financial_keywords=("pure", "clean", "pollute", "degrade", "sacred"),
        ca_rule_triggers=("trust:high", "transparency:high"),
        ca_state_indicators=("trust:high", "transparency:high"),
        opposite_frame="DEGRADATION",
        commonly_cooccurs=("PURITY", "CLEANLINESS", "TRUST"),
        icon_variant="✨"
    ),
    LakoffFrame(
        id="DEGRADATION",
        name="Degradation",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Pollution, contamination, corruption, defilement",
        theoretical_source="MFT",
        prototype_centrality=0.2,
        financial_keywords=("degrade", "pollute", "contaminate", "corrupt", "defile"),
        ca_rule_triggers=("trust:low", "transparency:low"),
        ca_state_indicators=("trust:low", "transparency:low"),
        opposite_frame="SANCTITY",
        commonly_cooccurs=("CORRUPTION", "POLLUTION", "CONTAMINATION"),
        icon_variant="☣"
    ),
    LakoffFrame(
        id="VIOLENCE",
        name="Violence",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Physical force intended to hurt, damage, or kill",
        theoretical_source="MFT",
        prototype_centrality=0.1,
        financial_keywords=("violence", "force", "aggression", "brutality", "coercion"),
        ca_rule_triggers=("regime:crisis", "portfolio_value:distressed"),
        ca_state_indicators=("regime:crisis", "portfolio_value:distressed"),
        opposite_frame="NONVIOLENCE",
        commonly_cooccurs=("HARM", "DESTRUCTION", "FEAR"),
        icon_variant="👊"
    ),
    LakoffFrame(
        id="ATROCITY",
        name="Atrocity",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Extremely cruel or violent act, often involving civilians",
        theoretical_source="MFT",
        prototype_centrality=0.05,
        financial_keywords=("atrocity", "war_crime", "crimes_against_humanity", "massacre", "brutality"),
        ca_rule_triggers=("trust:low", "institutional_quality:low"),
        ca_state_indicators=("trust:low", "institutional_quality:low"),
        opposite_frame="JUSTICE",
        commonly_cooccurs=("VIOLENCE", "GENOCIDE", "DEGRADATION"),
        icon_variant="⚰"
    ),
    LakoffFrame(
        id="OPPRESSION",
        name="Oppression",
        category=LakoffCategory.MORAL_FOUNDATIONS,
        description="Prolonged cruel or unjust treatment or control",
        theoretical_source="MFT",
        prototype_centrality=0.15,
        financial_keywords=("oppression", "tyranny", "authoritarian", "repression", "subjugation"),
        ca_rule_triggers=("trust:low", "institutional_quality:low"),
        ca_state_indicators=("trust:low", "institutional_quality:low"),
        opposite_frame="LIBERATION",
        commonly_cooccurs=("AUTHORITY", "COERCION", "FEAR"),
        icon_variant="⛓"
    ),
]


# ============================================================================
# EMOTIONAL FRAMES (Affective/emotional structuring)
# ============================================================================

EMOTIONAL_FRAMES = [
    LakoffFrame(
        id="FEAR",
        name="Fear",
        category=LakoffCategory.EMOTIONAL_FRAMES,
        description="Anxiety, threat perception, risk aversion, safety seeking",
        theoretical_source="Emotion",
        prototype_centrality=0.4,
        financial_keywords=("fear", "anxiety", "threat", "risk_averse", "safety"),
        ca_rule_triggers=("volatility:high", "regime:crisis"),
        ca_state_indicators=("volatility:high", "regime:crisis"),
        opposite_frame="CONFIDENCE",
        commonly_cooccurs=("RISK", "THREAT", "ANXIETY"),
        icon_variant="😨"
    ),
    LakoffFrame(
        id="CONFIDENCE",
        name="Confidence",
        category=LakoffCategory.EMOTIONAL_FRAMES,
        description="Trust, certainty, optimism, self-assurance",
        theoretical_source="Emotion",
        prototype_centrality=0.6,
        financial_keywords=("confidence", "trust", "certainty", "optimism", "assurance"),
        ca_rule_triggers=("regime:bull", "momentum:positive"),
        ca_state_indicators=("regime:bull", "momentum:positive"),
        opposite_frame="FEAR",
        commonly_cooccurs=("TRUST", "OPTIMISM", "CERTAINTY"),
        icon_variant="😊"
    ),
    LakoffFrame(
        id="HOPE",
        name="Hope",
        category=LakoffCategory.EMOTIONAL_FRAMES,
        description="Positive expectation, aspiration, looking forward",
        theoretical_source="Emotion",
        prototype_centrality=0.5,
        financial_keywords=("hope", "expectation", "aspiration", "forward", "positive"),
        ca_rule_triggers=("regime:recovery", "momentum:turning"),
        ca_state_indicators=("regime:recovery", "momentum:turning"),
        opposite_frame="DESPAIR",
        commonly_cooccurs=("OPTIMISM", "EXPECTATION", "ASPIRATION"),
        icon_variant="🌟"
    ),
    LakoffFrame(
        id="DESPAIR",
        name="Despair",
        category=LakoffCategory.EMOTIONAL_FRAMES,
        description="Hopelessness, resignation, giving up, bleak outlook",
        theoretical_source="Emotion",
        prototype_centrality=0.2,
        financial_keywords=("despair", "hopeless", "resign", "give_up", "bleak"),
        ca_rule_triggers=("portfolio_value:distressed", "regime:crisis"),
        ca_state_indicators=("portfolio_value:distressed", "regime:crisis"),
        opposite_frame="HOPE",
        commonly_cooccurs=("HOPELESSNESS", "RESIGNATION", "BLEAK"),
        icon_variant="😞"
    ),
    LakoffFrame(
        id="ANGER",
        name="Anger",
        category=LakoffCategory.EMOTIONAL_FRAMES,
        description="Frustration, outrage, blame, retribution seeking",
        theoretical_source="Emotion",
        prototype_centrality=0.3,
        financial_keywords=("anger", "frustration", "outrage", "blame", "retribution"),
        ca_rule_triggers=("volatility:spike", "regime:break"),
        ca_state_indicators=("volatility:spike", "regime:break"),
        opposite_frame="ACCEPTANCE",
        commonly_cooccurs=("FRUSTRATION", "OUTRAGE", "BLAME"),
        icon_variant="😠"
    ),
    LakoffFrame(
        id="ACCEPTANCE",
        name="Acceptance",
        category=LakoffCategory.EMOTIONAL_FRAMES,
        description="Resignation, peace, letting go, coming to terms",
        theoretical_source="Emotion",
        prototype_centrality=0.4,
        financial_keywords=("accept", "resign", "peace", "let_go", "terms"),
        ca_rule_triggers=("volatility:calm", "regime:steady"),
        ca_state_indicators=("volatility:calm", "regime:steady"),
        opposite_frame="ANGER",
        commonly_cooccurs=("PEACE", "RESIGNATION", "TERMS"),
        icon_variant="🙏"
    ),
    LakoffFrame(
        id="GREED",
        name="Greed",
        category=LakoffCategory.EMOTIONAL_FRAMES,
        description="Excessive desire, appetite for more, insatiability",
        theoretical_source="Emotion",
        prototype_centrality=0.3,
        financial_keywords=("greed", "desire", "appetite", "insatiable", "excess"),
        ca_rule_triggers=("leverage_ratio:extreme", "momentum:strong"),
        ca_state_indicators=("leverage_ratio:extreme", "momentum:strong"),
        opposite_frame="CAUTION",
        commonly_cooccurs=("DESIRE", "EXCESS", "INSATIABLE"),
        icon_variant="💰"
    ),
    LakoffFrame(
        id="CAUTION",
        name="Caution",
        category=LakoffCategory.EMOTIONAL_FRAMES,
        description="Prudence, carefulness, restraint, risk awareness",
        theoretical_source="Emotion",
        prototype_centrality=0.5,
        financial_keywords=("caution", "prudent", "careful", "restraint", "risk_aware"),
        ca_rule_triggers=("leverage_ratio:conservative", "volatility:calm"),
        ca_state_indicators=("leverage_ratio:conservative", "volatility:calm"),
        opposite_frame="GREED",
        commonly_cooccurs=("PRUDENCE", "RESTRAINT", "RISK_AWARENESS"),
        icon_variant="⚠"
    ),
    LakoffFrame(
        id="PANIC",
        name="Panic",
        category=LakoffCategory.EMOTIONAL_FRAMES,
        description="Sudden overwhelming fear, irrational action, herd behavior",
        theoretical_source="Emotion",
        prototype_centrality=0.2,
        financial_keywords=("panic", "overwhelm", "irrational", "herd", "sudden"),
        ca_rule_triggers=("volatility:extreme", "regime:crisis"),
        ca_state_indicators=("volatility:extreme", "regime:crisis"),
        opposite_frame="CALM",
        commonly_cooccurs=("FEAR", "HERD", "IRRATIONAL"),
        icon_variant="😱"
    ),
    LakoffFrame(
        id="CALM",
        name="Calm",
        category=LakoffCategory.EMOTIONAL_FRAMES,
        description="Serenity, composure, level-headedness, rationality",
        theoretical_source="Emotion",
        prototype_centrality=0.5,
        financial_keywords=("calm", "serene", "composed", "level", "rational"),
        ca_rule_triggers=("volatility:calm", "regime:steady"),
        ca_state_indicators=("volatility:calm", "regime:steady"),
        opposite_frame="PANIC",
        commonly_cooccurs=("SERENITY", "COMPOSURE", "RATIONALITY"),
        icon_variant="😌"
    ),
]


# ============================================================================
# FINANCIAL-SPECIFIC FRAMES (Domain-specific financial cognition)
# ============================================================================

FINANCIAL_SPECIFIC_FRAMES = [
    LakoffFrame(
        id="RISK",
        name="Risk",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Uncertainty, probability, exposure, danger, potential loss",
        theoretical_source="Finance",
        prototype_centrality=0.7,
        financial_keywords=("risk", "uncertainty", "probability", "exposure", "danger"),
        ca_rule_triggers=("volatility:high", "leverage_ratio:high"),
        ca_state_indicators=("volatility:high", "leverage_ratio:high"),
        opposite_frame="SAFETY",
        commonly_cooccurs=("UNCERTAINTY", "DANGER", "EXPOSURE"),
        icon_variant="🎲"
    ),
    LakoffFrame(
        id="SAFETY",
        name="Safety",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Security, protection, certainty, preservation",
        theoretical_source="Finance",
        prototype_centrality=0.6,
        financial_keywords=("safety", "secure", "protect", "certain", "preserve"),
        ca_rule_triggers=("volatility:calm", "leverage_ratio:low"),
        ca_state_indicators=("volatility:calm", "leverage_ratio:low"),
        opposite_frame="RISK",
        commonly_cooccurs=("SECURITY", "PROTECTION", "CERTAINTY"),
        icon_variant="🛡"
    ),
    LakoffFrame(
        id="RETURN",
        name="Return",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Gain, profit, yield, reward, compensation",
        theoretical_source="Finance",
        prototype_centrality=0.8,
        financial_keywords=("return", "gain", "profit", "yield", "reward"),
        ca_rule_triggers=("momentum:positive", "portfolio_value:growth"),
        ca_state_indicators=("momentum:positive", "portfolio_value:growth"),
        opposite_frame="LOSS_FINANCIAL",
        commonly_cooccurs=("GAIN", "PROFIT", "REWARD"),
        icon_variant="📈"
    ),
    LakoffFrame(
        id="LOSS_FINANCIAL",
        name="Loss (Financial)",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Financial loss, drawdown, negative return, cost",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("loss", "drawdown", "negative", "cost", "deficit"),
        ca_rule_triggers=("portfolio_value:distressed", "momentum:negative"),
        ca_state_indicators=("portfolio_value:distressed", "momentum:negative"),
        opposite_frame="RETURN",
        commonly_cooccurs=("DRAWDOWN", "COST", "DEFICIT"),
        icon_variant="📉"
    ),
    LakoffFrame(
        id="LEVERAGE",
        name="Leverage",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Amplification, magnification, debt, gearing",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("leverage", "amplify", "magnify", "debt", "gearing"),
        ca_rule_triggers=("leverage_ratio:high", "leverage_ratio:extreme"),
        ca_state_indicators=("leverage_ratio:high", "leverage_ratio:extreme"),
        opposite_frame="DELEVERAGE",
        commonly_cooccurs=("AMPLIFICATION", "DEBT", "GEARING"),
        icon_variant="📏"
    ),
    LakoffFrame(
        id="DELEVERAGE",
        name="Deleverage",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Reduction, unwinding, paying down, risk reduction",
        theoretical_source="Finance",
        prototype_centrality=0.4,
        financial_keywords=("deleverage", "reduce", "unwind", "pay_down", "risk_reduce"),
        ca_rule_triggers=("leverage_ratio:decreasing", "regime:crisis"),
        ca_state_indicators=("leverage_ratio:decreasing", "regime:crisis"),
        opposite_frame="LEVERAGE",
        commonly_cooccurs=("REDUCTION", "UNWIND", "RISK_REDUCTION"),
        icon_variant="📐"
    ),
    LakoffFrame(
        id="VOLATILITY",
        name="Volatility",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Variability, fluctuation, instability, uncertainty",
        theoretical_source="Finance",
        prototype_centrality=0.6,
        financial_keywords=("volatility", "variable", "fluctuate", "unstable", "uncertain"),
        ca_rule_triggers=("volatility:high", "volatility:extreme"),
        ca_state_indicators=("volatility:high", "volatility:extreme"),
        opposite_frame="STABILITY",
        commonly_cooccurs=("VARIABILITY", "FLUCTUATION", "INSTABILITY"),
        icon_variant="🌊"
    ),
    LakoffFrame(
        id="STABILITY",
        name="Stability",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Steadiness, consistency, predictability, reliability",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("stability", "steady", "consistent", "predictable", "reliable"),
        ca_rule_triggers=("volatility:calm", "regime:steady"),
        ca_state_indicators=("volatility:calm", "regime:steady"),
        opposite_frame="VOLATILITY",
        commonly_cooccurs=("STEADINESS", "CONSISTENCY", "PREDICTABILITY"),
        icon_variant="🏔"
    ),
    LakoffFrame(
        id="LIQUIDITY",
        name="Liquidity",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Fluidity, convertibility, availability, market depth",
        theoretical_source="Finance",
        prototype_centrality=0.7,
        financial_keywords=("liquidity", "fluid", "convertible", "available", "market_depth"),
        ca_rule_triggers=("liquidity:adequate", "liquidity:excess"),
        ca_state_indicators=("liquidity:adequate", "liquidity:excess"),
        opposite_frame="ILLIQUIDITY",
        commonly_cooccurs=("FLUIDITY", "AVAILABILITY", "MARKET_DEPTH"),
        icon_variant="💧"
    ),
    LakoffFrame(
        id="ILLIQUIDITY",
        name="Illiquidity",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Illiquidity, frozen, stuck, unavailable, market thinness",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("illiquidity", "frozen", "stuck", "unavailable", "market_thin"),
        ca_rule_triggers=("liquidity:critical", "liquidity:tight"),
        ca_state_indicators=("liquidity:critical", "liquidity:tight"),
        opposite_frame="LIQUIDITY",
        commonly_cooccurs=("FROZEN", "STUCK", "UNAVAILABLE"),
        icon_variant="🧊"
    ),
    LakoffFrame(
        id="DECEPTION",
        name="Deception",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Fraud, manipulation, misrepresentation, hiding truth",
        theoretical_source="Finance",
        prototype_centrality=0.2,
        financial_keywords=("deception", "fraud", "manipulate", "misrepresent", "hide"),
        ca_rule_triggers=("trust:low", "transparency:low"),
        ca_state_indicators=("trust:low", "transparency:low"),
        opposite_frame="TRANSPARENCY",
        commonly_cooccurs=("FRAUD", "MANIPULATION", "HIDING"),
        icon_variant="🎭"
    ),
    LakoffFrame(
        id="TRANSPARENCY",
        name="Transparency",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Openness, clarity, visibility, honesty, disclosure",
        theoretical_source="Finance",
        prototype_centrality=0.6,
        financial_keywords=("transparency", "open", "clear", "visible", "honest"),
        ca_rule_triggers=("trust:high", "transparency:high"),
        ca_state_indicators=("trust:high", "transparency:high"),
        opposite_frame="DECEPTION",
        commonly_cooccurs=("OPENNESS", "CLARITY", "HONESTY"),
        icon_variant="🔍"
    ),
    LakoffFrame(
        id="CORRUPTION",
        name="Corruption",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Abuse of power, bribery, cronyism, institutional decay",
        theoretical_source="Finance",
        prototype_centrality=0.2,
        financial_keywords=("corruption", "abuse", "bribery", "cronyism", "decay"),
        ca_rule_triggers=("trust:low", "institutional_quality:low"),
        ca_state_indicators=("trust:low", "institutional_quality:low"),
        opposite_frame="INTEGRITY",
        commonly_cooccurs=("ABUSE", "BRIBERY", "DECAY"),
        icon_variant="🕳"
    ),
    LakoffFrame(
        id="INTEGRITY",
        name="Integrity",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Honesty, principle, ethics, soundness, wholeness",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("integrity", "honest", "principle", "ethics", "sound"),
        ca_rule_triggers=("trust:high", "institutional_quality:high"),
        ca_state_indicators=("trust:high", "institutional_quality:high"),
        opposite_frame="CORRUPTION",
        commonly_cooccurs=("HONESTY", "ETHICS", "SOUNDNESS"),
        icon_variant="⭐"
    ),
    LakoffFrame(
        id="CASCADE",
        name="Cascade",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Chain reaction, domino effect, contagion, systemic risk",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("cascade", "chain", "domino", "contagion", "systemic"),
        ca_rule_triggers=("volatility:extreme", "leverage_ratio:extreme"),
        ca_state_indicators=("volatility:extreme", "leverage_ratio:extreme"),
        opposite_frame="CONTAINMENT",
        commonly_cooccurs=("CHAIN_REACTION", "CONTAGION", "SYSTEMIC"),
        icon_variant="🎯"
    ),
    LakoffFrame(
        id="CONTAINMENT",
        name="Containment",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Isolation, limitation, control, firewall, circuit breaker",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("containment", "isolate", "limit", "control", "firewall"),
        ca_rule_triggers=("volatility:calm", "regime:steady"),
        ca_state_indicators=("volatility:calm", "regime:steady"),
        opposite_frame="CASCADE",
        commonly_cooccurs=("ISOLATION", "LIMITATION", "CONTROL"),
        icon_variant="🚧"
    ),
    LakoffFrame(
        id="ATTRACTOR",
        name="Attractor",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Positive force drawing capital or attention; appealing position or state",
        theoretical_source="Finance",
        prototype_centrality=0.6,
        financial_keywords=("attractor", "appeal", "draw", "positive_force", "magnet"),
        ca_rule_triggers=("momentum:positive", "regime:bull"),
        ca_state_indicators=("momentum:positive", "regime:bull"),
        opposite_frame="REPELLER",
        commonly_cooccurs=("GROWTH", "FORCE", "ATTRACTION"),
        icon_variant="🧲"
    ),
    LakoffFrame(
        id="AMPLIFICATION",
        name="Amplification",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Magnification of effects through leverage, feedback, or sentiment",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("amplification", "magnify", "feedback", "leverage", "multiply"),
        ca_rule_triggers=("leverage_ratio:high", "volatility:high"),
        ca_state_indicators=("leverage_ratio:high", "volatility:high"),
        opposite_frame="DAMPENING",
        commonly_cooccurs=("LEVERAGE", "FEEDBACK", "MULTIPLICATION"),
        icon_variant="🔊"
    ),
    LakoffFrame(
        id="RECOVERY",
        name="Recovery",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Healing, rebound, restoration after decline or crisis",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("recovery", "rebound", "healing", "restoration", "bounce"),
        ca_rule_triggers=("regime:recovery", "portfolio_value:increasing"),
        ca_state_indicators=("regime:recovery", "portfolio_value:increasing"),
        opposite_frame="DECLINE",
        commonly_cooccurs=("HEALING", "REBOUND", "RESTORATION"),
        icon_variant="🔄"
    ),
    LakoffFrame(
        id="GROWTH_FINANCIAL",
        name="Growth (Financial)",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Expansion, increase, appreciation, positive development",
        theoretical_source="Finance",
        prototype_centrality=0.7,
        financial_keywords=("growth", "expansion", "increase", "appreciation", "develop"),
        ca_rule_triggers=("portfolio_value:growth", "momentum:positive"),
        ca_state_indicators=("portfolio_value:growth", "momentum:positive"),
        opposite_frame="DECLINE",
        commonly_cooccurs=("EXPANSION", "INCREASE", "APPRECIATION"),
        icon_variant="📊"
    ),
    LakoffFrame(
        id="COERCION",
        name="Coercion",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Force, pressure, compulsion, undue influence",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("coercion", "force", "pressure", "compulsion", "influence"),
        ca_rule_triggers=("trust:low", "institutional_quality:low"),
        ca_state_indicators=("trust:low", "institutional_quality:low"),
        opposite_frame="VOLUNTARY",
        commonly_cooccurs=("PRESSURE", "FORCE", "COMPULSION"),
        icon_variant="🤜"
    ),
    LakoffFrame(
        id="MILITARY_CONFLICT",
        name="Military Conflict",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Actual warfare, armed conflict, combat operations affecting markets",
        theoretical_source="Finance",
        prototype_centrality=0.2,
        financial_keywords=("war", "military", "combat", "invasion", "armed_conflict", "defense_stocks"),
        ca_rule_triggers=("regime:crisis", "volatility:extreme"),
        ca_state_indicators=("regime:crisis", "volatility:extreme"),
        opposite_frame="PEACE",
        commonly_cooccurs=("DESTRUCTION", "GEOPOLITICAL_RISK", "FEAR"),
        icon_variant="⚔"
    ),
    LakoffFrame(
        id="GEOPOLITICAL_RISK",
        name="Geopolitical Risk",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Political tensions, international disputes, sovereign risk affecting investments",
        theoretical_source="Finance",
        prototype_centrality=0.4,
        financial_keywords=("geopolitical", "political_risk", "sovereign_risk", "international", "tension"),
        ca_rule_triggers=("volatility:high", "credit_spread:wide"),
        ca_state_indicators=("volatility:high", "credit_spread:wide"),
        opposite_frame="STABILITY",
        commonly_cooccurs=("UNCERTAINTY", "RISK", "VOLATILITY"),
        icon_variant="🌍"
    ),
    LakoffFrame(
        id="SANCTIONS",
        name="Sanctions",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Economic sanctions, trade restrictions, asset freezes, embargoes",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("sanctions", "embargo", "trade_restriction", "asset_freeze", "blockade"),
        ca_rule_triggers=("liquidity:critical", "credit_spread:wide"),
        ca_state_indicators=("liquidity:critical", "credit_spread:wide"),
        opposite_frame="FREE_TRADE",
        commonly_cooccurs=("CONSTRAINT", "LIMITATION", "ILLIQUIDITY"),
        icon_variant="🚫"
    ),
    LakoffFrame(
        id="DESTRUCTION",
        name="Destruction",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Physical destruction of assets, infrastructure, capital stock",
        theoretical_source="Finance",
        prototype_centrality=0.1,
        financial_keywords=("destruction", "destroy", "infrastructure", "physical_damage", "asset_loss"),
        ca_rule_triggers=("portfolio_value:distressed", "regime:crisis"),
        ca_state_indicators=("portfolio_value:distressed", "regime:crisis"),
        opposite_frame="CONSTRUCTION",
        commonly_cooccurs=("LOSS_FINANCIAL", "HARM", "VIOLENCE"),
        icon_variant="💥"
    ),
    LakoffFrame(
        id="GENOCIDE",
        name="Genocide",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Mass atrocities, ethnic cleansing, systematic destruction of populations",
        theoretical_source="Finance",
        prototype_centrality=0.05,
        financial_keywords=("genocide", "atrocity", "ethnic_cleansing", "mass_killing", "crimes_against_humanity"),
        ca_rule_triggers=("trust:low", "institutional_quality:low", "regime:crisis"),
        ca_state_indicators=("trust:low", "institutional_quality:low", "regime:crisis"),
        opposite_frame="HUMAN_RIGHTS",
        commonly_cooccurs=("VIOLENCE", "DESTRUCTION", "DEGRADATION"),
        icon_variant="☠"
    ),
    LakoffFrame(
        id="WAR_ECONOMY",
        name="War Economy",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Militarization of economy, defense spending, military-industrial complex",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("war_economy", "defense_spending", "military_industrial", "armaments", "militarization"),
        ca_rule_triggers=("leverage_ratio:high", "regime:crisis"),
        ca_state_indicators=("leverage_ratio:high", "regime:crisis"),
        opposite_frame="PEACE_DIVIDEND",
        commonly_cooccurs=("MILITARY_CONFLICT", "GEOPOLITICAL_RISK", "AMPLIFICATION"),
        icon_variant="💰"
    ),
    LakoffFrame(
        id="RESOURCE_WAR",
        name="Resource War",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Conflict over natural resources, commodity competition, resource nationalism",
        theoretical_source="Finance",
        prototype_centrality=0.25,
        financial_keywords=("resource_war", "commodity_conflict", "energy_security", "water_conflict", "mineral_rights"),
        ca_rule_triggers=("volatility:high", "portfolio_value:distressed"),
        ca_state_indicators=("volatility:high", "portfolio_value:distressed"),
        opposite_frame="COOPERATION",
        commonly_cooccurs=("GEOPOLITICAL_RISK", "SANCTIONS", "VOLATILITY"),
        icon_variant="🛢"
    ),
    LakoffFrame(
        id="TERROR",
        name="Terror",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Terrorism, asymmetric warfare, psychological fear campaigns",
        theoretical_source="Finance",
        prototype_centrality=0.15,
        financial_keywords=("terror", "terrorism", "asymmetric_warfare", "psychological_warfare", "fear_campaign"),
        ca_rule_triggers=("volatility:extreme", "regime:crisis"),
        ca_state_indicators=("volatility:extreme", "regime:crisis"),
        opposite_frame="SECURITY",
        commonly_cooccurs=("FEAR", "PANIC", "UNCERTAINTY"),
        icon_variant="😱"
    ),
    LakoffFrame(
        id="REFUGEE_CRISIS",
        name="Refugee Crisis",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Mass displacement, humanitarian crisis, migration flows affecting economies",
        theoretical_source="Finance",
        prototype_centrality=0.2,
        financial_keywords=("refugee", "displacement", "humanitarian_crisis", "migration", "asylum"),
        ca_rule_triggers=("liquidity:critical", "portfolio_value:distressed"),
        ca_state_indicators=("liquidity:critical", "portfolio_value:distressed"),
        opposite_frame="STABILITY",
        commonly_cooccurs=("DESTRUCTION", "GENOCIDE", "HUMAN_SUFFERING"),
        icon_variant="🏃"
    ),
    LakoffFrame(
        id="PEACE",
        name="Peace",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Absence of conflict, stability, cooperation, diplomatic resolution",
        theoretical_source="Finance",
        prototype_centrality=0.6,
        financial_keywords=("peace", "diplomacy", "cooperation", "stability", "conflict_resolution"),
        ca_rule_triggers=("regime:steady", "volatility:calm"),
        ca_state_indicators=("regime:steady", "volatility:calm"),
        opposite_frame="MILITARY_CONFLICT",
        commonly_cooccurs=("STABILITY", "COOPERATION", "SAFETY"),
        icon_variant="🕊"
    ),
    LakoffFrame(
        id="FREE_TRADE",
        name="Free Trade",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Open markets, tariff elimination, economic integration, globalization",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("free_trade", "open_markets", "globalization", "tariff_free", "economic_integration"),
        ca_rule_triggers=("liquidity:adequate", "credit_spread:tight"),
        ca_state_indicators=("liquidity:adequate", "credit_spread:tight"),
        opposite_frame="SANCTIONS",
        commonly_cooccurs=("GROWTH_FINANCIAL", "LIQUIDITY", "COOPERATION"),
        icon_variant="🤝"
    ),
    LakoffFrame(
        id="HUMAN_RIGHTS",
        name="Human Rights",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Fundamental rights and freedoms, dignity, rule of law, justice",
        theoretical_source="Finance",
        prototype_centrality=0.4,
        financial_keywords=("human_rights", "dignity", "rule_of_law", "justice", "freedom"),
        ca_rule_triggers=("trust:high", "institutional_quality:high"),
        ca_state_indicators=("trust:high", "institutional_quality:high"),
        opposite_frame="GENOCIDE",
        commonly_cooccurs=("INTEGRITY", "FAIRNESS", "CARE"),
        icon_variant="⚖"
    ),
    LakoffFrame(
        id="PEACE_DIVIDEND",
        name="Peace Dividend",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Economic benefits from reduced military spending, reallocation to civilian needs",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("peace_dividend", "disarmament", "civilian_spending", "social_investment", "demilitarization"),
        ca_rule_triggers=("portfolio_value:growth", "regime:bull"),
        ca_state_indicators=("portfolio_value:growth", "regime:bull"),
        opposite_frame="WAR_ECONOMY",
        commonly_cooccurs=("GROWTH_FINANCIAL", "PEACE", "RETURN"),
        icon_variant="📈"
    ),
    LakoffFrame(
        id="SECURITY",
        name="Security",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Safety, protection, freedom from danger or threat",
        theoretical_source="Finance",
        prototype_centrality=0.6,
        financial_keywords=("security", "safety", "protection", "defense", "stability"),
        ca_rule_triggers=("volatility:calm", "regime:steady"),
        ca_state_indicators=("volatility:calm", "regime:steady"),
        opposite_frame="TERROR",
        commonly_cooccurs=("SAFETY", "STABILITY", "CONFIDENCE"),
        icon_variant="🛡"
    ),
    LakoffFrame(
        id="COOPERATION",
        name="Cooperation",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Collaboration, mutual benefit, partnership, alliance",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("cooperation", "collaboration", "partnership", "alliance", "mutual_benefit"),
        ca_rule_triggers=("regime:steady", "volatility:calm"),
        ca_state_indicators=("regime:steady", "volatility:calm"),
        opposite_frame="CONFLICT",
        commonly_cooccurs=("PEACE", "FREE_TRADE", "GROWTH_FINANCIAL"),
        icon_variant="🤝"
    ),
    LakoffFrame(
        id="CONFLICT",
        name="Conflict",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Dispute, disagreement, opposition, clash of interests",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("conflict", "dispute", "clash", "opposition", "tension"),
        ca_rule_triggers=("volatility:high", "regime:crisis"),
        ca_state_indicators=("volatility:high", "regime:crisis"),
        opposite_frame="COOPERATION",
        commonly_cooccurs=("GEOPOLITICAL_RISK", "VOLATILITY", "UNCERTAINTY"),
        icon_variant="⚡"
    ),
    LakoffFrame(
        id="CONSTRUCTION",
        name="Construction",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Building, creation, development, infrastructure investment",
        theoretical_source="Finance",
        prototype_centrality=0.6,
        financial_keywords=("construction", "building", "creation", "development", "infrastructure"),
        ca_rule_triggers=("portfolio_value:growth", "regime:bull"),
        ca_state_indicators=("portfolio_value:growth", "regime:bull"),
        opposite_frame="DESTRUCTION",
        commonly_cooccurs=("GROWTH_FINANCIAL", "RETURN", "INVESTMENT"),
        icon_variant="🏗"
    ),
    LakoffFrame(
        id="CREATIVE_ACCOUNTING",
        name="Creative Accounting",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Aggressive but legal accounting techniques to improve financial appearance",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("creative accounting", "earnings management", "window dressing"),
        ca_rule_triggers=("trust:low", "transparency:low"),
        ca_state_indicators=("trust:low", "transparency:low"),
        opposite_frame="TRANSPARENCY",
        commonly_cooccurs=("DECEPTION", "FRAUD", "MANIPULATION"),
        icon_variant="🧮"
    ),
    LakoffFrame(
        id="TAX_AVOIDANCE",
        name="Tax Avoidance",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Legal minimization of tax liability through planning",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("tax avoidance", "tax planning", "tax shelter"),
        ca_rule_triggers=("trust:low", "transparency:low"),
        ca_state_indicators=("trust:low", "transparency:low"),
        opposite_frame="REGULATORY_COMPLIANCE",
        commonly_cooccurs=("LEGAL_LOOPHOLE", "CREATIVE_ACCOUNTING", "DECEPTION"),
        icon_variant="💰"
    ),
    LakoffFrame(
        id="LEGAL_LOOPHOLE",
        name="Legal Loophole",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Exploitation of legal technicalities to achieve advantageous outcomes",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("loophole", "legal technicality", "exploit"),
        ca_rule_triggers=("trust:low", "transparency:low"),
        ca_state_indicators=("trust:low", "transparency:low"),
        opposite_frame="REGULATORY_COMPLIANCE",
        commonly_cooccurs=("TAX_AVOIDANCE", "CREATIVE_ACCOUNTING", "DECEPTION"),
        icon_variant="🕳️"
    ),
    LakoffFrame(
        id="REGULATORY_COMPLIANCE",
        name="Regulatory Compliance",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Adherence to laws, regulations, and standards",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("compliance", "regulation", "adherence", "standards"),
        ca_rule_triggers=("trust:high", "transparency:high"),
        ca_state_indicators=("trust:high", "transparency:high"),
        opposite_frame="LEGAL_LOOPHOLE",
        commonly_cooccurs=("SAFETY", "TRANSPARENCY", "INTEGRITY"),
        icon_variant="📜"
    ),
    LakoffFrame(
        id="INNOVATION",
        name="Innovation",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Novelty, invention, disruption, creative destruction",
        theoretical_source="Finance",
        prototype_centrality=0.6,
        financial_keywords=("innovation", "novelty", "invention", "disruption"),
        ca_rule_triggers=("momentum:positive", "portfolio_value:growth"),
        ca_state_indicators=("momentum:positive", "portfolio_value:growth"),
        opposite_frame=None,
        commonly_cooccurs=("GROWTH_FINANCIAL", "PROGRESS", "CHANGE"),
        icon_variant="💡"
    ),
    LakoffFrame(
        id="MARKET_EFFICIENCY",
        name="Market Efficiency",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Prices reflect all available information, no arbitrage opportunities",
        theoretical_source="Finance",
        prototype_centrality=0.7,
        financial_keywords=("efficiency", "arbitrage", "information", "price discovery"),
        ca_rule_triggers=("volatility:calm", "regime:steady"),
        ca_state_indicators=("volatility:calm", "regime:steady"),
        opposite_frame=None,
        commonly_cooccurs=("TRANSPARENCY", "LIQUIDITY", "STABILITY"),
        icon_variant="⚖️"
    ),
    LakoffFrame(
        id="LIQUIDITY_CRUNCH",
        name="Liquidity Crunch",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Severe shortage of liquidity, inability to buy/sell assets",
        theoretical_source="Finance",
        prototype_centrality=0.2,
        financial_keywords=("liquidity crunch", "dry up", "freeze", "illiquidity"),
        ca_rule_triggers=("liquidity:low", "regime:crisis"),
        ca_state_indicators=("liquidity:low", "regime:crisis"),
        opposite_frame="LIQUIDITY",
        commonly_cooccurs=("CRISIS", "PANIC", "BREAKDOWN"),
        icon_variant="💧"
    ),
    # Kindleberger crisis frames (Manias, Panics and Crashes)
    LakoffFrame(
        id="DISPLACEMENT",
        name="Displacement",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="External shock creating new profit opportunities, triggering credit expansion and speculation",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("displacement", "shock", "new_opportunities", "structural_change", "kindleberger"),
        ca_rule_triggers=("regime:transition", "volatility:spike"),
        ca_state_indicators=("regime:transition", "volatility:spike"),
        opposite_frame="STASIS",
        commonly_cooccurs=("CREDIT_EXPANSION", "EUPHORIA", "SHOCK"),
        icon_variant="⚡"
    ),
    LakoffFrame(
        id="CREDIT_EXPANSION",
        name="Credit Expansion",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Monetary expansion, new financial instruments, easy credit fueling speculation",
        theoretical_source="Finance",
        prototype_centrality=0.4,
        financial_keywords=("credit_expansion", "easy_money", "leverage", "monetary_policy", "kindleberger"),
        ca_rule_triggers=("liquidity:excess", "leverage_ratio:high"),
        ca_state_indicators=("liquidity:excess", "leverage_ratio:high"),
        opposite_frame="DELEVERAGE",
        commonly_cooccurs=("EUPHORIA", "MANIA", "LEVERAGE"),
        icon_variant="💰"
    ),
    LakoffFrame(
        id="EUPHORIA",
        name="Euphoria",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Speculative enthusiasm, irrational exuberance, optimism disconnected from fundamentals",
        theoretical_source="Finance",
        prototype_centrality=0.2,
        financial_keywords=("euphoria", "irrational_exuberance", "speculation", "bubble", "kindleberger"),
        ca_rule_triggers=("momentum:strong", "leverage_ratio:extreme"),
        ca_state_indicators=("momentum:strong", "leverage_ratio:extreme"),
        opposite_frame="CAUTION",
        commonly_cooccurs=("MANIA", "GREED", "OPTIMISM"),
        icon_variant="🎭"
    ),
    LakoffFrame(
        id="MANIA",
        name="Mania",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Intense speculative fever, widespread participation, asset prices disconnected from reality",
        theoretical_source="Finance",
        prototype_centrality=0.1,
        financial_keywords=("mania", "speculative_fever", "frenzy", "bubble_peak", "kindleberger"),
        ca_rule_triggers=("volatility:extreme", "herding:high"),
        ca_state_indicators=("volatility:extreme", "herding:high"),
        opposite_frame="RATIONALITY",
        commonly_cooccurs=("EUPHORIA", "GREED", "PANIC"),
        icon_variant="🔥"
    ),
    LakoffFrame(
        id="DISTRESS",
        name="Distress",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Rising interest rates, strained reserves, warnings ignored, early signs of trouble",
        theoretical_source="Finance",
        prototype_centrality=0.2,
        financial_keywords=("distress", "warning_signs", "rising_rates", "strained_reserves", "kindleberger"),
        ca_rule_triggers=("credit_spread:wide", "liquidity:tight"),
        ca_state_indicators=("credit_spread:wide", "liquidity:tight"),
        opposite_frame="STABILITY",
        commonly_cooccurs=("PANIC", "REVULSION", "CRISIS"),
        icon_variant="⚠"
    ),
    LakoffFrame(
        id="REVULSION",
        name="Revulsion",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Sudden aversion to risk, flight to safety, liquidation of positions, credit contraction",
        theoretical_source="Finance",
        prototype_centrality=0.2,
        financial_keywords=("revulsion", "risk_aversion", "flight_to_safety", "liquidation", "kindleberger"),
        ca_rule_triggers=("volatility:extreme", "portfolio_value:distressed"),
        ca_state_indicators=("volatility:extreme", "portfolio_value:distressed"),
        opposite_frame="GREED",
        commonly_cooccurs=("PANIC", "DISTRESS", "CRISIS"),
        icon_variant="🏃"
    ),
    LakoffFrame(
        id="INTERVENTION",
        name="Intervention",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Lender of last resort, government bailouts, policy responses to stabilize markets",
        theoretical_source="Finance",
        prototype_centrality=0.5,
        financial_keywords=("intervention", "bailout", "lender_of_last_resort", "government_support", "kindleberger"),
        ca_rule_triggers=("regime:crisis", "liquidity:critical"),
        ca_state_indicators=("regime:crisis", "liquidity:critical"),
        opposite_frame="LAISSEZ_FAIRE",
        commonly_cooccurs=("LENDER_OF_LAST_RESORT", "STABILITY", "RECOVERY"),
        icon_variant="🛡"
    ),
    LakoffFrame(
        id="SWINDLE",
        name="Swindle",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Fraud, Ponzi schemes, and deception that emerge during manias and trigger panic when discovered",
        theoretical_source="Finance",
        prototype_centrality=0.1,
        financial_keywords=("swindle", "fraud", "ponzi", "deception", "kindleberger"),
        ca_rule_triggers=("trust:low", "transparency:low"),
        ca_state_indicators=("trust:low", "transparency:low"),
        opposite_frame="INTEGRITY",
        commonly_cooccurs=("DECEPTION", "MANIA", "PANIC"),
        icon_variant="🎭"
    ),
    LakoffFrame(
        id="CONTAGION",
        name="Contagion",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="International propagation of crisis via trade, capital flows, commodity prices, exchange rates",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("contagion", "cross_border", "propagation", "spillover", "kindleberger"),
        ca_rule_triggers=("correlation:high", "volatility:extreme"),
        ca_state_indicators=("correlation:high", "volatility:extreme"),
        opposite_frame="CONTAINMENT",
        commonly_cooccurs=("CASCADE", "CRISIS", "VOLATILITY"),
        icon_variant="🌍"
    ),
    LakoffFrame(
        id="MORAL_HAZARD",
        name="Moral Hazard",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Expectation of bailout encouraging excessive risk‑taking, undermining market discipline",
        theoretical_source="Finance",
        prototype_centrality=0.3,
        financial_keywords=("moral_hazard", "bailout_expectation", "risk_taking", "implicit_guarantee", "kindleberger"),
        ca_rule_triggers=("leverage_ratio:high", "trust:low"),
        ca_state_indicators=("leverage_ratio:high", "trust:low"),
        opposite_frame="ACCOUNTABILITY",
        commonly_cooccurs=("INTERVENTION", "LENDER_OF_LAST_RESORT", "RISK"),
        icon_variant="⚖"
    ),
    LakoffFrame(
        id="LENDER_OF_LAST_RESORT",
        name="Lender of Last Resort",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Central bank or institution providing liquidity during crises to prevent systemic collapse",
        theoretical_source="Finance",
        prototype_centrality=0.4,
        financial_keywords=("lender_of_last_resort", "central_bank", "bailout", "liquidity_provider", "kindleberger"),
        ca_rule_triggers=("liquidity:critical", "regime:crisis"),
        ca_state_indicators=("liquidity:critical", "regime:crisis"),
        opposite_frame="LAISSEZ_FAIRE",
        commonly_cooccurs=("INTERVENTION", "STABILITY", "RECOVERY"),
        icon_variant="🏦"
    ),
    LakoffFrame(
        id="BOOM",
        name="Boom",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Economic expansion phase, rising asset prices, optimism, increasing leverage",
        theoretical_source="Finance",
        prototype_centrality=0.6,
        financial_keywords=("boom", "expansion", "growth", "prosperity", "kindleberger"),
        ca_rule_triggers=("momentum:positive", "portfolio_value:growth"),
        ca_state_indicators=("momentum:positive", "portfolio_value:growth"),
        opposite_frame="BUST",
        commonly_cooccurs=("EUPHORIA", "CREDIT_EXPANSION", "GROWTH_FINANCIAL"),
        icon_variant="📈"
    ),
    LakoffFrame(
        id="BUST",
        name="Bust",
        category=LakoffCategory.FINANCIAL_SPECIFIC,
        description="Contraction phase, falling asset prices, pessimism, deleveraging, recession",
        theoretical_source="Finance",
        prototype_centrality=0.2,
        financial_keywords=("bust", "contraction", "recession", "downturn", "kindleberger"),
        ca_rule_triggers=("momentum:negative", "portfolio_value:distressed"),
        ca_state_indicators=("momentum:negative", "portfolio_value:distressed"),
        opposite_frame="BOOM",
        commonly_cooccurs=("PANIC", "REVULSION", "CRISIS"),
        icon_variant="📉"
    ),
]


# ============================================================================
# Dynamical Signatures Computation
# ============================================================================

def enhance_frame_with_dynamical_signatures(frame: LakoffFrame) -> LakoffFrame:
    """Compute and add dynamical signature fields to a LakoffFrame.
    
    Uses heuristics based on prototype centrality, category, and frame ID.
    """
    # Heuristic: attractor type based on centrality and category
    centrality = frame.prototype_centrality
    if centrality > 0.7:
        attractor = AttractorType.FIXED_POINT
    elif centrality < 0.3:
        attractor = AttractorType.STRANGE_ATTRACTOR
    elif frame.category == LakoffCategory.EMOTIONAL_FRAMES:
        attractor = AttractorType.LIMIT_CYCLE
    else:
        attractor = AttractorType.NONE
    
    # Basin width: wider for stable frames (high centrality)
    basin_width = centrality  # 0-1, higher for stable frames
    
    # Bifurcation sensitivity: higher for crisis/low centrality frames
    bifurcation_sensitivity = 1.0 - centrality
    
    # Dynamical signature mapping
    if attractor == AttractorType.FIXED_POINT:
        dyn_sig = DynamicalSignature.FIXED_POINT
    elif attractor == AttractorType.LIMIT_CYCLE:
        dyn_sig = DynamicalSignature.PERIODIC
    elif attractor == AttractorType.STRANGE_ATTRACTOR:
        dyn_sig = DynamicalSignature.CHAOTIC
    else:
        dyn_sig = DynamicalSignature.TRANSIENT
    
    # Regime transition probability: higher for low centrality
    regime_transition_prob = 0.1 + (1.0 - centrality) * 0.3  # 0.1-0.4
    
    # Volatility multiplier based on frame keywords
    volatility_mult = 1.0
    if any(kw in frame.id.lower() or any(kw in kw_lower for kw_lower in frame.financial_keywords) 
           for kw in ['volatility', 'panic', 'cascade', 'explosion', 'shock', 'crisis']):
        volatility_mult = 1.5 + (1.0 - centrality) * 1.0  # 1.5-2.5
    elif any(kw in frame.id.lower() or any(kw in kw_lower for kw_lower in frame.financial_keywords)
             for kw in ['calm', 'stability', 'balance', 'steady']):
        volatility_mult = 0.5 + centrality * 0.5  # 0.5-1.0
    
    # Liquidity impact
    liquidity_impact = 0.0
    if any(kw in frame.id.lower() or any(kw in kw_lower for kw_lower in frame.financial_keywords)
           for kw in ['liquidity', 'flow', 'fluid', 'circulation']):
        liquidity_impact = 0.3 + centrality * 0.4  # 0.3-0.7
    elif any(kw in frame.id.lower() or any(kw in kw_lower for kw_lower in frame.financial_keywords)
             for kw in ['illiquidity', 'frozen', 'stuck', 'blockage']):
        liquidity_impact = -0.3 - (1.0 - centrality) * 0.4  # -0.3 to -0.7
    
    # Correlation effect
    correlation_effect = 0.0
    if any(kw in frame.id.lower() or any(kw in kw_lower for kw_lower in frame.financial_keywords)
           for kw in ['herd', 'following', 'imitation', 'group', 'loyalty', 'correlation']):
        correlation_effect = 0.2 + centrality * 0.3  # 0.2-0.5
    elif any(kw in frame.id.lower() or any(kw in kw_lower for kw_lower in frame.financial_keywords)
             for kw in ['deception', 'betrayal', 'subversion', 'disruption']):
        correlation_effect = -0.2 - (1.0 - centrality) * 0.3  # -0.2 to -0.5
    
    # Create new frame with dynamical signatures
    return LakoffFrame(
        id=frame.id,
        name=frame.name,
        category=frame.category,
        description=frame.description,
        theoretical_source=frame.theoretical_source,
        prototype_centrality=frame.prototype_centrality,
        financial_keywords=frame.financial_keywords,
        ca_rule_triggers=frame.ca_rule_triggers,
        ca_state_indicators=frame.ca_state_indicators,
        opposite_frame=frame.opposite_frame,
        commonly_cooccurs=frame.commonly_cooccurs,
        attractor_type=attractor,
        basin_width=basin_width,
        bifurcation_sensitivity=bifurcation_sensitivity,
        dynamical_signature=dyn_sig,
        regime_transition_probability=regime_transition_prob,
        volatility_multiplier=volatility_mult,
        liquidity_impact=liquidity_impact,
        correlation_effect=correlation_effect,
        icon_variant=frame.icon_variant,
    )


def enhance_all_frames():
    """Apply dynamical signature enhancement to all frame lists."""
    global CONCEPTUAL_METAPHOR_FRAMES, FRAME_SEMANTICS_FRAMES, MORAL_FOUNDATIONS_FRAMES
    global EMOTIONAL_FRAMES, FINANCIAL_SPECIFIC_FRAMES
    
    CONCEPTUAL_METAPHOR_FRAMES = [enhance_frame_with_dynamical_signatures(f) 
                                  for f in CONCEPTUAL_METAPHOR_FRAMES]
    FRAME_SEMANTICS_FRAMES = [enhance_frame_with_dynamical_signatures(f) 
                              for f in FRAME_SEMANTICS_FRAMES]
    MORAL_FOUNDATIONS_FRAMES = [enhance_frame_with_dynamical_signatures(f) 
                                for f in MORAL_FOUNDATIONS_FRAMES]
    EMOTIONAL_FRAMES = [enhance_frame_with_dynamical_signatures(f) 
                        for f in EMOTIONAL_FRAMES]
    FINANCIAL_SPECIFIC_FRAMES = [enhance_frame_with_dynamical_signatures(f) 
                                 for f in FINANCIAL_SPECIFIC_FRAMES]


# Apply enhancement
enhance_all_frames()


# ============================================================================
# Complete Taxonomy Assembly
# ============================================================================
# Complete Taxonomy Assembly
# ============================================================================

ALL_FRAMES = (
    CONCEPTUAL_METAPHOR_FRAMES +
    FRAME_SEMANTICS_FRAMES +
    MORAL_FOUNDATIONS_FRAMES +
    EMOTIONAL_FRAMES +
    FINANCIAL_SPECIFIC_FRAMES
)

# Create registry
LAKOFF_REGISTRY: Dict[str, LakoffFrame] = {frame.id: frame for frame in ALL_FRAMES}


# ============================================================================
# Taxonomy Management Class
# ============================================================================

class LakoffTaxonomy:
    """Manager for Lakoff frame taxonomy."""
    
    def __init__(self):
        self._by_id = LAKOFF_REGISTRY.copy()
        self._by_category: Dict[LakoffCategory, List[LakoffFrame]] = {}
        for frame in ALL_FRAMES:
            self._by_category.setdefault(frame.category, []).append(frame)
    
    def get(self, frame_id: str) -> LakoffFrame:
        """Get frame by ID."""
        if frame_id not in self._by_id:
            raise KeyError(f"Unknown Lakoff frame: {frame_id}")
        return self._by_id[frame_id]
    
    def frames_by_category(self, category: LakoffCategory) -> List[LakoffFrame]:
        """Get all frames in a category."""
        return self._by_category.get(category, [])
    
    def frames_for_ca_state(self, state_key: str) -> List[LakoffFrame]:
        """Get frames that match a CA state indicator."""
        matches = []
        for frame in ALL_FRAMES:
            if state_key in frame.ca_state_indicators:
                matches.append(frame)
        return matches
    
    def frames_for_ca_rule(self, rule_key: str) -> List[LakoffFrame]:
        """Get frames that match a CA rule trigger."""
        matches = []
        for frame in ALL_FRAMES:
            if rule_key in frame.ca_rule_triggers:
                matches.append(frame)
        return matches
    
    def frames_by_prototype_range(self, min_centrality: float = 0.0,
                                  max_centrality: float = 1.0) -> List[LakoffFrame]:
        """Get frames within prototype centrality range."""
        return [
            frame for frame in ALL_FRAMES
            if min_centrality <= frame.prototype_centrality <= max_centrality
        ]
    
    def find_frames_by_keyword(self, keyword: str) -> List[LakoffFrame]:
        """Find frames containing keyword in financial keywords."""
        keyword_lower = keyword.lower()
        return [
            frame for frame in ALL_FRAMES
            if any(keyword_lower in kw.lower() for kw in frame.financial_keywords)
        ]
    
    def get_opposite_frame(self, frame_id: str) -> Optional[LakoffFrame]:
        """Get the opposite frame if defined."""
        frame = self.get(frame_id)
        if frame.opposite_frame:
            return self.get(frame.opposite_frame)
        return None


# ============================================================================
# Global Taxonomy Instance
# ============================================================================

TAXONOMY = LakoffTaxonomy()


# ============================================================================
# Integration with Pattern Language
# ============================================================================

# Mapping from pattern language frame IDs to taxonomy frame IDs
PATTERN_TO_TAXONOMY_MAP = {
    # Conceptual metaphors
    "MOMENTUM": "FORCE",
    "GROWTH": "GROWTH_FINANCIAL",
    "OPTIMISM": "HOPE",
    "LOSS": "LOSS_FINANCIAL",
    "PANIC": "PANIC",
    "REGRET": "DESPAIR",
    "RISK": "RISK",
    "UNCERTAINTY": "RISK",
    "CLUSTERING": "VOLATILITY",
    "CONTAINMENT": "CONTAINMENT",
    "BLOCKAGE": "CONTAINMENT",
    "FRICTION": "ILLIQUIDITY",
    "FORCE": "FORCE",
    "CASCADE": "CASCADE",
    "COLLAPSE": "CASCADE",
    "ATTRACTION": "ATTRACTOR",
    "REBOUND": "RECOVERY",
    "RECOVERY": "RECOVERY",
    "HOPE": "HOPE",
    "STASIS": "STABILITY",
    "BALANCE": "BALANCE",
    "FOLLOWING": "LOYALTY",
    "IMITATION": "LOYALTY",
    "GROUP": "LOYALTY",
    "REVERSAL": "CHANGE",
    "EXTREMITY": "VOLATILITY",
    "SUDDEN": "EVENT",
    "SHOCK": "EVENT",
    "EXPLOSION": "CASCADE",
    "RELEASE": "FLOW",
    "ABSORPTION": "CARE",  # PROTECTION -> CARE
    "PROTECTION": "CARE",
    "EXPANSION": "GROWTH_FINANCIAL",
    "AMPLIFICATION": "AMPLIFICATION",
    "FEEDBACK": "AMPLIFICATION",
    "CHAIN_REACTION": "CASCADE",
    
    # Moral foundations
    "DECEPTION": "DECEPTION",
    "HIDDEN_TRUTH": "DECEPTION",
    "HIDING": "DECEPTION",
    "FALSIFICATION": "DECEPTION",
    "UNFAIR": "UNFAIRNESS",
    "ADVANTAGE": "UNFAIRNESS",
    "SECRET": "DECEPTION",
    "LEAK": "TRANSPARENCY",  # Opposite
    "FAILURE": "DEGRADATION",
    "NEGLIGENCE": "DEGRADATION",
    "COMPLACENCY": "ACCEPTANCE",
    "BREAKDOWN": "DEGRADATION",
    "CORRUPTION": "CORRUPTION",
    "ABUSE_OF_POWER": "CORRUPTION",
    "SECRECY": "DECEPTION",
    "COERCION": "COERCION",
    "PRESSURE": "COERCION",
    "DOMINATION": "AUTHORITY",
    # Military/War frames
    "MILITARY_CONFLICT": "MILITARY_CONFLICT",
    "DESTRUCTION": "DESTRUCTION",
    "GEOPOLITICAL_RISK": "GEOPOLITICAL_RISK",
    "SANCTIONS": "SANCTIONS",
    "GENOCIDE": "GENOCIDE",
    "ATROCITY": "ATROCITY",
    "HUMAN_RIGHTS": "HUMAN_RIGHTS",
    "WAR_ECONOMY": "WAR_ECONOMY",
    "RESOURCE_WAR": "RESOURCE_WAR",
    "TERROR": "TERROR",
    "PEACE": "PEACE",
    "FREE_TRADE": "FREE_TRADE",
    "PEACE_DIVIDEND": "PEACE_DIVIDEND",
    "SECURITY": "SECURITY",
    "COOPERATION": "COOPERATION",
    "CONSTRUCTION": "CONSTRUCTION",
    "REFUGEE_CRISIS": "REFUGEE_CRISIS",
    "CONSTRAINT": "CONTAINMENT",
}


def map_pattern_frames_to_taxonomy(pattern_frames: List[str]) -> List[LakoffFrame]:
    """Map pattern language frame strings to taxonomy frames."""
    frames = []
    for pattern_frame_id in pattern_frames:
        # First try direct match in taxonomy
        if pattern_frame_id in TAXONOMY._by_id:
            frames.append(TAXONOMY.get(pattern_frame_id))
            continue
        
        # Try mapping dictionary
        mapped_id = PATTERN_TO_TAXONOMY_MAP.get(pattern_frame_id)
        if mapped_id and mapped_id in TAXONOMY._by_id:
            frames.append(TAXONOMY.get(mapped_id))
            continue
        
        # Try case-insensitive match in taxonomy
        matched = False
        for tax_id in TAXONOMY._by_id.keys():
            if tax_id.upper() == pattern_frame_id.upper():
                frames.append(TAXONOMY.get(tax_id))
                matched = True
                break
        
        if not matched:
            # Create placeholder for unknown frame
            frames.append(LakoffFrame(
                id=pattern_frame_id,
                name=pattern_frame_id.title().replace("_", " "),
                category=LakoffCategory.FINANCIAL_SPECIFIC,
                description=f"Frame from pattern language: {pattern_frame_id}",
                theoretical_source="Pattern",
                prototype_centrality=0.5,
            ))
    return frames


def compute_composite_centrality(frames: List[LakoffFrame]) -> float:
    """Compute composite prototype centrality from multiple frames.
    
    Weighted average with higher weight for frames with more extreme centrality.
    """
    if not frames:
        return 0.5
    
    weights = []
    centralities = []
    for frame in frames:
        # More extreme centralities (close to 0 or 1) get higher weight
        centrality = frame.prototype_centrality
        weight = abs(centrality - 0.5) * 2  # 0 at 0.5, 1 at 0 or 1
        weights.append(weight + 0.1)  # Add small base weight
        centralities.append(centrality)
    
    # Weighted average
    total_weight = sum(weights)
    if total_weight == 0:
        return 0.5
    return sum(w * c for w, c in zip(weights, centralities)) / total_weight


# ============================================================================
# Quick Tests
# ============================================================================

if __name__ == "__main__":
    print(f"Lakoff taxonomy loaded: {len(ALL_FRAMES)} frames")
    print(f"Categories: {[c.value for c in LakoffCategory]}")
    
    # Test mapping pattern language frames
    test_frames = ["DECEPTION", "HIDDEN_TRUTH", "REVERSAL", "CORRUPTION"]
    mapped = map_pattern_frames_to_taxonomy(test_frames)
    print(f"\nMapped {len(test_frames)} pattern frames:")
    for frame in mapped:
        print(f"  {frame.id}: {frame.name} ({frame.category.value}) - centrality: {frame.prototype_centrality}")
    
    # Compute composite centrality
    comp_centrality = compute_composite_centrality(mapped)
    print(f"\nComposite centrality: {comp_centrality:.3f}")
    
    # Test financial crisis frames
    crisis_frames = TAXONOMY.frames_by_prototype_range(0.0, 0.3)
    print(f"\nLow centrality (crisis) frames: {len(crisis_frames)}")
    for frame in crisis_frames[:5]:
        print(f"  {frame.id}: {frame.prototype_centrality:.2f}")