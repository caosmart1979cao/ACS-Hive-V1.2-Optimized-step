"""
ACS-Mentor V3.0 - ACS-Coordinator (Queen Agent)

Meta-cognitive controller for multi-agent research support system.
Routes queries to specialist agents and synthesizes their outputs.

Author: ACS-Mentor Development Team
Version: 3.0.0
Date: 2025-11-17
"""

from typing import Dict, List, Optional, Union, Literal
import yaml
import os
from dataclasses import dataclass
from enum import Enum

try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage, AIMessage
    from langchain.prompts import ChatPromptTemplate
except ImportError:
    print("Warning: LangChain not installed. Install with: pip install langchain")


class CollaborationPattern(Enum):
    """Types of multi-agent collaboration"""
    SINGLE = "single"  # Route to single specialist
    SEQUENTIAL = "sequential"  # Specialists work in sequence
    PARALLEL = "parallel"  # Specialists work in parallel
    ITERATIVE = "iterative"  # Iterative back-and-forth


@dataclass
class RoutingDecision:
    """Coordinator's routing decision"""
    pattern: CollaborationPattern
    specialists: List[str]  # List of specialist names
    reasoning: str
    complexity_score: float
    domains: List[str]


@dataclass
class SpecialistOutput:
    """Output from a specialist agent"""
    specialist_name: str
    domain: str
    output: str
    confidence: float
    references: List[str]  # Citations or guideline references


