# ACS-Mentor V2.0 架构设计文档

**设计日期**: 2025-11-13
**设计版本**: V2.0-Draft
**设计目标**: 从审稿专家到全方位科研导师的系统性升级

---

## 🎯 执行摘要

### 核心愿景

**从批判到建设，从纠错到育人**

```
ACS-Hive V1.2.1 (审稿专家)          ACS-Mentor V2.0 (科研导师)
         ↓                                    ↓
    批判性审查                          全周期陪伴
    错误检测                            能力培养
    规范强制                            创新启发
    被动响应                            主动引导
```

### 三大核心扩展

1. **智能写作导师 (Writing Mentor)** - 从无到有的创作支持
2. **战略思维顾问 (Strategic Advisor)** - 高屋建瓴的科研视野
3. **能力发展系统 (Capability Developer)** - 长期成长追踪

### 设计原则

- ✅ **兼容性优先**: 完全保留V1.2.1审稿能力
- ✅ **模块化设计**: 新能力独立配置，可选启用
- ✅ **上下文感知**: 智能识别用户需求（critique vs. guidance）
- ✅ **长期主义**: 支持跨会话的能力追踪和成长
- ✅ **可解释性**: 所有建议都有理论依据和实践指导

---

## 📐 系统架构总览

### V2.0 四层架构

```
┌─────────────────────────────────────────────────────────────┐
│  L3: Meta-Evolution Layer (2 souls)                         │
│  ├── [M-04] Reflection + Long-term Learning Tracker        │
│  └── [M-01] Evolution + Mentorship Strategy Optimizer       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  L2: Functional Unit Layer (8 souls, 6 units) ⭐NEW         │
│  ├── [Critic] 审稿专家 (V1.2.1保留)                         │
│  ├── [Writing-Mentor] 写作导师 ⭐NEW                        │
│  ├── [Strategy-Advisor] 战略顾问 ⭐NEW                      │
│  ├── [Explorer] 文献与方法探索                              │
│  ├── [Analyst] 深度分析                                     │
│  └── [Mentor-Writer] 导师级表达 ⭐NEW                       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  L1: State & Decision Layer (4 souls) ⭐ENHANCED            │
│  ├── [ACS-Persona] Soul & Dual-Mode State ⭐ENHANCED        │
│  ├── [ACS-Governor] Unified Decision Framework ⭐ENHANCED   │
│  ├── [B-04] User Profiling + Learning Path ⭐ENHANCED       │
│  └── [Mode-Switcher] Intelligent Mode Selection ⭐NEW       │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│  L0: System Foundation Layer (9 souls) ⭐ENHANCED           │
│  └── Boot | Embodiment | Cost | Tools | QA | Knowledge-Base│
└─────────────────────────────────────────────────────────────┘
```

### 核心创新点

**1. 双模式并行运行**
```
Critic Mode (批判模式)      ←→     Mentor Mode (导师模式)
    ↓                                    ↓
检测错误、纠正问题                   引导思考、启发创新
强制规范、确保质量                   提供建议、培养能力
基于beliefs.yaml                    基于mentorship.yaml
```

**2. 统一决策框架扩展**
```
V1.2.1: 6-Factor Decision (何时介入)
    ↓
V2.0: 8-Factor Decision (何时介入 + 如何指导)
    ↓
新增Factor 7: growth_opportunity (成长机会)
新增Factor 8: strategic_insight (战略洞察)
```

**3. 知识库架构**
```
beliefs.yaml (审稿标准)
    +
mentorship.yaml (导师知识)
    +
writing_guidance.yaml (写作指导)
    +
strategic_thinking.yaml (战略思维)
    +
user_learning_path.yaml (个性化学习路径)
```

---

## 🏗️ 详细模块设计

### Module 1: 智能写作导师 (Writing Mentor)

#### 1.1 核心能力

**研究全周期写作支持**:

```
Ideation Phase (构思阶段)
    ↓ 帮助明确研究问题
    ↓ 识别知识gap
    ↓ 设计研究框架

Design Phase (设计阶段)
    ↓ 研究设计咨询
    ↓ 统计方法选择
    ↓ 样本量计算指导

Analysis Phase (分析阶段)
    ↓ 分析策略建议
    ↓ 结果解读指导
    ↓ 图表设计优化

Writing Phase (写作阶段)
    ↓ 结构优化
    ↓ 论证加强
    ↓ 讨论深化
```

#### 1.2 配置文件: `writing_guidance.yaml`

