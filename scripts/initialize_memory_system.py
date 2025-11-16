#!/usr/bin/env python3
"""
ACS-Mentor V2.1 - Memory System Initialization Script
初始化混合内存系统（ChromaDB + SQLite）

Usage:
    python initialize_memory_system.py [--no-chromadb] [--migrate-from-v2]

Options:
    --no-chromadb      只初始化SQLite，跳过ChromaDB（最小化依赖）
    --migrate-from-v2  从V2.0迁移user_profile数据
"""

import os
import sys
import sqlite3
import json
import argparse
from pathlib import Path
from datetime import datetime
import logging

# 配置logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# ============================================================================
# 配置
# ============================================================================

BASE_DIR = Path(__file__).parent.parent  # ACS-Hive-V1.2-Optimized-step/
MEMORY_DIR = BASE_DIR / ".acs_mentor"
VECTOR_DB_DIR = MEMORY_DIR / "vector_db"
SQLITE_DB_PATH = MEMORY_DIR / "memory.db"

# ============================================================================
# 目录创建
# ============================================================================

def create_directories():
    """创建必要的目录结构"""
    logger.info("Creating directory structure...")

    MEMORY_DIR.mkdir(exist_ok=True)
    VECTOR_DB_DIR.mkdir(exist_ok=True)

    logger.info(f"✓ Created: {MEMORY_DIR}")
    logger.info(f"✓ Created: {VECTOR_DB_DIR}")

# ============================================================================
# SQLite初始化
# ============================================================================

def initialize_sqlite():
    """初始化SQLite数据库和所有表"""
    logger.info("Initializing SQLite database...")

    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    # 启用外键约束
    cursor.execute("PRAGMA foreign_keys = ON;")

    # Table 1: user_profiles
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_profiles (
            user_id TEXT PRIMARY KEY,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            -- 能力水平评估
            overall_level TEXT CHECK(overall_level IN ('novice', 'intermediate', 'advanced')) DEFAULT 'novice',

            -- 技能领域评分 (0.0-1.0)
            skill_study_design REAL DEFAULT 0.0,
            skill_statistics REAL DEFAULT 0.0,
            skill_writing REAL DEFAULT 0.0,
            skill_critical_appraisal REAL DEFAULT 0.0,

            -- 交互统计
            total_interactions INTEGER DEFAULT 0,
            total_errors_detected INTEGER DEFAULT 0,
            total_guidance_received INTEGER DEFAULT 0,

            -- 学习轨迹
            current_learning_focus TEXT,
            skill_tree_progress TEXT,  -- JSON format

            -- 偏好设置
            preferred_mode TEXT DEFAULT 'balanced',
            response_depth_preference TEXT DEFAULT 'standard'
        );
    """)

    # 索引
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_user_level ON user_profiles(overall_level);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_updated ON user_profiles(updated_at);")

    # Table 2: session_history
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS session_history (
            session_id TEXT PRIMARY KEY,
            user_id TEXT,
            start_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            end_time TIMESTAMP,

            -- 会话元数据
            session_type TEXT,  -- research_review, writing_guidance, strategic_planning
            primary_topic TEXT,
            mode_used TEXT,

            -- 会话统计
            total_turns INTEGER DEFAULT 0,
            errors_detected INTEGER DEFAULT 0,
            guidance_provided INTEGER DEFAULT 0,

            -- 会话评估
            complexity_score REAL,
            user_satisfaction REAL,

            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
        );
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_user ON session_history(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_session_time ON session_history(start_time);")

    # Table 3: skill_progress
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS skill_progress (
            progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            skill_domain TEXT,  -- study_design, statistics, writing, critical_appraisal
            skill_name TEXT,

            -- 进展记录
            previous_level TEXT,
            current_level TEXT,
            advancement_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            -- 晋级证据
            mastery_evidence TEXT,  -- 描述达成mastery_criteria的具体表现

            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id)
        );
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_skill_user ON skill_progress(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_skill_domain ON skill_progress(skill_domain);")

    # Table 4: error_tracking
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS error_tracking (
            error_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id TEXT,
            session_id TEXT,
            detected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            -- 错误详情
            error_type TEXT,
            error_category TEXT,  -- statistical, methodological, reporting, interpretation
            error_severity TEXT CHECK(error_severity IN ('critical', 'moderate', 'minor')),
            error_description TEXT,

            -- 纠正记录
            correction_provided TEXT,
            user_acknowledged BOOLEAN DEFAULT 0,
            recurrence_flag BOOLEAN DEFAULT 0,

            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id),
            FOREIGN KEY (session_id) REFERENCES session_history(session_id)
        );
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_error_user ON error_tracking(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_error_type ON error_tracking(error_type);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_error_time ON error_tracking(detected_at);")

    # Table 5: user_interactions (for ChromaDB fallback)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS user_interactions (
            interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
            session_id TEXT,
            user_id TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

            -- 对话内容
            user_message TEXT,
            guidance_response TEXT,

            -- 元数据
            user_level TEXT,
            topic_category TEXT,
            mode_used TEXT,
            complexity_score REAL,
            quality_score REAL,
            user_satisfaction REAL,

            FOREIGN KEY (user_id) REFERENCES user_profiles(user_id),
            FOREIGN KEY (session_id) REFERENCES session_history(session_id)
        );
    """)

    cursor.execute("CREATE INDEX IF NOT EXISTS idx_interaction_user ON user_interactions(user_id);")
    cursor.execute("CREATE INDEX IF NOT EXISTS idx_interaction_time ON user_interactions(timestamp);")

    # 创建触发器：自动更新user_profiles的updated_at
    cursor.execute("""
        CREATE TRIGGER IF NOT EXISTS update_user_profile_timestamp
        AFTER UPDATE ON user_profiles
        FOR EACH ROW
        BEGIN
            UPDATE user_profiles SET updated_at = CURRENT_TIMESTAMP WHERE user_id = NEW.user_id;
        END;
    """)

    conn.commit()
    conn.close()

    logger.info(f"✓ SQLite initialized: {SQLITE_DB_PATH}")
    logger.info("✓ Created tables: user_profiles, session_history, skill_progress, error_tracking, user_interactions")
    logger.info("✓ Created indexes and triggers")