class ACSCoordinator:
    """
    Queen Agent: Routes queries and coordinates specialists

    Responsibilities:
    1. Analyze user queries (domain, complexity, dependencies)
    2. Route to appropriate specialist(s)
    3. Coordinate sequential or parallel execution
    4. Synthesize multi-specialist outputs
    5. Maintain project-level context
    """

    def __init__(self, config_path: str = ".acs_mentor/multi_agent_config.yaml"):
        """
        Initialize coordinator

        Args:
            config_path: Path to multi-agent configuration
        """
        self.config = self._load_config(config_path)
        self.llm = self._initialize_llm()

        # Lazy-load specialists (only initialize when needed)
        self._specialists = {}

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration"""
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config not found: {config_path}")

        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def _initialize_llm(self):
        """Initialize LLM for coordinator"""
        llm_config = self.config.get('coordinator', {}).get('llm_config', {})

        return ChatOpenAI(
            model=llm_config.get('model', 'gpt-4'),
            temperature=llm_config.get('temperature', 0.3),
            max_tokens=llm_config.get('max_tokens', 2000)
        )

    def _get_specialist(self, specialist_name: str):
        """
        Lazy-load specialist agent

        Args:
            specialist_name: Name of specialist (Design-Specialist, etc.)

        Returns:
            Specialist agent instance
        """
        if specialist_name in self._specialists:
            return self._specialists[specialist_name]

        # Import and initialize specialist
        if specialist_name == "Design-Specialist":
            from agents.design_specialist import DesignSpecialist
            specialist = DesignSpecialist(self.config)
        elif specialist_name == "Stats-Specialist":
            from agents.stats_specialist import StatsSpecialist
            specialist = StatsSpecialist(self.config)
        elif specialist_name == "Writing-Specialist":
            from agents.writing_specialist import WritingSpecialist
            specialist = WritingSpecialist(self.config)
        elif specialist_name == "Strategy-Advisor":
            from agents.strategy_advisor import StrategyAdvisor
            specialist = StrategyAdvisor(self.config)
        else:
            raise ValueError(f"Unknown specialist: {specialist_name}")

        self._specialists[specialist_name] = specialist
        return specialist

    def analyze_and_route(
        self,
        user_message: str,
        user_level: str = "intermediate",
        project_context: Optional[Dict] = None
    ) -> RoutingDecision:
        """
        Analyze query and determine routing strategy

        Args:
            user_message: User's query
            user_level: User's expertise level
            project_context: Ongoing project context

        Returns:
            RoutingDecision with pattern and specialists
        """
        # Build routing prompt
        routing_prompt = self.config['coordinator']['prompts']['routing_prompt']
        filled_prompt = routing_prompt.format(
            user_message=user_message,
            user_level=user_level,
            project_context=project_context or "None"
        )

        messages = [
            SystemMessage(content=self.config['coordinator']['prompts']['system_prompt']),
            HumanMessage(content=filled_prompt)
        ]

        # Get routing decision from LLM
        response = self.llm(messages)
        decision_text = response.content

        # Parse decision (in production, use structured output)
        # For now, use heuristics
        routing_decision = self._parse_routing_decision(decision_text, user_message)

        return routing_decision

    def _parse_routing_decision(
        self,
        decision_text: str,
        user_message: str
    ) -> RoutingDecision:
        """
        Parse LLM's routing decision

        Args:
            decision_text: LLM's decision text
            user_message: Original query

        Returns:
            Structured RoutingDecision
        """
        # Simple heuristic-based parsing (in production, use structured output)

        # Detect domains
        domains = []
        if any(kw in user_message.lower() for kw in ["design", "study", "rct", "cohort", "sample"]):
            domains.append("design")
        if any(kw in user_message.lower() for kw in ["statistical", "analysis", "test", "power", "regression"]):
            domains.append("stats")
        if any(kw in user_message.lower() for kw in ["write", "manuscript", "methods", "results", "discussion"]):
            domains.append("writing")
        if any(kw in user_message.lower() for kw in ["strategy", "career", "publication", "journal", "feasibility"]):
            domains.append("strategy")

        # Map domains to specialists
        specialist_map = {
            "design": "Design-Specialist",
            "stats": "Stats-Specialist",
            "writing": "Writing-Specialist",
            "strategy": "Strategy-Advisor"
        }

        specialists = [specialist_map[d] for d in domains if d in specialist_map]

        # Determine pattern
        if len(specialists) == 0:
            # Default to Design-Specialist for unclear queries
            specialists = ["Design-Specialist"]
            pattern = CollaborationPattern.SINGLE
        elif len(specialists) == 1:
            pattern = CollaborationPattern.SINGLE
        elif "design" in domains and "stats" in domains:
            # Design → Stats is a common sequence
            pattern = CollaborationPattern.SEQUENTIAL
        else:
            # Multiple independent domains
            pattern = CollaborationPattern.PARALLEL

        # Estimate complexity
        complexity_score = min(len(domains) * 0.3 + 0.3, 1.0)

        return RoutingDecision(
            pattern=pattern,
            specialists=specialists,
            reasoning=decision_text,
            complexity_score=complexity_score,
            domains=domains
        )

    def execute_single(
        self,
        specialist_name: str,
        user_message: str,
        context: Optional[Dict] = None
    ) -> SpecialistOutput:
        """
        Execute single specialist consultation

        Args:
            specialist_name: Which specialist to consult
            user_message: User's query
            context: Additional context

        Returns:
            SpecialistOutput
        """
        specialist = self._get_specialist(specialist_name)
        output = specialist.consult(user_message, context)
        return output

    def execute_sequential(
        self,
        specialists: List[str],
        user_message: str,
        context: Optional[Dict] = None
    ) -> List[SpecialistOutput]:
        """
        Execute sequential consultation (each builds on previous)

        Args:
            specialists: Ordered list of specialists
            user_message: User's query
            context: Additional context

        Returns:
            List of SpecialistOutputs in order
        """
        outputs = []
        cumulative_context = context or {}

        for specialist_name in specialists:
            # Add previous outputs to context
            if outputs:
                cumulative_context['previous_specialist_outputs'] = [
                    {'specialist': o.specialist_name, 'output': o.output}
                    for o in outputs
                ]

            specialist = self._get_specialist(specialist_name)
            output = specialist.consult(user_message, cumulative_context)
            outputs.append(output)

        return outputs

    def execute_parallel(
        self,
        specialists: List[str],
        user_message: str,
        context: Optional[Dict] = None
    ) -> List[SpecialistOutput]:
        """
        Execute parallel consultation (specialists work independently)

        Args:
            specialists: List of specialists
            user_message: User's query
            context: Additional context

        Returns:
            List of SpecialistOutputs
        """
        outputs = []

        for specialist_name in specialists:
            specialist = self._get_specialist(specialist_name)
            output = specialist.consult(user_message, context)
            outputs.append(output)

        return outputs

    def synthesize(
        self,
        user_message: str,
        specialist_outputs: List[SpecialistOutput],
        routing_decision: RoutingDecision
    ) -> str:
        """
        Synthesize multiple specialist outputs into coherent guidance

        Args:
            user_message: Original user query
            specialist_outputs: Outputs from specialists
            routing_decision: Original routing decision

        Returns:
            Synthesized guidance
        """
        # Format specialist outputs for synthesis
        formatted_outputs = "\n\n".join([
            f"### {output.specialist_name} ({output.domain})\n{output.output}"
            for output in specialist_outputs
        ])

        # Build synthesis prompt
        synthesis_prompt = self.config['coordinator']['prompts']['synthesis_prompt']
        filled_prompt = synthesis_prompt.format(
            user_message=user_message,
            specialist_outputs=formatted_outputs
        )

        messages = [
            SystemMessage(content=self.config['coordinator']['prompts']['system_prompt']),
            HumanMessage(content=filled_prompt)
        ]

        # Get synthesis
        response = self.llm(messages)
        synthesized_output = response.content

        return synthesized_output

    def coordinate(
        self,
        user_message: str,
        user_level: str = "intermediate",
        project_context: Optional[Dict] = None
    ) -> str:
        """
        Main coordination workflow

        Args:
            user_message: User's query
            user_level: User's expertise level
            project_context: Ongoing project context

        Returns:
            Final synthesized guidance
        """
        # Step 1: Analyze and route
        routing_decision = self.analyze_and_route(
            user_message, user_level, project_context
        )

        print(f"[Coordinator] Routing: {routing_decision.pattern.value}")
        print(f"[Coordinator] Specialists: {routing_decision.specialists}")

        # Step 2: Execute based on pattern
        if routing_decision.pattern == CollaborationPattern.SINGLE:
            specialist_outputs = [
                self.execute_single(
                    routing_decision.specialists[0],
                    user_message,
                    {'user_level': user_level, 'project_context': project_context}
                )
            ]

        elif routing_decision.pattern == CollaborationPattern.SEQUENTIAL:
            specialist_outputs = self.execute_sequential(
                routing_decision.specialists,
                user_message,
                {'user_level': user_level, 'project_context': project_context}
            )

        elif routing_decision.pattern == CollaborationPattern.PARALLEL:
            specialist_outputs = self.execute_parallel(
                routing_decision.specialists,
                user_message,
                {'user_level': user_level, 'project_context': project_context}
            )

        else:
            raise ValueError(f"Unsupported pattern: {routing_decision.pattern}")

        # Step 3: Synthesize (if multiple specialists)
        if len(specialist_outputs) == 1:
            # Single specialist, return directly
            final_output = specialist_outputs[0].output
        else:
            # Multiple specialists, synthesize
            final_output = self.synthesize(
                user_message,
                specialist_outputs,
                routing_decision
            )

        return final_output


# Example usage
if __name__ == "__main__":
    coordinator = ACSCoordinator()

    # Test single specialist routing
    query1 = "Should I use an RCT or cohort study for my research on medication adherence?"
    result1 = coordinator.coordinate(query1, user_level="novice")
    print(f"\nQuery: {query1}\n")
    print(f"Result:\n{result1}\n")

    # Test multi-specialist routing
    query2 = "I need help designing an RCT, calculating sample size, and drafting the methods section."
    result2 = coordinator.coordinate(query2, user_level="intermediate")
    print(f"\nQuery: {query2}\n")
    print(f"Result:\n{result2}\n")
