# 🚀 START HERE - ACS蜂巢系统快速开始

**当前版本**: V4.0（灵魂DNA架构） | **生产版本**: V2.5（知识增强导师）
**最后更新**: 2025-11-17

---

## ⚡ 5分钟快速决策

### 我应该使用哪个版本？

```
┌─────────────────────────────────────────────────────────────┐
│  需求场景                                    →  推荐版本     │
├─────────────────────────────────────────────────────────────┤
│  🎯 立即投入生产，需要稳定可靠               →  V2.5        │
│  🔬 探索前沿架构，体验灵魂DNA系统            →  V4.0        │
│  📖 仅需审稿功能，追求简单                   →  V1.2        │
│  🚀 需要多智能体协作                         →  V3.0/V4.0   │
└─────────────────────────────────────────────────────────────┘
```

### 版本特性对比

| 特性 | V1.2 | V2.5 | V3.0 | V4.0 |
|------|------|------|------|------|
| 审稿专家 | ✅ | ✅ | ✅ | ✅ |
| 教学辅导 | ❌ | ✅ | ✅ | ✅ |
| 文献探索 | ❌ | ✅ | ✅ | ✅ |
| 统计分析 | ❌ | ✅ | ✅ | ✅ |
| 学术写作 | ❌ | ✅ | ✅ | ✅ |
| 记忆系统 | ❌ | ✅ | ✅ | ✅ |
| 多智能体 | ❌ | ❌ | ✅ | ✅ |
| 灵魂DNA | ❌ | ❌ | ❌ | ✅ |
| 生产就绪 | ✅ | ✅ | 🔶 | 🔶 |

> 图例：✅ 支持 | ❌ 不支持 | 🔶 实验性

---

## 📖 必读文档（按推荐顺序）

### 🌟 核心文档

1. **[README.md](./README.md)** - 系统总览（含所有版本）
   > 10分钟了解完整系统和版本演进

2. **[ARCHITECTURE_UNIFIED.md](./ARCHITECTURE_UNIFIED.md)** - 统一架构文档 ⭐
   > 完整版本演进分析（V1.2→V4.0），版本选择指南

3. **[CHANGELOG.md](./CHANGELOG.md)** - 变更日志
   > 详细的版本变更记录

### 📚 版本专属文档

#### V4.0 灵魂DNA架构（当前最新）
- **[SOUL_DNA_CONFIGURATION.md](./SOUL_DNA_CONFIGURATION.md)** - 灵魂DNA配置详解
- **[mindsymphony.config.yml](./mindsymphony.config.yml)** - 蜂巢总配置
- **[.acs_mentor/souls/](/.acs_mentor/souls/)** - 灵魂DNA定义文件
  - `explorer_dna.yaml` - ACS-Explorer（文献探索）
  - `analyst_dna.yaml` - ACS-Analyst（统计分析）
  - `writer_dna.yaml` - ACS-Writer（学术写作）
  - `mentor_dna.yaml` - ACS-Mentor（教学辅导）

#### V3.0 多智能体架构
- **[ACS_MENTOR_V3_0_ARCHITECTURE.md](./ACS_MENTOR_V3_0_ARCHITECTURE.md)** - 架构文档
- **[.acs_mentor/multi_agent_config.yaml](./.acs_mentor/multi_agent_config.yaml)** - 配置文件

#### V2.5 知识增强导师（生产就绪）
- **[ACS_MENTOR_V2_5_ARCHITECTURE.md](./ACS_MENTOR_V2_5_ARCHITECTURE.md)** - 架构文档

#### V1.2 单一审稿专家
- **[system_configs/](./system_configs/)** - 配置目录
  - `beliefs.yaml` - 认知核心（审稿标准）
  - `goals.yaml` - 主动目标
  - `agenda.yaml` - 战略议程
  - `decision_logic_guide.md` - 六因素决策算法

### 🗺️ 系统演进文档
- **[SYSTEM_EVOLUTION_MAP.md](./SYSTEM_EVOLUTION_MAP.md)** - 系统演进地图
- **[SYSTEM_CLEANUP_REPORT.md](./SYSTEM_CLEANUP_REPORT.md)** - 系统整理报告

---

## 🚀 快速开始指南

### V4.0 灵魂DNA架构

#### 1. 查看配置
```bash
# 蜂巢总配置
cat mindsymphony.config.yml

# 灵魂DNA定义
ls -la .acs_mentor/souls/
cat .acs_mentor/souls/explorer_dna.yaml
```

#### 2. 理解核心概念
- **8维灵魂DNA**: 认知类型、核心信念、内在冲突、独特视角、美学追求、系统定位、核心能力、工作流协议
- **蜂后机制**: ACS-Coordinator作为元认知控制器
- **三级工具协议**: L1(项目) > L2(用户) > L3(系统)
- **信息素工作流**: 事件驱动的自动化流程

#### 3. 开始使用
```
你：帮我设计一个关于XX的研究方案
→ Coordinator分析任务，分配给Explorer+Analyst
→ Explorer提供文献综述
→ Analyst设计统计方案
→ Writer生成研究计划
→ Mentor提供教学指导
```

---

### V2.5 知识增强导师（推荐生产使用）

#### 1. 查看配置
```bash
cat ACS_MENTOR_V2_5_ARCHITECTURE.md
```

#### 2. 理解核心概念
- **双模式运行**: 批判审稿 + 苏格拉底教学
- **记忆系统**: 跨会话学习和优化
- **知识增强**: 外部文献实时融合
- **成熟稳定**: 经过实战验证

