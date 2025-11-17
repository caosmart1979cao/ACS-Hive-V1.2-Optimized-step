"""
ACS-Mentor V3.0 - Full Research Lifecycle Manager

End-to-end research support from question to publication:
1. Research Question Formulation (PICO/FINER)
2. Study Design & Protocol
3. Data Analysis
4. Manuscript Writing
5. Submission & Revision

Author: ACS-Mentor Development Team
Version: 3.0.0
Date: 2025-11-17
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum
import yaml
import os
from datetime import datetime


class ResearchPhase(Enum):
    """Research lifecycle phases"""
    QUESTION_FORMULATION = "question_formulation"
    STUDY_DESIGN = "study_design"
    DATA_ANALYSIS = "data_analysis"
    MANUSCRIPT_WRITING = "manuscript_writing"
    SUBMISSION = "submission"


@dataclass
class Milestone:
    """Research milestone"""
    name: str
    phase: ResearchPhase
    completed: bool = False
    completed_date: Optional[datetime] = None


@dataclass
class ResearchProject:
    """Full research project state"""
    project_id: str
    created_date: datetime

    # Question Formulation
    research_question: Optional[str] = None
    pico_elements: Dict[str, str] = field(default_factory=dict)
    finer_scores: Dict[str, float] = field(default_factory=dict)

    # Study Design
    study_design: Optional[str] = None
    protocol_status: str = "not_started"
    sample_size: Optional[int] = None
    ethics_status: str = "pending"

    # Data Analysis
    data_collection_status: str = "not_started"
    analysis_plan: Optional[str] = None
    results: Dict = field(default_factory=dict)

    # Writing
    manuscript_status: str = "not_started"
    target_journal: Optional[str] = None
    word_count: int = 0

    # Submission
    submission_status: str = "not_submitted"
    submission_date: Optional[datetime] = None
    revision_rounds: int = 0

    # Progress tracking
    current_phase: ResearchPhase = ResearchPhase.QUESTION_FORMULATION
    milestones: List[Milestone] = field(default_factory=list)

    # Specialist consultations
    consultations_log: List[Dict] = field(default_factory=list)


class ResearchLifecycleManager:
    """Manages full research lifecycle"""

    def __init__(self, config_path: str = ".acs_mentor/lifecycle_config.yaml"):
        """Initialize lifecycle manager"""
        self.config = self._load_config(config_path)
        self.projects: Dict[str, ResearchProject] = {}

    def _load_config(self, config_path: str) -> Dict:
        """Load configuration"""
        if not os.path.exists(config_path):
            print(f"Warning: Config not found: {config_path}")
            return {}

        with open(config_path, 'r', encoding='utf-8') as f:
            return yaml.safe_load(f)

    def create_project(self, project_id: str) -> ResearchProject:
        """
        Create new research project

        Args:
            project_id: Unique project identifier

        Returns:
            ResearchProject
        """
        project = ResearchProject(
            project_id=project_id,
            created_date=datetime.now()
        )

        # Initialize milestones
        milestones_config = self.config.get('context_management', {}).get('milestones_tracking', [])
        for milestone_def in milestones_config:
            milestone = Milestone(
                name=milestone_def['milestone'],
                phase=ResearchPhase(milestone_def['phase'])
            )
            project.milestones.append(milestone)

        self.projects[project_id] = project
        return project

    def formulate_question(
        self,
        project_id: str,
        research_question: str,
        pico_elements: Optional[Dict[str, str]] = None
    ) -> Dict:
        """
        Phase 1: Research Question Formulation

        Args:
            project_id: Project ID
            research_question: Initial research question
            pico_elements: PICO framework elements

        Returns:
            Formulation guidance and assessment
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")

        # Update project state
        project.research_question = research_question
        if pico_elements:
            project.pico_elements = pico_elements

        # PICO template
        pico_template = self.config.get('question_formulation', {}).get('frameworks', {}).get('PICO', {})

        # FINER assessment (simplified - in production, use LLM)
        finer_scores = {
            'Feasible': 4.0,  # Placeholder
            'Interesting': 4.5,
            'Novel': 3.5,
            'Ethical': 5.0,
            'Relevant': 4.0
        }
        project.finer_scores = finer_scores

        # Check if milestone completed
        for milestone in project.milestones:
            if milestone.name == "RQ formulated":
                milestone.completed = True
                milestone.completed_date = datetime.now()

        # Move to next phase
        project.current_phase = ResearchPhase.STUDY_DESIGN

        return {
            'research_question': research_question,
            'pico_elements': project.pico_elements,
            'finer_scores': finer_scores,
            'recommendations': [
                "PICO framework suggests clear population and outcome",
                "FINER assessment indicates strong feasibility",
                "Next step: Design study protocol"
            ]
        }

    def design_study(
        self,
        project_id: str,
        study_design: str,
        sample_size: Optional[int] = None
    ) -> Dict:
        """
        Phase 2: Study Design

        Args:
            project_id: Project ID
            study_design: Type of study (RCT, cohort, etc.)
            sample_size: Calculated sample size

        Returns:
            Design guidance
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")

        # Update state
        project.study_design = study_design
        project.sample_size = sample_size
        project.protocol_status = "draft"

        # Get reporting standard
        reporting_standards = self.config.get('study_design', {}).get('reporting_standards', {})
        reporting_standard = reporting_standards.get(study_design.lower(), "STROBE")

        # Protocol template
        protocol_template = self.config.get('study_design', {}).get('protocol_template', {})

        # Mark milestone
        for milestone in project.milestones:
            if milestone.name == "Protocol complete":
                milestone.completed = True
                milestone.completed_date = datetime.now()

        return {
            'study_design': study_design,
            'sample_size': sample_size,
            'reporting_standard': reporting_standard,
            'protocol_sections': protocol_template.get('sections', []),
            'recommendations': [
                f"Follow {reporting_standard} guidelines for reporting",
                "Complete protocol before data collection",
                "Obtain ethics approval"
            ]
        }

    def analyze_data(
        self,
        project_id: str,
        analysis_type: str = "primary"
    ) -> Dict:
        """
        Phase 3: Data Analysis

        Args:
            project_id: Project ID
            analysis_type: Type of analysis (primary, secondary, sensitivity)

        Returns:
            Analysis guidance
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")

        # Get analysis workflow
        workflow = self.config.get('data_analysis', {}).get('workflow', [])

        # Analysis plan template
        sap_template = self.config.get('data_analysis', {}).get('analysis_plan_template', '')

        # Mark milestone
        for milestone in project.milestones:
            if milestone.name == "Analysis complete":
                milestone.completed = True
                milestone.completed_date = datetime.now()

        # Move to writing phase
        project.current_phase = ResearchPhase.MANUSCRIPT_WRITING

        return {
            'analysis_workflow': workflow,
            'sap_template': sap_template,
            'recommendations': [
                "Follow pre-specified analysis plan",
                "Check all assumptions",
                "Perform sensitivity analyses",
                "Prepare Table 1 (baseline characteristics)"
            ]
        }

    def write_manuscript(
        self,
        project_id: str,
        section: str = "methods"
    ) -> Dict:
        """
        Phase 4: Manuscript Writing

        Args:
            project_id: Project ID
            section: Which section to write (abstract, intro, methods, results, discussion)

        Returns:
            Writing guidance
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")

        # Get structure
        manuscript_structure = self.config.get('manuscript_writing', {}).get('structure', [])

        # Find section guidance
        section_guidance = None
        for sec in manuscript_structure:
            if sec['section'].lower() == section.lower():
                section_guidance = sec
                break

        # Mark milestone
        for milestone in project.milestones:
            if milestone.name == "Manuscript drafted":
                milestone.completed = True
                milestone.completed_date = datetime.now()

        # Move to submission phase
        project.current_phase = ResearchPhase.SUBMISSION

        return {
            'section': section,
            'guidance': section_guidance,
            'reporting_standard': f"Follow {project.study_design} checklist",
            'recommendations': [
                f"Word limit: {section_guidance.get('word_limit', 'N/A') if section_guidance else 'N/A'}",
                "Use clear, concise language",
                "Follow IMRaD structure"
            ]
        }

    def prepare_submission(
        self,
        project_id: str,
        target_journal: str
    ) -> Dict:
        """
        Phase 5: Submission

        Args:
            project_id: Project ID
            target_journal: Target journal name

        Returns:
            Submission guidance
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")

        # Update state
        project.target_journal = target_journal

        # Get checklist
        checklist = self.config.get('submission', {}).get('submission_checklist', [])

        # Cover letter template
        cover_letter_template = self.config.get('submission', {}).get('cover_letter_template', '')

        return {
            'target_journal': target_journal,
            'checklist': checklist,
            'cover_letter_template': cover_letter_template,
            'recommendations': [
                "Complete all checklist items",
                "Ensure manuscript follows journal format",
                "Include reporting checklist"
            ]
        }

    def get_progress(self, project_id: str) -> Dict:
        """
        Get project progress summary

        Args:
            project_id: Project ID

        Returns:
            Progress summary
        """
        project = self.projects.get(project_id)
        if not project:
            raise ValueError(f"Project not found: {project_id}")

        completed_milestones = [m for m in project.milestones if m.completed]
        total_milestones = len(project.milestones)

        return {
            'project_id': project_id,
            'current_phase': project.current_phase.value,
            'milestones_completed': len(completed_milestones),
            'total_milestones': total_milestones,
            'progress_percentage': (len(completed_milestones) / total_milestones * 100) if total_milestones > 0 else 0,
            'next_milestone': next((m.name for m in project.milestones if not m.completed), "All complete!"),
            'project_summary': {
                'research_question': project.research_question,
                'study_design': project.study_design,
                'target_journal': project.target_journal,
                'created_date': project.created_date.isoformat()
            }
        }


