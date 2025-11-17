"""
ACS-Mentor V3.0 - Specialist Agents

Four domain experts for comprehensive research support:
1. Design-Specialist: Research design and methodology
2. Stats-Specialist: Statistical analysis and inference
3. Writing-Specialist: Scientific writing and reporting
4. Strategy-Advisor: Research strategy and career planning

Author: ACS-Mentor Development Team
Version: 3.0.0
Date: 2025-11-17
"""

from typing import Dict, List, Optional
from abc import ABC, abstractmethod
from dataclasses import dataclass

try:
    from langchain.chat_models import ChatOpenAI
    from langchain.schema import HumanMessage, SystemMessage
except ImportError:
    print("Warning: LangChain not installed")


@dataclass
class SpecialistOutput:
    """Output from a specialist agent"""
    specialist_name: str
    domain: str
    output: str
    confidence: float
    references: List[str]


class BaseSpecialist(ABC):
    """Base class for all specialist agents"""

    def __init__(self, config: Dict, specialist_key: str):
        """
        Initialize specialist

        Args:
            config: Full multi-agent configuration
            specialist_key: Key in config (e.g., 'design_specialist')
        """
        self.config = config
        self.specialist_config = config.get(specialist_key, {})
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        """Initialize LLM for this specialist"""
        llm_config = self.specialist_config.get('llm_config', {})
        return ChatOpenAI(
            model=llm_config.get('model', 'gpt-4'),
            temperature=llm_config.get('temperature', 0.2),
            max_tokens=llm_config.get('max_tokens', 2000)
        )

    @abstractmethod
    def consult(self, user_message: str, context: Optional[Dict] = None) -> SpecialistOutput:
        """
        Provide specialist consultation

        Args:
            user_message: User's query
            context: Additional context

        Returns:
            SpecialistOutput
        """
        pass


# ============================================================================
# 1. Design-Specialist
# ============================================================================

class DesignSpecialist(BaseSpecialist):
    """Research design and methodology expert"""

    def __init__(self, config: Dict):
        super().__init__(config, 'design_specialist')
        self.name = "Design-Specialist"
        self.domain = "research_design"

    def consult(self, user_message: str, context: Optional[Dict] = None) -> SpecialistOutput:
        """
        Provide research design consultation

        Args:
            user_message: User's design question
            context: User level, research question, etc.

        Returns:
            Design guidance
        """
        # Extract context
        user_level = context.get('user_level', 'intermediate') if context else 'intermediate'
        research_question = context.get('research_question', 'Not specified') if context else 'Not specified'

        # Build task prompt
        task_prompt = self.specialist_config['prompts']['task_prompt'].format(
            user_message=user_message,
            research_question=research_question,
            user_level=user_level
        )

        messages = [
            SystemMessage(content=self.specialist_config['prompts']['system_prompt']),
            HumanMessage(content=task_prompt)
        ]

        # Get consultation
        response = self.llm(messages)
        output_text = response.content

        # Extract references (simplified - in production, parse structured output)
        references = self._extract_references(output_text)

        return SpecialistOutput(
            specialist_name=self.name,
            domain=self.domain,
            output=output_text,
            confidence=0.85,  # In production, estimate from LLM
            references=references
        )

    def _extract_references(self, text: str) -> List[str]:
        """Extract guideline references from text"""
        references = []
        if "CONSORT" in text:
            references.append("CONSORT 2010")
        if "STROBE" in text:
            references.append("STROBE 2007")
        if "SPIRIT" in text:
            references.append("SPIRIT 2013")
        return references


# ============================================================================
# 2. Stats-Specialist
# ============================================================================

