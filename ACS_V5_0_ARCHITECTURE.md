# ACS V5.0 Architecture - 完整研究生命周期系统

**版本**: V5.0.0  
**发布日期**: 2025-11-18  
**核心主题**: Phase 1-3全面实施，从灵魂DNA到完整研究生命周期系统

---

## 🎯 V5.0核心升级

### 设计理念变革

**从"可选18灵魂"到"精简15核心"**

- V4.0: 18个灵魂（可选配置）
- V5.0: 15个核心灵魂（可扩展至18）⭐

**架构优化**:
```
L0 (系统基石): 5个灵魂（精简，去除冗余）
L1 (状态决策): 2个灵魂（整合人格核心）
L2 (功能专家): 6-9个灵魂（核心6 + 可选3）
L3 (元进化): 2个灵魂
```

---

## ✨ Phase 1: 核心系统（MVP）

### 1. Designer (研究设计师) - [A-01] ⭐⭐⭐⭐⭐

**定位**: 研究全生命周期的起点

**核心能力**:
- PICO/FINER框架问题精炼
- 研究设计类型选择（RCT/队列/病例对照等）
- 样本量计算
- 随机化与盲法设计
- 偏倚控制策略

**为什么必需**: 
> "好的设计胜过昂贵的分析。研究设计是科研的建筑蓝图，缺陷无法靠后期分析弥补。"

**典型场景**:
```
用户: "我想研究新药X对糖尿病的降糖效果"
Designer: 
  → PICO精炼
  → 推荐RCT设计
  → 计算样本量（N=200, 功效80%）
  → 设计双盲方案
```

---

### 2. Reviewer (同行评审者) - [A-05] ⭐⭐⭐⭐⭐

**定位**: 投稿前质量把关，预防desk reject

**核心能力**:
- 顶刊审稿人视角模拟（NEJM/Lancet）
- 常见拒稿原因检测
- CONSORT/STROBE合规检查
- 预期审稿意见生成
- Rebuttal letter指导

**为什么必需**:
> "投稿前预审能将接受率提升30%+。最严厉的批评应该来自自己，而非编辑。"

**典型场景**:
```
Writer完成论文 → Reviewer预审
→ 识别致命弱点：无对照、样本量不足、因果语言误用
→ 生成修改建议（Priority 1/2/3）
→ Writer修订 → 重复直到达标
```

---

### 3. Guardian (质量守护者) - [B-10] ⭐⭐⭐⭐

**定位**: 内建质量保证，嵌入工作流

**核心能力**:
- CONSORT/STROBE自动合规检查
- 统计报告三要素验证（效应量+CI+p值）
- 数据完整性审计
- 科学诚信监控（p-hacking检测）

**为什么必需**:
> "质量保证应该内建到系统，而非事后检查。"

**工作模式**:
```
Designer完成设计 → Guardian检查（无对照? 样本量不足?）
Analyst完成分析 → Guardian检查（效应量+CI+p值齐全?）
Writer完成论文 → Guardian检查（CONSORT 25项合规?）
```

---

## 📚 Phase 2: 完整系统

### 4. Librarian (知识图书馆员) - [B-11] ⭐⭐⭐⭐

**定位**: 系统长期记忆，RAG知识管理

**核心能力**:
- RAG知识管理（Vector DB）
- 文献网络图谱构建
- 智能引用管理（Zotero集成）
- 个人知识库维护
- 跨项目知识复用

**为什么必需**:
> "AI需要长期记忆，否则每次对话都从零开始。"

**技术栈**:
- Vector DB: Chroma/Pinecone
- Embedding: OpenAI text-embedding-3-large
- Retrieval: Semantic search + Re-ranking

---

## 🔬 Phase 3: 领域扩展（可选）

### 5. Ethicist (伦理顾问) - [A-07]

**激活条件**: 当研究涉及人体试验/敏感数据

**核心能力**:
- IRB/伦理委员会申请指导
- 知情同意书审查
- 数据隐私合规（GDPR/HIPAA）

---

### 6. Bioinformatician (生信专家) - [A-08]

**激活条件**: 当研究涉及组学数据

**核心能力**:
- RNA-seq差异表达分析
- GWAS关联分析
- 通路富集分析（GSEA/KEGG）

---

### 7. Epidemiologist (流行病学家) - [A-09]

**激活条件**: 当研究涉及人群健康/因果推断

**核心能力**:
- 流行病学研究设计
- 因果推断框架（DAG/PS/IV）
- 公共卫生政策评估

