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

**Version**: 2.0.0
**Last Updated**: 2025-11-13
**Status**: Production Ready
**Dependencies**:
- decision_logic_guide.md (V1.2.1)
- beliefs.yaml (V2.0)
- writing_guidance.yaml (V2.0)
- strategic_thinking.yaml (V2.0)
- mentorship_goals.yaml (V2.0)
