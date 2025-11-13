# 🚀 部署指南 - ACS蜂巢V1.2优化版

## 📦 下载与安装

### 方式1: 直接下载压缩包

[下载: ACS-Hive-V1.2-Optimized.tar.gz](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized.tar.gz) (约30KB)

```bash
# 解压
tar -xzf ACS-Hive-V1.2-Optimized.tar.gz

# 进入目录
cd ACS-Hive-V1.2-Optimized

# 开始使用
cat 🚀_START_HERE.md
```

### 方式2: 直接访问目录

[浏览完整目录](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized)

---

## 📁 完整文件列表

### 🎯 快速入口
- [🚀_START_HERE.md](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/🚀_START_HERE.md) - 快速导航

### 📖 核心文档
- [UPGRADE_SUMMARY.md](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/UPGRADE_SUMMARY.md) - 升级摘要
- [README.md](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/README.md) - 完整说明
- [CHANGELOG.md](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/CHANGELOG.md) - 变更日志
- [FILE_MANIFEST.md](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/FILE_MANIFEST.md) - 文件清单

### ⚙️ 系统配置
- [beliefs.yaml](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/system_configs/beliefs.yaml) - 认知核心
- [goals.yaml](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/system_configs/goals.yaml) - 主动目标
- [agenda.yaml](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/system_configs/agenda.yaml) - 战略议程
- [decision_logic_guide.md](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/system_configs/decision_logic_guide.md) - 决策算法
- [long_term_goals.md](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/system_configs/long_term_goals.md) - 长期追踪

---

## 🎯 使用流程

### Step 1: 理解系统 (10分钟)

```markdown
1. 阅读 🚀_START_HERE.md (2分钟)
   → 了解快速导航

2. 阅读 UPGRADE_SUMMARY.md (5分钟)
   → 了解核心变更

3. 浏览 README.md (3分钟)
   → 了解系统功能
```

### Step 2: 配置系统 (5分钟)

```yaml
# 检查 system_configs/ 中的5个文件

1. beliefs.yaml
   → 确认 epistemic_threshold: 0.70 (可调整)
   
2. goals.yaml  
   → 查看9个通用目标
   
3. agenda.yaml
   → 查看8个议程

4. decision_logic_guide.md
   → 理解六因素决策算法

5. long_term_goals.md
   → 准备追踪长期进展
```

### Step 3: 开始使用

#### 对话模式 (推荐)

直接在Claude对话中激活系统：

```
你：请基于ACS蜂巢V1.2优化版的配置，
    审查以下研究设计...

系统将自动：
1. 读取 beliefs/goals/agenda配置
2. 应用六因素决策算法
3. 选择介入模式 (Pattern A/B/C/D)
4. 生成批判或建议
```

#### 测试模式

验证系统功能：

```
测试1: 错误检测 (Pattern A)
你：我们的N=15研究显示X显著导致Y (p<0.05)

期望：
- Factor 1 (error_detection): 0.9 (小样本)
- Factor 2 (goal_threatened): 0.72 (样本量目标)
- Urgency: 1.62
- Pattern: A (强介入)

---

测试2: 战略沉默 (Pattern D)
你：这个手术的最佳切口位置是...

期望：
- Factor 3 (expertise_match): 0.0 (非专长)
- Urgency: <0.35
- Pattern: D (沉默，defer to experts)

---

测试3: 议程推进 (Factor 6)
你：我的模型AUC=0.90，性能很好

期望：
- Factor 1 (error_detection): 0.9 (无验证)
- Factor 6 (agenda_opportunity): 0.95 (validation_culture)
- Urgency: 1.76
- Pattern: A (强介入+推进议程)
```

---

## 🔧 自定义配置

### 调整认知阈值

**beliefs.yaml**
```yaml
epistemic_threshold: 0.70  # 默认
# 可调范围: 0.60-0.85
# 更高 = 更严格，更低 = 更宽容
```

### 调整目标优先级

**goals.yaml**
```yaml
- id: goal_ensure_adequate_power
  priority: 0.95  # 默认
  # 可调范围: 0.50-1.00
```

### 调整介入阈值

**goals.yaml (底部)**
```yaml
intervention_thresholds:
  critical: 0.85   # Pattern A触发
  high: 0.70       # Pattern B触发
  moderate: 0.50   # Pattern C触发
  # 可根据实际使用调整
```

---

## 📊 质量验证清单

### ✅ 配置完整性

```bash
# 检查核心文件存在
[ -f system_configs/beliefs.yaml ] && echo "✓ beliefs.yaml"
[ -f system_configs/goals.yaml ] && echo "✓ goals.yaml"
[ -f system_configs/agenda.yaml ] && echo "✓ agenda.yaml"
[ -f system_configs/decision_logic_guide.md ] && echo "✓ decision_logic_guide.md"
[ -f system_configs/long_term_goals.md ] && echo "✓ long_term_goals.md"
```

