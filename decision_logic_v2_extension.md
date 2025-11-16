# Decision Logic V2.0 Extension
# ACS-Mentor V2.0 新增决策逻辑

**基础**: 本文档扩展`decision_logic_guide.md`(V1.2.1)
**版本**: V2.0
**日期**: 2025-11-13

---

## 概述

V2.0在V1.2.1的6因子决策框架基础上，新增2个因子以支持导师模式：

```
V1.2.1 (6 Factors - Critic Mode)        V2.0 (8 Factors - Dual Mode)
├── error_detection                     ├── error_detection
├── goal_threatened                     ├── goal_threatened
├── expertise_match                     ├── expertise_match
├── misrepresented                      ├── misrepresented
├── silence_too_long                    ├── silence_too_long
└── agenda_opportunity                  ├── agenda_opportunity
                                        ├── growth_opportunity ⭐ NEW
                                        └── strategic_insight  ⭐ NEW
```

---

## Factor 7: Growth Opportunity (成长机会)

### 定义

检测用户的学习时刻和能力发展机会。

**与error_detection的区别**:
- `error_detection`: 已经犯的错误（reactive）
- `growth_opportunity`: 可以学习的机会（proactive），即使没犯错

### 检测算法

```python
def detect_growth_opportunity(user_message, user_profile, history):
    """
    检测用户成长机会

    Returns:
        score: 0.0-1.0
        opportunities: list of detected opportunity types
    """
    score = 0.0
    opportunities = []

    # A. 用户表达困惑或不确定
    uncertainty_signals = [
        "不知道", "不确定", "是否可以", "哪个更好", "应该用",
        "confused", "not sure", "which is better", "should I use"
    ]

    if any(sig in user_message.lower() for sig in uncertainty_signals):
        score += 0.8
        opportunities.append("user_expressed_uncertainty")

    # B. 用户处于关键决策点
    decision_points = {
        "study_design": ["设计", "design", "RCT", "观察性", "cohort"],
        "statistical_method": ["统计", "分析", "检验", "模型", "回归"],
        "sample_size": ["样本量", "sample size", "power", "功效"],
        "interpretation": ["解释", "interpret", "意义", "significance"],
    }

    for decision_type, keywords in decision_points.items():
        if any(kw in user_message for kw in keywords):
            score += 0.6
            opportunities.append(f"decision_point_{decision_type}")
            break  # 只计分一次

    # C. 用户展示学习意愿
    learning_signals = [
        "为什么", "怎么做", "能教我", "如何", "原理",
        "why", "how to", "teach me", "explain", "principle"
    ]

    if any(sig in user_message.lower() for sig in learning_signals):
        score += 0.7
        opportunities.append("learning_intent_detected")

    # D. 基于用户历史的gap识别
    if user_profile and hasattr(user_profile, 'skill_gaps'):
        current_topic = extract_topic(user_message)
        if current_topic in user_profile.skill_gaps:
            score += 0.9
            opportunities.append("known_skill_gap")

    # E. Recurring error pattern (from mentorship_goals.yaml)
    if history:
        recent_errors = get_recent_error_patterns(history, window=10)
        for pattern in recent_errors:
            if pattern.count >= 2 and is_relevant_to(pattern, user_message):
                score += 0.95  # 高优先级
                opportunities.append(f"recurring_pattern_{pattern.id}")
                break

    return min(score, 1.0), opportunities


def extract_topic(user_message):
    """
    简化版: 提取消息主题
    实际实现可以更复杂
    """
    # 关键词匹配
    topics = {
        "sample_size": ["样本量", "sample size", "power"],
        "validation": ["验证", "validation", "cross-validation"],
        "causality": ["因果", "causal", "导致", "cause"],
        # ... 更多主题
    }

    for topic, keywords in topics.items():
        if any(kw in user_message.lower() for kw in keywords):
            return topic

    return "general"


def is_relevant_to(pattern, user_message):
    """检查error pattern是否与当前消息相关"""
    pattern_keywords = {
        "multiple_testing_忘记校正": ["检验", "比较", "test", "comparison"],
        "validation_遗漏": ["模型", "预测", "AUC", "performance"],
        "因果语言_observational": ["导致", "cause", "effect", "影响"],
    }

    if pattern.id in pattern_keywords:
        keywords = pattern_keywords[pattern.id]
        return any(kw in user_message.lower() for kw in keywords)

    return False
```

### 示例场景

```python
# 场景1: 用户表达困惑
user_message = "我不确定应该用logistic regression还是log-binomial regression"
score, opps = detect_growth_opportunity(user_message, user_profile, history)
# → score ≈ 0.8 (uncertainty) + 0.6 (decision_point)
# → opps = ["user_expressed_uncertainty", "decision_point_statistical_method"]

# 场景2: 用户主动学习
user_message = "为什么要做validation？能教我validation的原理吗？"
score, opps = detect_growth_opportunity(user_message, user_profile, history)
# → score ≈ 0.7 (learning_intent) + 0.6 (decision_point_validation)

# 场景3: Recurring pattern
user_message = "我建了一个预测模型，AUC是0.85"
# 假设history显示用户已2次遗漏validation
score, opps = detect_growth_opportunity(user_message, user_profile, history)
# → score ≈ 0.95 (recurring_pattern)
# → opps = ["recurring_pattern_validation_遗漏"]
```

---

## Factor 8: Strategic Insight (战略洞察)

### 定义

检测提供高层次视角和战略建议的机会。

**与其他因子的区别**:
- 不是纠错（error_detection）
- 不是教学（growth_opportunity）
- 而是提供**big picture thinking**

### 检测算法

