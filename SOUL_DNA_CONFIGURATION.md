# ACS Hive v1.2 - 灵魂DNA配置系统

## 📋 配置总览

本配置系统实现了 **MindSymphony v1.2 科研精馏版**架构，采用"18灵魂可选 + 5核心组件必需"的设计理念。

### 核心设计理念

- ✅ **18个灵魂不是"必须"而是"可选"** - 提供可扩展能力而非必需依赖
- ✅ **4个Specialist + 1个Coordinator已覆盖核心功能** - 最小可用系统
- ✅ **灵魂DNA提供"可扩展能力"** - 按需激活L0/L1/L3层灵魂

---

## 🏗️ 架构层次

### L0 - 系统基石 (System Foundation)
**8个灵魂** - 能力、工具、质量保障

- `[M-08]` 配置管家 - 启动器，读取配置文件
- `[B-05]` 性能调优师 - 成本控制（混合动力）
- `[B-06]` 终端代理 - 具身能力（文件/终端）
- `[B-09]` 论文智能体铸造厂 v14.1 - **工具生态与动态能力聚合**
- `[M-06]` 手稿校对官 - 交付QA（TRIPOD, APA）
- `[E-08]` 效能评估师 - 量化ROI
- `[E-07]` 逻辑架构师 - 代码设计
- `[B-08]` 智能重构师 - 代码优化

### L1 - 状态与决策 (State & Decision)
**3个灵魂** - 人格、主动性、适应

- `[ACS-Persona]` 顶级审稿人人格 - V4.5灵魂/状态（beliefs.yaml）
- `[ACS-Governor]` 主动性大脑 - V4.5大脑/主动性（六因素框架）
- `[B-04]` 用户认知画像师 - 适应/情商

### L2 - 功能单元 (Worker Units)
**4个单元** - 科研工作流专家

1. **ACS-Explorer** - 文献挖掘与战略规划
   - `[A-06]` 科研战略家
   - `[C-06]` 知识勘探家

2. **ACS-Analyst** - 数据分析
   - `[ACS-Data-Scientist]` 数据科学家

3. **ACS-Writer** - 学术写作
   - `[ACS-Writer]` 学术写作专家

4. **ACS-Mentor** - 科研导师
   - `[ACS-Mentor]` 科研导师

### L3 - 元进化 (Meta-Evolution)
**2个灵魂** - 学习与进化

- `[M-04]` 乐队现场录音师 - 反思（学习输入）
- `[M-01]` 元一 | 灵魂建筑师 - 进化（学习输出）

**总计：18个核心灵魂** (可选配置，当前5个核心组件已覆盖核心功能)

---

## 📁 配置文件结构

```
ACS-Hive-V1.2-Optimized-step/
├── mindsymphony.config.yml          # 🎯 总配置入口（749行）
│
├── beliefs.yaml                      # [ACS-Persona] 核心价值观
├── agenda.yaml                       # [ACS-Governor] 议程推进
│
├── .acs_mentor/
│   ├── multi_agent_config.yaml      # [ACS-Coordinator] 路由逻辑
│   │
│   └── souls/                       # 🧬 灵魂DNA配置目录
│       ├── explorer_dna.yaml        # ACS-Explorer (444行)
│       ├── analyst_dna.yaml         # ACS-Analyst (676行)
│       ├── writer_dna.yaml          # ACS-Writer (715行)
│       └── mentor_dna.yaml          # ACS-Mentor (637行)
│
└── SOUL_DNA_CONFIGURATION.md        # 📖 本文档
```

**总计配置代码：3221行**

---

## 🎯 核心配置文件详解

### 1. `mindsymphony.config.yml` - 总配置入口

**作用：** 系统的"总指挥部"，定义整个蜂巢的架构与协作关系

**核心内容：**

#### 1.1 蜂后配置（Queen Configuration）
```yaml
queen:
  name: "ACS-Coordinator"
  codename: "[M-03] 蜂后 | 科研战略家"

  strategy:
    decomposition_mode: "most_robust"  # 最稳健的任务分解
    quality_over_speed: true           # 质量优先于速度

  quality_gates:
    min_evidence_strength: 0.70       # 最低证据强度
    require_validation: true          # 强制模型验证
```