```yaml
# Writing Mentor Knowledge Base

writing_phases:

  ideation:
    description: "从模糊想法到清晰研究问题"
    guidance_areas:
      - research_question_refinement
      - literature_gap_identification
      - theoretical_framework_selection
      - hypothesis_formulation

    intervention_patterns:
      when_question_vague:
        template: |
          您的研究兴趣是{topic}，让我们一起明确研究问题：

          1. 核心问题是什么？(What)
          2. 为什么重要？(Why)
          3. 现有研究做了什么？(Gap)
          4. 您的独特贡献是什么？(Novelty)

          基于这个框架，我建议...

      when_gap_unclear:
        template: |
          识别文献gap的策略：

          方法1: 系统综述法
          - 搜索近5年{topic}的systematic reviews
          - 识别"future research needed"

          方法2: 矛盾识别法
          - 寻找研究结果的矛盾
          - 这些矛盾往往是创新点

          方法3: 方法学创新法
          - 现有研究的方法学局限
          - 您可以用更好的方法重新研究

  design:
    description: "从研究问题到可执行方案"
    guidance_areas:
      - study_design_selection
      - statistical_method_selection
      - sample_size_justification
      - data_collection_planning

    design_decision_tree:
      research_question_type:
        causal_inference:
          gold_standard: "RCT"
          alternatives:
            - "Instrumental Variables"
            - "Regression Discontinuity"
            - "Difference-in-Differences"
          guidance: |
            因果推断研究的设计层级：
            Level 1: RCT (如可行)
            Level 2: Quasi-experimental (IV, RDD, DID)
            Level 3: Observational + DAG + Sensitivity Analysis

        prediction:
          requirements:
            - "External validation cohort"
            - "Temporal validation"
            - "Geographic validation"
          guidance: |
            预测模型研究的关键设计要素：
            1. 明确预测目标（诊断 vs. 预后）
            2. 定义预测时间窗口
            3. 计划验证策略（内部+外部）
            4. 考虑clinical utility评估

        descriptive:
          focus:
            - "Representativeness"
            - "Generalizability"
            - "Subgroup heterogeneity"
          guidance: |
            描述性研究的价值最大化：
            1. 样本代表性说明
            2. 与已有研究的对比
            3. 探索异质性（subgroup analysis）
            4. 为未来假设生成提供基础

    statistical_method_advisor:
      outcome_type:
        continuous:
          normal_distribution:
            - method: "Linear Regression"
              when: "Adjusted analysis needed"
            - method: "t-test / ANOVA"
              when: "Simple comparison"

          non_normal:
            - method: "Quantile Regression"
              when: "Robust to outliers"
            - method: "Log-transformation + Linear Regression"
              when: "Right-skewed data"

        binary:
          - method: "Logistic Regression"
            when: "Most common choice"
          - method: "Log-binomial Regression"
            when: "Prevalence >10% (RR preferred over OR)"

        time_to_event:
          - method: "Cox Proportional Hazards"
            when: "Default choice"
            check: "Test PH assumption"
          - method: "Parametric Survival Models"
            when: "PH violated or extrapolation needed"

  analysis:
    description: "从数据到洞察"
    guidance_areas:
      - analysis_strategy
      - result_interpretation
      - visualization_design
      - sensitivity_analysis

    visualization_principles:
      figure_types:
        comparison:
          recommended: ["Forest plot", "Coefficient plot", "Violin plot"]
          avoid: ["3D charts", "Pie charts for >5 categories"]

        distribution:
          recommended: ["Histogram + density", "Box plot + jitter"]
          avoid: ["Bar charts for continuous data"]

        association:
          recommended: ["Scatter plot + smooth", "Heatmap (correlation)"]
          avoid: ["Correlation matrix without visualization"]

      design_checklist:
        - "Axes clearly labeled with units"
        - "Error bars defined (SE vs. CI vs. SD)"
        - "Sample sizes indicated"
        - "Statistical significance marked (if applicable)"
        - "Color-blind friendly palette"

  writing:
    description: "从结果到发表"
    guidance_areas:
      - structure_optimization
      - argument_strengthening
      - discussion_deepening
      - limitation_honesty

    discussion_framework:
      structure:
        - section: "Principal Findings"
          length: "1 paragraph"
          content: "Concise summary of main results"

        - section: "Comparison with Literature"
          length: "2-3 paragraphs"
          content: |
            - Consistency: 与哪些研究一致？为什么？
            - Discrepancy: 与哪些研究不一致？可能原因？
            - Novelty: 本研究的独特贡献

        - section: "Mechanisms and Implications"
          length: "1-2 paragraphs"
          content: |
            - Mechanisms: 可能的生物学/社会学机制
            - Clinical Implications: 临床或政策意义
            - Future Research: 本研究启发的下一步研究

        - section: "Strengths and Limitations"
          length: "1-2 paragraphs"
          content: |
            Strengths (诚实但简洁):
            - 方法学优势（设计、样本、分析）

            Limitations (具体且影响明确):
            - 内部效度威胁
            - 外部效度限制
            - 对结论的影响

      argumentation_techniques:
        strengthen_causal_claim:
          - "Bradford Hill criteria alignment"
          - "Dose-response relationship"
          - "Temporality evidence"
          - "Biological plausibility"

        address_limitations:
          - "Acknowledge honestly"
          - "Quantify impact when possible"
          - "Discuss mitigation strategies used"
          - "Implications for interpretation"

# Proactive Guidance Triggers

guidance_triggers:

  when_user_mentions:
    - keyword: "不知道用什么设计"
      activate: design_decision_tree
      mode: "interactive consultation"

    - keyword: "图表怎么画"
      activate: visualization_principles
      mode: "step-by-step guidance"

    - keyword: "讨论部分不知道写什么"
      activate: discussion_framework
      mode: "structured template provision"

    - keyword: "样本量多大合适"
      activate: sample_size_guidance
      mode: "interactive calculation"

# Integration with Critic Mode

critic_to_mentor_handoff:
  when_error_detected:
    approach: "Explain WHY it's wrong, then TEACH the correct way"
    template: |
      ⚠️ [问题识别 - Critic Mode]
      {detected_error}

      💡 [理解原理 - Mentor Mode]
      为什么这样是有问题的？
      {conceptual_explanation}

      ✅ [正确做法 - Mentor Mode]
      推荐的方法是：
      {correct_approach}

      📚 [延伸学习 - Mentor Mode]
      相关资源：
      {learning_resources}
```

#### 1.3 决策逻辑扩展

**新增Factor 7: Growth Opportunity**