class StatsSpecialist(BaseSpecialist):
    """Statistical analysis and inference expert"""

    def __init__(self, config: Dict):
        super().__init__(config, 'stats_specialist')
        self.name = "Stats-Specialist"
        self.domain = "statistics"

    def consult(self, user_message: str, context: Optional[Dict] = None) -> SpecialistOutput:
        """
        Provide statistical consultation

        Args:
            user_message: User's statistical question
            context: Study design, data type, sample size, etc.

        Returns:
            Statistical guidance
        """
        # Extract context
        user_level = context.get('user_level', 'intermediate') if context else 'intermediate'
        study_design = context.get('study_design', 'Not specified') if context else 'Not specified'
        data_type = context.get('data_type', 'Not specified') if context else 'Not specified'
        sample_size = context.get('sample_size', 'Not specified') if context else 'Not specified'

        # Check for previous specialist outputs (if sequential)
        previous_outputs = context.get('previous_specialist_outputs', []) if context else []
        if previous_outputs:
            # Extract study design from Design-Specialist if available
            for prev in previous_outputs:
                if prev['specialist'] == 'Design-Specialist' and 'RCT' in prev['output']:
                    study_design = "Randomized Controlled Trial"

        # Build task prompt
        task_prompt = self.specialist_config['prompts']['task_prompt'].format(
            user_message=user_message,
            study_design=study_design,
            data_type=data_type,
            sample_size=sample_size,
            user_level=user_level
        )

        messages = [
            SystemMessage(content=self.specialist_config['prompts']['system_prompt']),
            HumanMessage(content=task_prompt)
        ]

        # Get consultation
        response = self.llm(messages)
        output_text = response.content

        # Extract references
        references = self._extract_methods(output_text)

        return SpecialistOutput(
            specialist_name=self.name,
            domain=self.domain,
            output=output_text,
            confidence=0.90,  # Stats often has high confidence
            references=references
        )

    def _extract_methods(self, text: str) -> List[str]:
        """Extract statistical methods from text"""
        methods = []
        if "t-test" in text.lower():
            methods.append("t-test")
        if "anova" in text.lower():
            methods.append("ANOVA")
        if "regression" in text.lower():
            methods.append("Regression")
        if "chi-square" in text.lower():
            methods.append("Chi-square test")
        return methods


# ============================================================================
# 3. Writing-Specialist
# ============================================================================

class WritingSpecialist(BaseSpecialist):
    """Scientific writing and reporting expert"""

    def __init__(self, config: Dict):
        super().__init__(config, 'writing_specialist')
        self.name = "Writing-Specialist"
        self.domain = "scientific_writing"

    def consult(self, user_message: str, context: Optional[Dict] = None) -> SpecialistOutput:
        """
        Provide writing consultation

        Args:
            user_message: User's writing question
            context: Writing task, study type, target journal, etc.

        Returns:
            Writing guidance
        """
        # Extract context
        user_level = context.get('user_level', 'intermediate') if context else 'intermediate'
        writing_task = context.get('writing_task', 'methods') if context else 'methods'
        study_type = context.get('study_type', 'Not specified') if context else 'Not specified'
        target_journal = context.get('target_journal', 'General medical journal') if context else 'General medical journal'

        # Check for previous outputs (if sequential)
        previous_outputs = context.get('previous_specialist_outputs', []) if context else []
        if previous_outputs:
            # Incorporate design and stats info
            for prev in previous_outputs:
                if prev['specialist'] == 'Design-Specialist':
                    if 'RCT' in prev['output']:
                        study_type = "RCT"
                    elif 'cohort' in prev['output'].lower():
                        study_type = "Cohort study"

        # Build task prompt
        task_prompt = self.specialist_config['prompts']['task_prompt'].format(
            user_message=user_message,
            writing_task=writing_task,
            study_type=study_type,
            target_journal=target_journal,
            user_level=user_level
        )

        messages = [
            SystemMessage(content=self.specialist_config['prompts']['system_prompt']),
            HumanMessage(content=task_prompt)
        ]

        # Get consultation
        response = self.llm(messages)
        output_text = response.content

        # Extract guidelines
        guidelines = self._extract_guidelines(output_text, study_type)

        return SpecialistOutput(
            specialist_name=self.name,
            domain=self.domain,
            output=output_text,
            confidence=0.88,
            references=guidelines
        )

    def _extract_guidelines(self, text: str, study_type: str) -> List[str]:
        """Extract reporting guidelines"""
        guidelines = []

        # Map study type to guideline
        guideline_map = self.specialist_config.get('reporting_guidelines', {})
        if study_type == "RCT" or "RCT" in text:
            guidelines.append(guideline_map.get('RCT', 'CONSORT'))
        elif "cohort" in study_type.lower() or "observational" in text.lower():
            guidelines.append(guideline_map.get('observational', 'STROBE'))
        elif "systematic review" in text.lower():
            guidelines.append(guideline_map.get('systematic_review', 'PRISMA'))
        elif "prediction" in text.lower() or "model" in text.lower():
            guidelines.append(guideline_map.get('prediction_model', 'TRIPOD'))

        return guidelines