```python
def detect_strategic_insight_opportunity(user_message, user_profile, context):
    """
    检测战略洞察机会

    Returns:
        score: 0.0-1.0
        insights: list of detected insight opportunities
    """
    score = 0.0
    insights = []

    # A. 用户在规划或选择研究方向
    planning_signals = [
        "想做", "计划", "打算", "是否值得", "有没有意义",
        "planning", "considering", "worth", "should I pursue"
    ]

    if any(sig in user_message.lower() for sig in planning_signals):
        score += 0.8
        insights.append("research_planning")

    # B. 用户询问前沿或趋势
    frontier_signals = [
        "最新", "前沿", "趋势", "热点", "创新", "未来",
        "latest", "frontier", "trend", "hot topic", "future direction"
    ]

    if any(sig in user_message.lower() for sig in frontier_signals):
        score += 0.85
        insights.append("frontier_inquiry")

    # C. 用户面临战略选择
    choice_signals = [
        "选哪个", "还是", "或者", "两者", "比较", "vs",
        "which", "or", "versus", "compare", "between"
    ]

    # 需要有实际的选项
    if any(sig in user_message.lower() for sig in choice_signals):
        # 检查是否真的在比较研究方向（vs. 仅比较统计方法）
        if contains_research_direction(user_message):
            score += 0.75
            insights.append("strategic_choice")

    # D. 用户描述研究想法（主动提供创新性评估）
    if contains_research_idea(user_message):
        score += 0.70
        insights.append("idea_assessment_opportunity")

    # E. 用户讨论长期规划
    longterm_signals = [
        "职业", "长期", "5年", "10年", "研究线",
        "career", "long-term", "research line", "program"
    ]

    if any(sig in user_message.lower() for sig in longterm_signals):
        score += 0.80
        insights.append("longterm_planning")

    # F. 用户处于career transition
    if user_profile and user_profile.at_career_transition():
        score += 0.65
        insights.append("career_transition")

    return min(score, 1.0), insights


def contains_research_direction(user_message):
    """检查是否在讨论研究方向"""
    direction_keywords = [
        "研究方向", "课题", "项目", "方向", "领域",
        "research direction", "topic", "project", "field"
    ]
    return any(kw in user_message.lower() for kw in direction_keywords)


def contains_research_idea(user_message):
    """检查是否描述了研究想法"""
    idea_signals = [
        "想法", "idea", "hypothesis", "假设",
        "想研究", "想探索", "plan to study"
    ]

    # 需要有想法 + 具体内容
    has_idea_signal = any(sig in user_message.lower() for sig in idea_signals)
    has_substance = len(user_message) > 50  # 简化判断

    return has_idea_signal and has_substance
```

### 示例场景

```python
# 场景1: 研究方向规划
user_message = "我在考虑做AI在临床决策中的应用，不知道是否值得投入"
score, insights = detect_strategic_insight_opportunity(user_message, user_profile, context)
# → score ≈ 0.8 (planning) + 0.7 (idea_assessment)
# → insights = ["research_planning", "idea_assessment_opportunity"]

# 场景2: 前沿趋势咨询
user_message = "现在因果推断领域有什么前沿方法吗？"
score, insights = detect_strategic_insight_opportunity(user_message, user_profile, context)
# → score ≈ 0.85 (frontier_inquiry)

# 场景3: 战略选择
user_message = "我在考虑两个研究方向：精准医疗 vs. 健康公平，哪个更有前景？"
score, insights = detect_strategic_insight_opportunity(user_message, user_profile, context)
# → score ≈ 0.75 (strategic_choice)
```

---

## V2.0 Urgency计算

### 8因子统一计算

```python
def calculate_urgency_v2(factors, weights, mode='balanced'):
    """
    V2.0: 8因子urgency计算

    Args:
        factors: dict with 8 factor scores
        weights: dict with base weights (from beliefs.yaml)
        mode: 'critic' | 'mentor' | 'balanced'

    Returns:
        urgency_score: float
    """

    # 应用mode-specific权重调整
    adjusted_weights = apply_mode_adjustments(weights, mode)

    # 计算base urgency (6因子 - V1.2.1)
    base_urgency = (
        factors['error_detection'] * adjusted_weights['error_detection'] +
        factors['goal_threatened'] * adjusted_weights['goal_threatened'] +
        factors['expertise_match'] * adjusted_weights['expertise_match'] +
        factors['misrepresented'] * adjusted_weights['misrepresented'] +
        factors['silence_too_long'] * adjusted_weights['silence_too_long'] +
        factors['agenda_opportunity'] * adjusted_weights['agenda_opportunity']
    )

    # 计算mentorship urgency (2新因子 - V2.0)
    mentorship_urgency = (
        factors['growth_opportunity'] * adjusted_weights['growth_opportunity'] +
        factors['strategic_insight'] * adjusted_weights['strategic_insight']
    )

    # 总urgency
    total_urgency = base_urgency + mentorship_urgency

    # 理论最大值 = 0.9+0.8+0.6+0.7+0.4+0.75+0.7+0.65 = 5.5
    # 实际最大值约3.0（很少所有因子都高分）
    return min(total_urgency, 3.5)


def apply_mode_adjustments(base_weights, mode):
    """
    应用mode-specific权重调整

    从beliefs.yaml中的mode_specific_weights读取
    """
    adjusted = base_weights.copy()

    mode_adjustments = {
        'critic': {
            'error_detection': 1.0,
            'goal_threatened': 1.0,
            'agenda_opportunity': 1.0,
            'growth_opportunity': 0.5,
            'strategic_insight': 0.3,
        },
        'mentor': {
            'error_detection': 0.7,
            'goal_threatened': 0.7,
            'growth_opportunity': 1.2,
            'strategic_insight': 1.1,
            'agenda_opportunity': 0.8,
        },
        'balanced': {
            # 不调整，使用base weights
        }
    }

    if mode in mode_adjustments:
        for factor, multiplier in mode_adjustments[mode].items():
            if factor in adjusted:
                adjusted[factor] = base_weights[factor] * multiplier

    return adjusted
```

---

## 模式选择逻辑

### 智能模式选择