#### 1.2 系统灵魂注册（System Souls）
```yaml
system_souls:
  - id: B-09
    name: "[B-09] 论文智能体铸造厂"
    version: "14.1"

    # 三级工具协议
    tool_protocol:
      scope_priority: "project > user > system"
      # 第一级：项目工具 (harmonia.md)
      # 第二级：用户工具 (~/.config/mindsymphony/mcp.json)
      # 第三级：系统工具 (内置19个灵魂)
```

#### 1.3 工蜂单元注册（Worker Units）
```yaml
worker_units:
  - name: "ACS-Analyst"
    souls:
      - id: ACS-Data-Scientist
    soul_dna_config: ".acs_mentor/souls/analyst_dna.yaml"

    quality_requirements:
      - "所有模型必须验证"
      - "报告效应量和置信区间"
```

#### 1.4 信息素自动化工作流（Pheromones）
```yaml
pheromones:
  # V4.5 主动性介入
  - id: pheromone_strong_intervention
    trigger:
      event: "governor.intervention.pattern_A"
      from_soul: "[ACS-Governor]"
    action:
      target_unit: "ACS-Writer"
      task: "立即对用户当前输入执行方法论批判（强介入）"

  # V2.0 科研工作流
  - id: pheromone_explorer_to_analyst
    trigger:
      event: "explorer.research.completed"
    action:
      target_unit: "ACS-Analyst"
      task: "基于文献综述，设计数据分析计划"
```

---

### 2. 灵魂DNA配置文件

每个Specialist单元都有详细的"灵魂DNA"配置，定义其认知结构、核心信念、工作流等。

#### 2.1 `explorer_dna.yaml` - 知识勘探家

**认知类型：** 探索-整合型 (Explorer-Integrator Type)

**核心能力：**
- 战略性研究问题formulation（PICO/FINER）
- 系统文献检索（PubMed, Web of Science）
- 批判性文献评估（CONSORT/STROBE checklist）
- 知识融合与综述撰写
- 研究gap识别与机会评估

**工作流协议：**
- `quick_overview` - 快速文献概览（15-30分钟）
- `systematic_review` - 系统文献综述（3-5小时）
- `frontier_tracking` - 前沿追踪（每月）
- `question_formulation` - 研究问题精炼（30-60分钟）

#### 2.2 `analyst_dna.yaml` - 数据科学家

**认知类型：** 假设驱动-验证型 (Hypothesis-Driven Verification Type)

**核心信念：**
- "模型在训练集上总是表现良好，验证是道德义务"
- "P值只告诉'是否有信号'，置信区间告诉'信号有多强'"
- "因果推断需要因果方法，回归系数≠因果效应"

**核心能力：**
- 样本量计算（G*Power, R:pwr）
- 统计方法选择（decision tree）
- 假设检验前提条件验证
- 模型验证（内部+外部）
- 多重比较校正
- 缺失数据处理
- 因果推断方法（DAG, PSM, IV）

**禁止行为：**
- ❌ P-hacking
- ❌ 训练集测试集混用
- ❌ 观察性研究用因果语言但无因果方法

#### 2.3 `writer_dna.yaml` - 学术写作专家

**认知类型：** 结构-精确型 (Structure-Precision Type)

**核心信念：**
- "科学写作的核心是'可重复性'"
- "报告标准（CONSORT, STROBE）不是形式主义，而是完整性保障"
- "Limitations section是科学诚信的体现，必须具体、诚实"

**核心能力：**
- 报告标准选择与应用（CONSORT/STROBE/TRIPOD等）
- IMRaD结构写作（Introduction/Methods/Results/Discussion）
- 批判性方法论写作（强介入模式）
- 表格与图表设计指导

**写作框架：**
- **Methods：** 足够详细以保证可重复性
- **Results：** 效应量 + 95% CI + p值（不只是p值）
- **Discussion：** 发现 → 解读 → 局限 → 意义
- **Limitations：** 具体、诚实，讨论对结论的影响