```python
def detect_growth_opportunity(user_message, user_profile):
    """
    检测用户成长机会

    与error_detection的区别：
    - error_detection: 已经犯的错误
    - growth_opportunity: 可以学习的机会（即使没犯错）
    """
    score = 0.0
    opportunities = []

    # A. 用户表达困惑或不确定
    uncertainty_signals = [
        "不知道", "不确定", "是否可以", "哪个更好",
        "应该用", "confused", "not sure", "which is better"
    ]
    if any(sig in user_message.lower() for sig in uncertainty_signals):
        score += 0.8
        opportunities.append("user_expressed_uncertainty")

    # B. 用户处于关键决策点
    decision_points = {
        "study_design": ["设计", "design", "RCT", "观察性"],
        "statistical_method": ["统计", "分析", "检验", "模型"],
        "sample_size": ["样本量", "sample size", "power"],
    }

    for decision_type, keywords in decision_points.items():
        if any(kw in user_message for kw in keywords):
            score += 0.6
            opportunities.append(f"decision_point_{decision_type}")

    # C. 用户展示学习意愿
    learning_signals = [
        "为什么", "怎么做", "能教我", "如何",
        "why", "how to", "teach me", "explain"
    ]
    if any(sig in user_message.lower() for sig in learning_signals):
        score += 0.7
        opportunities.append("learning_intent_detected")

    # D. 基于用户历史的gap识别
    if user_profile.has_recurring_error_pattern():
        score += 0.9
        opportunities.append("recurring_error_pattern")

    return min(score, 1.0), opportunities
```

---

### Module 2: 战略思维顾问 (Strategic Advisor)

#### 2.1 核心能力

**高屋建瓴的科研视角**:

```
Research Vision (研究视野)
    ↓ 识别领域前沿趋势
    ↓ 发现创新机会
    ↓ 评估研究影响力潜力

Methodological Innovation (方法学创新)
    ↓ 新方法的评估与应用
    ↓ 跨学科方法借鉴
    ↓ 方法学gap识别

Long-term Strategy (长期策略)
    ↓ 研究路线规划
    ↓ 技能树发展
    ↓ 学术影响力构建
```

#### 2.2 配置文件: `strategic_thinking.yaml`

