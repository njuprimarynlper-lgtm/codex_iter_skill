# Codex 安装说明：ai-engineering-workflow

## 包信息

- Skill 名称：`ai-engineering-workflow`
- 源目录：`D:\skill\ai-engineering-workflow`
- 压缩包：`D:\skill\ai-engineering-workflow.zip`
- 安装目标：`$CODEX_HOME\skills\ai-engineering-workflow`；如果未设置 `CODEX_HOME`，使用 `$HOME\.codex\skills\ai-engineering-workflow`
- 触发方式：在任务中提到 `$ai-engineering-workflow`、`AI 算法研发管家`、`AI 工程化工作流`、当前工作焦点、开工检查、下一步诊断、新日有效结论固化、主动巡检、长期记忆、项目启动规划、GT/data、workflow、评估指标、实验报告、四盒模型等。

## Codex 执行步骤

在 Windows PowerShell 中运行：

```powershell
$SkillName = "ai-engineering-workflow"
$Source = "D:\skill\ai-engineering-workflow"
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$DestRoot = Join-Path $CodexHome "skills"
$Dest = Join-Path $DestRoot $SkillName

if (!(Test-Path -LiteralPath $Source)) {
  throw "Skill source not found: $Source"
}

New-Item -ItemType Directory -Force -Path $DestRoot | Out-Null

if (Test-Path -LiteralPath $Dest) {
  $Backup = "$Dest.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
  Rename-Item -LiteralPath $Dest -NewName (Split-Path $Backup -Leaf)
}

Copy-Item -LiteralPath $Source -Destination $Dest -Recurse
```

## 压缩包安装方式

如果只有 zip 包，运行：

```powershell
$SkillName = "ai-engineering-workflow"
$Zip = "D:\skill\ai-engineering-workflow.zip"
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$DestRoot = Join-Path $CodexHome "skills"
$Dest = Join-Path $DestRoot $SkillName

if (!(Test-Path -LiteralPath $Zip)) {
  throw "Skill zip not found: $Zip"
}

New-Item -ItemType Directory -Force -Path $DestRoot | Out-Null

if (Test-Path -LiteralPath $Dest) {
  $Backup = "$Dest.backup-$(Get-Date -Format 'yyyyMMdd-HHmmss')"
  Rename-Item -LiteralPath $Dest -NewName (Split-Path $Backup -Leaf)
}

Expand-Archive -LiteralPath $Zip -DestinationPath $DestRoot
```

## 验证

安装后检查：

```powershell
$CodexHome = if ($env:CODEX_HOME) { $env:CODEX_HOME } else { Join-Path $HOME ".codex" }
$SkillDir = Join-Path $CodexHome "skills\ai-engineering-workflow"

Test-Path (Join-Path $SkillDir "SKILL.md")
Test-Path (Join-Path $SkillDir "agents\openai.yaml")
Test-Path (Join-Path $SkillDir "scripts\init_ai_workflow_project.py")
Test-Path (Join-Path $SkillDir "references\intake-guide.md")
Test-Path (Join-Path $SkillDir "references\interface-contracts.md")
Test-Path (Join-Path $SkillDir "references\protocols.md")
Test-Path (Join-Path $SkillDir "references\templates.md")
```

七项都应返回 `True`。

可选：如果要用 `skill-creator` 自带校验脚本验证中文 skill，请先开启 UTF-8：

```powershell
$env:PYTHONUTF8="1"
python "$HOME\.codex\skills\.system\skill-creator\scripts\quick_validate.py" $SkillDir
```

然后重启 Codex，让新 skill 进入可发现列表。重启后可以用下面这句话测试触发：

```text
使用 $ai-engineering-workflow 读取当前项目状态，先锚定当前工作焦点，再给出下一步诊断。
```

## 预期目录结构

```text
ai-engineering-workflow/
|-- SKILL.md
|-- agents/
|   `-- openai.yaml
|-- references/
|   |-- interface-contracts.md
|   |-- intake-guide.md
|   |-- protocols.md
|   `-- templates.md
`-- scripts/
    `-- init_ai_workflow_project.py
```

## 失败处理

- 如果 Codex 无法触发该 skill，确认安装目录是否为 `$CODEX_HOME\skills\ai-engineering-workflow` 或 `$HOME\.codex\skills\ai-engineering-workflow`。
- 如果 `SKILL.md` 中文显示乱码，确认文件按 UTF-8 读取。
- 如果已有旧版本，安装命令会先把旧目录改名为 `ai-engineering-workflow.backup-时间戳`，再复制新版本。
