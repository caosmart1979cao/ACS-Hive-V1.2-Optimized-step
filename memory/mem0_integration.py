"""
ACS-Mentor V2.5 - Mem0 Memory Integration

Replaces V2.1's ChromaDB+SQLite hybrid system with Mem0 unified memory layer.

Author: ACS-Mentor Development Team
Version: 2.5.0
Date: 2025-11-16
"""

from mem0 import Memory
import yaml
import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional, Any
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ACSMentorMemory:
    """
    Mem0-based memory system for ACS-Mentor V2.5

    Features:
    - Unified memory layer (replaces ChromaDB + SQLite)
    - Personalized context retention across sessions
    - Adaptive learning from user interactions
    - Auto-degradation to SQLite if Mem0 unavailable

    Usage:
        memory = ACSMentorMemory()

        # Pre-guidance: Retrieve context
        context = memory.retrieve_context(user_message, user_id)

        # Post-guidance: Store interaction
        memory.store_interaction(
            user_message, guidance_response,
            metadata={...}, user_id, session_id
        )
    """

    def __init__(self, config_path=".acs_mentor/mem0_config.yaml"):
        """
        Initialize Mem0 memory system

        Args:
            config_path: Path to Mem0 configuration file
        """
        self.config_path = config_path
        self.config = self._load_config()

        # Initialize Mem0
        try:
            self.memory = Memory(config=self.config.get('mem0_config', {}))
            self.mem0_available = True
            logger.info("✅ Mem0 initialized successfully")
        except Exception as e:
            logger.warning(f"⚠️ Mem0 initialization failed: {e}")
            self.memory = None
            self.mem0_available = False

        # Fallback configuration
        self.fallback_enabled = self.config.get('fallback_enabled', True)
        self.fallback_db_path = self.config.get('fallback_db_path',
                                                '.acs_mentor/memory.db')

        # Performance tracking
        self.error_count = 0
        self.degradation_threshold = self.config.get(
            'degradation', {}
        ).get('fallback_after_errors', 3)

    def _load_config(self) -> Dict:
        """Load configuration from YAML file"""
        if not os.path.exists(self.config_path):
            logger.warning(f"Config file not found: {self.config_path}, using defaults")
            return self._get_default_config()

        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return yaml.safe_load(f)
        except Exception as e:
            logger.error(f"Failed to load config: {e}")
            return self._get_default_config()

    def _get_default_config(self) -> Dict:
        """Return default configuration"""
        return {
            'mem0_config': {},
            'fallback_enabled': True,
            'fallback_db_path': '.acs_mentor/memory.db',
            'degradation': {
                'max_latency_ms': 200,
                'max_error_rate': 0.05,
                'fallback_after_errors': 3
            }
        }

    def retrieve_context(self, user_message: str, user_id: str,
                        context_type: str = "all") -> Dict[str, Any]:
        """
        Retrieve relevant context for pre-guidance phase

        This replaces V2.1's multiple retrieval steps:
        - Step 2: Retrieve recent interactions
        - Step 3: Check recurring errors
        - Step 4: Semantic search similar success cases

        Args:
            user_message: Current user query
            user_id: User identifier
            context_type: "all" | "history" | "success_cases" | "error_patterns"

        Returns:
            enriched_context: Dict containing:
                - recent_history: List of recent interactions
                - similar_success_cases: List of high-quality similar cases
                - recurring_errors: List of recurring error patterns
        """
        try:
            if self.mem0_available and self.error_count < self.degradation_threshold:
                return self._retrieve_from_mem0(user_message, user_id, context_type)
            elif self.fallback_enabled:
                logger.info("Using SQLite fallback for retrieval")
                return self._fallback_retrieve(user_message, user_id)
            else:
                logger.warning("Memory system unavailable, returning empty context")
                return self._empty_context()

        except Exception as e:
            logger.error(f"Retrieval failed: {e}")
            self.error_count += 1

            if self.fallback_enabled:
                return self._fallback_retrieve(user_message, user_id)
            return self._empty_context()

    def _retrieve_from_mem0(self, user_message: str, user_id: str,
                           context_type: str) -> Dict[str, Any]:
        """Retrieve context using Mem0"""

        # Search memories
        results = self.memory.search(
            query=user_message,
            user_id=user_id,
            limit=10  # Retrieve top 10, then categorize
        )

        # Initialize context structure
        enriched_context = {
            "recent_history": [],
            "similar_success_cases": [],
            "recurring_errors": []
        }

        # Categorize results
        for result in results:
            memory_content = result.get('memory', '')
            metadata = result.get('metadata', {})
            score = result.get('score', 0.0)

            # Recurring errors (high priority)
            if metadata.get('error_type') and metadata.get('occurrence_count', 0) >= 2:
                enriched_context['recurring_errors'].append({
                    "error_type": metadata.get('error_type'),
                    "occurrence_count": metadata.get('occurrence_count'),
                    "last_occurrence": metadata.get('timestamp'),
                    "memory": memory_content,
                    "score": score
                })

            # High-quality success cases (for guidance templates)
            elif metadata.get('quality_score', 0) >= 0.85:
                enriched_context['similar_success_cases'].append({
                    "user_message": metadata.get('user_message', ''),
                    "guidance_response": metadata.get('guidance_response', ''),
                    "mode": metadata.get('mode'),
                    "quality_score": metadata.get('quality_score'),
                    "memory": memory_content,
                    "score": score
                })

            # Recent history
            else:
                enriched_context['recent_history'].append({
                    "user_message": metadata.get('user_message', ''),
                    "guidance_response": metadata.get('guidance_response', ''),
                    "mode": metadata.get('mode'),
                    "timestamp": metadata.get('timestamp'),
                    "memory": memory_content,
                    "score": score
                })

        # Limit each category
        enriched_context['recent_history'] = enriched_context['recent_history'][:5]
        enriched_context['similar_success_cases'] = enriched_context['similar_success_cases'][:3]
        enriched_context['recurring_errors'] = enriched_context['recurring_errors'][:5]

        logger.info(f"Retrieved context: {len(enriched_context['recent_history'])} history, "
                   f"{len(enriched_context['similar_success_cases'])} success cases, "
                   f"{len(enriched_context['recurring_errors'])} recurring errors")

        return enriched_context

    def store_interaction(self, user_message: str, guidance_response: str,
                         metadata: Dict, user_id: str, session_id: str) -> bool:
        """
        Store interaction to memory (post-guidance phase)

        This replaces V2.1's:
        - Step 5: Store interaction to SQLite + ChromaDB
        - Step 6: Store as guidance case if high quality

        Args:
            user_message: User's message
            guidance_response: System's guidance response
            metadata: Dict containing mode, quality_score, etc.
            user_id: User identifier
            session_id: Session identifier

        Returns:
            success: True if stored successfully
        """
        try:
            # Prepare metadata
            full_metadata = {
                **metadata,
                "session_id": session_id,
                "timestamp": datetime.now().isoformat(),
                "user_message": user_message,
                "guidance_response": guidance_response
            }

            # Update recurring error count if applicable
            if metadata.get('error_detected') and metadata.get('error_type'):
                full_metadata['occurrence_count'] = self._get_error_count(
                    user_id, metadata['error_type']
                ) + 1

            if self.mem0_available and self.error_count < self.degradation_threshold:
                # Store to Mem0
                self.memory.add(
                    messages=[
                        {"role": "user", "content": user_message},
                        {"role": "assistant", "content": guidance_response}
                    ],
                    user_id=user_id,
                    metadata=full_metadata
                )

                logger.info(f"✅ Stored interaction to Mem0 (quality: {metadata.get('quality_score', 'N/A')})")
                return True

            elif self.fallback_enabled:
                logger.info("Using SQLite fallback for storage")
                return self._fallback_store(user_message, guidance_response,
                                          full_metadata, user_id, session_id)
            else:
                logger.warning("Memory system unavailable, interaction not stored")
                return False

        except Exception as e:
            logger.error(f"Storage failed: {e}")
            self.error_count += 1

            if self.fallback_enabled:
                return self._fallback_store(user_message, guidance_response,
                                          metadata, user_id, session_id)
            return False

    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve user capability profile

        Aggregates all user interactions to build comprehensive profile

        Returns:
            profile: Dict with user statistics and skill levels
        """
        try:
            if self.mem0_available:
                # Get all user memories
                all_memories = self.memory.get_all(user_id=user_id)

                # Aggregate statistics
                profile = {
                    "user_id": user_id,
                    "total_interactions": len(all_memories),
                    "skill_levels": self._extract_skill_levels(all_memories),
                    "common_error_types": self._extract_error_patterns(all_memories),
                    "avg_quality_score": self._calculate_avg_quality(all_memories),
                    "last_interaction": self._get_last_interaction_time(all_memories)
                }

                return profile

            elif self.fallback_enabled:
                return self._fallback_get_profile(user_id)

            else:
                return {"user_id": user_id, "error": "Profile unavailable"}

        except Exception as e:
            logger.error(f"Failed to get user profile: {e}")
            if self.fallback_enabled:
                return self._fallback_get_profile(user_id)
            return {"user_id": user_id, "error": str(e)}

    def _get_error_count(self, user_id: str, error_type: str) -> int:
        """Get count of specific error type for user"""
        try:
            if self.mem0_available:
                # Search for this error type
                results = self.memory.search(
                    query=error_type,
                    user_id=user_id,
                    limit=50
                )

                # Count occurrences
                count = sum(1 for r in results
                          if r.get('metadata', {}).get('error_type') == error_type)
                return count
            else:
                return 0
        except:
            return 0

    def _extract_skill_levels(self, memories: List) -> Dict[str, str]:
        """Extract skill levels from memories"""
        # Placeholder - implement based on skill_advancement metadata
        return {
            "study_design": "intermediate",
            "statistical_methods": "intermediate",
            "causal_inference": "novice"
        }

    def _extract_error_patterns(self, memories: List) -> List[str]:
        """Extract common error patterns"""
        error_types = {}
        for memory in memories:
            error_type = memory.get('metadata', {}).get('error_type')
            if error_type:
                error_types[error_type] = error_types.get(error_type, 0) + 1

        # Return top 5 most common errors
        sorted_errors = sorted(error_types.items(), key=lambda x: x[1], reverse=True)
        return [error for error, count in sorted_errors[:5]]

    def _calculate_avg_quality(self, memories: List) -> float:
        """Calculate average quality score"""
        scores = [m.get('metadata', {}).get('quality_score')
                 for m in memories
                 if m.get('metadata', {}).get('quality_score') is not None]

        if scores:
            return sum(scores) / len(scores)
        return 0.0

    def _get_last_interaction_time(self, memories: List) -> Optional[str]:
        """Get timestamp of last interaction"""
        if not memories:
            return None

        timestamps = [m.get('metadata', {}).get('timestamp')
                     for m in memories
                     if m.get('metadata', {}).get('timestamp')]

        if timestamps:
            return max(timestamps)
        return None

    # ========== Fallback Methods (SQLite) ==========

    def _fallback_retrieve(self, user_message: str, user_id: str) -> Dict[str, Any]:
        """Fallback to V2.1 SQLite retrieval"""
        try:
            conn = sqlite3.connect(self.fallback_db_path)
            cursor = conn.cursor()

            # Retrieve recent history
            cursor.execute("""
                SELECT user_message, guidance_response, mode_used, timestamp
                FROM user_interactions
                WHERE user_id = ?
                ORDER BY timestamp DESC
                LIMIT 5
            """, (user_id,))

            recent_history = [
                {
                    "user_message": row[0],
                    "guidance_response": row[1],
                    "mode": row[2],
                    "timestamp": row[3]
                }
                for row in cursor.fetchall()
            ]

            # Retrieve recurring errors
            cursor.execute("""
                SELECT error_type, COUNT(*) as occurrence_count
                FROM error_tracking
                WHERE user_id = ?
                  AND timestamp >= datetime('now', '-30 days')
                GROUP BY error_type
                HAVING occurrence_count >= 2
            """, (user_id,))

            recurring_errors = [
                {
                    "error_type": row[0],
                    "occurrence_count": row[1]
                }
                for row in cursor.fetchall()
            ]

            conn.close()

            return {
                "recent_history": recent_history,
                "similar_success_cases": [],  # Not available in simple SQLite
                "recurring_errors": recurring_errors
            }

        except Exception as e:
            logger.error(f"SQLite fallback retrieval failed: {e}")
            return self._empty_context()

    def _fallback_store(self, user_message: str, guidance_response: str,
                       metadata: Dict, user_id: str, session_id: str) -> bool:
        """Fallback to V2.1 SQLite storage"""
        try:
            conn = sqlite3.connect(self.fallback_db_path)
            cursor = conn.cursor()

            # Store to user_interactions
            cursor.execute("""
                INSERT INTO user_interactions
                (user_id, session_id, user_message, guidance_response,
                 mode_used, quality_score, timestamp)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                user_id,
                session_id,
                user_message,
                guidance_response,
                metadata.get('mode'),
                metadata.get('quality_score'),
                datetime.now().isoformat()
            ))

            # If error detected, store to error_tracking
            if metadata.get('error_detected') and metadata.get('error_type'):
                cursor.execute("""
                    INSERT INTO error_tracking
                    (user_id, error_type, error_category, severity, timestamp)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    user_id,
                    metadata.get('error_type'),
                    metadata.get('error_category'),
                    metadata.get('error_severity'),
                    datetime.now().isoformat()
                ))

            conn.commit()
            conn.close()

            logger.info("✅ Stored interaction to SQLite fallback")
            return True

        except Exception as e:
            logger.error(f"SQLite fallback storage failed: {e}")
            return False

    def _fallback_get_profile(self, user_id: str) -> Dict[str, Any]:
        """Fallback: Get user profile from SQLite"""
        try:
            conn = sqlite3.connect(self.fallback_db_path)
            cursor = conn.cursor()

            cursor.execute("""
                SELECT * FROM user_profiles WHERE user_id = ?
            """, (user_id,))

            row = cursor.fetchone()
            conn.close()

            if row:
                return {
                    "user_id": row[0],
                    "overall_level": row[1],
                    # ... parse other fields from V2.1 schema
                }
            else:
                return {"user_id": user_id, "overall_level": "intermediate"}

        except Exception as e:
            logger.error(f"SQLite profile retrieval failed: {e}")
            return {"user_id": user_id, "error": str(e)}

    def _empty_context(self) -> Dict[str, Any]:
        """Return empty context when memory unavailable"""
        return {
            "recent_history": [],
            "similar_success_cases": [],
            "recurring_errors": []
        }

    # ========== Health Check ==========

    def health_check(self) -> Dict[str, Any]:
        """
        Check memory system health

        Returns:
            status: Dict with health metrics
        """
        status = {
            "mem0_available": self.mem0_available,
            "fallback_enabled": self.fallback_enabled,
            "error_count": self.error_count,
            "degraded": self.error_count >= self.degradation_threshold
        }

        # Test Mem0 connection if available
        if self.mem0_available:
            try:
                test_result = self.memory.search(query="test", user_id="health_check", limit=1)
                status["mem0_responsive"] = True
            except:
                status["mem0_responsive"] = False

        return status


# ========== Utility Functions ==========

def initialize_mem0_system(config_path=".acs_mentor/mem0_config.yaml"):
    """
    Initialize Mem0 system for first-time use

    Returns:
        memory: ACSMentorMemory instance
    """
    logger.info("=== Initializing Mem0 Memory System ===")

    # Create config directory if not exists
    os.makedirs(".acs_mentor", exist_ok=True)

    # Initialize memory
    memory = ACSMentorMemory(config_path=config_path)

    # Health check
    health = memory.health_check()
    logger.info(f"Health check: {health}")

    if health['mem0_available']:
        logger.info("✅ Mem0 system initialized successfully")
    elif health['fallback_enabled']:
        logger.info("⚠️ Mem0 unavailable, using SQLite fallback")
    else:
        logger.error("❌ Memory system unavailable")

    return memory


if __name__ == "__main__":
    # Test initialization
    memory = initialize_mem0_system()

    # Test retrieval
    context = memory.retrieve_context(
        user_message="How do I do propensity score matching?",
        user_id="test_user_001"
    )
    print(f"\nRetrieved context: {context}")

    # Test storage
    success = memory.store_interaction(
        user_message="How do I do propensity score matching?",
        guidance_response="Propensity score matching involves...",
        metadata={
            "mode": "standard_mentor",
            "quality_score": 0.85,
            "error_detected": False
        },
        user_id="test_user_001",
        session_id="session_001"
    )
    print(f"\nStorage success: {success}")

    # Test profile
    profile = memory.get_user_profile("test_user_001")
    print(f"\nUser profile: {profile}")
