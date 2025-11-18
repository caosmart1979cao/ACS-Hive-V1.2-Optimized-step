# ⚠️ ARCHIVED - FILE MANIFEST - ACS蜂巢V1.2优化版

> **归档警告**：本文档已归档，仅供历史参考。
>
> - **归档日期**：2025-11-17
> - **归档原因**：文件结构已随系统演进发生重大变化，本清单仅反映V1.2时期状态
> - **当前结构**：参见 [ARCHITECTURE_UNIFIED.md](../ARCHITECTURE_UNIFIED.md) 了解当前文件组织
> - **系统演进**：参见 [SYSTEM_EVOLUTION_MAP.md](../SYSTEM_EVOLUTION_MAP.md) 了解完整演进

---

# FILE MANIFEST - ACS蜂巢V1.2优化版

## 📦 完整文件清单

### 🆕 新增文件 (V1.2-Optimized)

```
/ACS-Hive-V1.2-Optimized/
├── CHANGELOG.md                   # ✨ 版本变更日志
└── FILE_MANIFEST.md               # ✨ 本文件
```

### ⚡ 重构文件 (核心配置)

```
/system_configs/
├── beliefs.yaml                   # ⚡ 从个人定制→通用审稿标准
├── goals.yaml                     # ⚡ 从个人目标→9个通用方法论目标
├── agenda.yaml                    # ⚡ 从个人议程→8个学术质量议程
├── decision_logic_guide.md        # ⚡ 补全Factor 4/5/6算法实现
└── long_term_goals.md            # ⚡ 从个人追踪→通用模板
```

### ⚡ 更新文件 (文档)

```
/
├── README.md                      # ⚡ 全面重写，反映通用定位
```

### ✅ 保留文件 (架构/灵魂 - 继承V1.2)

这些文件架构合理，无需修改，从V1.2原版继承：

```
/
├── mindsymphony.config.yml        # ✅ 保留 - 蜂巢核心配置
│
/docs/
├── QUICK_START.md                 # ✅ 保留 - 快速开始指南
└── SYSTEM_ARCHITECTURE.md         # ✅ 保留 - 系统架构文档
│
/souls/
├── L0_系统基石/                   # ✅ 保留 - 8个系统级灵魂
│   ├── 01_M08_配置管家.md
│   ├── 02_B05_性能调优师.md
│   ├── 03_B06_终端代理.md
│   ├── 04_B09_工具生态.md
│   ├── 05_M06_手稿校对官.md
│   ├── 06_E08_效能评估师.md
│   ├── 07_E07_逻辑架构师.md
│   └── 08_B08_智能重构师.md
│
├── L1_状态决策/                   # ✅ 保留 - 3个状态决策灵魂
│   ├── 01_ACS_Persona.md          # 需配合新的beliefs.yaml使用
│   ├── 02_ACS_Governor.md         # 需配合新的decision_logic_guide.md
│   └── 03_B04_用户认知画像师.md
│
├── L2_功能单元/                   # ✅ 保留 - 5个功能单元灵魂
│   ├── 01_ACS_Explorer.md
│   ├── 02_ACS_Analyst.md
│   ├── 03_ACS_Writer.md
│   └── 04_ACS_Mentor.md
│
├── L3_元进化/                     # ✅ 保留 - 2个元进化灵魂
│   ├── 01_M04_乐队现场录音师.md
│   └── 02_M01_元一_灵魂建筑师.md
│
└── SOULS_INDEX.md                 # ✅ 保留 - 灵魂索引
```

---

## 📊 文件统计

### 核心配置文件 (6个)

| 文件 | 状态 | 行数 | 用途 |
|------|------|------|------|
| beliefs.yaml | ⚡ 重构 | ~280 | 认知核心与审稿标准 |
| goals.yaml | ⚡ 重构 | ~200 | 9个通用方法论目标 |
| agenda.yaml | ⚡ 重构 | ~180 | 8个学术质量议程 |
| decision_logic_guide.md | ⚡ 补全 | ~650 | 完整决策算法实现 |
| long_term_goals.md | ⚡ 改版 | ~250 | 通用追踪模板 |
| mindsymphony.config.yml | ✅ 保留 | ~150 | 蜂巢总配置 |

### 灵魂定义文件 (18个)

| 层级 | 数量 | 状态 | 说明 |
|------|------|------|------|
| L0 系统基石 | 8 | ✅ 保留 | 无需修改 |
| L1 状态决策 | 3 | ✅ 保留 | 配合新配置使用 |
| L2 功能单元 | 5 | ✅ 保留 | 无需修改 |
| L3 元进化 | 2 | ✅ 保留 | 无需修改 |

### 文档文件 (5个)

| 文件 | 状态 | 用途 |
|------|------|------|
| README.md | ⚡ 重写 | 系统总览 |
| CHANGELOG.md | ✨ 新增 | 版本变更 |
| FILE_MANIFEST.md | ✨ 新增 | 本文件 |
| QUICK_START.md | ✅ 保留 | 快速开始 |
| SYSTEM_ARCHITECTURE.md | ✅ 保留 | 架构文档 |

---

## 🔍 关键文件详解

### 1. beliefs.yaml (⚡ 重构)
**变更**：
- 移除个人研究特征（bootstrap, geriatric）
- 新增顶级期刊审稿标准
- 新增Critical Review Checklist
- 新增Red Flags错误清单

