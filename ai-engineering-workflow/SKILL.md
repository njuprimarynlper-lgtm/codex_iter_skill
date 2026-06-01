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

把文件当作唯一真相源。对话只是工作界面，持久状态、层级选择、项目规划和交接结论都必须写入项目文件。

## 进入项目时先做什么

进入已有项目时：

1. 读取 `STATUS.md`、`TASK_SPEC.md`，以及当前盒子的专属文件。
2. 判断用户请求属于哪个思考层级和哪个盒子。
3. 修改前检查该盒子的输入、输出和依赖关系。
4. 更新归属文件，并同步写入受影响的交接记录。

如果用户只问“下一步做什么”“今天做什么”“继续”“帮我看下当前状态”“我们现在该推进什么”，不要要求用户指定盒子。主动进入“下一步诊断”：

1. 先读 `STATUS.md` 和 `TASK_SPEC.md`；如果存在 `PROJECT_INTAKE.md`，也读取它。
2. 快速判断当前阶段：刚初始化、信息不足、需要建立 baseline、需要补数据、需要跑实验、需要汇总、需要决策或需要收尾。
3. 输出当前判断、未来 3 到 5 步路线图、推荐顺序、候选方案、首选方案及原因、需要读取或修改的文件。
4. 如果信息足够，先执行推荐顺序中的第一步，同时保留后续几步的推进路线；如果信息不足，一次最多问 5 个会阻塞行动的问题。
5. 用户回答后，把信息写入对应文件。

创建新项目结构时，优先运行：

```bash
python <skill-dir>/scripts/init_ai_workflow_project.py <project-root> --task-name "<任务名称>"
```

只有当用户明确要求覆盖模板文件时，才使用 `--force`。

## 操作规则

- 每次改动先归属到一个盒子，再为其他盒子写交接说明。
- 每次新项目或新会话先复用这套流程，而不是临场重新发明规划清单。
- 用户指令不明确时，先判断歧义是否会影响方向、文件、数据、版本、实验结论、生产配置或不可逆操作。若会影响，必须先向用户确认，不要擅自执行。
- 需要确认时，输出当前理解、歧义点、推荐默认方案，以及 1 到 3 个最关键问题；不要把能从项目文件中读取的信息再问用户。
- 如果只是低风险实现细节，且不会改变用户目标或重要产物，可以声明“我先按某假设处理”并继续执行；相关假设要在交接或 `STATUS.md` 中标为待确认。
- 用户问“下一步做什么”时，不要只回答一个动作。必须给出下几步、推荐顺序、候选方案和首选建议；若存在多条合理路线，要说明每条路线适合的条件、代价和风险。
- 给人看的输出文件必须统一由当前项目管理：使用手册、设计文档、阶段总结、评审记录、决策说明等优先写入项目的 `docs/` 或项目已有文档目录；实验报告 `report.md` 留在对应 `experiments/` 目录；不要把项目专属交付文档写进 skill 目录、全局目录或零散临时目录。
- skill 目录只保存可复用的规则、模板、脚本和 reference。若发现项目专属的人类可读文档被写到 skill 目录，应迁移回项目文档目录，并在回复中给出项目内路径。
- 每次执行方案迭代后，包括修改 Skill、Workflow、数据处理、评估脚本或关键配置，都要主动问用户是否需要跑一遍测试或评估。若已有明确测试命令且用户已授权继续，可以直接运行；否则先说明建议测试范围、预计产出和是否需要用户确认。
- 每次生成或修改实际逻辑/业务代码时，必须同步新增或更新对应测试用例。测试应覆盖本次改动的核心业务边界、已知 badcase 和回归风险；交付前至少运行相关测试子集，无法运行时必须把原因、风险和建议补跑命令写入交接记录。
- 每次测试或评估结束后，都要判断是否达到 `TASK_SPEC.md` 中的验收线和护栏指标。若不达标，必须输出当轮指标、未达标项、存在的问题、典型 badcase、可能原因和下一轮建议；不要只说“测试失败”或“性能不达标”。
- 所有可比较产物都要版本化：任务定义、Schema、GT、Skill、Workflow、指标、报告 Schema、实验配置。
- 使用 manifest 做查找。实验变多后不要只靠目录名理解含义。
- 实验 ID 从配置维度生成，例如 `exp_skill-v2_data-v21_flow-filter`。
- 每个实验都必须同时输出 `report.json` 和 `report.md`：前者给机器汇总，后者给人阅读。
- 比较实验前，先确认指标定义、数据切分、报告 Schema 和运行假设是否兼容。
- 如果实验网格不平衡，说明哪些主效应或交互效应结论证据不足。
- 胜出的变体要通过复制或引用提升到稳定的 `pipeline/` 文件，并在 `experiments/CHANGELOG.md` 记录决策。
- 不要静默修改已完成的实验目录。实验有误时，标记为 invalid 并重新生成新实验。
- 写给人的使用手册时，重点写“人需要做什么、AI 会帮什么、最后得到什么、如何验收”。不要把内部配置字段、登记格式或机器可读契约作为主线；这些放到设计文档或 reference。
- 在 Windows/PowerShell 中生成中文 Markdown、CSV 或报告时，避免把包含中文字符串常量的 here-string 通过管道传给 `python -` 或其他解释器；PowerShell 可能按当前代码页下转换源码，导致中文标题被永久写成 `?`。优先使用已有 UTF-8 脚本文件、`apply_patch` 创建/修改 UTF-8 文件，或让临时代码只含 ASCII 字符并用 `\uXXXX` 转义生成中文。写出文件时显式使用 UTF-8，并在交付前用 `rg -n "\?{3,}|\x{FFFD}" <输出.md>` 自检；命中时必须重新生成或修复，不能把乱码文件交付给用户。

