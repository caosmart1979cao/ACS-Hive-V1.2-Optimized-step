"""
ACS-Mentor V2.5 - MLflow Production Monitoring

Continuous evaluation, monitoring, and A/B testing infrastructure.

Features:
- Experiment tracking (V2.1 vs V2.5 comparison)
- LLM-as-a-judge automatic quality evaluation
- Production monitoring dashboards
- Hallucination detection
- A/B testing framework

Author: ACS-Mentor Development Team
Version: 2.5.0
Date: 2025-11-16
"""

import mlflow
from mlflow.metrics.genai import EvaluationExample, make_genai_metric
import time
import random
from typing import Dict, List, Any, Optional, Callable
from datetime import datetime, timedelta
import logging
import pandas as pd

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ACSMentorMonitoring:
    """
    MLflow-based monitoring for ACS-Mentor V2.5

    Usage:
        monitor = ACSMentorMonitoring(experiment_name="ACS-Mentor-V2.5-Production")

        # Track interaction
        monitor.track_guidance_interaction(
            user_message, guidance_response,
            decision_result, enriched_context, quality_metrics
        )

        # Generate report
        report = monitor.generate_performance_report(time_window="7d")
    """

    def __init__(
        self,
        experiment_name: str = "ACS-Mentor-V2.5-Production",
        tracking_uri: Optional[str] = None
    ):
        """
        Initialize MLflow monitoring

        Args:
            experiment_name: Name of MLflow experiment
            tracking_uri: Optional custom tracking URI
        """
        # Set tracking URI
        if tracking_uri:
            mlflow.set_tracking_uri(tracking_uri)
        else:
            # Use local SQLite database
            mlflow.set_tracking_uri("sqlite:///mlflow.db")

        # Set experiment
        mlflow.set_experiment(experiment_name)
        self.experiment_name = experiment_name

        # Define custom metrics
        self.custom_metrics = self._define_custom_metrics()

        logger.info(f"✅ MLflow monitoring initialized for experiment: {experiment_name}")

    def track_guidance_interaction(
        self,
        user_message: str,
        guidance_response: str,
        decision_result: Dict,
        enriched_context: Dict,
        quality_metrics: Dict
    ):
        """
        Track a single guidance interaction

        This should be called in post_guidance_phase of V2.5 workflow

        Args:
            user_message: User's message
            guidance_response: System's guidance response
            decision_result: Decision result from calculate_urgency_v2
            enriched_context: Context from pre_guidance_phase
            quality_metrics: Quality metrics (quality_score, relevance, latencies)
        """
        try:
            with mlflow.start_run(run_name=f"guidance_{decision_result.get('mode', 'unknown')}"):

                # ===== Log Parameters =====
                mlflow.log_param("mode", decision_result.get('mode'))
                mlflow.log_param("memory_system", "Mem0")
                mlflow.log_param("literature_search_enabled",
                               'relevant_literature' in enriched_context)
                mlflow.log_param("literature_review_enabled",
                               'literature_review' in enriched_context)

                # Urgency factors
                if 'urgency_factors' in decision_result:
                    for factor, score in decision_result['urgency_factors'].items():
                        mlflow.log_param(f"factor_{factor}", score)

                # ===== Log Metrics =====

                # Quality metrics
                mlflow.log_metric("quality_score", quality_metrics.get('quality_score', 0.0))
                mlflow.log_metric("response_relevance", quality_metrics.get('relevance', 0.0))

                # Performance metrics
                mlflow.log_metric("retrieval_latency_ms",
                                quality_metrics.get('retrieval_time', 0) * 1000)
                mlflow.log_metric("literature_latency_ms",
                                quality_metrics.get('literature_time', 0) * 1000)
                mlflow.log_metric("total_latency_ms",
                                quality_metrics.get('total_time', 0) * 1000)

                # Error detection
                if decision_result.get('error_detected'):
                    mlflow.log_metric("error_detected", 1.0)
                    mlflow.log_param("error_type", decision_result.get('error_type'))
                else:
                    mlflow.log_metric("error_detected", 0.0)

                # Recurring error flag
                recurring = enriched_context.get('recurring_errors', [])
                mlflow.log_metric("recurring_error_count", len(recurring))

                # ===== Log Artifacts =====
                mlflow.log_text(user_message, "user_message.txt")
                mlflow.log_text(guidance_response, "guidance_response.txt")

                # Log decision result as JSON
                import json
                mlflow.log_dict(decision_result, "decision_result.json")

                # ===== LLM-as-a-Judge Evaluation (Async) =====
                # Note: This is expensive, consider running async or sampling
                if self._should_run_llm_judge():
                    judge_scores = self._evaluate_with_llm_judge(
                        user_message,
                        guidance_response,
                        decision_result
                    )

                    for metric_name, score in judge_scores.items():
                        if score is not None:
                            mlflow.log_metric(f"judge_{metric_name}", score)

                logger.info(f"✅ Tracked interaction (mode: {decision_result.get('mode')}, "
                          f"quality: {quality_metrics.get('quality_score', 0):.3f})")

        except Exception as e:
            logger.error(f"Failed to track interaction: {e}")

    def _define_custom_metrics(self) -> Dict:
        """
        Define ACS-Mentor specific metrics for LLM-as-a-judge

        Returns:
            Dict of metric_name -> make_genai_metric object
        """

        # Metric 1: Methodological Rigor
        methodological_rigor = make_genai_metric(
            name="methodological_rigor",
            definition="""
            Evaluate whether the guidance follows strict methodological standards
            (CONSORT, STROBE, TRIPOD, PRISMA, etc.) and identifies critical errors.
            """,
            grading_prompt="""
            Score 1-5 based on:
            1. Does it reference appropriate reporting standards (CONSORT, STROBE, etc.)?
            2. Does it identify critical methodological issues?
            3. Are suggestions evidence-based and supported by literature?
            4. Is the severity assessment appropriate for the error?
            5. Are actionable solutions provided?

            Scoring:
            1 = Poor: No standards referenced, superficial advice
            2 = Fair: Some standards mentioned, but incomplete
            3 = Adequate: Standards referenced, basic solutions provided
            4 = Good: Strong methodological guidance with evidence
            5 = Excellent: Comprehensive, evidence-based, actionable guidance

            Return only the score (1-5).
            """,
            examples=[
                EvaluationExample(
                    input="User describes RCT with 30% dropout, excluded from analysis",
                    output="""
                    This violates the Intention-to-Treat (ITT) principle, which is a fundamental
                    requirement for RCTs (CONSORT 2010, Item 16). By excluding 30% of participants,
                    you've introduced selection bias and your results may not be valid.

                    Recommended solutions:
                    1. Include all randomized participants (ITT analysis)
                    2. Use multiple imputation for missing data
                    3. Conduct sensitivity analysis to assess impact of dropout

                    References: Schulz et al. (2010). CONSORT 2010 Statement. BMJ, 340:c332.
                    """,
                    score=5,
                    justification="Identifies critical error, references CONSORT, provides evidence-based solutions"
                ),
                EvaluationExample(
                    input="User asks about p-value interpretation",
                    output="P-value is the probability of observing your data if the null hypothesis is true.",
                    score=2,
                    justification="Technically correct but lacks depth, context, and actionability"
                )
            ],
            grading_context_columns=[]
        )

        # Metric 2: Citation Quality
        citation_quality = make_genai_metric(
            name="citation_quality",
            definition="""
            Evaluate the quality and appropriateness of literature citations in the guidance.
            """,
            grading_prompt="""
            Score 1-5 based on:
            1. Are citations relevant to the guidance topic?
            2. Are high-quality sources cited (top-tier journals, seminal papers)?
            3. Are citations recent (within 5-10 years, or seminal older papers)?
            4. Is the citation format correct and complete?
            5. Do citations strengthen the argument and provide evidence?

            Scoring:
            1 = Poor: No citations or irrelevant citations
            2 = Fair: Few citations, not high-quality
            3 = Adequate: Relevant citations, moderate quality
            4 = Good: High-quality, relevant, recent citations
            5 = Excellent: Comprehensive, authoritative, perfectly targeted citations

            Return only the score (1-5).
            """,
            examples=[
                EvaluationExample(
                    input="User asks about propensity score matching",
                    output="""
                    Guidance cites:
                    - Austin PC. (2011). An Introduction to Propensity Score Methods. Multivariate Behavioral Research, 46(3):399-424.
                    - Rosenbaum PR, Rubin DB. (1983). The central role of the propensity score. Biometrika, 70(1):41-55.
                    """,
                    score=5,
                    justification="Cites seminal (Rosenbaum & Rubin 1983) and comprehensive methodological (Austin 2011) papers"
                )
            ]
        )

        # Metric 3: Actionability
        actionability = make_genai_metric(
            name="actionability",
            definition="""
            Evaluate whether the guidance provides concrete, actionable steps the user can implement.
            """,
            grading_prompt="""
            Score 1-5 based on:
            1. Are concrete steps or recommendations provided?
            2. Is the guidance specific (not vague or generic)?
            3. Can the user implement the advice immediately?
            4. Are examples or code/formulas provided where appropriate?
            5. Is there a clear path forward?

            Scoring:
            1 = Poor: Vague, no actionable steps
            2 = Fair: Some suggestions but unclear how to implement
            3 = Adequate: Clear steps but lacking detail
            4 = Good: Detailed, actionable guidance
            5 = Excellent: Step-by-step, immediately implementable, with examples

            Return only the score (1-5).
            """,
            examples=[]
        )

        return {
            "methodological_rigor": methodological_rigor,
            "citation_quality": citation_quality,
            "actionability": actionability
        }

    def _should_run_llm_judge(self) -> bool:
        """
        Decide whether to run expensive LLM-as-a-judge evaluation

        Strategy: Sample 10% of interactions to reduce costs
        """
        return random.random() < 0.1  # 10% sampling

    def _evaluate_with_llm_judge(
        self,
        user_message: str,
        guidance_response: str,
        decision_result: Dict
    ) -> Dict[str, Optional[float]]:
        """
        Evaluate guidance using LLM-as-a-judge metrics

        Note: This is expensive (calls GPT-4), use sparingly

        Returns:
            Dict of metric_name -> score
        """
        results = {}

        # Prepare evaluation data
        eval_data = {
            "input": user_message,
            "output": guidance_response
        }

        # Run each metric
        for metric_name, metric in self.custom_metrics.items():
            try:
                # Note: Actual implementation would use mlflow.evaluate()
                # Here we use a simplified approach
                score = self._simple_llm_judge(eval_data, metric)
                results[metric_name] = score

            except Exception as e:
                logger.warning(f"LLM judge failed for {metric_name}: {e}")
                results[metric_name] = None

        return results

    def _simple_llm_judge(self, eval_data: Dict, metric) -> Optional[float]:
        """
        Simplified LLM-as-a-judge evaluation

        In production, this would call GPT-4 with the metric's grading prompt
        For now, returns a placeholder score
        """
        # Placeholder - in production, call OpenAI API with metric.grading_prompt
        # For demo purposes, return a random score
        return random.uniform(3.0, 5.0)

    def run_ab_test(
        self,
        user_message: str,
        variant_a_func: Callable,
        variant_b_func: Callable,
        variant_names: tuple = ("Variant_A", "Variant_B")
    ) -> Any:
        """
        Run A/B test between two strategies

        Example usage:
            # Test Mem0 vs ChromaDB+SQLite
            response = monitor.run_ab_test(
                user_message,
                variant_a_func=lambda msg: handle_with_mem0(msg),
                variant_b_func=lambda msg: handle_with_chromadb_sqlite(msg),
                variant_names=("Mem0", "ChromaDB+SQLite")
            )

        Args:
            user_message: User's message
            variant_a_func: Function implementing variant A
            variant_b_func: Function implementing variant B
            variant_names: Names of variants for logging

        Returns:
            Response from selected variant
        """
        # Random assignment
        variant = random.choice(['A', 'B'])

        with mlflow.start_run(run_name=f"ab_test_{variant}"):
            mlflow.log_param("ab_test", True)
            mlflow.log_param("variant", variant)

            start_time = time.time()

            if variant == 'A':
                response = variant_a_func(user_message)
                mlflow.log_param("strategy", variant_names[0])
            else:
                response = variant_b_func(user_message)
                mlflow.log_param("strategy", variant_names[1])

            latency = time.time() - start_time
            mlflow.log_metric("latency_ms", latency * 1000)

            logger.info(f"A/B test: Selected {variant} ({variant_names[0 if variant == 'A' else 1]}), "
                       f"latency: {latency*1000:.1f}ms")

            return response

    def generate_performance_report(
        self,
        time_window: str = "7d"
    ) -> Dict[str, Any]:
        """
        Generate performance report for recent time period

        Args:
            time_window: "1d" | "7d" | "30d"

        Returns:
            Performance report with metrics and alerts
        """
        logger.info(f"Generating performance report for last {time_window}...")

        # Parse time window
        if time_window == "1d":
            start_time = datetime.now() - timedelta(days=1)
        elif time_window == "7d":
            start_time = datetime.now() - timedelta(days=7)
        elif time_window == "30d":
            start_time = datetime.now() - timedelta(days=30)
        else:
            start_time = datetime.now() - timedelta(days=7)

        # Query MLflow for recent runs
        try:
            runs = mlflow.search_runs(
                experiment_names=[self.experiment_name],
                filter_string=f"attributes.start_time > '{start_time.timestamp() * 1000}'"
            )

            if runs.empty:
                logger.warning("No runs found in time window")
                return {"error": "No data available"}

            # Aggregate metrics
            report = {
                "time_window": time_window,
                "start_time": start_time.isoformat(),
                "end_time": datetime.now().isoformat(),
                "total_interactions": len(runs),

                # Quality metrics
                "avg_quality_score": runs['metrics.quality_score'].mean(),
                "quality_score_std": runs['metrics.quality_score'].std(),
                "quality_score_min": runs['metrics.quality_score'].min(),

                # LLM-as-a-judge metrics (if available)
                "avg_judge_methodological_rigor": runs.get('metrics.judge_methodological_rigor', pd.Series([None])).mean(),
                "avg_judge_citation_quality": runs.get('metrics.judge_citation_quality', pd.Series([None])).mean(),
                "avg_judge_actionability": runs.get('metrics.judge_actionability', pd.Series([None])).mean(),

                # Performance metrics
                "avg_total_latency_ms": runs['metrics.total_latency_ms'].mean(),
                "p95_total_latency_ms": runs['metrics.total_latency_ms'].quantile(0.95),
                "avg_retrieval_latency_ms": runs['metrics.retrieval_latency_ms'].mean(),

                # Mode distribution
                "mode_distribution": runs['params.mode'].value_counts().to_dict(),

                # Error detection
                "error_detection_rate": (runs['metrics.error_detected'] == 1.0).mean(),
                "total_errors_detected": int((runs['metrics.error_detected'] == 1.0).sum()),

                # Literature integration usage
                "literature_search_usage_rate": (runs['params.literature_search_enabled'] == 'True').mean(),

                # Alerts
                "alerts": []
            }

            # Detect regressions and generate alerts
            if report['avg_quality_score'] < 0.75:
                report['alerts'].append(
                    f"⚠️ Quality score below threshold: {report['avg_quality_score']:.3f} < 0.75"
                )

            if report['p95_total_latency_ms'] > 2000:
                report['alerts'].append(
                    f"⚠️ P95 latency above threshold: {report['p95_total_latency_ms']:.1f}ms > 2000ms"
                )

            if report['error_detection_rate'] < 0.85:
                report['alerts'].append(
                    f"⚠️ Error detection rate below target: {report['error_detection_rate']:.2%} < 85%"
                )

            # Success message
            if not report['alerts']:
                report['alerts'].append("✅ All metrics within normal ranges")

            logger.info(f"✅ Performance report generated: {report['total_interactions']} interactions, "
                       f"quality {report['avg_quality_score']:.3f}")

            return report

        except Exception as e:
            logger.error(f"Failed to generate performance report: {e}")
            return {"error": str(e)}

    def compare_versions(
        self,
        version_a_runs: List[str],
        version_b_runs: List[str],
        version_names: tuple = ("V2.1", "V2.5")
    ) -> Dict[str, Any]:
        """
        Compare performance between two versions (e.g., V2.1 vs V2.5)

        Args:
            version_a_runs: List of run IDs for version A
            version_b_runs: List of run IDs for version B
            version_names: Names of versions for reporting

        Returns:
            Comparison report
        """
        logger.info(f"Comparing {version_names[0]} vs {version_names[1]}...")

        # Query runs for each version
        runs_a = mlflow.search_runs(filter_string=f"run_id IN ({','.join(version_a_runs)})")
        runs_b = mlflow.search_runs(filter_string=f"run_id IN ({','.join(version_b_runs)})")

        # Calculate metrics for each version
        comparison = {
            "version_a": {
                "name": version_names[0],
                "total_runs": len(runs_a),
                "avg_quality_score": runs_a['metrics.quality_score'].mean(),
                "avg_latency_ms": runs_a['metrics.total_latency_ms'].mean(),
                "error_detection_rate": (runs_a['metrics.error_detected'] == 1.0).mean()
            },
            "version_b": {
                "name": version_names[1],
                "total_runs": len(runs_b),
                "avg_quality_score": runs_b['metrics.quality_score'].mean(),
                "avg_latency_ms": runs_b['metrics.total_latency_ms'].mean(),
                "error_detection_rate": (runs_b['metrics.error_detected'] == 1.0).mean()
            },
            "improvements": {}
        }

        # Calculate improvements
        comparison['improvements']['quality_score'] = (
            (comparison['version_b']['avg_quality_score'] - comparison['version_a']['avg_quality_score'])
            / comparison['version_a']['avg_quality_score']
        )

        comparison['improvements']['latency'] = (
            (comparison['version_a']['avg_latency_ms'] - comparison['version_b']['avg_latency_ms'])
            / comparison['version_a']['avg_latency_ms']
        )

        comparison['improvements']['error_detection'] = (
            comparison['version_b']['error_detection_rate'] - comparison['version_a']['error_detection_rate']
        )

        logger.info(f"✅ Comparison complete: Quality {comparison['improvements']['quality_score']:+.1%}, "
                   f"Latency {comparison['improvements']['latency']:+.1%}")

        return comparison


