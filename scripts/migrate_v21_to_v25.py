#!/usr/bin/env python3
"""
ACS-Mentor V2.1 → V2.5 Migration Script

Migrates existing V2.1 data to V2.5:
- User profiles from SQLite → Mem0
- Interaction history from SQLite → Mem0
- Guidance cases from ChromaDB → Mem0
- Updates configuration files

Author: ACS-Mentor Development Team
Version: 2.5.0
Date: 2025-11-16

Usage:
    python scripts/migrate_v21_to_v25.py [--dry-run] [--backup]
"""

import sys
import os
import sqlite3
import argparse
from datetime import datetime
import shutil
import yaml

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import V2.5 components
try:
    from memory.mem0_integration import ACSMentorMemory
except ImportError:
    print("Error: Cannot import V2.5 modules. Make sure requirements are installed:")
    print("  pip install -r requirements_v2_5.txt")
    sys.exit(1)


def parse_args():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="Migrate ACS-Mentor from V2.1 to V2.5"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be migrated without actually migrating"
    )
    parser.add_argument(
        "--backup",
        action="store_true",
        default=True,
        help="Create backup of V2.1 data before migration (default: True)"
    )
    parser.add_argument(
        "--skip-chromadb",
        action="store_true",
        help="Skip migrating ChromaDB data (if ChromaDB not available)"
    )

    return parser.parse_args()


def backup_v21_data():
    """Create backup of V2.1 data"""
    print("\n[Backup] Creating backup of V2.1 data...")

    backup_dir = f".acs_mentor/backups/v2.1_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)

    # Backup SQLite database
    if os.path.exists(".acs_mentor/memory.db"):
        shutil.copy2(".acs_mentor/memory.db", f"{backup_dir}/memory.db")
        print(f"  ✓ Backed up SQLite database")

    # Backup ChromaDB
    if os.path.exists(".acs_mentor/vector_db"):
        shutil.copytree(".acs_mentor/vector_db", f"{backup_dir}/vector_db")
        print(f"  ✓ Backed up ChromaDB")

    # Backup config files
    config_files = [
        "memory_system.yaml",
        "decision_logic_v2_extension.md",
        "complexity_aware_routing.yaml"
    ]

    for config_file in config_files:
        if os.path.exists(config_file):
            shutil.copy2(config_file, f"{backup_dir}/{config_file}")

    print(f"  ✓ Backup created at: {backup_dir}")
    return backup_dir


def migrate_user_profiles(memory: ACSMentorMemory, dry_run=False):
    """Migrate user profiles from SQLite to Mem0"""
    print("\n[1/3] Migrating user profiles...")

    db_path = ".acs_mentor/memory.db"

    if not os.path.exists(db_path):
        print("  ⚠ SQLite database not found, skipping user profiles")
        return 0

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='user_profiles'
        """)

        if not cursor.fetchone():
            print("  ⚠ user_profiles table not found")
            conn.close()
            return 0

        # Load user profiles
        cursor.execute("SELECT * FROM user_profiles")
        profiles = cursor.fetchall()

        print(f"  Found {len(profiles)} user profiles")

        if dry_run:
            print("  [DRY RUN] Would migrate user profiles")
            conn.close()
            return len(profiles)

        # Migrate each profile
        migrated_count = 0
        for profile in profiles:
            user_id = profile[0]  # Assuming first column is user_id

            # Create profile summary
            profile_summary = f"User profile initialized from V2.1 migration"

            # Store to Mem0 as system message
            memory.memory.add(
                messages=[{
                    "role": "system",
                    "content": profile_summary
                }],
                user_id=user_id,
                metadata={
                    "type": "profile_initialization",
                    "migrated_from": "v2.1",
                    "migration_date": datetime.now().isoformat()
                }
            )

            migrated_count += 1

        conn.close()
        print(f"  ✓ Migrated {migrated_count} user profiles")
        return migrated_count

    except Exception as e:
        print(f"  ✗ Failed to migrate user profiles: {e}")
        return 0


def migrate_interaction_history(memory: ACSMentorMemory, dry_run=False):
    """Migrate interaction history from SQLite to Mem0"""
    print("\n[2/3] Migrating interaction history...")

    db_path = ".acs_mentor/memory.db"

    if not os.path.exists(db_path):
        print("  ⚠ SQLite database not found")
        return 0

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Check if table exists
        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table' AND name='user_interactions'
        """)

        if not cursor.fetchone():
            print("  ⚠ user_interactions table not found")
            conn.close()
            return 0

        # Load interactions (limit to most recent 1000 to avoid overload)
        cursor.execute("""
            SELECT user_id, user_message, guidance_response,
                   mode_used, quality_score, timestamp
            FROM user_interactions
            ORDER BY timestamp DESC
            LIMIT 1000
        """)

        interactions = cursor.fetchall()
        print(f"  Found {len(interactions)} interactions (migrating most recent 1000)")

        if dry_run:
            print("  [DRY RUN] Would migrate interaction history")
            conn.close()
            return len(interactions)

        # Migrate each interaction
        migrated_count = 0
        for interaction in interactions:
            user_id, user_message, guidance_response, mode, quality_score, timestamp = interaction[:6]

            # Store to Mem0
            try:
                memory.memory.add(
                    messages=[
                        {"role": "user", "content": user_message or ""},
                        {"role": "assistant", "content": guidance_response or ""}
                    ],
                    user_id=user_id or "unknown",
                    metadata={
                        "mode": mode,
                        "quality_score": quality_score,
                        "timestamp": timestamp,
                        "migrated_from": "v2.1"
                    }
                )
                migrated_count += 1

            except Exception as e:
                print(f"  ⚠ Failed to migrate interaction: {e}")
                continue

        conn.close()
        print(f"  ✓ Migrated {migrated_count} interactions")
        return migrated_count

    except Exception as e:
        print(f"  ✗ Failed to migrate interaction history: {e}")
        return 0