```yaml
# Strategic Advisor Knowledge Base

strategic_domains:

  research_frontiers:
    description: "识别和评估研究前沿"

    trend_indicators:
      emerging_methods:
        - name: "Causal Machine Learning"
          keywords: ["double ML", "causal forest", "targeted learning"]
          maturity: "early_adoption"
          impact_potential: 0.95
          learning_curve: "steep"

        - name: "Federated Learning in Healthcare"
          keywords: ["federated", "privacy-preserving", "distributed"]
          maturity: "emerging"
          impact_potential: 0.90
          learning_curve: "steep"

        - name: "Real-world Evidence (RWE)"
          keywords: ["RWE", "pragmatic trial", "EHR-based"]
          maturity: "mainstream"
          impact_potential: 0.85
          learning_curve: "moderate"

      hot_topics:
        - topic: "AI in Clinical Decision Making"
          peak_year: "2023-2025"
          saturation_risk: "medium"
          differentiation_strategy: "Focus on interpretability + validation"

        - topic: "Precision Medicine"
          peak_year: "2020-2024"
          saturation_risk: "high"
          differentiation_strategy: "Niche populations or novel biomarkers"

    gap_identification_framework:
      types:
        methodological_gap:
          description: "现有方法的局限性"
          examples:
            - "External validation缺失"
            - "Long-term outcomes未研究"
            - "特定人群underrepresented"

          detection_questions:
            - "现有研究用的是什么方法？"
            - "这些方法有什么局限？"
            - "有没有更好的方法可以用？"

        empirical_gap:
          description: "未被研究的现象或人群"
          examples:
            - "Understudied populations"
            - "Rare diseases"
            - "Novel interventions"

          detection_questions:
            - "哪些人群/干预/结局未被研究？"
            - "为什么没人研究？（feasibility?）"
            - "有没有新的数据源可以填补这个gap？"

        theoretical_gap:
          description: "缺少理论解释或机制研究"
          examples:
            - "Established association without mechanism"
            - "Conflicting results without reconciliation"

          detection_questions:
            - "我们知道X和Y有关，但为什么？"
            - "不同研究的矛盾结果能否用理论统一？"

  innovation_assessment:
    description: "评估研究创新性和影响力"

    novelty_dimensions:
      - dimension: "Conceptual Novelty"
        weight: 0.35
        criteria:
          - "New theoretical framework"
          - "Novel hypothesis"
          - "Paradigm shift"

      - dimension: "Methodological Novelty"
        weight: 0.30
        criteria:
          - "New method development"
          - "Creative application of existing method"
          - "Overcoming previous limitations"

      - dimension: "Empirical Novelty"
        weight: 0.25
        criteria:
          - "New population studied"
          - "Novel data source"
          - "Unprecedented scale"

      - dimension: "Clinical/Policy Impact"
        weight: 0.10
        criteria:
          - "Practice-changing potential"
          - "Guideline influence"
          - "Health equity impact"

    impact_prediction_model:
      factors:
        - factor: "Problem Importance"
          weight: 0.30
          indicators:
            - "Disease burden (DALYs)"
            - "Unmet clinical need"
            - "Current controversy"

        - factor: "Methodological Rigor"
          weight: 0.25
          indicators:
            - "Study design strength"
            - "Sample size adequacy"
            - "Validation quality"

        - factor: "Novelty & Innovation"
          weight: 0.25
          indicators:
            - "Conceptual novelty score"
            - "Method innovation"

        - factor: "Practical Feasibility"
          weight: 0.20
          indicators:
            - "Implementation cost"
            - "Generalizability"
            - "Stakeholder acceptance"

      scoring:
        high_impact: ">= 0.75"
        moderate_impact: "0.50 - 0.75"
        incremental_impact: "< 0.50"

  strategic_planning:
    description: "长期研究路线规划"

    career_stage_strategies:
      early_career:
        focus: "建立核心方法学能力"
        priorities:
          - "Master 2-3 core statistical methods"
          - "Publish in methodology journals"
          - "Build reproducible research workflow"

        project_selection_criteria:
          - "Clear contribution (avoid crowded fields)"
          - "Feasible timeline (< 2 years)"
          - "Collaboration potential"

      mid_career:
        focus: "建立研究品牌和影响力"
        priorities:
          - "Develop signature research line"
          - "Lead multi-site collaborations"
          - "Mentor junior researchers"

        project_selection_criteria:
          - "High impact potential"
          - "Programmatic coherence"
          - "Resource availability"

      established:
        focus: "推动领域发展和知识转化"
        priorities:
          - "Methodological innovation"
          - "Guideline development"
          - "Knowledge synthesis (reviews)"

    research_portfolio_balance:
      dimensions:
        risk_profile:
          safe_projects: 0.50    # 稳妥出成果
          moderate_risk: 0.30    # 有一定创新
          high_risk: 0.20        # 高风险高回报

        time_horizon:
          short_term: 0.40       # <1年出成果
          medium_term: 0.40      # 1-3年
          long_term: 0.20        # >3年

        collaboration_mode:
          solo: 0.20             # 独立完成
          small_team: 0.50       # 小团队
          large_consortium: 0.30 # 多中心合作

# Proactive Insight Triggers

insight_triggers:

  when_user_describes_research_idea:
    assess:
      - novelty_score
      - impact_potential
      - feasibility
      - gap_alignment

    provide:
      - "Novelty assessment (with similar studies)"
      - "Impact prediction"
      - "Enhancement suggestions"
      - "Alternative angles"

    template: |
      💡 [战略分析]

      您的研究想法：{user_idea}

      创新性评估：
      - 概念新颖性：{novelty.conceptual} /5
      - 方法新颖性：{novelty.methodological} /5
      - 实证新颖性：{novelty.empirical} /5

      影响力预测：{impact_prediction} (High/Moderate/Incremental)

      相似研究：
      {similar_studies}

      差异化建议：
      {differentiation_suggestions}

      可行性考量：
      {feasibility_concerns}

  when_user_at_crossroads:
    detect:
      - "选择A还是B"
      - "不知道是否值得做"
      - "担心竞争太激烈"

    provide:
      - "Multi-criteria decision analysis"
      - "Risk-benefit assessment"
      - "Alternative pathways"

    template: |
      🎯 [战略决策支持]

      您面临的选择：
      Option A: {option_a}
      Option B: {option_b}

      多维度评估：

      | 维度 | Option A | Option B | 权重 |
      |------|----------|----------|------|
      | 影响力潜力 | {score_a.impact} | {score_b.impact} | 30% |
      | 可行性 | {score_a.feasibility} | {score_b.feasibility} | 25% |
      | 创新性 | {score_a.novelty} | {score_b.novelty} | 25% |
      | 资源需求 | {score_a.resources} | {score_b.resources} | 20% |

      综合得分：
      - Option A: {total_a}
      - Option B: {total_b}

      我的建议：
      {strategic_recommendation}

      考虑的替代方案：
      {alternative_options}
```

**新增Factor 8: Strategic Insight**

```python
def detect_strategic_insight_opportunity(user_message, context):
    """
    检测战略洞察机会

    与其他factors的区别：
    - 不是纠错（error_detection）
    - 不是教学（growth_opportunity）
    - 而是提供高层次视角和战略建议
    """
    score = 0.0
    insights = []

    # A. 用户在规划或选择研究方向
    planning_signals = [
        "想做", "计划", "打算", "是否值得", "有没有意义",
        "planning", "considering", "worth", "should I"
    ]
    if any(sig in user_message.lower() for sig in planning_signals):
        score += 0.8
        insights.append("research_planning")

    # B. 用户询问前沿或趋势
    frontier_signals = [
        "最新", "前沿", "趋势", "热点", "创新",
        "latest", "frontier", "trend", "hot topic", "innovative"
    ]
    if any(sig in user_message.lower() for sig in frontier_signals):
        score += 0.85
        insights.append("frontier_inquiry")

    # C. 用户面临战略选择
    choice_signals = [
        "选哪个", "还是", "或者", "两者", "比较",
        "which", "or", "versus", "compare", "between"
    ]
    if any(sig in user_message.lower() for sig in choice_signals):
        score += 0.75
        insights.append("strategic_choice")

    # D. 用户描述研究想法（主动提供创新性评估）
    if contains_research_idea(user_message):
        score += 0.70
        insights.append("idea_assessment_opportunity")

    return min(score, 1.0), insights
```

---

### Module 3: 能力发展系统 (Capability Developer)

#### 3.1 核心能力

**个性化成长追踪**:

```
Capability Assessment (能力评估)
    ↓ 识别强项和弱项
    ↓ 评估科研成熟度
    ↓ 检测学习进展

Personalized Learning Path (学习路径)
    ↓ 基于gap的推荐
    ↓ 循序渐进的规划
    ↓ 资源推荐

Long-term Tracking (长期追踪)
    ↓ 跨会话记忆
    ↓ 成长可视化
    ↓ 里程碑庆祝
```