```python
def select_response_mode(urgency_breakdown, user_profile):
    """
    根据urgency breakdown智能选择响应模式

    Returns: {
        'mode': 'critic' | 'mentor' | 'hybrid',
        'primary_pattern': 'A' | 'B' | 'C' | 'D' | 'M-A' | 'M-B' | 'M-C',
        'mentorship_layer': None | 'teaching' | 'strategic' | 'celebration'
    }
    """

    # 计算各模式的urgency
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
            # 但也有教学机会 → Hybrid模式
            return {
                'mode': 'hybrid',
                'primary_pattern': determine_critic_pattern(critic_score),
                'mentorship_layer': 'teaching'
            }
        else:
            # 纯批判模式
            return {
                'mode': 'critic',
                'primary_pattern': determine_critic_pattern(critic_score),
                'mentorship_layer': None
            }

    elif mentor_score >= 1.2:
        # 高成长机会或战略洞察 → Mentor Mode主导
        mentorship_type = 'strategic' if urgency_breakdown['strategic_insight'] > 0.7 else 'teaching'

        return {
            'mode': 'mentor',
            'primary_pattern': determine_mentor_pattern(mentor_score),
            'mentorship_layer': mentorship_type
        }

    else:
        # 平衡模式或沉默
        total = critic_score + mentor_score

        if total >= 0.85:
            return {
                'mode': 'hybrid',
                'primary_pattern': 'B',
                'mentorship_layer': 'teaching'
            }
        elif total >= 0.35:
            return {
                'mode': 'mentor',
                'primary_pattern': 'M-C',
                'mentorship_layer': 'teaching'
            }
        else:
            return {
                'mode': 'balanced',
                'primary_pattern': 'D',
                'mentorship_layer': None
            }


def determine_critic_pattern(critic_score):
    """
    Critic模式的Pattern分类 (V1.2.1)

    Pattern A: urgency >= 0.85
    Pattern B: 0.60 <= urgency < 0.85
    Pattern C: 0.35 <= urgency < 0.60
    Pattern D: urgency < 0.35
    """
    if critic_score >= 0.85:
        return 'A'
    elif critic_score >= 0.60:
        return 'B'
    elif critic_score >= 0.35:
        return 'C'
    else:
        return 'D'


def determine_mentor_pattern(mentor_score):
    """
    Mentor模式的Pattern分类 (V2.0新增)

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
        Low │   D           A/B    │
Mentor      │ (观察)    (纠错为主) │
Score       │                     │
            │   M-C        Hybrid  │
       High │ (启发)   (纠错+教学) │
            └─────────────────────┘
```

---

## Hybrid模式设计

### 无缝过渡模板

Hybrid模式的核心是"先纠错，后教学"的无缝过渡：

```markdown
⚠️ **[Critic] 问题识别**
{detected_error}

💡 **[Mentor] 概念解释**
为什么这样是有问题的？
{conceptual_explanation}

✅ **[Mentor] 正确做法**
推荐的方法/表述是：
{correct_approach}

📚 **[Mentor] 延伸学习**
相关知识点：
{learning_resources}
```

### 实际示例

```markdown
⚠️ **[Critic] 方法选择不当**
患病率>10%时，Logistic regression的OR会高估关联强度。

💡 **[Mentor] OR vs RR的区别**
- OR (Odds Ratio): Logistic regression输出，odds的比值
- RR (Risk Ratio): 风险的比值，更直观

当患病率>10%时，OR≠RR，且OR会夸大效应。

例如：真实RR=1.5，OR可能=2.0

✅ **[Mentor] 正确做法**
使用log-binomial regression估计RR：

```r
model <- glm(outcome ~ exposure + covariates,
             family = binomial(link = "log"),
             data = data)
```

如果log-binomial不收敛，备选方案：
- Poisson regression with robust SE
- Modified Poisson approach

📚 **[Mentor] 延伸学习**
- Zou G. Modified Poisson regression. Am J Epidemiol. 2004
- 理解何时OR可以近似RR（罕见疾病假设）
```

---

## 完整决策流程示例

### 场景: 用户咨询研究设计

```python
user_message = """
我想研究社交媒体使用是否导致青少年抑郁。
计划收集1000名青少年的问卷数据，测量社交媒体使用时间和抑郁症状。
用logistic regression分析。
不知道这个设计是否合适？
"""

# ========== Step 1: 8因子分析 ==========

factors = {}

# Factor 1: Error Detection
# - "导致" (causal language) in observational design
# - Missing confounding control discussion
factors['error_detection'] = 0.75

# Factor 2: Goal Threatened
# - goal_causal_language_precision threatened
# - Related topics: ["causal", "导致"]
factors['goal_threatened'] = 0.90 * 0.8 = 0.72

# Factor 3: Expertise Match
# - Study design, statistical analysis
factors['expertise_match'] = 0.6

# Factor 4: Misrepresented
factors['misrepresented'] = 0.0

# Factor 5: Silence Too Long
factors['silence_too_long'] = 0.0  # First turn

# Factor 6: Agenda Opportunity
# - agenda_causal_inference_rigor
factors['agenda_opportunity'] = 0.90 (importance)

# Factor 7: Growth Opportunity ⭐
# - User expressed "不知道...是否合适" (uncertainty)
# - Decision point: study_design
# - Learning intent implied
factors['growth_opportunity'] = 0.8 + 0.6 = 1.0 (capped)

# Factor 8: Strategic Insight ⭐
# - Research planning ("想研究...")
# - Could provide idea assessment
factors['strategic_insight'] = 0.8

# ========== Step 2: 计算Urgency ==========

urgency_breakdown = {
    'error_detection': 0.75,
    'goal_threatened': 0.72,
    'expertise_match': 0.6,
    'misrepresented': 0.0,
    'silence_too_long': 0.0,
    'agenda_opportunity': 0.90,
    'growth_opportunity': 1.0,
    'strategic_insight': 0.8
}

# Base urgency (6因子)
base = 0.75*0.9 + 0.72*0.8 + 0.6*0.6 + 0 + 0 + 0.90*0.75
     = 0.675 + 0.576 + 0.36 + 0 + 0 + 0.675
     = 2.286

# Mentorship urgency (2因子)
mentor = 1.0*0.7 + 0.8*0.65
       = 0.7 + 0.52
       = 1.22

# Total
total_urgency = 2.286 + 1.22 = 3.51

# ========== Step 3: 模式选择 ==========

critic_score = 0.75 + 0.72 + 0.90 = 2.37  # High!
mentor_score = 1.0 + 0.8 = 1.8            # High!

# → Hybrid Mode
selected_mode = {
    'mode': 'hybrid',
    'primary_pattern': 'A',  # critic_score >= 1.5
    'mentorship_layer': 'teaching'  # mentor_score >= 0.6
}

# ========== Step 4: 生成响应 ==========
```

**响应输出**:

```markdown
⚠️ **[Critic] 研究设计问题**

您的设计有两个需要调整的地方：

1. **因果语言问题**: "是否导致"暗示因果关系，但横断面问卷调查无法支持因果推断
2. **混杂控制**: 未提及如何控制混杂因素（如家庭背景、学业压力等）

💡 **[Mentor] 为什么这样有问题？**

**因果推断的三个基本条件**：
1. 时序性：X在Y之前发生
2. 关联性：X和Y有统计关联
3. 排除混杂：没有Z同时影响X和Y

横断面设计的局限：
- ❌ 时序性：同时测量，无法确定谁先谁后
- ✓ 关联性：可以检验
- ⚠️ 混杂：难以完全控制（只能调整测量到的混杂）

✅ **[Mentor] 三种改进方案**

**方案1: 修改语言（最简单）**
- 不说"导致"，改为"关联"
- 目的：探索社交媒体使用与抑郁症状的关联
- 统计：Logistic regression可以用，但结论谨慎

**方案2: 升级为纵向设计（推荐）**
- Baseline测量：社交媒体使用
- Follow-up（6个月后）：抑郁症状
- 这样可以建立时序性
- 统计：Mixed models或GEE

**方案3: 使用因果推断方法**
即使是横断面，也可以：
- 构建DAG（有向无环图）识别混杂
- 使用倾向性评分匹配（PSM）
- 进行敏感性分析

🎯 **[Strategic Advisor] 研究影响力评估**

您的研究topic很relevant（社交媒体与心理健康）。

**创新性评估**：
- 概念：Medium（该主题已有研究）
- 方法：可以提升（用纵向设计或因果方法）
- 人群：看您的样本特征

**影响力建议**：
- 如果是pilot study：横断面可以接受，明确标注exploratory
- 如果目标是top-tier journal：建议纵向设计
- Differentiation: 可以focus on特定机制（如sleep mediation）

📚 **[Mentor] 延伸学习**

推荐资源：
1. 因果推断入门：Hernán & Robins. Causal Inference What If. (免费在线)
2. DAG构建：DAGitty (http://dagitty.net)
3. 类似研究：Twenge et al. (2018) on social media and wellbeing

您想从哪个方案入手？我可以提供更详细的指导。
```

---

## 性能监控

### V2.0新增指标

```yaml
v2_performance_metrics:

  mode_distribution:
    healthy_range:
      critic_only: 0.30-0.40
      mentor_only: 0.20-0.30
      hybrid: 0.25-0.35
      silence: 0.10-0.20

    alerts:
      if_critic_only_gt_50: "可能过度批判，缺少指导"
      if_mentor_only_gt_40: "可能忽视错误检测"

  mentorship_effectiveness:
    - metric: "Growth opportunity capture rate"
      target: ">85%"
      description: "检测到的学习机会中提供指导的比例"

    - metric: "Strategic insight adoption"
      target: ">70%"
      description: "战略建议被用户采纳的比例"

    - metric: "Hybrid mode smoothness"
      target: ">90%"
      description: "用户认为Critic→Mentor过渡自然的比例"
```

---

## 总结

V2.0决策逻辑的核心改进：

1. ✅ **8因子系统**: 新增growth_opportunity和strategic_insight
2. ✅ **双模式支持**: Critic + Mentor + Hybrid
3. ✅ **智能切换**: 基于urgency breakdown自动选择模式
4. ✅ **无缝过渡**: Hybrid模式的"纠错→教学"流程
5. ✅ **可观测性**: 完整的性能监控指标

**向后兼容**: V1.2.1的所有功能完全保留，V2.0是纯增量升级。

---

**Version**: 2.1.0
**Last Updated**: 2025-11-16
**Status**: Production Ready (V2.1 with Memory System)
**Dependencies**:
- decision_logic_guide.md (V1.2.1)
- beliefs.yaml (V2.0)
- writing_guidance.yaml (V2.0)
- strategic_thinking.yaml (V2.0)
- mentorship_goals.yaml (V2.0)
- memory_system.yaml (V2.1) ⭐ NEW
- memory_operations_guide.md (V2.1) ⭐ NEW

---

# V2.1 Extension: Hooks Lifecycle Integration

**新增日期**: 2025-11-16
**核心功能**: Pre/Post Hooks自动化、内存系统集成、持续学习

**灵感来源**: Claude-Flow v2.7.0的生命周期管理机制

---

## 概述：从V2.0到V2.1

```
V2.0 (无状态决策)                V2.1 (有记忆决策)
    ↓                                   ↓
用户消息 → 决策 → 响应          Pre → 决策 → Post
                                 ↓            ↓
                             上下文增强      学习提取
                             ↓            ↓
                         内存系统 ←→ 持久化存储
```

### V2.1核心改进

1. **Pre-Guidance Phase**: 响应前自动加载相关历史
2. **Post-Guidance Phase**: 响应后自动学习和更新
3. **Memory Integration**: 跨会话学习和个性化
4. **Quality Assurance**: 自动质量检查

---

## Pre-Guidance Phase

### 目的

在生成响应**之前**，自动从内存系统加载相关上下文，使决策更加informed。

### 完整流程

