"""
ACS-Mentor V3.0 - Causal DAG Advisor

Interactive causal inference support:
1. DAG construction through conversation
2. Adjustment set identification
3. Sensitivity analysis (E-values)
4. Identification strategy validation

Author: ACS-Mentor Development Team
Version: 3.0.0
Date: 2025-11-17
"""

from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
import yaml
import os
import math

try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
except ImportError:
    print("Warning: LangChain not installed")


@dataclass
class DAGNode:
    """Node in causal DAG"""
    name: str
    node_type: str  # exposure, outcome, confounder, mediator, collider
    measured: bool = True


@dataclass
class DAGEdge:
    """Edge in causal DAG"""
    from_node: str
    to_node: str
    edge_type: str = "causal"  # causal, unmeasured_confounding


@dataclass
class AdjustmentSet:
    """Recommended adjustment set"""
    variables: List[str]
    set_type: str  # minimal_sufficient, all_valid
    blocks_paths: List[str]  # Which backdoor paths are blocked
    warnings: List[str]  # Warnings about colliders, etc.


@dataclass
class EValue:
    """E-value for sensitivity analysis"""
    point_estimate: float
    ci_bound: float
    interpretation: str
    robustness_assessment: str


class CausalDAG:
    """Represents a causal directed acyclic graph"""

    def __init__(self):
        self.nodes: List[DAGNode] = []
        self.edges: List[DAGEdge] = []
        self.exposure: Optional[str] = None
        self.outcome: Optional[str] = None

    def add_node(self, name: str, node_type: str, measured: bool = True):
        """Add node to DAG"""
        node = DAGNode(name, node_type, measured)
        self.nodes.append(node)

        if node_type == "exposure":
            self.exposure = name
        elif node_type == "outcome":
            self.outcome = name

    def add_edge(self, from_node: str, to_node: str, edge_type: str = "causal"):
        """Add edge to DAG"""
        edge = DAGEdge(from_node, to_node, edge_type)
        self.edges.append(edge)

    def get_parents(self, node: str) -> List[str]:
        """Get parent nodes"""
        return [e.from_node for e in self.edges if e.to_node == node]

    def get_children(self, node: str) -> List[str]:
        """Get child nodes"""
        return [e.to_node for e in self.edges if e.from_node == node]

    def find_backdoor_paths(self) -> List[List[str]]:
        """Find all backdoor paths from exposure to outcome"""
        # Simplified implementation
        # Real implementation would use graph algorithms
        backdoor_paths = []

        if not self.exposure or not self.outcome:
            return backdoor_paths

        # Find paths exposure ← ... → outcome
        for node in self.nodes:
            if node.name != self.exposure and node.name != self.outcome:
                # Check if node points to both exposure and outcome (confounder pattern)
                if (self.exposure in self.get_children(node.name) and
                    self.outcome in self.get_children(node.name)):
                    backdoor_paths.append([self.exposure, node.name, self.outcome])

        return backdoor_paths

    def to_dot(self) -> str:
        """Convert to GraphViz DOT notation"""
        dot_lines = ["digraph CausalDAG {"]

        # Add nodes
        for node in self.nodes:
            attrs = []
            if node.node_type == "exposure":
                attrs.append("color=blue, shape=box")
            elif node.node_type == "outcome":
                attrs.append("color=red, shape=box")
            elif node.node_type == "confounder":
                attrs.append("color=orange, shape=ellipse")
            elif node.node_type == "mediator":
                attrs.append("color=green, shape=ellipse")

            if not node.measured:
                attrs.append("style=dashed")

            attr_str = ", ".join(attrs) if attrs else ""
            dot_lines.append(f'  "{node.name}" [{attr_str}];')

        # Add edges
        for edge in self.edges:
            style = "dashed, color=red" if edge.edge_type == "unmeasured_confounding" else "solid"
            dot_lines.append(f'  "{edge.from_node}" -> "{edge.to_node}" [style={style}];')

        dot_lines.append("}")
        return "\n".join(dot_lines)