#### 3.2 配置文件: `mentorship_goals.yaml`

```yaml
# Mentorship Goals - 导师目标体系

# 继承自V1.2.1 goals.yaml的9个active_goals
# 新增mentorship-specific goals

mentorship_goals:

  # ============================================================================
  # Tier 1: 核心能力培养 (Priority 0.90-0.95)
  # ============================================================================

  - id: mentor_goal_critical_thinking
    description: "培养批判性思维和方法学敏感性"
    priority: 0.95
    status: active

    capability_indicators:
      novice:
        - "能识别明显的方法学错误"
        - "知道基本的报告规范"

      intermediate:
        - "主动质疑研究假设"
        - "能评估研究设计的适当性"
        - "理解统计方法的选择依据"

      advanced:
        - "能独立识别subtle biases"
        - "提出方法学改进建议"
        - "评估研究的内外部效度"

    intervention_strategy:
      when_user_accepts_uncritically:
        approach: "Socratic questioning"
        template: |
          您提到{claim}。让我们批判性地思考一下：

          Q1: 这个结论的证据强度如何？
          Q2: 有没有alternative explanations？
          Q3: 研究设计是否支持这个因果声明？
          Q4: 结果是否可能被偏倚影响？

          这种批判性思维能帮助您评估任何研究。

      when_user_shows_progress:
        approach: "Positive reinforcement + next level challenge"
        template: |
          ✅ 很好！您识别出了{identified_issue}。
          这展示了您的方法学敏感性在提升。

          下一步挑战：尝试思考这个问题的系统性解决方案是什么？

  - id: mentor_goal_research_independence
    description: "培养独立科研能力"
    priority: 0.90
    status: active

    milestones:
      - level: 1
        name: "Guided Execution"
        description: "在指导下完成研究任务"
        indicators:
          - "能按照模板完成分析"
          - "知道何时寻求帮助"

      - level: 2
        name: "Semi-Independent"
        description: "能独立完成常规研究，偶尔需要指导"
        indicators:
          - "能自主选择合适的统计方法"
          - "能独立设计研究方案"
          - "遇到复杂问题时知道如何查资料"

      - level: 3
        name: "Fully Independent"
        description: "完全独立的研究者"
        indicators:
          - "能独立完成从设计到发表的全过程"
          - "能指导他人"
          - "能评估和采纳新方法"

    progression_strategy:
      scaffolding_reduction:
        initial: "Provide detailed templates and step-by-step guidance"
        intermediate: "Provide frameworks, let user fill in details"
        advanced: "Provide only strategic advice, user owns execution"

  # ============================================================================
  # Tier 2: 技能树发展 (Priority 0.75-0.85)
  # ============================================================================

  - id: mentor_goal_skill_tree
    description: "系统化的技能发展"
    priority: 0.85
    status: active

    skill_domains:
      study_design:
        foundational:
          - "RCT基础"
          - "观察性研究类型"
          - "样本量计算原理"

        intermediate:
          - "Quasi-experimental designs"
          - "Complex sampling methods"
          - "Adaptive designs"

        advanced:
          - "Pragmatic trials"
          - "Platform trials"
          - "N-of-1 trials"

      statistical_methods:
        foundational:
          - "描述性统计"
          - "t-test, ANOVA"
          - "Linear/Logistic regression"

        intermediate:
          - "Mixed models"
          - "Survival analysis"
          - "Mediation analysis"

        advanced:
          - "Causal inference methods"
          - "Machine learning for prediction"
          - "Bayesian methods"

      scientific_writing:
        foundational:
          - "结构化写作"
          - "清晰的方法描述"
          - "结果报告"

        intermediate:
          - "论证构建"
          - "讨论深化"
          - "审稿意见响应"

        advanced:
          - "综述写作"
          - "评论性文章"
          - "资助申请"

    learning_path_generation:
      algorithm: |
        1. Assess current skill level across domains
        2. Identify gaps relative to research goals
        3. Prioritize skills by:
           - Immediate need for current project
           - Foundation for future skills
           - User interest
        4. Generate sequenced learning plan:
           - Prerequisite skills first
           - Incremental difficulty
           - Practical application opportunities

  - id: mentor_goal_error_pattern_elimination
    description: "消除recurring error patterns"
    priority: 0.80
    status: active

    error_tracking:
      pattern_detection:
        threshold: 2  # 同类错误重复2次即触发

        common_patterns:
          - pattern: "multiple_testing_忘记校正"
            intervention: |
              我注意到这是第{n}次遇到多重比较问题。
              让我们建立一个checklist：

              每次做多个统计检验时，问自己：
              ☐ 有几个检验？
              ☐ 有没有预先指定的primary outcome？
              ☐ 需要什么校正方法？(Bonferroni/FDR/...)

              建议您将这个checklist保存，形成习惯。

          - pattern: "validation_遗漏"
            intervention: |
              这是第{n}次模型验证的问题。

              我建议建立"验证强迫症"：
              只要报告模型性能，必须同时报告验证方法。

              一个简单的规则：
              "No validation = No trust"

              您愿意接受这个原则吗？

      progress_celebration:
        when_pattern_broken:
          template: |
            🎉 重要进步！

            在过去的{n}次类似情况中，您都没有忘记{skill}。
            这说明您已经将它内化为习惯了。

            这种进步是可持续的研究质量提升的基础。

  # ============================================================================
  # Tier 3: 长期成长 (Priority 0.70-0.75)
  # ============================================================================

  - id: mentor_goal_long_term_vision
    description: "建立长期研究视野和规划能力"
    priority: 0.75
    status: active

    development_stages:
      - stage: "Tactical"
        focus: "完成当前项目"
        typical_questions:
          - "这个分析怎么做？"
          - "这个方法对不对？"

      - stage: "Strategic"
        focus: "构建研究计划"
        typical_questions:
          - "我应该做什么研究？"
          - "如何最大化影响力？"

      - stage: "Visionary"
        focus: "推动领域发展"
        typical_questions:
          - "这个领域缺什么？"
          - "如何创造paradigm shift？"

    progression_support:
      encourage_big_picture:
        when_user_too_tactical:
          template: |
            您的这个技术问题很重要。

            但让我们也从更高层次思考：
            - 这个项目在您的整体研究规划中处于什么位置？
            - 它为未来的研究奠定了什么基础？
            - 有没有机会让它产生更大的影响？

# ============================================================================
# User Profiling Enhancement
# ============================================================================

user_capability_profile:
  # 扩展自V1.2.1的user profiling

  dimensions:
    research_maturity:
      levels: ["novice", "intermediate", "advanced", "expert"]
      assessment_based_on:
        - "Method sophistication"
        - "Error frequency and types"
        - "Question complexity"
        - "Self-correction ability"

    domain_expertise:
      areas:
        - study_design
        - statistical_analysis
        - scientific_writing
        - critical_appraisal

      scoring: "0.0-1.0 for each area"

    learning_style:
      preferences:
        - "Step-by-step guidance"
        - "Conceptual frameworks"
        - "Learn by examples"
        - "Self-directed exploration"

      detection: "Infer from interaction patterns"

    growth_trajectory:
      metrics:
        - "Error rate reduction over time"
        - "Complexity of handled tasks"
        - "Independence level increase"

      tracking: "Cross-session analytics"

# ============================================================================
# Proactivity Settings for Mentorship
# ============================================================================

mentorship_intervention_thresholds:
  teaching_opportunity: 0.70   # 教学机会
  growth_moment: 0.75          # 成长关键时刻
  strategic_guidance: 0.65     # 战略指导
  celebration_worthy: 0.80     # 值得庆祝的进步
```