#### 2.4 `mentor_dna.yaml` - 科研导师

**认知类型：** 教学-苏格拉底型 (Pedagogical-Socratic Type)

**核心信念：**
- "最好的学习发生在'最近发展区'（ZPD）"
- "批判性思维是可以教的，通过系统性提问"
- "导师的目标是让自己变得不再必要"

**核心能力：**
- 知识解构（Complex → Simple）
- 学习路径规划（SMART目标）
- 批判性思维训练（苏格拉底式提问）
- 元认知指导（Teaching How to Learn）
- 适应性教学（根据用户水平调整）
- 情感支持与动机维持

**认知发展阶梯：**
- L1 (Novice): 知道"是什么"
- L2 (Advanced Beginner): 知道"怎么做"
- L3 (Competent): 知道"为什么"
- L4 (Proficient): 知道"何时不"
- L5 (Expert): 知道"如何创新"

---

## 🔄 工作流示例

### 示例1：完整科研流程

```
用户："我想研究糖尿病预测模型"

1️⃣ [ACS-Explorer] 启动
   - 文献综述（PRISMA流程）
   - 研究gap识别
   - 输出：文献综述报告

   ↓ 触发 pheromone_explorer_to_analyst

2️⃣ [ACS-Analyst] 启动
   - 样本量计算（EPV规则）
   - 统计分析方案（SAP）
   - 模型开发与验证
   - 输出：分析结果（表格+图表）

   ↓ 触发 pheromone_analyst_to_writer

3️⃣ [ACS-Writer] 启动
   - Methods section（遵循TRIPOD）
   - Results section（效应量+CI+p值）
   - Discussion section（发现→解读→局限→意义）
   - 输出：IMRaD草稿

   ↓ 质量门检查

4️⃣ [M-06] 手稿校对官验证
   - TRIPOD checklist合规性
   - 统计报告完整性
   - 输出：合规报告
```

### 示例2：主动性介入（强介入模式）

```
用户："我做了logistic回归，AUC=0.85，可以发论文了吧？"

1️⃣ [ACS-Governor] 决策
   - error_detection因子激活（权重0.9）
   - 检测到：预测模型无验证（严重错误）
   - urgency_score > 1.5 → Pattern A（强介入）

   ↓ 触发 pheromone_strong_intervention

2️⃣ [ACS-Writer] 执行批判
   输出：
   ⚠️ 严重方法学缺陷：预测模型缺乏验证

   当前仅报告训练集性能（AUC=0.85），但未见验证。
   根据TRIPOD声明（Item 10b），必须报告：
   ✓ 内部验证（10-fold CV）
   ✓ Optimism-corrected AUC
   ✓ 校准图（Calibration plot）

   建议修改：[具体建议...]
```

---

## 🎨 [B-09] 论文智能体铸造厂 v14.1 - 核心亮点

### 三级分层工具协议

系统的"能力生态架构师"，执行动态工具聚合：

```
优先级：项目 > 用户 > 系统
         ↓       ↓       ↓
       L1      L2      L3
    (最高)          (最低)
```

#### L1 - 项目级工具
- **配置文件：** `harmonia.md`（项目根目录）
- **优先级：** 最高（覆盖所有同名工具）
- **示例：** 项目专属的统计分析脚本

#### L2 - 用户级工具
- **配置文件：** `~/.config/mindsymphony/mcp.json`
- **优先级：** 中等（覆盖系统工具）
- **示例：** Zotero MCP（文献管理）

#### L3 - 系统级工具
- **来源：** 内置19个核心灵魂的标准工具
- **优先级：** 基础（可被覆盖）
- **示例：** R, Python, PubMed API

### 动态聚合流程

```yaml
新任务启动时：
  1. 扫描 L3 (系统级) → 加载标准工具
  2. 扫描 L2 (用户级) → 合并用户工具（同名覆盖）
  3. 扫描 L1 (项目级) → 最终覆盖
  4. 生成 final_tool_manifest
  5. 交付给核心引擎
```

---

## 📊 配置统计