class DAGAdvisor:
    """Interactive DAG construction and causal inference advisor"""

    def __init__(self, config_path: str = ".acs_mentor/causal_dag_config.yaml"):
        """Initialize DAG advisor"""
        self.config = self._load_config(config_path)
        self.llm = self._initialize_llm()
        self.current_dag: Optional[CausalDAG] = None

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration"""
        if not os.path.exists(config_path):
            print(f"Warning: Config not found: {config_path}, using defaults")
            return {}

        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _initialize_llm(self):
        """Initialize LLM"""
        llm_config = self.config.get('llm_config', {})
        return ChatOpenAI(
            model=llm_config.get('model', 'gpt-4'),
            temperature=llm_config.get('temperature', 0.2),
            max_tokens=2000
        )

    def construct_dag_interactive(
        self,
        research_question: str,
        user_inputs: Optional[Dict] = None
    ) -> CausalDAG:
        """
        Construct DAG through interactive conversation

        Args:
            research_question: User's research question
            user_inputs: Pre-collected inputs (exposure, outcome, confounders, etc.)

        Returns:
            CausalDAG
        """
        dag = CausalDAG()

        # If inputs provided, use them directly
        if user_inputs:
            # Add exposure
            if 'exposure' in user_inputs:
                dag.add_node(user_inputs['exposure'], 'exposure')

            # Add outcome
            if 'outcome' in user_inputs:
                dag.add_node(user_inputs['outcome'], 'outcome')

            # Add confounders
            if 'confounders' in user_inputs:
                for c in user_inputs['confounders']:
                    dag.add_node(c, 'confounder')
                    dag.add_edge(c, user_inputs['exposure'])
                    dag.add_edge(c, user_inputs['outcome'])

            # Add mediators
            if 'mediators' in user_inputs:
                for m in user_inputs['mediators']:
                    dag.add_node(m, 'mediator')
                    dag.add_edge(user_inputs['exposure'], m)
                    dag.add_edge(m, user_inputs['outcome'])

            # Add causal edge exposure → outcome
            dag.add_edge(user_inputs['exposure'], user_inputs['outcome'])

        self.current_dag = dag
        return dag

    def identify_adjustment_sets(self, dag: Optional[CausalDAG] = None) -> List[AdjustmentSet]:
        """
        Identify valid adjustment sets using backdoor criterion

        Args:
            dag: Causal DAG (uses current_dag if not provided)

        Returns:
            List of valid adjustment sets
        """
        if dag is None:
            dag = self.current_dag

        if dag is None or dag.exposure is None or dag.outcome is None:
            return []

        adjustment_sets = []

        # Find backdoor paths
        backdoor_paths = dag.find_backdoor_paths()

        # Minimal sufficient set: all confounders
        confounders = [n.name for n in dag.nodes if n.node_type == 'confounder']

        if confounders:
            adjustment_set = AdjustmentSet(
                variables=confounders,
                set_type="minimal_sufficient",
                blocks_paths=[" ← ".join(path) for path in backdoor_paths],
                warnings=[]
            )
            adjustment_sets.append(adjustment_set)

        # Check for colliders (warning)
        colliders = [n.name for n in dag.nodes if n.node_type == 'collider']
        if colliders:
            adjustment_sets[0].warnings.append(
                f"Do NOT control for colliders: {', '.join(colliders)} (induces bias)"
            )

        return adjustment_sets

    def calculate_e_value(
        self,
        effect_measure: str,  # "RR", "OR", "HR"
        effect_size: float,
        ci_lower: Optional[float] = None,
        ci_upper: Optional[float] = None
    ) -> EValue:
        """
        Calculate E-value for sensitivity analysis

        Args:
            effect_measure: Type of effect (RR, OR, HR)
            effect_size: Observed effect size
            ci_lower: Lower CI bound
            ci_upper: Upper CI bound

        Returns:
            EValue
        """
        # E-value calculation (simplified)
        # E-value = RR + sqrt(RR * (RR - 1))

        if effect_size <= 1:
            # Protective effect, use reciprocal
            effect_size = 1 / effect_size

        e_val_point = effect_size + math.sqrt(effect_size * (effect_size - 1))

        # E-value for CI bound closest to null
        e_val_ci = None
        if ci_lower and ci_upper:
            # Use bound closest to 1 (null)
            ci_closest_null = ci_lower if abs(ci_lower - 1) < abs(ci_upper - 1) else ci_upper
            if ci_closest_null > 1:
                e_val_ci = ci_closest_null + math.sqrt(ci_closest_null * (ci_closest_null - 1))
            else:
                e_val_ci = 1 / ci_closest_null + math.sqrt((1/ci_closest_null) * (1/ci_closest_null - 1))

        # Interpretation
        if e_val_point < 1.5:
            robustness = "weak"
            interpretation = "Low robustness to unmeasured confounding. Small bias could explain the effect."
        elif e_val_point < 2.0:
            robustness = "moderate"
            interpretation = "Moderate robustness. Unmeasured confounder would need moderate association with both exposure and outcome."
        else:
            robustness = "strong"
            interpretation = "Strong robustness. Unmeasured confounder would need strong association with both exposure and outcome."

        return EValue(
            point_estimate=round(e_val_point, 2),
            ci_bound=round(e_val_ci, 2) if e_val_ci else None,
            interpretation=interpretation,
            robustness_assessment=robustness
        )

    def recommend_identification_strategy(
        self,
        dag: Optional[CausalDAG] = None,
        data_available: Optional[List[str]] = None
    ) -> str:
        """
        Recommend identification strategy based on DAG

        Args:
            dag: Causal DAG
            data_available: List of variables with available data

        Returns:
            Recommended strategy
        """
        if dag is None:
            dag = self.current_dag

        if dag is None:
            return "Cannot recommend without DAG"

        # Check for confounders
        confounders = [n.name for n in dag.nodes if n.node_type == 'confounder']
        measured_confounders = [c for c in confounders if
                                any(n.name == c and n.measured for n in dag.nodes)]

        if len(measured_confounders) == len(confounders):
            return "Backdoor Adjustment: Control for all confounders in regression."

        # Check for instruments
        # (simplified - in practice, check IV assumptions)
        instruments = [n.name for n in dag.nodes if n.node_type == 'instrument']
        if instruments:
            return "Instrumental Variable: Use IV to address unmeasured confounding."

        # Check for mediators (front-door)
        mediators = [n.name for n in dag.nodes if n.node_type == 'mediator']
        if mediators and len(measured_confounders) < len(confounders):
            return "Front-door Adjustment: Use mediator if it fully mediates the effect."

        return "Standard regression adjustment with available confounders, but be aware of potential unmeasured confounding."


# Example usage
if __name__ == "__main__":
    advisor = DAGAdvisor()

    # Example: Medication adherence study
    research_question = "Does medication reminder app improve adherence?"

    # Construct DAG
    user_inputs = {
        'exposure': 'Reminder_App',
        'outcome': 'Adherence',
        'confounders': ['Age', 'Health_Literacy', 'Disease_Severity'],
        'mediators': []
    }

    dag = advisor.construct_dag_interactive(research_question, user_inputs)
    print("DAG constructed:")
    print(dag.to_dot())

    # Identify adjustment sets
    adjustment_sets = advisor.identify_adjustment_sets(dag)
    print("\nAdjustment Sets:")
    for adj_set in adjustment_sets:
        print(f"  Variables: {adj_set.variables}")
        print(f"  Blocks paths: {adj_set.blocks_paths}")

    # Calculate E-value
    e_value = advisor.calculate_e_value(
        effect_measure="RR",
        effect_size=1.5,
        ci_lower=1.2,
        ci_upper=1.9
    )
    print(f"\nE-value: {e_value.point_estimate}")
    print(f"Interpretation: {e_value.interpretation}")

    # Recommend strategy
    strategy = advisor.recommend_identification_strategy(dag)
    print(f"\nRecommended strategy: {strategy}")