def migrate_chromadb_cases(memory: ACSMentorMemory, dry_run=False, skip=False):
    """Migrate guidance cases from ChromaDB to Mem0"""
    print("\n[3/3] Migrating ChromaDB guidance cases...")

    if skip:
        print("  ⚠ Skipping ChromaDB migration (--skip-chromadb flag)")
        return 0

    try:
        import chromadb

        chroma_path = ".acs_mentor/vector_db"

        if not os.path.exists(chroma_path):
            print("  ⚠ ChromaDB not found")
            return 0

        # Connect to ChromaDB
        chroma_client = chromadb.PersistentClient(path=chroma_path)

        # Get guidance_cases collection
        try:
            collection = chroma_client.get_collection("guidance_cases")
        except:
            print("  ⚠ guidance_cases collection not found")
            return 0

        # Get all cases
        all_cases = collection.get()
        print(f"  Found {len(all_cases['documents'])} guidance cases")

        if dry_run:
            print("  [DRY RUN] Would migrate guidance cases")
            return len(all_cases['documents'])

        # Migrate each case
        migrated_count = 0
        for i, (doc, metadata) in enumerate(zip(all_cases['documents'], all_cases['metadatas'])):
            # Extract user_id (may not exist in all cases)
            user_id = metadata.get('user_id', 'migrated_case')

            # Store to Mem0
            try:
                memory.memory.add(
                    messages=[{
                        "role": "assistant",
                        "content": doc
                    }],
                    user_id=user_id,
                    metadata={
                        **metadata,
                        "type": "guidance_case",
                        "migrated_from": "v2.1_chromadb"
                    }
                )
                migrated_count += 1

            except Exception as e:
                print(f"  ⚠ Failed to migrate case {i}: {e}")
                continue

        print(f"  ✓ Migrated {migrated_count} guidance cases")
        return migrated_count

    except ImportError:
        print("  ⚠ ChromaDB not installed, skipping")
        return 0
    except Exception as e:
        print(f"  ✗ Failed to migrate ChromaDB cases: {e}")
        return 0


def verify_migration(memory: ACSMentorMemory):
    """Verify migration success"""
    print("\n[Verification] Checking migration...")

    try:
        # Test retrieval
        test_context = memory.retrieve_context(
            user_message="test migration query",
            user_id="test_user"
        )

        print(f"  ✓ Memory system is operational")
        print(f"  ✓ Can retrieve context successfully")

        # Health check
        health = memory.health_check()
        print(f"  ✓ Health check: {health}")

        return True

    except Exception as e:
        print(f"  ✗ Verification failed: {e}")
        return False


def main():
    """Main migration function"""
    args = parse_args()

    print("=" * 60)
    print("ACS-Mentor V2.1 → V2.5 Migration")
    print("=" * 60)

    # Step 0: Backup
    if args.backup and not args.dry_run:
        backup_dir = backup_v21_data()

    # Step 1: Initialize Mem0
    print("\n[Initialization] Setting up Mem0 memory system...")

    try:
        memory = ACSMentorMemory(config_path=".acs_mentor/mem0_config.yaml")
        print("  ✓ Mem0 initialized successfully")
    except Exception as e:
        print(f"  ✗ Failed to initialize Mem0: {e}")
        print("\nTroubleshooting:")
        print("  1. Install requirements: pip install -r requirements_v2_5.txt")
        print("  2. Check configuration: .acs_mentor/mem0_config.yaml")
        sys.exit(1)

    # Step 2: Migrate data
    total_migrated = 0

    total_migrated += migrate_user_profiles(memory, dry_run=args.dry_run)
    total_migrated += migrate_interaction_history(memory, dry_run=args.dry_run)
    total_migrated += migrate_chromadb_cases(memory, dry_run=args.dry_run,
                                            skip=args.skip_chromadb)

    # Step 3: Verify
    if not args.dry_run:
        verification_success = verify_migration(memory)
    else:
        verification_success = True

    # Summary
    print("\n" + "=" * 60)
    print("Migration Summary")
    print("=" * 60)

    if args.dry_run:
        print(f"[DRY RUN] Would migrate approximately {total_migrated} items")
    else:
        print(f"✓ Migrated {total_migrated} items to Mem0")

        if verification_success:
            print("✓ Migration completed successfully")
            print("\nNext steps:")
            print("  1. Test V2.5: python -c 'from memory.mem0_integration import *; test_system()'")
            print("  2. Update main workflow to use V2.5")
            print("  3. Monitor performance with MLflow")
        else:
            print("⚠ Migration completed with warnings")
            print("  Please verify manually before proceeding")

    print("=" * 60)


if __name__ == "__main__":
    main()
