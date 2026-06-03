# AI 算法研发管家型 Skill 四盒接口契约

当需要创建、审计或修复算法研发项目的四盒接口时，读取本参考。目标不是只服务实验归因，而是让个人在不同项目、不同思考层级之间切换时，有一套可复用、可检查、可交接的管家型接口框架。跨盒依赖越显式，越不需要每个项目重新规划，也越不容易遗漏关键步骤。

## 契约原则

- 每个持久 artifact 必须只有一个归属盒子。
- 每个跨盒 artifact 必须包含 `id`、`version`、`owner`、`status` 和 `updated_at`。
- 下游盒子通过稳定 ID 和版本导入 artifact，不使用 `latest` 这类模糊名称。
- 报告采用双格式：`report.json` 用于聚合分析，`report.md` 用于人工阅读。
- 只有当比较键明确声明哪些字段被控制、哪些字段在变化时，实验比较才有效。
- 决策是独立于指标的 artifact。好分数可以支持决策，但不能替代决策。
- 接口契约本身也是个人工作流的记忆装置：它记录“进入这一层时应该看什么、改什么、交付什么”。

## 盒子接口

| 盒子 | 拥有 | 导入 | 导出 | 验证门 |
| --- | --- | --- | --- | --- |
| 业务与指标 | `TASK_SPEC.md`、指标定义、验收阈值 | 业务背景、负责人决策 | `task_spec_version`、`metric_version`、验收门槛 | 指标可测试，并且同一轮比较中不被暗改 |
| 数据与 GT | `data/schema.yaml`、`data/README.md`、`data/versions/*`、split manifest | 任务定义、指标对数据的要求 | `schema_version`、`dataset_version`、`split_version`、标注说明 | Schema 和 GT 通过一致性检查 |
| Skill 与 Workflow | `pipeline/*`、`variants/skills/*`、`variants/workflows/*`、模型设置 | 任务定义、Schema、数据契约 | `skill_version`、`workflow_version`、可运行配置 | 配置能解析到真实文件，并与 Schema 兼容 |
| 评估与迭代 | `grid.yaml`、`experiments/*`、`report.json`、`report.md`、`experiments/CHANGELOG.md` | 所有被固定的版本字段 | 排名结果、效应分析、决策、下一轮 grid | 报告符合 Schema，且所有实验声明版本 |

## 必需 Artifact ID

使用稳定、简短、文件系统安全的 ID：

- 任务定义：`task-relation-extraction-v1`
- Schema：`schema-v1`
- 数据集：`gt-v2.1`
- 数据切分：`split-dev-v1`
- Skill：`skill-v3-schema-enhance`
- Workflow：`flow-filter-v1`
- Metric：`metric-entity-f1-v1`
- Experiment：`exp_skill-v3-schema-enhance_data-gt-v21_flow-filter-v1`
- Summary：`summary-2026-05-30-round-01`

## Manifest 最小字段

存在变体时，创建或更新 `variants/manifest.yaml`。

```yaml
skills:
  skill-v1-baseline:
    path: variants/skills/v1_baseline.txt
    status: active
    owner_box: skill_workflow
    created_from: pipeline/skill_prompt.txt
    notes: 生产版基线提示词。
data:
  gt-v2.1:
    path: data/versions/gt_v2.1.jsonl
    schema_version: schema-v1
    split_version: split-dev-v1
    status: active
workflows:
  flow-filter-v1:
    path: variants/workflows/flow_filter.yaml
    status: active
    compatible_schema: [schema-v1]
metrics:
  metric-entity-f1-v1:
    path: utils/metrics.py
    primary: entity_micro_f1
```

## 实验配置契约

每个实验目录都应该包含生成的 `config.yaml`。实验开始后，该文件应保持不可变。

```yaml
experiment_id: exp_skill-v3_data-gt-v21_flow-filter
created_at: 2026-05-30T00:00:00Z
comparison_group: round-2026-05-30-01
varying_factors:
  skill: skill-v3-schema-enhance
  data: gt-v2.1
  workflow: flow-filter-v1
controlled_factors:
  task_spec_version: task-re-v1
  schema_version: schema-v1
  split_version: split-dev-v1
  metric_version: metric-entity-f1-v1
runtime:
  model: gpt-4.1
  temperature: 0.1
  seed: 42
paths:
  prompt_file: variants/skills/v3_schema_enhance.txt
  data_file: data/versions/gt_v2.1.jsonl
  workflow_file: variants/workflows/flow_filter.yaml
  output_dir: experiments/exp_skill-v3_data-gt-v21_flow-filter
```