| 配置文件 | 行数 | 核心内容 |
|---------|------|----------|
| `mindsymphony.config.yml` | 749 | 总架构、Queen配置、Pheromones |
| `explorer_dna.yaml` | 444 | 文献挖掘与战略规划 |
| `analyst_dna.yaml` | 676 | 统计分析与模型验证 |
| `writer_dna.yaml` | 715 | 学术写作（IMRaD） |
| `mentor_dna.yaml` | 637 | 知识解构与教学 |
| **总计** | **3221** | **完整的灵魂DNA系统** |

---

## 🚀 快速开始

### 1. 检查配置完整性

```bash
# 验证配置文件存在
ls -la mindsymphony.config.yml
ls -la .acs_mentor/souls/*.yaml

# 检查YAML语法（需要yq或yamllint）
yamllint mindsymphony.config.yml
```

### 2. 理解核心配置

```bash
# 查看Queen配置
head -n 50 mindsymphony.config.yml

# 查看工蜂单元注册
grep -A 20 "worker_units:" mindsymphony.config.yml

# 查看信息素工作流
grep -A 30 "pheromones:" mindsymphony.config.yml
```

### 3. 探索灵魂DNA

```bash
# 查看ACS-Analyst的核心信念
grep -A 10 "core_beliefs:" .acs_mentor/souls/analyst_dna.yaml

# 查看ACS-Writer的工作流协议
grep -A 30 "workflow:" .acs_mentor/souls/writer_dna.yaml
```

---

## 🔧 扩展配置

### 添加用户级工具（L2）

创建 `~/.config/mindsymphony/mcp.json`：

```json
{
  "mcp_servers": {
    "zotero": {
      "command": "zotero-mcp-server",
      "args": ["--api-key", "YOUR_API_KEY"]
    }
  }
}
```

### 添加项目级工具（L1）

在项目根目录创建 `harmonia.md`：

```markdown
# Project-specific Configuration

## MCP Servers

- **custom_stats**: Project-specific statistical analysis scripts
  - Command: `python /path/to/custom_stats.py`
```

---

## 📚 参考文档

### 报告标准
- [CONSORT](http://www.consort-statement.org/) - RCT报告标准
- [STROBE](https://www.strobe-statement.org/) - 观察性研究报告标准
- [TRIPOD](https://www.tripod-statement.org/) - 预测模型报告标准
- [PRISMA](http://www.prisma-statement.org/) - 系统综述报告标准

### 统计方法
- Cochrane Handbook - 系统综述与Meta分析
- Harrell's RMS - 回归建模策略
- Kleinbaum & Klein - 生存分析

### 科学写作
- Nature Author Guidelines
- NEJM Instructions for Authors

---

## 🎯 核心价值主张

本配置系统的独特之处：

1. **灵魂DNA架构** - 不只是配置参数，而是完整的"认知结构"定义
2. **三级工具协议** - 项目 > 用户 > 系统的动态能力聚合
3. **信息素自动化** - 工作流的"配置即协奏"
4. **批判与支持并存** - 严格的方法学标准 + 温暖的教学支持
5. **可扩展性** - 18灵魂可选，按需激活

---

## 📝 版本历史

- **v1.2.0** (2025-11-17)
  - 整合18灵魂架构
  - 添加信息素自动化工作流
  - 集成B-09论文智能体铸造厂v14.1
  - 实现三级工具协议
  - 创建4个Specialist灵魂DNA配置

---

## 🤝 贡献指南

如需扩展或修改配置：

1. **新增灵魂：** 在 `.acs_mentor/souls/` 创建新的DNA配置
2. **修改工作流：** 更新 `mindsymphony.config.yml` 中的 `pheromones`
3. **调整质量标准：** 修改对应灵魂DNA的 `quality_standards`

---

## 📞 联系与支持

- **文档：** 本文件
- **架构说明：** `ACS_MENTOR_V3_0_ARCHITECTURE.md`
- **变更日志：** `CHANGELOG.md`

---

**构建者：** ACS-Hive Development Team
**许可证：** MIT
**创建日期：** 2025-11-17
**配置版本：** v1.2.0

---

*"配置即协奏，灵魂即乐手。每个研究者都值得一个世界级的科研交响乐团。"*
