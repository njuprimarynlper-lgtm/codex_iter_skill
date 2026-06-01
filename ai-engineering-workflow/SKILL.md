---
name: ai-engineering-workflow
description: "设计、初始化、运行和复盘文件驱动的个人 AI 工程化工作流，用于固化不同层级思考切换、项目启动规划、prompt/skill、GT/data、workflow、评估指标、实验报告和决策交接。Use when Codex needs to create or refine a reusable four-box AI project workflow, reduce repeated project planning, define interfaces between business metrics, data, skills, workflows, experiments, and reports, build parallel experiment matrices, standardize reports, summarize experiment effects, or turn ad hoc AI work into a reproducible workflow."
---

# AI 工程化工作流

## 核心模型

这个 skill 的核心不是只解决实验归因，而是把个人在 AI 项目中的多层级思考方式固化成可复用流程。它帮助用户在“业务目标、数据事实、执行方案、评估决策”之间切换时，不必每个项目都重新规划一套方法，也不必靠记忆避免遗漏。

使用“四盒模型 + 文件驱动”的方式管理 AI 项目：

1. 业务与指标盒：负责任务定义、验收标准和指标含义。
2. 数据与 GT 盒：负责 Schema、标注规则、数据版本、数据切分和 GT 质量。
3. Skill 与 Workflow 盒：负责提示词、Skill 变体、流程步骤、模型参数和运行配置。
4. 评估与迭代盒：负责实验运行、报告、badcase、汇总、决策和下一步行动。

把项目文件当作唯一真相源。对话只是工作界面，持久状态、层级选择、项目规划和交接结论都必须写入项目文件。

## 进入项目

进入已有项目时：

1. 读取 `STATUS.md`、`TASK_SPEC.md`，以及当前盒子的专属文件。
2. 判断用户请求属于哪个思考层级和哪个盒子。
3. 按任务类型读取下方对应 reference，不要一次性加载全部 reference。
4. 修改前检查该盒子的输入、输出和依赖关系。
5. 更新归属文件，并同步写入受影响的交接记录。

创建新项目结构时，优先运行：

```bash
python <skill-dir>/scripts/init_ai_workflow_project.py <project-root> --task-name "<任务名称>"
```

只有当用户明确要求覆盖模板文件时，才使用 `--force`。

## 协议路由

按当前任务读取最小必要 reference：

| 场景 | 读取 |
| --- | --- |
| 用户问“下一步做什么”“今天做什么”“继续”“当前状态” | `references/protocols.md` 的“下一步诊断协议” |
| 指令不明确，且可能影响方向、版本、数据、实验结论或生产配置 | `references/protocols.md` 的“不明确指令确认协议” |
| 涉及 GT、标注规则、验收标准或边界定义变化 | `references/protocols.md` 的“GT 标准变更确认协议” |
| 完成 Skill、Workflow、数据处理、评估脚本或关键配置迭代 | `references/protocols.md` 的“方案迭代测试门” |
| 生成给人看的手册、设计文档、阶段总结、评审记录或决策说明 | `references/protocols.md` 的“项目文档归档协议” |
| 比较实验、汇总实验、晋升胜出方案或处理无效实验 | `references/protocols.md` 的“实验比较与晋升协议” |
| 初始化后缺少任务、数据、Skill 或状态信息 | `references/intake-guide.md` |
| 设计或审计盒子之间的输入输出接口 | `references/interface-contracts.md` |
| 需要创建或修复标准项目文件 | `references/templates.md` |
| 在 Windows/PowerShell 中生成中文 Markdown、CSV 或报告 | `references/protocols.md` 的“中文文件编码协议” |

## 不可压缩硬规则

- 每次改动先归属到一个盒子，再为其他盒子写交接说明。
- 每次新项目或新会话先复用这套流程，而不是临场重新发明规划清单。
- 用户问“下一步做什么”时，不要只回答一个动作；必须给出下几步、推荐顺序、候选方案和首选建议。
- 指令不明确且会影响关键方向或重要产物时，必须先确认；低风险细节可以声明假设后继续。
- 给人看的项目产物统一放在当前项目的 `docs/` 或项目已有文档目录；skill 目录只放可复用规则、模板、脚本和 reference。
- GT、标注规则、验收标准或边界定义变更必须先向用户确认标准，再更新数据或评估结论。
- 每次方案迭代后主动询问是否跑测试或评估；测试不达标时必须输出当轮指标、问题、典型 badcase、可能原因和下一轮建议。
- 所有可比较产物都要版本化：任务定义、Schema、GT、Skill、Workflow、指标、报告 Schema、实验配置。
- 每个实验必须同时输出 `report.json` 和 `report.md`：前者给机器汇总，后者给人阅读。
- 不要静默修改已完成的实验目录；实验有误时标记为 invalid，并重新生成新实验。

## 常见任务

### 初始化或修复项目结构

用初始化脚本生成干净骨架。如果用户需要更贴近项目的文件内容，再读取 `references/templates.md`。

初始化后不要只留下空 TODO。若 `TASK_SPEC.md`、`data/schema.yaml`、`pipeline/skill_prompt.txt` 或 `STATUS.md` 缺少关键信息，读取 `references/intake-guide.md`，主动进入信息补齐向导。

### 设计接口

定义或审计盒子之间如何对齐时，读取 `references/interface-contracts.md`，确保每个 artifact 都有 owner、imports、exports、version 和 validation gate。

### 构建或汇总实验

构建实验矩阵、比较实验、汇总结果、判断主效应或交互效应、晋升胜出方案时，读取 `references/protocols.md` 的“实验比较与晋升协议”；需要接口字段细节时再读取 `references/interface-contracts.md`。

### 方案迭代后的测试闭环

完成 Skill、Workflow、数据处理、评估脚本或关键配置修改后，读取 `references/protocols.md` 的“方案迭代测试门”，询问是否运行测试或评估，并按达标/不达标/无法测试三类结果输出。

### 关闭一次会话

更新 `STATUS.md`，至少包含：

- 完成了什么。
- 改了哪些文件。
- 当前版本是什么。
- 做了哪些决策。
- 还有哪些阻塞。
- 下次建议进入哪个盒子、先读哪些文件。

## 详细参考

- `references/protocols.md`：下一步诊断、不明确指令确认、GT 标准确认、方案迭代测试门、文档归档、实验比较与晋升、中文文件编码。
- `references/interface-contracts.md`：盒子归属、交接契约、Schema、验证门和防止盒子漂移的检查项。
- `references/intake-guide.md`：初始化后缺少信息时，应该向用户询问什么、为什么问、答案可以长什么样。
- `references/templates.md`：`STATUS.md`、`TASK_SPEC.md`、manifest、grid、实验配置、报告和 changelog 的简洁模板。