## Report JSON 契约

`report.json` 是聚合分析的来源。保持格式朴素、可解析。

```json
{
  "experiment_id": "exp_skill-v3_data-gt-v21_flow-filter",
  "status": "completed",
  "comparison_group": "round-2026-05-30-01",
  "versions": {
    "task_spec": "task-re-v1",
    "schema": "schema-v1",
    "dataset": "gt-v2.1",
    "split": "split-dev-v1",
    "skill": "skill-v3-schema-enhance",
    "workflow": "flow-filter-v1",
    "metrics": "metric-entity-f1-v1"
  },
  "runtime": {
    "model": "gpt-4.1",
    "temperature": 0.1,
    "seed": 42
  },
  "metrics": {
    "primary": "entity_micro_f1",
    "entity_micro_f1": 0.85,
    "precision": 0.81,
    "recall": 0.90
  },
  "badcases": [
    {
      "id": "case-001",
      "type": "boundary_error",
      "summary": "LOC 边界漏掉区县后缀。"
    }
  ],
  "notes": "Skill 增加了 Schema 相关 few-shot 示例。"
}
```

## 验证门

生成 grid 前：

- 所有被引用的变体 ID 都存在于 `variants/manifest.yaml`。
- 所有数据变体都声明了兼容的 `schema_version`。
- 所有 Workflow 都声明了兼容 Schema 或必需字段。
- 除非 metric 本身是本轮变量，否则整个 comparison group 固定同一 `metric_version`。
- 无效组合必须通过 include/exclude 规则显式声明。

汇总前：

- 所有 completed 实验都有 `report.json`。
- failed 和 invalid run 与 missing run 分开统计。
- 主指标存在，并且在被比较实验中定义一致。
- 数据切分和 GT 版本差异被标为数据因素，而不是隐藏噪声。
- Runtime 差异要么被控制，要么被显式视为实验因素。

晋升前：

- 胜出组合在主指标上超过 baseline，并且护栏指标没有超出容忍范围。
- Badcase 没有暴露业务不可接受的回归。
- 被晋升的 artifact 已复制或引用到稳定的 `pipeline/` 路径。
- `STATUS.md` 和 `experiments/CHANGELOG.md` 记录晋升原因。

方案迭代后：

- 主动询问用户是否跑一遍测试或评估；如果已有明确授权和测试命令，可以直接运行。
- 项目第一次测试或评估前，先询问用户希望测试完成后展示哪些字段，例如指标、耗时、测试用例 ID、失败用例、badcase、日志/报告路径、成本/token 和环境版本，并把确认结果写入 `TASK_SPEC.md` 或 `STATUS.md`。
- 测试前说明本轮改动、建议测试范围、主指标、护栏指标和预期产出。
- 测试后先按用户确认的展示字段输出，再对照 `TASK_SPEC.md` 的验收线判断是否达标。
- 若不达标，输出当轮指标、目标阈值、差距、存在的问题、典型 badcase、可能原因和下一轮候选方案。
- 若用户选择不测试或当前无法测试，把“未验证”及原因写入 `STATUS.md` 或本轮交接记录。

## 常见缺口

- 补充 `report.json`；只有 Markdown 报告很难安全聚合。
- 补充 manifest；实验变多后，文件夹名会变得不可靠。
- 固定 metric、split、schema、model、seed 和 runtime 版本；否则“同一实验”并不真的相同。
- 分离 GT 质量变化和 Skill 变化；数据修正可能让分数上升或下降，但这不等于模型能力变化。
- 为坏实验增加 invalid 状态，不要直接编辑 completed 输出。
- 增加晋升和回滚记录，让“最佳实验”能安全进入生产配置。
- 需要判断交互效应时使用平衡网格；如果是稀疏网格，就把结论降级为假设。
- Workflow 增加步骤时，记录成本、时延和失败率等护栏指标。