#### 3. 开始使用
```
你：切换到导师模式，解释一下什么是Bootstrap
→ 系统进入教学模式，使用苏格拉底式提问
→ 结合外部文献提供深度解释
→ 记忆本次交互，持续优化
```

---

### V1.2 单一审稿专家

#### 1. 查看配置
```bash
# 核心配置文件
cat system_configs/beliefs.yaml
cat system_configs/goals.yaml
cat system_configs/decision_logic_guide.md
```

#### 2. 理解核心概念
- **六因素决策框架**: 结构化主动介入
- **国际审稿标准**: CONSORT, STROBE, TRIPOD
- **四层架构**: L0-L3有机体系统

#### 3. 开始使用
```
你：我们的N=18研究显示X显著导致Y（p<0.05）

系统检测到严重错误：
→ Factor 1: error_detection = 1.0 (样本量不足)
→ Factor 1: error_detection = 0.9 (因果语言误用)
→ urgency = 0.95 → Pattern A (强介入)
→ 提供详细批判和改进建议
```

---

## 🎯 核心功能速查

### 文献探索（V2.5+）
```
"帮我综述一下XX领域的最新进展"
→ ACS-Explorer执行文献挖掘
→ 提供结构化综述
```

### 统计分析（V2.5+）
```
"我的数据适合用什么统计方法？"
→ ACS-Analyst评估数据特征
→ 推荐适当方法并解释原因
```

### 学术写作（V2.5+）
```
"帮我写Methods部分"
→ ACS-Writer应用IMRaD结构
→ 遵循CONSORT/STROBE规范
```

### 教学辅导（V2.5+）
```
"解释一下什么是多重比较校正"
→ ACS-Mentor进入教学模式
→ 苏格拉底式引导理解
```

### 审稿评估（所有版本）
```
"帮我审查这个研究设计"
→ 应用六因素决策算法
→ 识别方法学问题
→ 提供改进建议
```

---

## 💡 使用建议

### For 研究新手
1. **推荐**: V2.5（教学功能强大）
2. **路径**: 先阅读 README.md → 使用导师模式学习
3. **重点**: 利用教学功能培养批判性思维

### For 资深研究者
1. **推荐**: V2.5（生产稳定）或 V4.0（探索前沿）
2. **路径**: 快速扫描 ARCHITECTURE_UNIFIED.md → 直接使用
3. **重点**: 利用专业深度节省时间

### For 系统开发者
1. **推荐**: 研究 V4.0 架构
2. **路径**: SOUL_DNA_CONFIGURATION.md → mindsymphony.config.yml
3. **重点**: 理解灵魂DNA系统设计理念

---

## 🔧 配置验证

### V4.0 检查清单
```bash
✓ mindsymphony.config.yml 存在
✓ .acs_mentor/souls/ 目录存在
✓ 4个DNA文件完整 (explorer, analyst, writer, mentor)
✓ version: "4.0.0"
→ V4.0 就绪 ✅
```

### V2.5 检查清单
```bash
✓ ACS_MENTOR_V2_5_ARCHITECTURE.md 存在
✓ .acs_mentor/ 目录存在
✓ 多智能体配置文件存在
→ V2.5 就绪 ✅
```

### V1.2 检查清单
```bash
✓ system_configs/beliefs.yaml 存在
✓ system_configs/goals.yaml 存在
✓ 9个目标定义完整
✓ 8个议程定义完整
→ V1.2 就绪 ✅
```

---

## 📞 获取帮助

### 文档导航
- **系统总览**: [README.md](./README.md)
- **完整演进**: [ARCHITECTURE_UNIFIED.md](./ARCHITECTURE_UNIFIED.md)
- **版本选择**: [SYSTEM_EVOLUTION_MAP.md](./SYSTEM_EVOLUTION_MAP.md)

### 快速链接
- **V4.0配置**: [SOUL_DNA_CONFIGURATION.md](./SOUL_DNA_CONFIGURATION.md)
- **V3.0架构**: [ACS_MENTOR_V3_0_ARCHITECTURE.md](./ACS_MENTOR_V3_0_ARCHITECTURE.md)
- **V2.5文档**: [ACS_MENTOR_V2_5_ARCHITECTURE.md](./ACS_MENTOR_V2_5_ARCHITECTURE.md)
- **V1.2算法**: [decision_logic_guide.md](./system_configs/decision_logic_guide.md)

---

## 🎓 学习路径推荐

### 路径 1: 快速上手（30分钟）
```
1. 阅读本文档 (10分钟)
2. 浏览 README.md (10分钟)
3. 选择版本并开始使用 (10分钟)
→ 可立即投入使用
```

### 路径 2: 深度理解（2小时）
```
1. 阅读 ARCHITECTURE_UNIFIED.md (40分钟)
2. 阅读对应版本架构文档 (40分钟)
3. 研究配置文件 (40分钟)
→ 全面掌握系统设计
```

### 路径 3: 系统开发（1天）
```
1. 研究完整演进历史 (2小时)
2. 深入V4.0灵魂DNA设计 (3小时)
3. 实验配置和定制 (3小时)
→ 具备二次开发能力
```

---

**当前版本**: V4.0 (灵魂DNA架构)
**生产版本**: V2.5 (知识增强导师)
**文档状态**: 完整 ✅
**最后更新**: 2025-11-17

*"选择适合的版本，开启高效研究之旅"* 🚀
