# AI 算法研发管家型 Skill 模板

当用户要求创建或修复算法研发管家型项目文件时，使用这些模板。项目特有内容应该写入项目目录，不要堆在 skill 里。

## docs/README.md

```markdown
# 项目文档索引

给人看的项目文档统一放在本目录，或放在项目已有的文档目录中。

## 建议存放
- 使用手册
- 设计文档
- 阶段总结
- 评审记录
- 决策说明

## 文档索引
| 文档 | 位置 | 用途 |
| --- | --- | --- |
| 使用手册 | docs/ai_engineering_workflow_user_manual_zh.md | 给人看的操作说明。 |
| 设计文档 | docs/ai_engineering_workflow_design_doc_zh.md | 给维护者看的系统设计、接口和协议说明。 |
| 项目长期记忆 | PROJECT_MEMORY.md | 记录当前有效结论、当前最优结果、待确认假设和历史归档。 |
| 编辑授权边界 | EDIT_SCOPE.md | 维护 AI 可修改文件白名单、确认区和禁止区。 |
| 任务定义 | TASK_SPEC.md | 说明业务目标、输入输出、指标和验收线。 |
| 数据说明 | data/README.md | 说明数据版本、GT 变更和标注规则。 |
| 实验日志 | experiments/CHANGELOG.md | 说明实验意图、结果和决策。 |

## 维护规则
- 每次逻辑修改后，必须同步更新对应说明文档。
- 每次写文件前，先按 `EDIT_SCOPE.md` 判断文件是否在可修改白名单；未确认过的文件必须先问用户。
- 执行动作前先按授权边界判断：低风险直接做，中风险先提醒，高风险必须确认。
- 新的一天开始任何会写文件的动作前，先确认历史未提交改动是否需要提交 Git；固化昨日结论/方法也算写文件动作。
- Git 检查完成或确认不适用后，再检查前一天形成的有效结论和方法是否需要固化；不确定要固化的必须询问用户。
- 开工、下一步诊断和收尾时，必须维护 `STATUS.md` 的当前工作焦点；跨窗口继续时优先围绕该焦点给路线图。
- Markdown 不得无限增长；`STATUS.md`/本索引超过 200 行、`PROJECT_MEMORY.md` 超过 300 行、普通说明文档超过 600 行时，先压缩、归档或拆分，再继续追加。
- 若没有合适文档，先在本索引登记新文档的位置和用途。
- 交付时说明本次更新了哪些说明文档。

## 例外
- 单次实验的人类可读报告 `report.md` 保存在对应 `experiments/` 目录。
- 可复用的 skill 规则、模板和脚本保存在 skill 目录，不在本项目文档目录维护。
```

## PROJECT_INTAKE.md

```markdown
# 项目信息补齐清单

## 使用方式
当以下信息缺失时，请让 AI 按本清单分批提问，并把回答写回对应文件。

## 主动触发
当你问“下一步做什么”“今天做什么”“继续”“帮我看当前状态”时，AI 应主动读取 `STATUS.md`、`TASK_SPEC.md` 和本文件，先识别当前工作焦点，再判断当前阶段，并给出围绕焦点的未来 3 到 5 步路线图、推荐顺序、首选方案和备选方案。当你在新窗口说“使用这个 Skill，在这个工程中，分析最新测试结果”时，AI 应主动定位最新报告和当前最优基线，输出指标、问题、badcase、可比性和下一步建议。若项目没有最近巡检记录，或存在未验证改动、待确认标准、缺失报告、文档未同步，AI 应主动提醒你可以做一次巡检。若缺少关键信息，AI 应一次最多问 5 个问题，并给示例答案。

## 1. TASK_SPEC.md
- 业务目标：
- 输入样例：
- 输出示例：
- 主指标：
- 验收线：
- 非目标：

示例：
目标：从客服对话中抽取投诉原因和责任部门。
输入：一段客服对话文本。
输出：`{"complaint_reason": "...", "department": "...", "evidence_span": "..."}`
主指标：complaint_reason micro-F1，验收线 0.82。

## 2. data/schema.yaml
- 字段：
- 标签或实体：
- 关系：
- 边界规则：
- 冲突规则：

示例：
实体：PERSON、ORG、LOCATION。
关系：WORK_AT(PERSON, ORG)。
边界：地点包含行政区后缀，不包含前置介词。

## 3. pipeline/skill_prompt.txt
- AI 角色：
- 输出格式：
- 必须遵守的规则：
- 不确定时的处理方式：
- 是否已有 baseline prompt：

示例：
角色：信息抽取助手。
输出：只输出 JSON。
不确定时：保留 evidence_span，并标记 confidence=low。

## 4. STATUS.md
- 当前工作焦点：
- 推荐顺序：
- 昨日待固化结论：
- 昨日待固化方法：
- 当前思考层级：
- 当前项目阶段：
- 当前版本：
- 当前最优结果：
- 最大阻塞：
- 下一步：
- 最近巡检：
- 最近记忆压缩：
- 是否存在未验证改动：

示例：
当前思考层级：项目启动规划。
阶段：刚初始化，还没有 baseline。
阻塞：缺少代表性样例和验收指标。
最近巡检：未执行。
最近记忆压缩：未执行。
```