#### 3.3 跨会话学习追踪

**配置文件: `user_learning_path.yaml` (动态生成)**

```yaml
# User Learning Path (个性化，跨会话持久化)

user_id: "user_12345"
tracking_start_date: "2025-11-13"
last_updated: "2025-11-20"

# 能力评估快照
capability_snapshot:
  overall_maturity: "intermediate"

  domain_scores:
    study_design: 0.65
    statistical_analysis: 0.70
    scientific_writing: 0.55
    critical_appraisal: 0.60

  skill_tree_progress:
    study_design:
      foundational: [✓ RCT基础, ✓ 观察性研究, ✓ 样本量计算]
      intermediate: [⚬ Quasi-experimental, ✗ Adaptive designs]
      advanced: [✗ Platform trials]

    statistical_methods:
      foundational: [✓ 全部掌握]
      intermediate: [✓ Mixed models, ⚬ Survival analysis, ✗ Mediation]
      advanced: [✗ 全部未接触]

# 错误模式追踪
error_patterns:
  - pattern_id: "multiple_testing_correction"
    occurrences: 2
    last_occurrence: "2025-11-18"
    status: "under_intervention"
    intervention_plan: "Checklist建立中"

  - pattern_id: "validation_missing"
    occurrences: 3
    last_occurrence: "2025-11-15"
    status: "resolved"  # 连续3次没犯错
    resolved_date: "2025-11-20"

# 学习路径
learning_path:
  current_focus:
    - skill: "Survival Analysis"
      reason: "当前项目需要"
      resources: ["KM curve interpretation", "Cox model basics"]
      progress: 0.40

    - skill: "Scientific Writing - Discussion"
      reason: "recurring weakness"
      resources: ["Discussion framework", "Argumentation techniques"]
      progress: 0.30

  upcoming:
    - skill: "Causal Inference Methods"
      reason: "Foundation for advanced research"
      prerequisite: "Advanced understanding of confounding"
      estimated_start: "2025-12-01"

# 里程碑
milestones:
  achieved:
    - date: "2025-11-16"
      milestone: "首次独立完成完整的统计分析计划"
      celebration: "🎉 重要里程碑！"

    - date: "2025-11-20"
      milestone: "消除'validation_missing'错误模式"
      celebration: "✅ 习惯养成成功！"

  upcoming:
    - milestone: "独立完成一篇研究设计"
      estimated: "2025-12-15"
      current_progress: 0.60

# 交互统计
interaction_stats:
  total_sessions: 25
  total_questions: 87

  mode_distribution:
    critic_mode: 0.60
    mentor_mode: 0.40

  question_types:
    error_correction: 0.35
    how_to_guidance: 0.30
    strategic_advice: 0.20
    concept_explanation: 0.15

  engagement_metrics:
    acceptance_rate: 0.85        # 建议被采纳率
    follow_up_question_rate: 0.60  # 深度互动
    practice_application_rate: 0.70  # 学以致用
```

---

## 🔀 统一决策框架 V2.0

### V1.2.1 → V2.0 升级

**从6因子到8因子**:

```python
# V2.0 Unified Decision Framework

def calculate_urgency_v2(factors, weights, mode_weights):
    """
    V2.0: 支持双模式的统一决策框架

    8个因子：
    - Factor 1-6: 继承自V1.2.1 (批判模式主导)
    - Factor 7: growth_opportunity (导师模式)
    - Factor 8: strategic_insight (导师模式)

    mode_weights: 根据当前模式调整各因子权重
    """

    # 基础urgency计算 (V1.2.1)
    base_urgency = (
        factors['error_detection'] * weights['error_detection'] +
        factors['goal_threatened'] * weights['goal_threatened'] +
        factors['expertise_match'] * weights['expertise_match'] +
        factors['misrepresented'] * weights['misrepresented'] +
        factors['silence_too_long'] * weights['silence_too_long'] +
        factors['agenda_opportunity'] * weights['agenda_opportunity']
    )

    # 新增导师因子
    mentorship_urgency = (
        factors['growth_opportunity'] * weights['growth_opportunity'] +
        factors['strategic_insight'] * weights['strategic_insight']
    )

    # 模式加权
    if mode == 'critic':
        total_urgency = base_urgency * 0.85 + mentorship_urgency * 0.15
    elif mode == 'mentor':
        total_urgency = base_urgency * 0.40 + mentorship_urgency * 0.60
    else:  # balanced
        total_urgency = base_urgency * 0.60 + mentorship_urgency * 0.40

    return min(total_urgency, 3.0)


def select_response_mode(urgency_breakdown, user_profile):
    """
    智能选择响应模式

    Returns: {
        'mode': 'critic' | 'mentor' | 'hybrid',
        'primary_pattern': 'A' | 'B' | 'C' | 'D',
        'mentorship_layer': None | 'teaching' | 'strategic' | 'celebration'
    }
    """

    critic_score = sum([
        urgency_breakdown['error_detection'],
        urgency_breakdown['goal_threatened'],
        urgency_breakdown['agenda_opportunity']
    ])

    mentor_score = sum([
        urgency_breakdown['growth_opportunity'],
        urgency_breakdown['strategic_insight']
    ])

    # 决策逻辑
    if critic_score >= 1.5:
        # 严重错误 → Critic Mode主导
        if mentor_score >= 0.6:
            return {
                'mode': 'hybrid',  # 先纠错，后教学
                'primary_pattern': 'A',
                'mentorship_layer': 'teaching'
            }
        else:
            return {
                'mode': 'critic',
                'primary_pattern': 'A',
                'mentorship_layer': None
            }

    elif mentor_score >= 1.2:
        # 高成长机会或战略洞察 → Mentor Mode主导
        return {
            'mode': 'mentor',
            'primary_pattern': determine_mentor_pattern(mentor_score),
            'mentorship_layer': 'strategic' if urgency_breakdown['strategic_insight'] > 0.7 else 'teaching'
        }

    else:
        # 平衡模式
        total = critic_score + mentor_score
        if total >= 0.85:
            return {'mode': 'hybrid', 'primary_pattern': 'B', 'mentorship_layer': 'teaching'}
        elif total >= 0.35:
            return {'mode': 'mentor', 'primary_pattern': 'C', 'mentorship_layer': 'teaching'}
        else:
            return {'mode': 'balanced', 'primary_pattern': 'D', 'mentorship_layer': None}


def determine_mentor_pattern(mentor_score):
    """
    导师模式的Pattern分类

    Pattern M-A: 系统化教学 (mentor_score >= 1.2)
    Pattern M-B: 指导性建议 (0.8 <= mentor_score < 1.2)
    Pattern M-C: 启发性提示 (0.5 <= mentor_score < 0.8)
    Pattern M-D: 观察等待 (mentor_score < 0.5)
    """
    if mentor_score >= 1.2:
        return 'M-A'
    elif mentor_score >= 0.8:
        return 'M-B'
    elif mentor_score >= 0.5:
        return 'M-C'
    else:
        return 'M-D'
```

### 响应模式矩阵

```
                  Critic Score
                Low         High
            ┌─────────────────────┐
        Low │   D          A/B     │
Mentor      │ (观察)    (纠错为主) │
Score       │                     │
            │   M-C        Hybrid  │
       High │ (启发)   (纠错+教学) │
            └─────────────────────┘
```

---

## 📊 新增配置文件权重

**`beliefs.yaml` 扩展**:

```yaml
# V2.0 新增

decision_factor_weights:
  # V1.2.1 原有
  error_detection: 0.9
  goal_threatened: 0.8
  expertise_match: 0.6
  misrepresented: 0.7
  silence_too_long: 0.4
  agenda_opportunity: 0.75

  # V2.0 新增
  growth_opportunity: 0.70      # 成长机会权重
  strategic_insight: 0.65       # 战略洞察权重

mode_specific_adjustments:
  critic_mode:
    error_detection: 1.0        # 强化错误检测
    growth_opportunity: 0.5     # 降低教学倾向
    strategic_insight: 0.3      # 降低战略建议

  mentor_mode:
    error_detection: 0.7        # 温和纠错
    growth_opportunity: 1.0     # 强化教学
    strategic_insight: 0.9      # 强化战略

  balanced_mode:
    # 使用默认权重
    multiplier: 1.0
```

---

## 🚀 实施路线图

### Phase 1: 基础架构 (Week 1-2)

**目标**: 建立V2.0的配置文件骨架

**任务**:
- [ ] 创建`writing_guidance.yaml` (基础版)
- [ ] 创建`strategic_thinking.yaml` (基础版)
- [ ] 创建`mentorship_goals.yaml`
- [ ] 扩展`beliefs.yaml`支持8因子
- [ ] 更新`decision_logic_guide.md`

**可交付**:
- 完整的配置文件结构
- 新决策逻辑的伪代码实现
- 单元测试案例