# Example usage
if __name__ == "__main__":
    manager = ResearchLifecycleManager()

    # Create project
    project_id = "adherence_study_2025"
    project = manager.create_project(project_id)
    print(f"Created project: {project_id}\n")

    # Phase 1: Formulate question
    rq_result = manager.formulate_question(
        project_id,
        research_question="Does a medication reminder app improve adherence in elderly patients?",
        pico_elements={
            'P': 'Elderly patients (≥65 years) with chronic conditions',
            'I': 'Medication reminder mobile app',
            'C': 'Standard care',
            'O': 'Medication adherence rate'
        }
    )
    print("Phase 1 - Question Formulation:")
    print(f"  RQ: {rq_result['research_question']}")
    print(f"  FINER scores: {rq_result['finer_scores']}\n")

    # Phase 2: Design study
    design_result = manager.design_study(
        project_id,
        study_design="RCT",
        sample_size=200
    )
    print("Phase 2 - Study Design:")
    print(f"  Design: {design_result['study_design']}")
    print(f"  Sample size: {design_result['sample_size']}")
    print(f"  Reporting: {design_result['reporting_standard']}\n")

    # Get progress
    progress = manager.get_progress(project_id)
    print("Project Progress:")
    print(f"  Current phase: {progress['current_phase']}")
    print(f"  Milestones: {progress['milestones_completed']}/{progress['total_milestones']}")
    print(f"  Progress: {progress['progress_percentage']:.1f}%")
    print(f"  Next: {progress['next_milestone']}")