# ============================================================================
# 4. Strategy-Advisor
# ============================================================================

class StrategyAdvisor(BaseSpecialist):
    """Research strategy and career planning expert"""

    def __init__(self, config: Dict):
        super().__init__(config, 'strategy_advisor')
        self.name = "Strategy-Advisor"
        self.domain = "research_strategy"

    def consult(self, user_message: str, context: Optional[Dict] = None) -> SpecialistOutput:
        """
        Provide strategic consultation

        Args:
            user_message: User's strategic question
            context: Career stage, research interest, constraints, etc.

        Returns:
            Strategic guidance
        """
        # Extract context
        user_level = context.get('user_level', 'intermediate') if context else 'intermediate'
        career_stage = context.get('career_stage', 'early_career') if context else 'early_career'
        research_interest = context.get('research_interest', 'Not specified') if context else 'Not specified'
        constraints = context.get('constraints', 'Not specified') if context else 'Not specified'

        # Build task prompt
        task_prompt = self.specialist_config['prompts']['task_prompt'].format(
            user_message=user_message,
            career_stage=career_stage,
            research_interest=research_interest,
            constraints=constraints,
            user_level=user_level
        )

        messages = [
            SystemMessage(content=self.specialist_config['prompts']['system_prompt']),
            HumanMessage(content=task_prompt)
        ]

        # Get consultation
        response = self.llm(messages)
        output_text = response.content

        # Extract frameworks used
        frameworks = self._extract_frameworks(output_text)

        return SpecialistOutput(
            specialist_name=self.name,
            domain=self.domain,
            output=output_text,
            confidence=0.75,  # Strategy has more uncertainty
            references=frameworks
        )

    def _extract_frameworks(self, text: str) -> List[str]:
        """Extract strategic frameworks mentioned"""
        frameworks = []
        if "PICO" in text:
            frameworks.append("PICO framework")
        if "FINER" in text:
            frameworks.append("FINER criteria")
        if "SMART" in text.upper():
            frameworks.append("SMART goals")
        return frameworks


# ============================================================================
# Factory function
# ============================================================================

def create_specialist(specialist_name: str, config: Dict) -> BaseSpecialist:
    """
    Factory function to create specialists

    Args:
        specialist_name: Name of specialist
        config: Configuration dict

    Returns:
        Specialist instance
    """
    if specialist_name == "Design-Specialist":
        return DesignSpecialist(config)
    elif specialist_name == "Stats-Specialist":
        return StatsSpecialist(config)
    elif specialist_name == "Writing-Specialist":
        return WritingSpecialist(config)
    elif specialist_name == "Strategy-Advisor":
        return StrategyAdvisor(config)
    else:
        raise ValueError(f"Unknown specialist: {specialist_name}")


# Example usage
if __name__ == "__main__":
    import yaml

    # Load config
    with open('.acs_mentor/multi_agent_config.yaml', 'r') as f:
        config = yaml.safe_load(f)

    # Test Design-Specialist
    design = DesignSpecialist(config)
    result = design.consult(
        "Should I use an RCT or cohort study for medication adherence?",
        context={'user_level': 'novice', 'research_question': 'Effect of reminders on adherence'}
    )
    print(f"{result.specialist_name}:\n{result.output}\n")

    # Test Stats-Specialist
    stats = StatsSpecialist(config)
    result = stats.consult(
        "What statistical test should I use for comparing two groups?",
        context={'user_level': 'novice', 'data_type': 'continuous', 'study_design': 'RCT'}
    )
    print(f"{result.specialist_name}:\n{result.output}\n")