**核心内容**：
```yaml
core_values: [7个通用价值观]
methodological_stance: "evidence_based_skeptic"
epistemic_threshold: 0.70
critical_review_checklist: {study_design, statistical_analysis, causality, reporting}
critical_errors: {statistical, methodological, reporting, validation}
```

### 2. goals.yaml (⚡ 重构)
**变更**：
- 移除个人项目（gastric cancer, nonagenarian）
- 新增9个通用方法论目标
- 每个目标包含intervention_template

**核心内容**：
```yaml
active_goals: [9个目标，priority 0.70-0.95]
  - goal_ensure_adequate_power (0.95)
  - goal_demand_validation (0.90)
  - goal_causal_language_precision (0.90)
  - goal_multiple_testing_correction (0.85)
  - ...
```

### 3. agenda.yaml (⚡ 重构)
**变更**：
- 移除个人议程（bootstrap advocacy）
- 新增8个学术质量议程
- 每个包含intervention_examples

**核心内容**：
```yaml
agenda_items: [8个议程，importance 0.70-0.95]
  - agenda_validation_culture (0.95)
  - agenda_causal_inference_rigor (0.90)
  - ...
context_sensitivity: {适应用户类型}
```

### 4. decision_logic_guide.md (⚡ 补全)
**变更**：
- 补充Factor 4 (Misrepresented) 算法
- 补充Factor 5 (Silence Too Long) 追踪
- 补充Factor 6 (Agenda Opportunity) 匹配
- 新增完整示例演示

**核心内容**：
```markdown
- Factor 1-6完整检测算法（伪代码）
- Urgency计算公式
- Pattern A/B/C/D选择逻辑
- 完整示例演示（从输入到输出）
```

### 5. long_term_goals.md (⚡ 改版)
**变更**：
- 从个人项目追踪→通用目标模板
- 新增L3反思记录区
- 新增进度仪表盘

**核心内容**：
```markdown
- Goal 1: 提升研究者方法论质量
- Goal 2: 完善审稿决策框架
- Goal 3: 培养批判性思维
- L3反思与进化记录模板
- 进度仪表盘
```

---

## 💾 文件大小估算

```
beliefs.yaml              : ~15 KB
goals.yaml               : ~12 KB
agenda.yaml              : ~10 KB
decision_logic_guide.md  : ~35 KB
long_term_goals.md       : ~12 KB
README.md                : ~20 KB
CHANGELOG.md             : ~8 KB
FILE_MANIFEST.md         : ~5 KB
-----------------------------------
核心配置总计             : ~117 KB
```

---

## 🎯 使用优先级

### 必读文件 (启动前)
1. **README.md** - 系统概览和快速开始
2. **beliefs.yaml** - 了解系统的认知标准
3. **decision_logic_guide.md** - 理解决策机制

### 进阶文件 (深度使用)
4. **goals.yaml** - 查看主动目标清单
5. **agenda.yaml** - 了解战略议程
6. **long_term_goals.md** - 追踪长期进展

### 架构文件 (开发/定制)
7. **SYSTEM_ARCHITECTURE.md** - 理解蜂巢架构
8. **souls/* ** - 查看18个灵魂定义
9. **mindsymphony.config.yml** - 修改蜂巢配置

---

## 🔄 文件依赖关系

```
decision_logic_guide.md
    ↓ 读取
beliefs.yaml + goals.yaml + agenda.yaml
    ↓ 驱动
[ACS-Governor] 决策
    ↓ 触发
[ACS-Writer] 响应
    ↓ 记录
[M-04] 反思
    ↓ 提案
[M-01] 进化
    ↓ 更新
long_term_goals.md
```

---

## 📦 部署清单

### 最小可用配置 (核心5文件)
```
✅ beliefs.yaml
✅ goals.yaml
✅ agenda.yaml
✅ decision_logic_guide.md
✅ long_term_goals.md
```

### 完整配置 (推荐)
```
✅ 核心5文件
✅ README.md
✅ mindsymphony.config.yml
✅ souls/* (18个灵魂)
✅ docs/* (架构文档)
```

---

## ⚙️ 配置文件版本

| 文件 | 版本 | 最后更新 |
|------|------|----------|
| beliefs.yaml | v1.2-gen | 2025-11-10 |
| goals.yaml | v1.2-gen | 2025-11-10 |
| agenda.yaml | v1.2-gen | 2025-11-10 |
| decision_logic_guide.md | v1.2-complete | 2025-11-10 |
| long_term_goals.md | v1.2-template | 2025-11-10 |

**版本命名规则**：
- `v1.2-gen`: 通用化版本
- `v1.2-complete`: 完整实现版本
- `v1.2-template`: 模板版本

---

## 🚀 快速验证

运行系统前检查：

```bash
# 检查核心配置文件存在
✓ system_configs/beliefs.yaml
✓ system_configs/goals.yaml
✓ system_configs/agenda.yaml
✓ system_configs/decision_logic_guide.md
✓ system_configs/long_term_goals.md

# 检查关键参数
✓ beliefs.epistemic_threshold = 0.70
✓ goals.active_goals.length = 9
✓ agenda.agenda_items.length = 8
✓ decision_logic_guide.factors = 6

# 验证通过 → 系统就绪 ✅
```

---

**Manifest Version**: 1.2-Optimized  
**Generated**: 2025-11-10  
**Total Files**: 31 (6核心 + 18灵魂 + 5文档 + 2新增)  
**Status**: Complete ✅