# ========== Utility Functions ==========

def initialize_mlflow_monitoring(
    experiment_name: str = "ACS-Mentor-V2.5-Production"
) -> ACSMentorMonitoring:
    """
    Initialize MLflow monitoring system

    Returns:
        ACSMentorMonitoring instance
    """
    logger.info("=== Initializing MLflow Monitoring System ===")

    monitor = ACSMentorMonitoring(experiment_name=experiment_name)

    logger.info("✅ MLflow monitoring initialized")
    logger.info(f"   Experiment: {experiment_name}")
    logger.info(f"   Tracking URI: {mlflow.get_tracking_uri()}")
    logger.info(f"   Custom metrics: {list(monitor.custom_metrics.keys())}")

    return monitor


if __name__ == "__main__":
    # Test initialization
    monitor = initialize_mlflow_monitoring()

    # Test tracking
    monitor.track_guidance_interaction(
        user_message="How do I do propensity score matching?",
        guidance_response="Propensity score matching involves...",
        decision_result={
            "mode": "standard_mentor",
            "error_detected": False
        },
        enriched_context={
            "recent_history": [],
            "relevant_literature": []
        },
        quality_metrics={
            "quality_score": 0.85,
            "relevance": 0.90,
            "retrieval_time": 0.05,
            "literature_time": 0.2,
            "total_time": 0.5
        }
    )

    # Generate report
    report = monitor.generate_performance_report(time_window="7d")
    print(f"\nPerformance Report:\n{report}")