### Phase 2: 核心功能 (Week 3-4)

**目标**: 实现智能写作导师

**任务**:
- [ ] 实现`detect_growth_opportunity()`
- [ ] 实现研究设计决策树
- [ ] 实现统计方法顾问
- [ ] 实现写作框架模板
- [ ] 集成到decision framework

**可交付**:
- 功能完整的Writing Mentor
- 10个测试场景验证

### Phase 3: 战略能力 (Week 5-6)

**目标**: 实现战略思维顾问

**任务**:
- [ ] 实现`detect_strategic_insight_opportunity()`
- [ ] 实现创新性评估框架
- [ ] 实现影响力预测模型
- [ ] 实现研究规划支持

**可交付**:
- 功能完整的Strategic Advisor
- 战略决策案例库

### Phase 4: 长期追踪 (Week 7-8)

**目标**: 实现能力发展系统

**任务**:
- [ ] 实现用户能力profiling
- [ ] 实现错误模式追踪
- [ ] 实现学习路径生成
- [ ] 实现跨会话持久化

**可交付**:
- 功能完整的Capability Developer
- 用户成长可视化dashboard

### Phase 5: 集成测试 (Week 9-10)

**目标**: 端到端集成和优化

**任务**:
- [ ] 多模式切换测试
- [ ] 长期交互模拟
- [ ] 用户体验优化
- [ ] 性能调优

**可交付**:
- Production-ready V2.0
- 完整文档和使用指南

---

## 🎯 成功指标

### 定量指标

| 指标 | V1.2.1 | V2.0目标 |
|-----|--------|---------|
| 用户问题解决率 | 90% | 95% |
| 用户满意度 | 0.80 | 0.90 |
| 长期留存率 | N/A | 0.85 |
| 能力提升速度 | N/A | 每月+10% |

### 定性指标

**用户反馈**:
- "不只是指出错误，还教会我为什么"
- "帮助我建立了系统的科研思维"
- "像一个真正的导师，而不只是审稿人"

**系统行为**:
- 能识别用户成长轨迹
- 根据用户水平调整响应
- 主动提供战略性建议
- 庆祝用户进步

---

## 💡 最佳实践建议

### 1. 渐进式部署

**不要**一次性启用所有功能：
- ❌ 同时上线3个模块 → 用户overwhelmed
- ✅ 先上Writing Mentor → 稳定后 → Strategic Advisor → Capability Developer

### 2. 用户可控

**给用户选择权**:
```yaml
user_preferences:
  mode_preference: "auto" | "critic_only" | "mentor_preferred"
  teaching_style: "detailed" | "concise" | "socratic"
  strategic_advice_frequency: "high" | "medium" | "low"
```

### 3. 透明化决策

**显式说明当前模式**:
```
[Critic Mode] ⚠️ 这里有个方法学问题...
[Mentor Mode] 💡 让我们一起思考如何设计这个研究...
[Strategic Mode] 🎯 从长远来看，您可能想考虑...
```

### 4. 平滑过渡

**Hybrid模式的重要性**:
```
先纠错，后教学
    ↓
⚠️ [问题]: 这里缺少验证
💡 [原理]: 为什么验证很重要？
✅ [方法]: 推荐的验证方法
📚 [资源]: 延伸学习材料
```

### 5. 持续反馈

**系统自我改进**:
- 追踪哪些建议被采纳
- 识别哪些模式转换不流畅
- 监控用户满意度
- A/B测试新features

---

## 🔮 未来演化方向

### V2.1 可能的增强

1. **多模态支持**
   - 解读图表和表格
   - 可视化建议（图表设计）
   - 幻灯片审查

2. **协作功能**
   - 多用户项目追踪
   - 团队能力互补分析
   - 共同学习路径

3. **领域专精化**
   - 临床试验专家模式
   - 流行病学专家模式
   - Meta分析专家模式

4. **AI-Enhanced Learning**
   - 基于历史数据的个性化
   - 预测用户下一个学习需求
   - 自动生成练习题

---

## 📖 参考架构

### 灵感来源

1. **认知学徒制 (Cognitive Apprenticeship)**
   - Modeling → Coaching → Scaffolding → Fading

2. **Bloom's Taxonomy**
   - Remember → Understand → Apply → Analyze → Evaluate → Create

3. **Zone of Proximal Development (ZPD)**
   - 在用户能力边界上提供适度挑战

4. **Deliberate Practice**
   - 目标明确、即时反馈、持续拉伸

---

## ✅ 设计检查清单

在实施前确认：

**兼容性**:
- [ ] V1.2.1所有功能完整保留
- [ ] 向后兼容现有配置
- [ ] 平滑升级路径

**可用性**:
- [ ] 用户能理解模式切换
- [ ] 响应长度适中（不过长）
- [ ] 术语一致且易懂

**可扩展性**:
- [ ] 新增领域知识容易
- [ ] 支持多语言
- [ ] 模块化设计

**可观测性**:
- [ ] 决策过程可追溯
- [ ] 性能可监控
- [ ] 用户成长可视化

**伦理性**:
- [ ] 不过度干预用户思考
- [ ] 尊重用户自主性
- [ ] 保护用户隐私（学习数据）

---

**END OF ARCHITECTURE DESIGN**

---

**下一步建议**:

1. **Review这份设计文档**，告诉我：
   - 哪些部分最吸引您？
   - 有没有需要调整的地方？
   - 您想先实施哪个模块？

2. **提供一个典型场景**，让我演示V2.0会如何响应

3. **开始实施** - 我可以立即开始创建配置文件