```python
def pre_guidance_phase(user_message, user_id, session_id):
    """
    Pre-Guidance阶段：上下文增强
    在calculate_urgency_v2之前调用

    参考: memory_operations_guide.md::pre_guidance_context_enrichment
    """

    enriched_context = {}

    # Step 1: Load User Profile
    # 从SQLite user_profiles表加载能力画像
    enriched_context['user_profile'] = load_user_profile(user_id)

    # 关键字段:
    # - overall_level: novice/intermediate/advanced
    # - skill_study_design, skill_statistics, skill_writing, skill_critical_appraisal
    # - current_learning_focus
    # - preferred_mode, response_depth_preference

    # Step 2: Retrieve Recent Interactions (最近5次对话)
    # 用于理解对话上下文和连续性
    enriched_context['recent_history'] = query_sql("""
        SELECT user_message, guidance_response, mode_used, timestamp
        FROM user_interactions
        WHERE user_id = ?
        ORDER BY timestamp DESC
        LIMIT 5
    """, [user_id])

    # Step 3: Check Recurring Errors
    # 检测过去30天内重复出现的错误模式
    enriched_context['recurring_errors'] = detect_recurring_errors(user_id, lookback_days=30)

    # recurring_errors格式:
    # [
    #   {
    #     'error_type': 'multiple_comparison_no_correction',
    #     'occurrence_count': 3,
    #     'last_occurrence': '2025-11-10',
    #     'recommended_strategies': [...]  # 从guidance_cases检索的最佳纠正策略
    #   }
    # ]

    # Step 4: Semantic Search for Similar Success Cases
    # 从ChromaDB guidance_cases collection检索相似的成功指导案例
    try:
        enriched_context['similar_success_cases'] = chromadb_semantic_search(
            collection="guidance_cases",
            query=user_message,
            filters={
                "user_level": enriched_context['user_profile'].overall_level,
                "effectiveness_score": {"$gte": 0.8}
            },
            top_k=3
        )
    except ChromaDBException:
        # Fallback to SQLite keyword matching
        enriched_context['similar_success_cases'] = sqlite_keyword_search(
            user_message,
            user_level=enriched_context['user_profile'].overall_level
        )

    # similar_success_cases格式:
    # [
    #   {
    #     'problem_type': 'study_design_selection',
    #     'user_message': '...',
    #     'guidance_template': '...',
    #     'effectiveness_score': 0.92,
    #     'similarity_score': 0.87
    #   }
    # ]

    # Step 5: Identify Current Learning Focus
    # 从skill_progress表识别用户当前学习重点
    enriched_context['current_focus'] = query_sql("""
        SELECT skill_domain, skill_name, current_level
        FROM skill_progress
        WHERE user_id = ?
        ORDER BY advancement_date DESC
        LIMIT 1
    """, [user_id])

    # Step 6: Estimate Task Complexity (为Phase 3准备)
    enriched_context['estimated_complexity'] = estimate_task_complexity(
        user_message=user_message,
        user_profile=enriched_context['user_profile']
    )

    log(f"[Pre-Guidance] Context enriched for session {session_id}")
    log(f"  • User level: {enriched_context['user_profile'].overall_level}")
    log(f"  • Recurring errors: {len(enriched_context['recurring_errors'])}")
    log(f"  • Similar cases found: {len(enriched_context['similar_success_cases'])}")

    return enriched_context
```

### 集成到V2.0决策流程

```python
# 修改后的calculate_urgency_v2函数

def calculate_urgency_v2_enhanced(user_message, user_id, session_id):
    """
    V2.1增强版urgency计算
    集成Pre-Guidance上下文增强
    """

    # 🆕 V2.1: Pre-Guidance Phase
    enriched_context = pre_guidance_phase(user_message, user_id, session_id)

    # V2.0: 8-factor检测 (现在可以使用enriched_context)
    factors = {
        'error_detection': detect_error(user_message),

        'goal_threatened': check_goal_threat(user_message),

        'expertise_match': calculate_expertise_match(user_message),

        'misrepresented': detect_misrepresentation(user_message),

        'silence_too_long': calculate_silence_duration(enriched_context['recent_history']),  # 🆕 使用历史

        'agenda_opportunity': detect_agenda_opportunity(user_message),

        # 🆕 V2.1: 使用enriched_context增强检测
        'growth_opportunity': detect_growth_opportunity_enhanced(
            user_message,
            user_profile=enriched_context['user_profile'],
            recurring_errors=enriched_context['recurring_errors'],
            current_focus=enriched_context['current_focus']
        ),

        'strategic_insight': detect_strategic_insight_enhanced(
            user_message,
            user_profile=enriched_context['user_profile'],
            recent_history=enriched_context['recent_history']
        )
    }

    # 🆕 V2.1: 根据重复错误动态调整权重
    weights = get_decision_weights()

    if enriched_context['recurring_errors']:
        # 重复错误检测到，强化error_detection和growth_opportunity
        weights['error_detection'] *= 1.2
        weights['growth_opportunity'] *= 1.3
        log("[Weight Boost] Recurring errors detected, boosting correction weights")

    # 🆕 V2.1: 根据用户历史选择模式
    recommended_mode = select_mode_from_context(enriched_context)
    adjusted_weights = apply_mode_adjustments(weights, recommended_mode)

    # 计算urgency
    urgency = calculate_weighted_sum(factors, adjusted_weights)

    return {
        'urgency': urgency,
        'factors': factors,
        'mode': recommended_mode,
        'enriched_context': enriched_context  # 🆕 传递给response generation
    }
```

### 增强的Factor检测

```python
def detect_growth_opportunity_enhanced(user_message, user_profile, recurring_errors, current_focus):
    """
    V2.1增强版growth_opportunity检测
    利用内存系统的上下文
    """

    score = 0.0
    opportunities = []

    # 原有的V2.0检测逻辑 (uncertainty, decision_points, learning_intent)
    base_score, base_opps = detect_growth_opportunity(user_message, user_profile, None)
    score += base_score
    opportunities.extend(base_opps)

    # 🆕 V2.1: 基于recurring_errors的检测
    if recurring_errors:
        for error in recurring_errors:
            # 检查当前消息是否与重复错误相关
            if is_message_related_to_error(user_message, error['error_type']):
                score += 0.95  # 最高优先级
                opportunities.append(f"recurring_error_{error['error_type']}_count_{error['occurrence_count']}")

                log(f"[Growth Opp] Recurring error detected: {error['error_type']} ({error['occurrence_count']} times)")
                break

    # 🆕 V2.1: 基于current_focus的检测
    if current_focus:
        focus_domain = current_focus['skill_domain']
        # 如果用户消息涉及当前学习重点，视为成长机会
        if is_message_related_to_domain(user_message, focus_domain):
            score += 0.7
            opportunities.append(f"aligned_with_current_focus_{focus_domain}")

            log(f"[Growth Opp] Message aligned with current focus: {focus_domain}")

    return min(score, 1.0), opportunities
```

---

## Post-Guidance Phase

### 目的

在生成响应**之后**，自动评估质量、提取学习点、更新内存系统。

### 完整流程