# ============================================================================
# ChromaDB初始化
# ============================================================================

def initialize_chromadb():
    """初始化ChromaDB向量数据库"""
    logger.info("Initializing ChromaDB...")

    try:
        import chromadb
    except ImportError:
        logger.warning("⚠️  ChromaDB not installed. Install with: pip install chromadb")
        logger.warning("   System will run in SQLite-only mode (degraded performance)")
        return False

    try:
        client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))

        # Collection 1: user_interactions
        try:
            client.get_collection("user_interactions")
            logger.info("  • user_interactions collection already exists")
        except:
            client.create_collection(
                name="user_interactions",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("  ✓ Created collection: user_interactions")

        # Collection 2: guidance_cases
        try:
            client.get_collection("guidance_cases")
            logger.info("  • guidance_cases collection already exists")
        except:
            client.create_collection(
                name="guidance_cases",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("  ✓ Created collection: guidance_cases")

        # Collection 3: error_patterns
        try:
            client.get_collection("error_patterns")
            logger.info("  • error_patterns collection already exists")
        except:
            client.create_collection(
                name="error_patterns",
                metadata={"hnsw:space": "cosine"}
            )
            logger.info("  ✓ Created collection: error_patterns")

        logger.info("✓ ChromaDB initialized successfully")
        return True

    except Exception as e:
        logger.error(f"✗ ChromaDB initialization failed: {e}")
        logger.warning("  System will run in SQLite-only mode")
        return False

# ============================================================================
# 健康检查
# ============================================================================

def health_check():
    """检查内存系统健康状态"""
    logger.info("\n" + "="*60)
    logger.info("Health Check")
    logger.info("="*60)

    health = {
        "sqlite": False,
        "chromadb": False
    }

    # Check SQLite
    try:
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()
        cursor.execute("SELECT 1;")
        result = cursor.fetchone()
        conn.close()

        if result:
            health["sqlite"] = True
            logger.info("✓ SQLite: Healthy")
    except Exception as e:
        logger.error(f"✗ SQLite: Unhealthy - {e}")

    # Check ChromaDB
    try:
        import chromadb
        client = chromadb.PersistentClient(path=str(VECTOR_DB_DIR))
        client.heartbeat()
        health["chromadb"] = True
        logger.info("✓ ChromaDB: Healthy")
    except ImportError:
        logger.warning("⚠ ChromaDB: Not installed (SQLite-only mode)")
    except Exception as e:
        logger.error(f"✗ ChromaDB: Unhealthy - {e}")

    # Overall status
    if health["sqlite"] and health["chromadb"]:
        logger.info("\n🎉 Overall Status: OPTIMAL (Hybrid mode)")
    elif health["sqlite"]:
        logger.info("\n⚠️  Overall Status: DEGRADED (SQLite-only mode)")
    else:
        logger.error("\n❌ Overall Status: CRITICAL (Memory system unavailable)")

    logger.info("="*60 + "\n")

    return health

# ============================================================================
# 从V2.0迁移
# ============================================================================

def migrate_from_v2():
    """从V2.0的mentorship_goals.yaml迁移用户数据"""
    logger.info("\n" + "="*60)
    logger.info("Migrating from V2.0")
    logger.info("="*60)

    try:
        import yaml
    except ImportError:
        logger.error("✗ PyYAML not installed. Install with: pip install pyyaml")
        return False

    v2_file = BASE_DIR / "mentorship_goals.yaml"

    if not v2_file.exists():
        logger.warning(f"⚠️  V2.0 file not found: {v2_file}")
        logger.info("  Skipping migration (this is OK for fresh installation)")
        return False

    try:
        with open(v2_file, 'r', encoding='utf-8') as f:
            v2_config = yaml.safe_load(f)

        user_profile = v2_config.get('user_capability_profile', {})

        if not user_profile:
            logger.warning("⚠️  No user_capability_profile found in V2.0 config")
            return False

        # 生成user_id（首次使用）
        user_id = "default_user_001"

        # 转换为V2.1格式
        v2_1_profile = {
            "user_id": user_id,
            "overall_level": user_profile.get('user_level', 'novice'),
            "skill_study_design": 0.0,
            "skill_statistics": 0.0,
            "skill_writing": 0.0,
            "skill_critical_appraisal": 0.0,
            "current_learning_focus": None,
            "skill_tree_progress": "{}",
            "preferred_mode": "balanced",
            "response_depth_preference": "standard"
        }

        # 如果V2.0有skill_scores，提取它们
        if 'skill_scores' in user_profile:
            skills = user_profile['skill_scores']
            v2_1_profile["skill_study_design"] = skills.get('study_design', 0.0)
            v2_1_profile["skill_statistics"] = skills.get('statistical_methods', 0.0)
            v2_1_profile["skill_writing"] = skills.get('scientific_writing', 0.0)
            v2_1_profile["skill_critical_appraisal"] = skills.get('critical_appraisal', 0.0)

        # 插入到SQLite
        conn = sqlite3.connect(SQLITE_DB_PATH)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT OR REPLACE INTO user_profiles (
                user_id, overall_level, skill_study_design, skill_statistics,
                skill_writing, skill_critical_appraisal, current_learning_focus,
                skill_tree_progress, preferred_mode, response_depth_preference
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            v2_1_profile["user_id"],
            v2_1_profile["overall_level"],
            v2_1_profile["skill_study_design"],
            v2_1_profile["skill_statistics"],
            v2_1_profile["skill_writing"],
            v2_1_profile["skill_critical_appraisal"],
            v2_1_profile["current_learning_focus"],
            v2_1_profile["skill_tree_progress"],
            v2_1_profile["preferred_mode"],
            v2_1_profile["response_depth_preference"]
        ))

        conn.commit()
        conn.close()

        logger.info(f"✓ Migrated user profile: user_id={user_id}")
        logger.info(f"  • Overall level: {v2_1_profile['overall_level']}")
        logger.info(f"  • Skills: design={v2_1_profile['skill_study_design']:.2f}, "
                   f"stats={v2_1_profile['skill_statistics']:.2f}, "
                   f"writing={v2_1_profile['skill_writing']:.2f}, "
                   f"appraisal={v2_1_profile['skill_critical_appraisal']:.2f}")

        logger.info("✓ Migration completed successfully")
        logger.info("="*60 + "\n")

        return True

    except Exception as e:
        logger.error(f"✗ Migration failed: {e}")
        return False

# ============================================================================
# 创建示例数据（可选）
# ============================================================================

def create_sample_data():
    """创建一些示例数据用于测试"""
    logger.info("Creating sample data for testing...")

    conn = sqlite3.connect(SQLITE_DB_PATH)
    cursor = conn.cursor()

    # 示例用户
    cursor.execute("""
        INSERT OR IGNORE INTO user_profiles (user_id, overall_level, skill_study_design, skill_statistics)
        VALUES ('test_user_001', 'novice', 0.3, 0.2)
    """)

    # 示例会话
    cursor.execute("""
        INSERT OR IGNORE INTO session_history (session_id, user_id, session_type, mode_used)
        VALUES ('session_001', 'test_user_001', 'research_review', 'critic')
    """)

    # 示例错误
    cursor.execute("""
        INSERT INTO error_tracking (
            user_id, session_id, error_type, error_category, error_severity, error_description
        ) VALUES (
            'test_user_001', 'session_001', 'multiple_comparison_no_correction',
            'statistical', 'critical', '用户在多重比较时未进行校正'
        )
    """)

    conn.commit()
    conn.close()

    logger.info("✓ Sample data created")

# ============================================================================
# 主函数
# ============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Initialize ACS-Mentor V2.1 Memory System"
    )
    parser.add_argument(
        '--no-chromadb',
        action='store_true',
        help="Skip ChromaDB initialization (SQLite-only mode)"
    )
    parser.add_argument(
        '--migrate-from-v2',
        action='store_true',
        help="Migrate user data from V2.0"
    )
    parser.add_argument(
        '--sample-data',
        action='store_true',
        help="Create sample data for testing"
    )

    args = parser.parse_args()

    logger.info("\n" + "="*60)
    logger.info("ACS-Mentor V2.1 - Memory System Initialization")
    logger.info("="*60 + "\n")

    # Step 1: 创建目录
    create_directories()

    # Step 2: 初始化SQLite
    initialize_sqlite()

    # Step 3: 初始化ChromaDB（可选）
    chromadb_available = False
    if not args.no_chromadb:
        chromadb_available = initialize_chromadb()
    else:
        logger.info("⚠️  Skipping ChromaDB initialization (--no-chromadb flag)")

    # Step 4: 从V2.0迁移（可选）
    if args.migrate_from_v2:
        migrate_from_v2()

    # Step 5: 创建示例数据（可选）
    if args.sample_data:
        create_sample_data()

    # Step 6: 健康检查
    health_check()

    # 最终总结
    logger.info("\n" + "="*60)
    logger.info("Initialization Summary")
    logger.info("="*60)
    logger.info(f"✓ Memory directory: {MEMORY_DIR}")
    logger.info(f"✓ SQLite database: {SQLITE_DB_PATH}")
    if chromadb_available:
        logger.info(f"✓ ChromaDB vectors: {VECTOR_DB_DIR}")
    else:
        logger.info(f"⚠️  ChromaDB: Not available (SQLite-only mode)")
    logger.info("\n🎉 ACS-Mentor V2.1 memory system is ready!")
    logger.info("="*60 + "\n")

    # 使用说明
    logger.info("Next Steps:")
    logger.info("1. (Optional) Install ChromaDB for better performance:")
    logger.info("   pip install chromadb sentence-transformers")
    logger.info("2. Start using ACS-Mentor V2.1 with memory-enhanced guidance")
    logger.info("3. Check memory_operations_guide.md for usage instructions")
    logger.info("")

if __name__ == "__main__":
    main()