## 常见任务模式

### 初始化或修复项目结构

用初始化脚本生成干净骨架。如果用户需要更贴近项目的文件内容，再读取 `references/templates.md`。

初始化后不要只留下空 TODO。若 `TASK_SPEC.md`、`data/schema.yaml`、`pipeline/skill_prompt.txt` 或 `STATUS.md` 缺少关键信息，进入“信息补齐向导”：

1. 读取 `PROJECT_INTAKE.md` 或 `references/intake-guide.md`。
2. 按四类文件列出缺失信息、用途和示例答案。
3. 一次最多问 5 个关键问题，优先询问会阻塞下一步的问题。
4. 对用户暂时不知道的信息，给出可接受的占位写法和需要后续确认的风险。
5. 用户回答后，把答案落到对应文件，而不是只留在对话中。

这个向导应由模型主动触发：只要扫描到关键文件为空、仍含 `待填写`/`TODO`，或用户提出宽泛推进请求，就先做补齐诊断，再继续执行。

### 设计接口

定义或审计盒子之间如何对齐时，读取 `references/interface-contracts.md`。确保每个 artifact 都有 owner、imports、exports、version 和 validation gate。

### 构建实验矩阵

把每个可变因素表示为变体库条目，然后组合成 `grid.yaml`。无效组合用 `include` 或 `exclude` 明确声明。每个生成的实验配置都应该固定：

- `task_spec_version`
- `schema_version`
- `dataset_version`
- `skill_version`
- `workflow_version`
- `metric_version`
- `model`
- `seed` 或 replay policy

### 汇总实验

优先读取所有 `report.json`；需要查看 badcase 细节和人工备注时再读取 `report.md`。汇总产出应包括：

- 按主指标排序的 Top 实验。
- 可比较前提下的因素主效应。
- 交互效应或条件性行为。
- 指标、GT、Schema 兼容性警告。
- 合并、回滚或下一轮 grid 建议。

### 方案迭代后的测试闭环

当完成一次方案迭代时，不要直接把工作视为完成。先输出本次迭代改了什么、建议跑哪类测试或评估、为什么需要跑，然后询问用户是否执行。

测试或评估完成后：

- 如果达标，说明达标依据、关键指标、护栏指标和是否建议进入晋升或下一轮探索。
- 如果不达标，输出固定结构：当轮指标、目标阈值、差距、主要问题、典型 badcase、可能原因、下一轮候选方案。
- 如果无法测试，说明原因、缺少什么、风险是什么，并把“未验证”写入交接记录或 `STATUS.md`。

### 关闭一次会话

更新 `STATUS.md`，至少包含：

- 完成了什么。
- 改了哪些文件。
- 当前版本是什么。
- 做了哪些决策。
- 还有哪些阻塞。
- 下次建议进入哪个盒子、先读哪些文件。

## 详细参考

- `references/interface-contracts.md`：盒子归属、交接契约、Schema、验证门和防止盒子漂移的检查项。
- `references/intake-guide.md`：初始化后缺少信息时，应该向用户询问什么、为什么问、答案可以长什么样。
- `references/templates.md`：`STATUS.md`、`TASK_SPEC.md`、manifest、grid、实验配置、报告和 changelog 的简洁模板。