```python
def post_guidance_phase(user_message, guidance_response, decision_result, user_id, session_id):
    """
    Post-Guidance阶段：学习提取和内存更新
    在返回响应给用户之后调用（异步）

    参考: memory_operations_guide.md::post_guidance_learning_extraction
    """

    learning_results = {}

    # Step 1: Quality Self-Check
    quality_score = evaluate_guidance_quality(
        guidance_response=guidance_response,
        decision_result=decision_result,
        enriched_context=decision_result['enriched_context']
    )

    learning_results['quality_score'] = quality_score

    if quality_score < 0.6:
        log(f"⚠️ [Quality] Low quality guidance detected (score={quality_score:.2f})")
        # 标记为需要改进，未来可触发人工审核

    log(f"✓ [Quality] Self-check completed: {quality_score:.2f}")

    # Step 2: Extract Learning Insights
    insights = extract_learning_insights(
        user_message=user_message,
        guidance_response=guidance_response,
        enriched_context=decision_result['enriched_context']
    )

    learning_results['insights'] = insights

    # insights格式:
    # {
    #   'problem_type': 'study_design_selection',
    #   'skill_demonstrated': ['understanding_RCT', 'identify_confounders'],
    #   'skill_advancement': True,
    #   'new_level': 0.6,
    #   'advancement_evidence': '用户正确识别了混杂因素',
    #   'user_confusion_points': ['unclear about propensity score']
    # }

    # Step 3: Update Skill Progress (if advancement detected)
    if insights['skill_advancement']:
        update_skill_progress(
            user_id=user_id,
            skill_domain=insights['skill_domain'],
            new_level=insights['new_level'],
            evidence=insights['advancement_evidence']
        )

        log(f"🎓 [Skill Up] {insights['skill_domain']} → {insights['new_level']}")

    # Step 4: Update User Profile Statistics
    update_user_profile_stats(
        user_id=user_id,
        total_interactions=1,  # increment
        errors_detected=len(decision_result['factors']['error_detection']),
        guidance_provided=1
    )

    # Step 5: Store Interaction to Memory
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

    # 存入SQLite user_interactions表
    insert_into_table("user_interactions", interaction_record)

    # 🆕 V2.1: 存入ChromaDB (仅存储中高质量交互)
    if quality_score >= 0.7:
        add_to_chromadb_async(
            collection="user_interactions",
            document=user_message + "\n" + guidance_response,
            metadata=interaction_record
        )

    log(f"✓ [Storage] Interaction stored (quality={quality_score:.2f})")

    # Step 6: Store as Guidance Case (仅高质量案例)
    if quality_score >= 0.85:
        guidance_case = {
            "case_id": generate_case_id(),
            "problem_type": insights['problem_type'],
            "user_level": decision_result['enriched_context']['user_profile'].overall_level,
            "guidance_strategy": decision_result['mode'],
            "effectiveness_score": quality_score,
            "user_message": user_message,
            "guidance_template": extract_template(guidance_response),
            "tags": extract_tags(insights)
        }

        add_to_chromadb(
            collection="guidance_cases",
            document=guidance_response,
            metadata=guidance_case
        )

        log(f"✨ [Best Practice] Stored as high-quality guidance case (score={quality_score:.2f})")

    # Step 7: Pattern Learning (为V2.5 Neural Learning准备)
    # 记录 (问题类型, 策略, 效果) 三元组
    store_pattern_triple(
        problem_type=insights['problem_type'],
        strategy=decision_result['mode'],
        effectiveness=quality_score
    )

    learning_results['stored'] = True

    log(f"✓ [Post-Guidance] Learning extraction completed for session {session_id}")

    return learning_results
```

---

## Quality Self-Check

### 自动质量评估标准

```python
def evaluate_guidance_quality(guidance_response, decision_result, enriched_context):
    """
    自动评估生成的guidance质量
    基于多维度检查

    参考: CLAUDE_FLOW_INSIGHTS.md::Phase 2::quality_check
    """

    score = 1.0  # 初始满分
    issues = []

    # Check 1: 是否引用了具体标准/文献? (权重: 0.15)
    has_references = check_for_references(guidance_response)
    # 检测关键词: "CONSORT", "STROBE", "et al.", "2023", "研究显示"
    if not has_references:
        score -= 0.15
        issues.append("missing_references")

    # Check 2: 是否提供了可操作建议? (权重: 0.20)
    has_actionable = check_for_actionable_advice(guidance_response)
    # 检测: "建议", "可以", "应该", "步骤", "方法"
    if not has_actionable:
        score -= 0.20
        issues.append("missing_actionable_advice")

    # Check 3: 是否匹配用户能力水平? (权重: 0.15)
    user_level = enriched_context['user_profile'].overall_level
    complexity_match = check_complexity_match(guidance_response, user_level)

    # novice: 避免过度技术术语
    # intermediate: 平衡解释与专业性
    # advanced: 可以使用高级概念

    if not complexity_match:
        score -= 0.15
        issues.append("complexity_mismatch")

    # Check 4: 是否回答了用户的实际问题? (权重: 0.20)
    relevance_score = calculate_semantic_relevance(
        user_message=decision_result['user_message'],
        guidance_response=guidance_response
    )

    if relevance_score < 0.7:
        score -= 0.20
        issues.append("low_relevance")

    # Check 5: 语言是否professional且constructive? (权重: 0.10)
    tone_analysis = analyze_tone(guidance_response)
    # 检测: 是否过于严厉、是否有建设性、是否有鼓励

    if tone_analysis != "professional_constructive":
        score -= 0.10
        issues.append(f"tone_issue_{tone_analysis}")

    # Check 6: 是否利用了similar_success_cases? (权重: 0.10)
    # 🆕 V2.1: 检查是否有效利用了检索到的成功案例
    similar_cases = enriched_context.get('similar_success_cases', [])
    if similar_cases and not check_case_utilization(guidance_response, similar_cases):
        score -= 0.10
        issues.append("underutilized_similar_cases")

    # Check 7: 是否针对recurring_errors提供深度指导? (权重: 0.10)
    # 🆕 V2.1: 如果检测到重复错误，必须提供深度教学
    recurring_errors = enriched_context.get('recurring_errors', [])
    if recurring_errors and decision_result['factors']['growth_opportunity'] > 0.9:
        # 应该包含: 概念框架、多个例子、练习题
        has_deep_teaching = check_deep_teaching_components(guidance_response)
        if not has_deep_teaching:
            score -= 0.10
            issues.append("shallow_teaching_for_recurring_error")

    final_score = max(score, 0.0)

    if issues:
        log(f"[Quality] Issues detected: {', '.join(issues)}")

    return final_score
```