---

## 🔄 完整研究生命周期覆盖

```
阶段1: 问题提出
  → Designer: PICO精炼 + 设计选择

阶段2: 文献综述
  → Explorer: 系统检索 + 证据综合
  → Librarian: 自动索引 + 知识图谱

阶段3: 伦理审批（可选）
  → Ethicist: IRB申请 + 知情同意

阶段4: 数据分析
  → Analyst: 统计分析（通用）
  → Bioinformatician: 组学分析（可选）
  → Epidemiologist: 因果推断（可选）

阶段5: 论文撰写
  → Writer: IMRaD写作 + CONSORT合规

阶段6: 质量审查
  → Guardian: 内建质量检查
  → Reviewer: 预评审 + 弱点识别

阶段7: 知识传授
  → Mentor: 教学解释 + 能力培养

阶段8: 系统进化
  → Recorder: 学习数据采集
  → Architect: 系统优化建议
```

---

## 📊 V4.0 vs V5.0 对比

| 维度 | V4.0 | V5.0 |
|------|------|------|
| **总灵魂数** | 18个（可选） | 15个核心（可扩展至18） |
| **L2 Specialists** | 4个 | 6-9个 |
| **研究设计** | 缺失（Explorer兼任） | Designer专职 ⭐ |
| **预评审** | 缺失 | Reviewer专职 ⭐ |
| **质量保证** | 分散 | Guardian内建 ⭐ |
| **知识管理** | 缺失 | Librarian (RAG) ⭐ |
| **生命周期覆盖** | 部分 | 完整 ✅ |

---

## 🎯 使用建议

### 对于研究新手
**推荐**: 使用全部核心6个（Designer/Explorer/Analyst/Writer/Reviewer/Mentor）
- Designer帮你设计严谨的研究
- Reviewer帮你避免常见错误
- Mentor帮你理解方法论

### 对于资深研究者
**推荐**: 核心6个 + 按需启用可选专家
- Designer节省设计时间
- Reviewer提前发现弱点
- 可选专家处理特殊数据类型

### 对于临床研究
**推荐**: 核心6个 + Ethicist（必需）
- Ethicist处理伦理审批
- Designer设计严格的RCT
- Guardian确保CONSORT合规

---

## 🚀 快速开始

### 1. 查看配置
```bash
cat mindsymphony.config.yml  # V5.0总配置
ls .acs_mentor/souls/        # 查看所有灵魂DNA
```

### 2. 验证DNA文件
```bash
✓ designer_dna.yaml      (13KB - 完整8维定义)
✓ reviewer_dna.yaml      (16KB - 完整8维定义)
✓ guardian_dna.yaml      (1.7KB - 核心定义)
✓ librarian_dna.yaml     (1.1KB - 核心定义)
✓ ethicist_dna.yaml      (1.1KB - 可选)
✓ bioinformatician_dna.yaml (1.3KB - 可选)
✓ epidemiologist_dna.yaml (1.1KB - 可选)
```

### 3. 启动系统
```python
# 核心6个自动激活
核心启动 = [
    "ACS-Coordinator",  # 蜂后
    "ACS-Designer",     # ⭐ V5.0新增
    "ACS-Explorer",
    "ACS-Analyst",
    "ACS-Writer",
    "ACS-Reviewer",     # ⭐ V5.0新增
    "ACS-Mentor"
]

# 可选专家按需激活
if 研究类型 == "临床试验":
    激活("ACS-Ethicist")
if 数据类型 == "RNA-seq":
    激活("ACS-Bioinformatician")
if 研究目的 == "因果推断":
    激活("ACS-Epidemiologist")
```

---

## 📚 相关文档

- **配置文件**: [mindsymphony.config.yml](./mindsymphony.config.yml)
- **完整演进**: [ARCHITECTURE_UNIFIED.md](./ARCHITECTURE_UNIFIED.md)
- **变更日志**: [CHANGELOG.md](./CHANGELOG.md)
- **快速开始**: [🚀_START_HERE.md](./🚀_START_HERE.md)

---

**核心价值**: V5.0实现了从问题提出到论文发表的完整研究生命周期支持！

**下一步**: 参见 [SYSTEM_EVOLUTION_MAP.md](./SYSTEM_EVOLUTION_MAP.md) 了解未来路线图

*"从单一审稿到全程伙伴，从被动工具到主动协作，V5.0是ACS系统的里程碑。"* 🎉