## STATUS.md

```markdown
# 项目状态

## 当前工作焦点
- 主线：
- 推荐顺序：
- 当前阶段：
- 正在处理的问题：
- 本轮不做：
- 最近焦点变化：
- 焦点来源：
- 待用户确认：

## 新日固化
- 昨日有效结论：
- 昨日有效方法：
- 建议固化位置：
- 不确定需确认：
- 最近固化日期：

## 当前层级
- 当前思考层级：
- 当前盒子：
- 当前目标：
- 下一步需要决策：

## 业务与指标
- 任务定义版本：
- 主指标：
- 验收阈值：
- 待确认问题：

## 数据与 GT
- Schema 版本：
- 数据集版本：
- 数据切分版本：
- 已知 GT 问题：

## Skill 与 Workflow
- 生产 Skill：
- 生产 Workflow：
- 候选变体：
- Runtime 假设：

## 评估与迭代
- 当前 comparison group：
- 最新 baseline：
- 上一轮最佳数据：
- 当前最佳候选：
- 待处理 badcase 主题：
- 首次测试展示偏好确认：
- 测试结果展示偏好：

## 长期记忆
- 当前最优结果：
- 最近记忆压缩时间：
- 待归档历史结果：
- 待合并摘要：

## 巡检状态
- 最近巡检时间：
- 最近巡检结论：
- 未验证改动：
- 待确认标准：
- 待补报告或文档：

## 交接
- 已变更文件：
- 需要通知的其他盒子：
- 下次启动应读取：
```

## PROJECT_MEMORY.md

```markdown
# 项目长期记忆

本文件只保存当前仍有决策价值的压缩记忆。完整实验历史保存在 `experiments/CHANGELOG.md` 和各实验报告中。

## 当前有效结论
- 暂无。项目初始化后，阶段性结论形成时再写入。

## 当前最优结果
- 方案：暂无。
- 依据：暂无。
- 指标数据：暂无。
- 适用条件：暂无。
- 护栏风险：暂无。
- 来源：暂无。

## 已固化方法
| 时间 | 方法 | 适用条件 | 固化来源 | 维护位置 |
| --- | --- | --- | --- | --- |

## 待确认假设
- 暂无。

## 下一轮优先级
1. 暂无。

## 已归档历史结果
| 时间 | 结果或方案 | 归档原因 | 来源 | 是否可比较 |
| --- | --- | --- | --- | --- |

## 已合并摘要
| 合并时间 | 合并来源 | 当前摘要位置 | 备注 |
| --- | --- | --- | --- |
```

## EDIT_SCOPE.md