### Quality Check辅助函数

```python
def check_for_references(text):
    """检查是否包含文献引用或标准"""
    reference_patterns = [
        r'\b(CONSORT|STROBE|PRISMA|TRIPOD|STARD)\b',  # 报告规范
        r'\bet al\.',  # 文献引用
        r'\b(19|20)\d{2}\b',  # 年份
        r'研究(显示|表明|发现)',  # 中文研究引用
        r'(Journal|Lancet|NEJM|BMJ)',  # 期刊名
    ]

    return any(re.search(pattern, text, re.IGNORECASE) for pattern in reference_patterns)


def check_for_actionable_advice(text):
    """检查是否包含可操作的建议"""
    actionable_keywords = [
        '建议', '可以', '应该', '步骤', '方法', '首先', '其次',
        'recommend', 'suggest', 'should', 'can', 'step', 'method'
    ]

    return sum(1 for kw in actionable_keywords if kw in text.lower()) >= 2


def check_complexity_match(text, user_level):
    """检查内容复杂度是否匹配用户水平"""
    # 简化版实现：统计技术术语密度

    advanced_terms = [
        'propensity score', 'instrumental variable', 'causal diagram',
        'marginal structural model', 'g-computation', '倾向性评分', '工具变量'
    ]

    intermediate_terms = [
        'confounding', 'selection bias', 'regression', 'validation',
        '混杂', '偏倚', '回归', '验证'
    ]

    advanced_count = sum(1 for term in advanced_terms if term in text.lower())
    intermediate_count = sum(1 for term in intermediate_terms if term in text.lower())

    if user_level == 'novice':
        # 新手：高级术语应少于2个
        return advanced_count < 2

    elif user_level == 'intermediate':
        # 中级：允许一些高级术语，但不能过多
        return advanced_count < 5

    else:  # advanced
        # 高级：可以自由使用专业术语
        return True


def calculate_semantic_relevance(user_message, guidance_response):
    """
    计算响应与用户问题的语义相关性
    简化版：关键词重叠度
    """
    user_keywords = extract_keywords(user_message)
    response_keywords = extract_keywords(guidance_response)

    overlap = set(user_keywords) & set(response_keywords)
    relevance = len(overlap) / max(len(user_keywords), 1)

    return relevance
```

---

## 完整V2.1决策流程示例

### 端到端流程

```python
def handle_user_message_v2_1(user_message, user_id, session_id):
    """
    ACS-Mentor V2.1完整工作流
    Pre → Decision → Generation → Post
    """

    log(f"\n{'='*60}")
    log(f"Session {session_id} - Processing user message")
    log(f"{'='*60}\n")

    # ========== Phase 1: Pre-Guidance ==========
    log("[Phase 1] Pre-Guidance: Context enrichment...")

    enriched_context = pre_guidance_phase(
        user_message=user_message,
        user_id=user_id,
        session_id=session_id
    )

    log(f"✓ Context loaded:")
    log(f"  • User level: {enriched_context['user_profile'].overall_level}")
    log(f"  • Recent interactions: {len(enriched_context['recent_history'])}")
    log(f"  • Recurring errors: {len(enriched_context['recurring_errors'])}")
    log(f"  • Similar success cases: {len(enriched_context['similar_success_cases'])}")

    # ========== Phase 2: Decision & Urgency Calculation ==========
    log("\n[Phase 2] Decision: Calculating urgency and selecting mode...")

    decision_result = calculate_urgency_v2_enhanced(
        user_message=user_message,
        user_id=user_id,
        session_id=session_id
    )

    log(f"✓ Decision made:")
    log(f"  • Urgency: {decision_result['urgency']:.2f}")
    log(f"  • Mode: {decision_result['mode']}")
    log(f"  • Top factors:")
    sorted_factors = sorted(
        decision_result['factors'].items(),
        key=lambda x: x[1] if isinstance(x[1], (int, float)) else 0,
        reverse=True
    )
    for factor, score in sorted_factors[:3]:
        if isinstance(score, (int, float)) and score > 0:
            log(f"    - {factor}: {score:.2f}")

    # ========== Phase 3: Response Generation ==========
    log("\n[Phase 3] Generation: Creating guidance response...")

    # 使用enriched_context中的similar_success_cases作为模板
    guidance_response = generate_guidance_response(
        user_message=user_message,
        decision_result=decision_result,
        template_cases=enriched_context['similar_success_cases']
    )

    log(f"✓ Response generated (length: {len(guidance_response)} chars)")

    # ========== Phase 4: Post-Guidance ==========
    log("\n[Phase 4] Post-Guidance: Learning extraction and memory update...")

    learning_results = post_guidance_phase(
        user_message=user_message,
        guidance_response=guidance_response,
        decision_result=decision_result,
        user_id=user_id,
        session_id=session_id
    )

    log(f"✓ Learning extracted:")
    log(f"  • Quality score: {learning_results['quality_score']:.2f}")
    log(f"  • Skill advancement: {learning_results['insights'].get('skill_advancement', False)}")
    log(f"  • Stored to memory: {learning_results['stored']}")

    # ========== Phase 5: Skill Advancement Check ==========
    if learning_results['insights'].get('skill_advancement'):
        skill_domain = learning_results['insights']['skill_domain']
        new_level = learning_results['insights']['new_level']

        # 在响应中添加祝贺信息
        celebration_message = f"\n\n🎉 **恭喜！您在「{skill_domain}」方面已晋级到 {new_level} 水平！**"
        guidance_response += celebration_message

        log(f"🎓 Skill advancement celebrated: {skill_domain} → {new_level}")

    log(f"\n{'='*60}")
    log(f"Session {session_id} completed")
    log(f"{'='*60}\n")

    return guidance_response
```

### 运行示例

