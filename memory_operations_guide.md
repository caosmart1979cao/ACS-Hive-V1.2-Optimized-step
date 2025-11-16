# Memory Operations Guide - ACS-Mentor V2.1
# 内存系统操作指南

**版本**: V2.1
**创建日期**: 2025-11-16
**适用于**: ACS-Mentor系统集成memory_system.yaml

---

## 📋 目录

1. [概述](#概述)
2. [系统初始化](#系统初始化)
3. [核心操作流程](#核心操作流程)
4. [Pre-Guidance内存增强](#pre-guidance内存增强)
5. [Post-Guidance学习提取](#post-guidance学习提取)
6. [错误模式检测](#错误模式检测)
7. [用户能力追踪](#用户能力追踪)
8. [降级与容错](#降级与容错)
9. [实现参考](#实现参考)

---

## 概述

### 内存系统架构

```
┌─────────────────────────────────────────────────────────┐
│  AI Agent (ACS-Mentor Decision Logic)                  │
└────────────┬────────────────────────────────────────────┘
             │
             ↓
┌─────────────────────────────────────────────────────────┐
│  Memory Operations Layer (本指南)                      │
│  ├── Context Enrichment (Pre-Guidance)                 │
│  ├── Retrieval Strategies                              │
│  └── Learning Extraction (Post-Guidance)               │
└────────┬────────────────────────────────┬───────────────┘
         ↓                                ↓
┌──────────────────────┐      ┌──────────────────────┐
│  Primary: ChromaDB   │      │  Fallback: SQLite    │
│  • Semantic Search   │◄────►│  • User Profiles     │
│  • 3 Collections     │ Auto │  • Session History   │
│  • 96x Faster        │ Fail │  • Skill Progress    │
└──────────────────────┘ over └──────────────────────┘
```

### 设计哲学

**从V2.0的"无状态专家"到V2.1的"有记忆导师"**

| V2.0 | V2.1 |
|------|------|
| 每次对话独立 | 跨会话连续学习 |
| 基于规则决策 | 基于历史经验决策 |
| 静态知识库 | 动态成长知识库 |
| 无个性化 | 深度个性化指导 |

---

## 系统初始化

### 首次启动流程

```python
# Pseudo-code: Memory System Initialization

def initialize_memory_system():
    """
    ACS-Mentor启动时的内存系统初始化
    应该在第一次使用系统时调用
    """

    # Step 1: 创建目录结构
    create_directory(".acs_mentor/vector_db")
    create_directory(".acs_mentor/")

    # Step 2: 初始化SQLite数据库
    sqlite_conn = connect_sqlite(".acs_mentor/memory.db")
    execute_sql(sqlite_conn, memory_system.fallback_store.initialization_sql)

    # 创建所有表
    for table_name, table_def in memory_system.fallback_store.tables.items():
        execute_sql(sqlite_conn, table_def.schema)
        for index_sql in table_def.indexes:
            execute_sql(sqlite_conn, index_sql)

    # Step 3: 初始化ChromaDB
    try:
        chroma_client = chromadb.PersistentClient(
            path=".acs_mentor/vector_db"
        )

        # 创建3个collections
        create_collection(
            chroma_client,
            name="user_interactions",
            metadata={"hnsw:space": "cosine"}
        )

        create_collection(
            chroma_client,
            name="guidance_cases",
            metadata={"hnsw:space": "cosine"}
        )

        create_collection(
            chroma_client,
            name="error_patterns",
            metadata={"hnsw:space": "cosine"}
        )

        log("ChromaDB initialized successfully")

    except Exception as e:
        log(f"ChromaDB initialization failed: {e}")
        log("System will use SQLite-only mode")

    # Step 4: 健康检查
    health_status = {
        "chromadb": check_chromadb_health(),
        "sqlite": check_sqlite_health()
    }

    log(f"Memory system initialized: {health_status}")

    return health_status
```

### 从V2.0迁移

```python
def migrate_from_v2_0():
    """
    将V2.0的user_capability_profile迁移到V2.1内存系统
    """

    # Step 1: 读取V2.0配置
    v2_profile = load_yaml("mentorship_goals.yaml").user_capability_profile

    # Step 2: 转换为V2.1格式
    v2_1_profile = {
        "user_id": generate_user_id(),  # 首次使用时生成
        "overall_level": v2_profile.user_level,
        "skill_study_design": v2_profile.skill_scores.study_design,
        "skill_statistics": v2_profile.skill_scores.statistical_methods,
        "skill_writing": v2_profile.skill_scores.scientific_writing,
        "skill_critical_appraisal": v2_profile.skill_scores.critical_appraisal,
        "current_learning_focus": v2_profile.current_focus_areas[0] if v2_profile.current_focus_areas else None,
        "skill_tree_progress": json.dumps(v2_profile.skill_tree)
    }

    # Step 3: 插入到SQLite
    insert_into_table("user_profiles", v2_1_profile)

    # Step 4: 迁移历史错误记录（如果有）
    if v2_profile.error_history:
        for error in v2_profile.error_history:
            error_record = {
                "user_id": v2_1_profile["user_id"],
                "error_type": error.type,
                "error_category": categorize_error(error.type),
                "error_severity": error.severity,
                "error_description": error.description,
                "detected_at": error.timestamp
            }
            insert_into_table("error_tracking", error_record)

            # 同时添加到ChromaDB error_patterns
            add_to_chromadb(
                collection="error_patterns",
                document=error.description,
                metadata=error_record
            )

    log("Migration from V2.0 completed")
```

---

## 核心操作流程

### 完整对话流程中的内存操作

```
用户消息到达
    ↓
┌──────────────────────────────────────┐
│ Pre-Guidance Phase (上下文增强)      │
│ ├── Load user profile                │
│ ├── Retrieve recent interactions     │
│ ├── Check recurring errors          │
│ └── Search similar success cases     │
└───────────┬──────────────────────────┘
            ↓
    [enriched_context]
            ↓
┌──────────────────────────────────────┐
│ Guidance Generation Phase            │
│ (现有V2.0 decision_logic_v2)         │
│ ├── Calculate urgency (8 factors)   │
│ ├── Select mode (Critic/Mentor)     │
│ └── Generate response                │
└───────────┬──────────────────────────┘
            ↓
    [guidance_response]
            ↓
┌──────────────────────────────────────┐
│ Post-Guidance Phase (学习提取)       │
│ ├── Quality self-check               │
│ ├── Extract learning insights        │
│ ├── Update user profile              │
│ └── Store as case (if high quality)  │
└───────────┬──────────────────────────┘
            ↓
    返回给用户
```

### 操作1: 加载用户画像

```python
def load_user_profile(user_id):
    """
    从SQLite加载用户能力画像
    使用缓存以提高性能
    """

    # 检查缓存
    cache_key = f"user_profile:{user_id}"
    cached = get_from_cache(cache_key)
    if cached and not is_expired(cached, ttl=300):  # 5分钟TTL
        return cached

    # 从数据库查询
    profile = query_sql("""
        SELECT *
        FROM user_profiles
        WHERE user_id = ?
    """, [user_id])

    if not profile:
        # 首次使用，创建新profile
        profile = create_default_profile(user_id)
        insert_into_table("user_profiles", profile)

    # 更新缓存
    set_cache(cache_key, profile, ttl=300)

    return profile
```

### 操作2: 语义搜索相似案例

```python
def semantic_search_similar_cases(user_message, user_profile, top_k=5):
    """
    使用ChromaDB进行语义相似度搜索
    失败时降级到SQLite关键词匹配
    """

    try:
        # Primary: ChromaDB语义搜索
        collection = get_chromadb_collection("guidance_cases")

        # 生成query embedding
        query_embedding = generate_embedding(user_message)

        # 构建metadata过滤器
        filters = {
            "$and": [
                {"user_level": {"$eq": user_profile.overall_level}},
                {"effectiveness_score": {"$gte": 0.8}}  # 只检索高质量案例
            ]
        }

        # 执行搜索
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            where=filters
        )

        # 重新排序
        ranked_results = rerank_results(
            results,
            user_profile=user_profile,
            ranking_formula=memory_system.retrieval_strategies.semantic_search.result_ranking.formula
        )

        return ranked_results

    except ChromaDBException as e:
        log(f"ChromaDB search failed, falling back to SQLite: {e}")

        # Fallback: SQLite关键词匹配
        keywords = extract_keywords(user_message)

        similar_cases = query_sql("""
            SELECT session_id, user_message, guidance_response, effectiveness_score
            FROM session_history sh
            JOIN user_interactions ui ON sh.session_id = ui.session_id
            WHERE ui.user_level = ?
              AND ui.effectiveness_score >= 0.8
              AND (
                  ui.user_message LIKE ? OR
                  ui.user_message LIKE ? OR
                  ui.user_message LIKE ?
              )
            ORDER BY ui.effectiveness_score DESC
            LIMIT ?
        """, [
            user_profile.overall_level,
            f"%{keywords[0]}%",
            f"%{keywords[1]}%",
            f"%{keywords[2]}%",
            top_k
        ])

        return similar_cases
```

### 操作3: 检测重复错误

```python
def detect_recurring_errors(user_id, lookback_days=30):
    """
    检测用户在过去N天内的重复错误模式
    触发深度指导
    """

    recurring_errors = query_sql("""
        SELECT
            error_type,
            error_category,
            COUNT(*) as occurrence_count,
            MAX(detected_at) as last_occurrence,
            GROUP_CONCAT(error_description, '; ') as all_descriptions
        FROM error_tracking
        WHERE user_id = ?
          AND detected_at >= date('now', '-{} days')
        GROUP BY error_type
        HAVING occurrence_count >= 2
        ORDER BY occurrence_count DESC
    """.format(lookback_days), [user_id])

    if recurring_errors:
        log(f"Detected {len(recurring_errors)} recurring error patterns")

        # 为每个重复错误检索最佳纠正策略
        for error in recurring_errors:
            # 从guidance_cases搜索针对此类错误的成功教学案例
            teaching_cases = semantic_search_by_error_type(
                error_type=error.error_type,
                min_effectiveness=0.85
            )

            error['recommended_strategies'] = teaching_cases

    return recurring_errors
```

---

## Pre-Guidance内存增强

### 完整实现

```python
def pre_guidance_context_enrichment(user_message, user_id, session_id):
    """
    Pre-Guidance阶段：加载所有相关上下文
    返回enriched_context供decision_logic使用

    对应 memory_system.yaml::retrieval_strategies::context_enrichment
    """

    enriched_context = {}

    # Stage 1: Load user profile
    enriched_context['user_profile'] = load_user_profile(user_id)

    # Stage 2: Retrieve recent interactions
    enriched_context['recent_history'] = query_sql("""
        SELECT session_id, user_message, guidance_response, mode_used, user_satisfaction
        FROM user_interactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 5
    """, [user_id])

    # Stage 3: Identify current learning focus
    enriched_context['current_focus'] = query_sql("""
        SELECT skill_domain, skill_name, current_level
        FROM skill_progress
        WHERE user_id = ?
        ORDER BY advancement_date DESC
        LIMIT 1
    """, [user_id])

    # Stage 4: Check for recurring errors
    enriched_context['recurring_errors'] = detect_recurring_errors(user_id)

    # Stage 5: Semantic search for similar success cases
    enriched_context['similar_success_cases'] = semantic_search_similar_cases(
        user_message=user_message,
        user_profile=enriched_context['user_profile'],
        top_k=3
    )

    # Stage 6: Complexity assessment (为Phase 3准备)
    enriched_context['estimated_complexity'] = estimate_task_complexity(
        user_message=user_message,
        user_profile=enriched_context['user_profile']
    )

    log(f"Context enrichment completed for session {session_id}")

    return enriched_context
```

### 在Decision Logic中使用

```python
# 在 decision_logic_v2_extension.md 的决策流程中集成

def calculate_urgency_v2_enhanced(user_message, user_id, session_id):
    """
    V2.1增强版urgency计算
    集成内存系统的上下文
    """

    # 🆕 V2.1: Pre-Guidance上下文增强
    enriched_context = pre_guidance_context_enrichment(
        user_message, user_id, session_id
    )

    # 原有的8-factor检测
    factors = {
        'error_detection': detect_error(user_message),
        'goal_threatened': check_goal_threat(user_message),
        'expertise_match': calculate_expertise_match(user_message),
        'misrepresented': detect_misrepresentation(user_message),
        'silence_too_long': calculate_silence_duration(),
        'agenda_opportunity': detect_agenda_opportunity(user_message),
        'growth_opportunity': detect_growth_opportunity(user_message, enriched_context),  # 🆕 使用上下文
        'strategic_insight': detect_strategic_moment(user_message, enriched_context)     # 🆕 使用上下文
    }

    # 🆕 V2.1: 根据重复错误调整权重
    weights = get_decision_weights()
    if enriched_context['recurring_errors']:
        # 如果检测到重复错误，强化error_detection和growth_opportunity权重
        weights['error_detection'] *= 1.2
        weights['growth_opportunity'] *= 1.3
        log("Boosted weights due to recurring errors")

    # 🆕 V2.1: 根据用户历史调整模式
    mode = select_mode_based_on_context(enriched_context)
    adjusted_weights = apply_mode_adjustments(weights, mode)

    # 计算urgency
    urgency = calculate_weighted_sum(factors, adjusted_weights)

    return {
        'urgency': urgency,
        'factors': factors,
        'mode': mode,
        'enriched_context': enriched_context  # 传递给response generation使用
    }
```

---

## Post-Guidance学习提取

### 完整实现

```python
def post_guidance_learning_extraction(
    user_message,
    guidance_response,
    decision_result,
    user_id,
    session_id
):
    """
    Post-Guidance阶段：从本次交互中学习
    更新内存系统
    """

    learning_results = {}

    # Step 1: Quality Self-Check
    quality_score = evaluate_guidance_quality(
        guidance_response=guidance_response,
        decision_result=decision_result
    )
    learning_results['quality_score'] = quality_score

    if quality_score < 0.6:
        log(f"⚠️ Low quality guidance detected (score={quality_score})")
        # 未来可以触发人工审核

    # Step 2: Extract Learning Insights
    insights = extract_learning_insights(
        user_message=user_message,
        guidance_response=guidance_response,
        enriched_context=decision_result['enriched_context']
    )
    learning_results['insights'] = insights

    # Step 3: Update User Profile
    if insights['skill_advancement']:
        update_skill_progress(
            user_id=user_id,
            skill_domain=insights['skill_domain'],
            new_level=insights['new_level'],
            evidence=insights['advancement_evidence']
        )

    update_user_profile_stats(
        user_id=user_id,
        interaction_count=1,
        errors_detected=len(decision_result['factors']['error_detection']),
        guidance_provided=1
    )

    # Step 4: Store Interaction
    interaction_record = {
        "session_id": session_id,
        "user_id": user_id,
        "user_message": user_message,
        "guidance_response": guidance_response,
        "mode_used": decision_result['mode'],
        "complexity_score": decision_result['enriched_context']['estimated_complexity'],
        "quality_score": quality_score,
        "timestamp": now()
    }

    # 存入SQLite
    insert_into_table("user_interactions", interaction_record)

    # 存入ChromaDB (异步，不阻塞响应)
    if quality_score >= 0.7:  # 只存储中等质量以上的交互
        add_to_chromadb_async(
            collection="user_interactions",
            document=user_message + " " + guidance_response,
            metadata=interaction_record
        )

    # Step 5: Store as Success Case (if exceptional)
    if quality_score >= 0.85:
        guidance_case = {
            "case_id": generate_case_id(),
            "problem_type": insights['problem_type'],
            "user_level": decision_result['enriched_context']['user_profile'].overall_level,
            "guidance_strategy": decision_result['mode'],
            "effectiveness_score": quality_score,
            "user_message": user_message,
            "guidance_template": extract_template(guidance_response)
        }

        add_to_chromadb(
            collection="guidance_cases",
            document=guidance_response,
            metadata=guidance_case
        )

        log(f"✨ Stored as high-quality guidance case (score={quality_score})")

    # Step 6: Pattern Learning (为V2.5 Neural Learning准备)
    store_pattern_triple(
        problem_type=insights['problem_type'],
        strategy=decision_result['mode'],
        effectiveness=quality_score
    )

    learning_results['stored'] = True

    return learning_results
```

### Quality Self-Check实现

```python
def evaluate_guidance_quality(guidance_response, decision_result):
    """
    自动评估guidance质量
    对应 CLAUDE_FLOW_INSIGHTS.md::Phase 2::quality_check
    """

    score = 1.0
    checks = []

    # Check 1: 是否引用了具体标准/文献?
    has_references = check_for_references(guidance_response)
    if not has_references:
        score -= 0.15
        checks.append("missing_references")

    # Check 2: 是否提供了可操作建议?
    has_actionable_advice = check_for_actionable_items(guidance_response)
    if not has_actionable_advice:
        score -= 0.20
        checks.append("missing_actionable_advice")

    # Check 3: 是否匹配用户能力水平?
    user_level = decision_result['enriched_context']['user_profile'].overall_level
    complexity_match = check_complexity_match(guidance_response, user_level)
    if not complexity_match:
        score -= 0.15
        checks.append("complexity_mismatch")

    # Check 4: 是否回答了用户的实际问题?
    relevance_score = calculate_relevance(
        user_message=decision_result['user_message'],
        guidance_response=guidance_response
    )
    if relevance_score < 0.7:
        score -= 0.20
        checks.append("low_relevance")

    # Check 5: 语言是否professional且constructive?
    tone_check = analyze_tone(guidance_response)
    if tone_check != "professional_constructive":
        score -= 0.10
        checks.append("tone_issue")

    final_score = max(score, 0.0)

    log(f"Quality check: score={final_score}, issues={checks}")

    return final_score
```

---

## 错误模式检测

### 完整工作流

```python
def handle_error_detection_with_memory(user_message, user_id, error_detected):
    """
    结合内存系统的错误处理流程
    检测是否为重复错误，并相应调整指导策略
    """

    if not error_detected:
        return None

    # Step 1: 记录本次错误
    error_record = {
        "user_id": user_id,
        "error_type": error_detected['type'],
        "error_category": error_detected['category'],
        "error_severity": error_detected['severity'],
        "error_description": error_detected['description'],
        "detected_at": now()
    }

    insert_into_table("error_tracking", error_record)

    # Step 2: 检查是否为重复错误
    recurrence_check = query_sql("""
        SELECT COUNT(*) as count
        FROM error_tracking
        WHERE user_id = ?
          AND error_type = ?
          AND detected_at >= date('now', '-30 days')
    """, [user_id, error_detected['type']])

    is_recurring = recurrence_check['count'] >= 2

    if is_recurring:
        log(f"🔁 Recurring error detected: {error_detected['type']} ({recurrence_check['count']} times)")

        # Step 3: 检索针对此重复错误的最佳教学策略
        teaching_strategies = semantic_search_by_error_type(
            error_type=error_detected['type'],
            search_collection="guidance_cases",
            filter_tags=["deep_teaching", "concept_framework"]
        )

        # Step 4: 升级到Deep Mentorship模式
        return {
            "error": error_detected,
            "is_recurring": True,
            "occurrence_count": recurrence_check['count'],
            "recommended_mode": "deep_mentorship",
            "teaching_strategies": teaching_strategies,
            "intervention_level": "high"
        }

    else:
        # 首次错误，标准纠正
        return {
            "error": error_detected,
            "is_recurring": False,
            "occurrence_count": 1,
            "recommended_mode": "standard_critic",
            "intervention_level": "moderate"
        }
```

### 存储到Error Patterns Collection

```python
def store_error_pattern(error_record, correction_strategy, effectiveness):
    """
    将错误及其纠正策略存入error_patterns collection
    用于未来相似错误的快速检索
    """

    pattern_document = f"""
    Error Type: {error_record['error_type']}
    Category: {error_record['error_category']}
    Description: {error_record['error_description']}

    Correction Strategy:
    {correction_strategy}

    Effectiveness: {effectiveness}
    """

    metadata = {
        "error_type": error_record['error_type'],
        "error_category": error_record['error_category'],
        "error_severity": error_record['error_severity'],
        "correction_strategy": correction_strategy,
        "effectiveness_score": effectiveness,
        "created_at": now()
    }

    add_to_chromadb(
        collection="error_patterns",
        document=pattern_document,
        metadata=metadata
    )
```

---

## 用户能力追踪

### 技能进展检测

```python
def check_skill_advancement(user_id, session_id, enriched_context):
    """
    检测用户在本次对话中是否展示了技能提升
    对应 mentorship_goals.yaml::skill_domains::mastery_criteria
    """

    # 获取用户当前技能评分
    current_skills = enriched_context['user_profile']

    # 分析本次对话中用户的表现
    performance_indicators = {
        "study_design": analyze_study_design_understanding(session_id),
        "statistics": analyze_statistical_understanding(session_id),
        "writing": analyze_writing_quality(session_id),
        "critical_appraisal": analyze_critical_thinking(session_id)
    }

    advancements = []

    for domain, performance in performance_indicators.items():
        current_level = getattr(current_skills, f"skill_{domain}")

        # 检查是否达到晋级标准
        if check_mastery_criteria(domain, current_level, performance):
            new_level = get_next_level(current_level)

            # 记录晋级
            advancement = {
                "user_id": user_id,
                "skill_domain": domain,
                "previous_level": level_to_string(current_level),
                "current_level": level_to_string(new_level),
                "mastery_evidence": performance['evidence'],
                "advancement_date": now()
            }

            insert_into_table("skill_progress", advancement)

            # 更新user_profile
            update_sql(f"""
                UPDATE user_profiles
                SET skill_{domain} = ?,
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, [new_level, user_id])

            advancements.append(advancement)

            log(f"🎓 Skill advancement: {domain} {level_to_string(current_level)} → {level_to_string(new_level)}")

    return advancements
```

### 学习轨迹可视化

```python
def get_learning_trajectory(user_id, time_window_days=90):
    """
    获取用户的学习轨迹
    用于向用户展示成长进度
    """

    trajectory = {
        "user_id": user_id,
        "time_window": time_window_days,
        "skill_advancements": [],
        "interaction_stats": {},
        "error_rate_trend": []
    }

    # 1. 技能晋级历史
    trajectory['skill_advancements'] = query_sql("""
        SELECT skill_domain, previous_level, current_level, advancement_date, mastery_evidence
        FROM skill_progress
        WHERE user_id = ?
          AND advancement_date >= date('now', '-{} days')
        ORDER BY advancement_date ASC
    """.format(time_window_days), [user_id])

    # 2. 交互统计
    trajectory['interaction_stats'] = query_sql("""
        SELECT
            COUNT(*) as total_sessions,
            AVG(complexity_score) as avg_complexity,
            AVG(quality_score) as avg_quality
        FROM session_history
        WHERE user_id = ?
          AND start_time >= date('now', '-{} days')
    """.format(time_window_days), [user_id])[0]

    # 3. 错误率趋势 (按周统计)
    trajectory['error_rate_trend'] = query_sql("""
        SELECT
            strftime('%Y-W%W', detected_at) as week,
            COUNT(*) as error_count
        FROM error_tracking
        WHERE user_id = ?
          AND detected_at >= date('now', '-{} days')
        GROUP BY week
        ORDER BY week ASC
    """.format(time_window_days), [user_id])

    return trajectory
```

---

## 降级与容错

### 健康检查

```python
def check_memory_system_health():
    """
    定期检查内存系统健康状态
    按 memory_system.yaml::fault_tolerance::health_checks 配置
    """

    health_status = {
        "chromadb": "unknown",
        "sqlite": "unknown",
        "overall": "unknown"
    }

    # Check ChromaDB
    try:
        chroma_client = get_chromadb_client()
        chroma_client.heartbeat()  # Ping
        health_status["chromadb"] = "healthy"
    except Exception as e:
        log(f"ChromaDB health check failed: {e}")
        health_status["chromadb"] = "unhealthy"

    # Check SQLite
    try:
        sqlite_conn = get_sqlite_connection()
        result = execute_sql(sqlite_conn, "SELECT 1;")
        if result:
            health_status["sqlite"] = "healthy"
        else:
            health_status["sqlite"] = "unhealthy"
    except Exception as e:
        log(f"SQLite health check failed: {e}")
        health_status["sqlite"] = "unhealthy"

    # Overall status
    if health_status["chromadb"] == "healthy" and health_status["sqlite"] == "healthy":
        health_status["overall"] = "optimal"
    elif health_status["sqlite"] == "healthy":
        health_status["overall"] = "degraded"  # ChromaDB失败，但SQLite正常
    else:
        health_status["overall"] = "critical"  # SQLite也失败

    return health_status
```

### 自动降级逻辑

```python
def execute_retrieval_with_fallback(query_type, **params):
    """
    带自动降级的检索操作
    优先使用ChromaDB，失败时降级到SQLite
    """

    health = check_memory_system_health()

    if health["chromadb"] == "healthy":
        # Primary: 使用ChromaDB语义搜索
        try:
            return chromadb_retrieval(query_type, **params)
        except Exception as e:
            log(f"ChromaDB retrieval failed, falling back: {e}")
            # 继续到fallback

    if health["sqlite"] == "healthy":
        # Fallback: 使用SQLite精确匹配
        log("Using SQLite fallback mode")
        return sqlite_retrieval(query_type, **params)

    # Both failed
    log("⚠️ Both ChromaDB and SQLite unavailable, using stateless mode")
    return None  # 系统将以V2.0无内存模式运行
```

---

## 实现参考

### Python依赖

```python
# requirements.txt for V2.1 Memory System

chromadb>=0.4.0              # 语义向量数据库
sentence-transformers>=2.2.0  # 本地embedding模型 (all-MiniLM-L6-v2)
sqlite3                       # 内置于Python
numpy>=1.24.0
```

### 完整集成示例

```python
# main_workflow_v2_1.py
# ACS-Mentor V2.1完整工作流示例

def handle_user_message_v2_1(user_message, user_id, session_id):
    """
    V2.1完整工作流：Pre → Decision → Post
    """

    # ========== Pre-Guidance Phase ==========
    enriched_context = pre_guidance_context_enrichment(
        user_message=user_message,
        user_id=user_id,
        session_id=session_id
    )

    log(f"✓ Context enriched: {len(enriched_context['similar_success_cases'])} similar cases found")

    # ========== Decision & Generation Phase ==========
    decision_result = calculate_urgency_v2_enhanced(
        user_message=user_message,
        user_id=user_id,
        session_id=session_id
    )

    # 生成响应 (使用enriched_context和similar_cases作为模板)
    guidance_response = generate_guidance_response(
        user_message=user_message,
        decision_result=decision_result,
        template_cases=enriched_context['similar_success_cases']
    )

    log(f"✓ Guidance generated: mode={decision_result['mode']}, urgency={decision_result['urgency']}")

    # ========== Post-Guidance Phase ==========
    learning_results = post_guidance_learning_extraction(
        user_message=user_message,
        guidance_response=guidance_response,
        decision_result=decision_result,
        user_id=user_id,
        session_id=session_id
    )

    log(f"✓ Learning extracted: quality={learning_results['quality_score']}")

    # 检查技能晋级
    advancements = check_skill_advancement(user_id, session_id, enriched_context)
    if advancements:
        for adv in advancements:
            log(f"🎓 Skill up: {adv['skill_domain']} → {adv['current_level']}")
            # 可以在响应中添加祝贺信息
            guidance_response += f"\n\n🎉 恭喜！您在 {adv['skill_domain']} 方面已晋级到 {adv['current_level']} 水平！"

    return guidance_response
```

---

## 总结

### V2.1内存系统的核心价值

1. **跨会话学习** - 从"健忘专家"到"有记忆导师"
2. **个性化指导** - 基于用户历史调整响应深度和模式
3. **重复错误检测** - 识别学习障碍，触发深度教学
4. **最佳实践复用** - 从历史成功案例中学习模板
5. **能力追踪可视化** - 让用户看到自己的成长轨迹

### 与Claude-Flow的对标

| 功能 | Claude-Flow | ACS-Mentor V2.1 |
|------|-------------|-----------------|
| 语义搜索 | ✅ AgentDB (96x加速) | ✅ ChromaDB (类似性能) |
| 持久化存储 | ✅ SQLite | ✅ SQLite (4表) |
| 自动降级 | ✅ Hybrid fallback | ✅ ChromaDB→SQLite→Stateless |
| Pattern learning | ✅ Neural training | 🔄 V2.5计划 |
| 跨会话恢复 | ✅ Hive-Mind | ✅ User profile + Session history |

### 下一步（Phase 2）

继续实施Pre/Post Hooks的decision_logic集成，将本指南中的操作嵌入到V2.0的决策流程中。

---

**文档版本**: 1.0
**最后更新**: 2025-11-16
**作者**: ACS-Mentor V2.1 Development Team