```markdown
# 编辑授权边界

## 匹配顺序
1. forbidden
2. confirm_required
3. always_allowed
4. generated_outputs
5. task_scoped
6. unmatched -> confirm_required

## always_allowed
| 模式 | 用途 | 备注 |
| --- | --- | --- |
| `STATUS.md` | 当前状态和交接 | 仅限短状态，不写长期历史 |
| `PROJECT_MEMORY.md` | 当前有效长期记忆 | 改变当前最优/历史归档前仍需确认 |
| `docs/README.md` | 文档索引 | 不写长正文 |
| `docs/archive/**` | 文档归档 | 保留来源和归档原因 |
| `tmp/**` | 临时诊断产物 | 不作为正式结论 |

## generated_outputs
| 模式 | 用途 |
| --- | --- |
| `experiments/**/report.md` | 单次实验人工报告 |
| `experiments/**/report.json` | 单次实验结构化报告 |

## confirm_required
| 模式 | 原因 |
| --- | --- |
| `data/**` | 数据、GT 或样本可能影响评估 |
| `eval_kit/**` | 指标和评估口径 |
| `pipeline/**` | 生产流程 |
| `autokg_pipeline/**` | 业务/模型逻辑 |
| `tests/**` | 验证口径会影响结论可信度 |
| `experiments/CHANGELOG.md` | 实验历史和决策记录 |

## forbidden
| 模式 | 原因 |
| --- | --- |
| `.git/**` | Git 内部数据 |
| `.env` | 本地密钥 |
| `**/*secret*` | 潜在密钥 |

## task_scoped
| 时间 | 用户授权 | 模式 | 过期条件 |
| --- | --- | --- | --- |
```

## TASK_SPEC.md

```markdown
# 任务定义

## 目标

## 输入

## 输出

## 标签或 Schema 含义

## 主指标
- 名称：
- 版本：
- 公式或脚本：
- 验收阈值：

## 护栏指标
- 时延：
- 成本：
- 失败率：
- 关键类别召回：

## 测试结果展示偏好
- 首次测试前确认：否
- 默认候选字段：主指标、护栏指标、耗时、测试用例 ID、失败用例、典型 badcase、日志路径、报告路径、成本/token、模型/环境版本
- 用户确认字段：

## 非目标

## 版本历史
- task-v1：
```

## data/schema.yaml

```yaml
schema_id: schema-v1
task_spec_version: task-v1
entities: []
relations: []
fields:
  id:
    type: string
    required: true
  text:
    type: string
    required: true
annotation_rules:
  boundary_policy: 待填写
  conflict_policy: 待填写
```

## grid.yaml

```yaml
comparison_group: round-YYYY-MM-DD-01
factors:
  skill: [skill-v1-baseline, skill-v2-fewshot]
  data: [gt-v2.0, gt-v2.1]
  workflow: [flow-default, flow-filter]
controlled:
  task_spec_version: task-v1
  schema_version: schema-v1
  split_version: split-dev-v1
  metric_version: metric-v1
  model: gpt-4.1
  temperature: 0.1
exclude:
  - {skill: skill-v1-baseline, workflow: flow-filter}
```

## report.md

```markdown
# 实验：<experiment_id>

## 状态
- 结果：
- Comparison group：

## 测试范围
- 测试用例 ID：
- 样本/切分：

## 运行信息
- 耗时：
- 日志路径：
- 报告路径：

## 版本
- 任务定义：
- Schema：
- 数据集：
- 数据切分：
- Skill：
- Workflow：
- 指标：

## 指标
| 指标 | 数值 | 目标/验收线 | 是否达标 |
| --- | ---: | ---: | --- |
| 主指标 |  |  |  |
| 精确率 |  |  |  |
| 召回率 |  |  |  |
| 成本 |  |  |  |
| 时延 |  |  |  |
| 失败率 |  |  |  |

## 达标判断
- 结论：
- 未达标项：
- 与目标差距：

## 存在的问题
1.

## Badcase
1. 

## 可能原因
1.

## 备注

## 决策建议
```

## experiments/CHANGELOG.md 条目

```markdown
## YYYY-MM-DD Round <id>

### 意图

### 实验网格
- 变化因素：
- 控制因素：
- 排除组合：

### 结果
- 最佳实验：
- Baseline：
- 上一轮最佳对照：
- 主效应：
- 交互效应备注：
- 护栏指标备注：

### 决策
- 晋升：
- 暂缓：
- 排查：

### 下一轮 Grid
- 对照基线：
```