```
用户消息: "我在做一个RCT研究，但是有20%的missing data，怎么处理？"

============================================================
Session abc123 - Processing user message
============================================================

[Phase 1] Pre-Guidance: Context enrichment...
✓ Context loaded:
  • User level: intermediate
  • Recent interactions: 3
  • Recurring errors: 1 (missing_data_deletion_only)
  • Similar success cases: 2

[Phase 2] Decision: Calculating urgency and selecting mode...
[Weight Boost] Recurring errors detected, boosting correction weights
✓ Decision made:
  • Urgency: 1.45
  • Mode: hybrid
  • Top factors:
    - growth_opportunity: 0.95 (recurring_error_missing_data_deletion_only_count_2)
    - expertise_match: 0.80
    - error_detection: 0.60

[Phase 3] Generation: Creating guidance response...
✓ Response generated (length: 1850 chars)

[Phase 4] Post-Guidance: Learning extraction and memory update...
[Quality] Self-check completed: 0.88
✓ Learning extracted:
  • Quality score: 0.88
  • Skill advancement: True
  • Stored to memory: True
✨ [Best Practice] Stored as high-quality guidance case (score=0.88)
🎓 Skill advancement celebrated: statistical_methods → 0.7

============================================================
Session abc123 completed
============================================================

返回响应:
```

🔍 **[Critic] 错误检测**

检测到缺失数据处理不当。20%的missing data是不能忽略的（通常>5%就需要特别处理）。

⚠️ **重要**: 这是您第2次在missing data处理上遇到问题。让我提供更深入的指导。

---

🎓 **[Mentor] 深度概念框架**

**缺失数据的三种机制** (Little & Rubin, 2002):

1. **MCAR** (Missing Completely At Random): 缺失与任何变量无关
2. **MAR** (Missing At Random): 缺失与观测到的变量相关
3. **MNAR** (Missing Not At Random): 缺失与未观测的变量相关

**为什么重要?** 不同机制需要不同处理方法。

---

📋 **[Mentor] 处理策略**

**方法1: Multiple Imputation (推荐) ✅**
- 适用于: MAR假设
- R包: `mice`
- 步骤:
  1. 生成m个完整数据集（通常m=5-20）
  2. 分别分析每个数据集
  3. 合并结果 (Rubin's rules)

**方法2: Full Information Maximum Likelihood (FIML)**
- 适用于: MAR假设，纵向数据
- R包: `lavaan`

**方法3: Sensitivity Analysis**
- 对于MNAR的保守策略
- 测试不同假设下的结果稳健性

---

**❌ 不推荐的方法**:
- Complete case analysis (listwise deletion) - 损失power且可能有偏
- Mean imputation - 低估标准误

---

🧪 **[Mentor] 实践练习**

尝试回答:
1. 您的missing data更可能是MAR还是MNAR？为什么？
2. 如果缺失主要发生在treatment组，这暗示什么机制？

---

📚 **延伸阅读**:
- Van Buuren (2018). Flexible Imputation of Missing Data (R `mice`包作者)
- 报告规范: CONSORT 2010 Extension for Missing Data

---

🎉 **恭喜！您在「statistical_methods」方面已晋级到 0.7 水平！**

```

---

## V2.1性能监控扩展

### 新增指标

```yaml
v2_1_performance_metrics:

  memory_system_health:
    - metric: "ChromaDB availability"
      target: "> 99%"
      degradation: "Auto-fallback to SQLite"

    - metric: "Retrieval latency (p95)"
      target: "< 100ms"
      alert_threshold: "> 200ms"

    - metric: "Memory growth rate"
      target: "< 10MB/week"
      alert_threshold: "> 50MB/week"

  context_enrichment_effectiveness:
    - metric: "Similar case retrieval success rate"
      target: "> 80%"
      description: "检索到至少1个相关案例的比例"

    - metric: "Recurring error detection rate"
      target: "> 95%"
      description: "成功检测到重复错误的比例"

  guidance_quality:
    - metric: "Average quality score"
      target: "> 0.80"
      alert_threshold: "< 0.70"

    - metric: "High-quality case storage rate"
      target: "15-25%"
      description: "quality >= 0.85的案例占比"

  learning_effectiveness:
    - metric: "Skill advancement rate"
      target: "平均每月至少1次晋级"
      measurement: "从skill_progress表统计"

    - metric: "Recurring error elimination rate"
      target: "> 60%"
      description: "重复错误被成功纠正（不再出现）的比例"
```

---

## 总结：V2.1核心价值

### 从V2.0到V2.1的质变

| 维度 | V2.0 | V2.1 |
|------|------|------|
| **状态** | 无状态 | 有记忆 |
| **个性化** | 无 | 深度个性化 |
| **学习** | 静态知识库 | 持续学习 |
| **质量保证** | 无 | 自动质检 |
| **错误处理** | 单次纠正 | 追踪重复错误 |
| **案例复用** | 无 | 语义搜索成功案例 |
| **技能追踪** | 手动 | 自动晋级检测 |

### V2.1关键能力

1. ✅ **Pre-Guidance Context Enrichment**: 响应前自动加载6类上下文
2. ✅ **Post-Guidance Learning Extraction**: 响应后自动学习和更新
3. ✅ **Recurring Error Detection**: 识别用户重复犯的错误（threshold=2）
4. ✅ **Semantic Case Retrieval**: 从历史成功案例中检索最佳模板
5. ✅ **Automatic Quality Check**: 7维度质量自动评估
6. ✅ **Skill Progression Tracking**: 自动检测和庆祝技能晋级
7. ✅ **Memory System Integration**: ChromaDB + SQLite混合架构

### 与Claude-Flow对标

| 功能 | Claude-Flow | ACS-Mentor V2.1 |
|------|-------------|-----------------|
| Pre-Task Context | ✅ 复杂度评估+任务分配 | ✅ 6-stage上下文增强 |
| Post-Task Learning | ✅ Neural pattern learning | ✅ 7-check质量评估+学习提取 |
| Memory System | ✅ AgentDB+ReasoningBank | ✅ ChromaDB+SQLite |
| Auto-degradation | ✅ Hybrid fallback | ✅ ChromaDB→SQLite→Stateless |

**V2.1达成Claude-Flow的核心工程价值**: 有记忆、可学习、持续优化。

---

**Version**: 2.1.0
**Last Updated**: 2025-11-16
**Status**: Production Ready
**New Capabilities**:
- Pre/Post Hooks自动化
- 混合内存系统 (ChromaDB + SQLite)
- 跨会话学习和个性化
- 自动质量保证