### ✅ 参数合理性

```yaml
# beliefs.yaml
epistemic_threshold: 0.60-0.85 ✓
openness_to_novelty: 0.40-0.70 ✓
tolerance_for_ambiguity: 0.20-0.50 ✓

# goals.yaml
active_goals.length: 9 ✓
每个goal.priority: 0.70-0.95 ✓

# agenda.yaml  
agenda_items.length: 8 ✓
每个item.importance: 0.70-0.95 ✓
```

### ✅ 算法完整性

```markdown
decision_logic_guide.md 包含:
✓ Factor 1: Error Detection (完整算法)
✓ Factor 2: Goal Threatened (完整算法)
✓ Factor 3: Expertise Match (完整算法)
✓ Factor 4: Misrepresented (完整算法)
✓ Factor 5: Silence Too Long (完整算法)
✓ Factor 6: Agenda Opportunity (完整算法)
✓ Urgency Calculation (公式)
✓ Pattern Selection (A/B/C/D逻辑)
✓ Complete Example (完整演示)
```

---

## 🎓 进阶使用

### L3元进化激活

在使用过程中持续优化：

```markdown
每10次交互后:
1. [M-04] 在 long_term_goals.md 记录反思
2. 识别改进机会

每50次交互后:
1. [M-01] 评估进化需求
2. 在 long_term_goals.md 提出调优建议
3. 等待你批准
4. 更新 beliefs/goals/agenda配置
```

### 领域特化 (可选)

如需为特定领域定制：

```yaml
# beliefs.yaml (添加)
domain_specific:
  field: "clinical_psychology"  # 你的领域
  additional_standards:
    - "APA reporting guidelines"
  domain_expertise:
    - "Randomized controlled trials in psychology"
    - "Psychometric validation"
```

---

## 🚨 常见问题

### Q1: 系统太严格怎么办？

```yaml
# 降低认知阈值
epistemic_threshold: 0.75 → 0.65

# 降低介入阈值
critical: 0.85 → 0.90  # 减少Pattern A触发
```

### Q2: 想要更主动的介入？

```yaml
# 提高议程权重
agenda_opportunity权重: 0.75 → 1.0

# 降低沉默阈值
silence_too_long权重: 0.4 → 0.6
```

### Q3: 如何追踪长期进展？

```markdown
在每次重要交互后:
1. 手动更新 long_term_goals.md
2. 记录 Contributions 表格
3. 更新 Milestone 进度
4. 定期review (月度/季度)
```

---

## 📈 性能监控

### 建议追踪指标

```yaml
intervention_statistics:
  total_interventions: 0
  pattern_distribution:
    pattern_A: 0  # 强介入
    pattern_B: 0  # 中度
    pattern_C: 0  # 轻度
    pattern_D: 0  # 沉默
  
  acceptance_rate: 0.0
  # 建议被采纳的比例
  # 目标: >70%
  
  proactivity_ratio: 0.0
  # 主动介入/总交互
  # 目标: 40-60%
```

### 记录在 long_term_goals.md

每次交互后更新进度仪表盘。

---

## 🔗 相关资源

### 原始系统参考

- **V4.5 Python版**: [project files] 中的 proactive_agent.py
- **V3.0 PersonalityCore**: personality_core.py
- **V2.0 DSPy版**: 原始学术协奏系统

### 国际标准文档

- **CONSORT**: http://www.consort-statement.org/
- **STROBE**: https://www.strobe-statement.org/
- **TRIPOD**: https://www.tripod-statement.org/
- **PRISMA**: http://www.prisma-statement.org/

---

## 💬 技术支持

### 配置问题

查看 [FILE_MANIFEST.md](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/FILE_MANIFEST.md)

### 算法细节

查看 [decision_logic_guide.md](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/system_configs/decision_logic_guide.md)

### 使用指南

查看 [README.md](computer:///mnt/user-data/outputs/ACS-Hive-V1.2-Optimized/README.md)

---

## ✅ 部署完成清单

部署前检查：

- [ ] 已下载/解压全部文件
- [ ] 阅读了 🚀_START_HERE.md
- [ ] 浏览了 UPGRADE_SUMMARY.md  
- [ ] 检查了 system_configs/ 中5个文件
- [ ] 理解了六因素决策算法
- [ ] 进行了至少1次测试
- [ ] 系统就绪，开始使用 ✅

---

**部署指南版本**: V1.2-Optimized  
**更新日期**: 2025-11-10  
**状态**: Production Ready ✅

*开始你的科研质量提升之旅* 🚀
