# forgeflow

Portable agent workflow tooling for Codex and Cursor.
Codex / Cursor 向けの再現可能な開発ワークフローを、どのプロジェクトにもすぐ入れられる形で配布するためのツールです。

## What It Is / これは何か

`forgeflow` keeps two things separate:

- Static workflow definition
- Per-project runtime artifacts

つまり、このリポジトリが持つのは workflow 本体です。各 project 側には `.ai-workflow/` だけを生成し、そこで意思決定と進捗を追跡します。

This separation is the core design:

- Reproducibility: every project uses the same skill set
- Speed: agents do not need to reinvent the workflow each time
- Traceability: intent, plan, execution deltas, and review results remain in artifacts

## Quickstart / クイックスタート

### 1. Install with `uv`

GitHub から clone せずにそのまま install できます。

```bash
uv tool install git+https://github.com/Motifman/forgeflow.git
```

更新する場合:

```bash
uv tool upgrade forgeflow
```

すでに install 済みの利用者が workflow 更新を確実に反映するには:

```bash
uv tool upgrade forgeflow
forgeflow install-skills --target codex --scope global -U
```

Cursor 向け skill を project local に入れている場合は、対象 project で更新します。

```bash
cd /path/to/your-project
forgeflow install-skills --target cursor --scope project --project . -U
```

ローカル clone から使う開発時は、こちらでも install できます。

```bash
uv tool install --from /path/to/forgeflow forgeflow
```

### 2. Install skills

```bash
forgeflow install-skills --target codex --scope global -U
```

Examples:

- Codex global: `forgeflow install-skills --target codex --scope global -U`
- Codex project local: `forgeflow install-skills --target codex --scope project --project . -U`
- Cursor global: `forgeflow install-skills --target cursor --scope global -U`
- Cursor project local: `forgeflow install-skills --target cursor --scope project --project . -U`

Default recommendation:

- Codex は global install
- Cursor は project local install

`-U` / `--upgrade` は既存の forgeflow skill を更新します。`.ai-workflow/` の runtime artifact は消しません。

### 3. Bootstrap a project

```bash
cd /path/to/your-project
forgeflow setup-project --project . --install-cursor-skills -U
```

This creates:

- `.ai-workflow/ideas/`
- `.ai-workflow/features/`
- `.ai-workflow/README.md`
- `.cursor/skills/` when `--install-cursor-skills` is enabled

## Core Commands / 主要コマンド

```bash
forgeflow install-skills --target codex --scope global -U
forgeflow setup-project --project . --install-cursor-skills -U
forgeflow install-skills --target cursor --scope project --project . -U
forgeflow new-idea --project . --slug guild-market
forgeflow init-feature --project . --slug guild-market
forgeflow status --project . --slug guild-market
forgeflow doctor --project . --slug guild-market
forgeflow version
```

## Workflow / ワークフロー

The default lifecycle is:

1. `flow-idea`
2. `flow-plan`
3. `flow-exec`
4. `flow-review`
5. `flow-ship`

### `flow-idea`

Turns a rough idea into a concrete implementation candidate.
雑な要望を、後で実装計画に昇格できる粒度まで具体化します。

### `flow-plan`

Creates a phase-based plan with explicit scope, success criteria, and alignment checkpoints.
phase 分割された計画を作り、scope と成功条件を固定します。

### `flow-exec`

Implements only the current phase, updates artifacts, and records what changed.
今の phase だけを実装し、学習した差分を artifact に戻します。

At phase end, `flow-exec` must also run a plan revision check.
新しい発見が全体目的の達成経路を変える場合は、後続 phase の修正や新 phase 追加が必要かを判定します。
必要な場合は user の許可を取ってから `PLAN.md` を更新し、plan 変更が発生したらその差分をコミットします。

Plan revision is required when one of these is true:

- newly discovered mandatory work is missing from future phases
- success criteria are no longer sufficient or observable
- phase ordering or dependency assumptions broke
- required design, migration, exception, or verification work no longer fits the current plan
- cost, risk, or impact changed enough that silent continuation would be unsafe

### `flow-review`

Checks implementation quality, testing rigor, and release readiness.
実装品質、テスト品質、出荷可否を確認します。

### `flow-ship`

Summarizes what shipped and how it is ready to land.
最終成果と merge / PR 動線を明示します。

## Glossary / 用語

### Static workflow definition

Shared files in this repository:

- skill definitions
- templates
- references
- install/export logic

### Runtime artifacts

Files created inside each target project under `.ai-workflow/`:

- idea notes
- feature plans
- progress journals
- review results
- ship summaries

### Alignment loop

A short decision loop to reduce drift between:

- what the human wants to build
- what the agent currently predicts it should build

`forgeflow` is optimized around this problem. 目的は会話を増やすことではなく、ズレを早く露出して修正することです。

## Workflow Design Principles / 設計原則

### 1. Reproducibility first

A good run should be easy to repeat with another agent or another session.
同じ project なら、別セッションでも同じ流れを再現できることを優先します。

### 2. Speed through explicit decisions

Free-form notes are hard to validate. `forgeflow` pushes decisions into explicit fields such as:

- `Proposal`
- `Selected option`
- `Assumptions`
- `Reopen alignment if`

### 3. State-machine style gates

`forgeflow doctor` treats missing decisions and broken stage gates as workflow defects.
つまり「だいたい埋まっている」ではなく、「次に進んでよい条件を満たしているか」を見ます。

### 4. Execution may learn, but not drift silently

During implementation, the agent may discover new constraints. That is allowed.
ただし、scope delta や alignment 再開条件を artifact に残さない変更は許しません。

## Repository Layout / 構成

```text
forgeflow/
  README.md
  pyproject.toml
  src/forgeflow/
    __init__.py
    cli.py
    shared/
      references/
      runtime/
      templates/
    targets/
      codex/skills/
      cursor/skills/
  scripts/
    forgeflow.py
    install_skills.sh
    install_codex.sh
    export_cursor_skills.sh
    bootstrap_project.sh
```

## Packaging Notes / パッケージ管理メモ

`uv` is the primary install path.

- End users should prefer `uv tool install`
- Repo scripts remain as thin wrappers for local development
- The Python package under `src/forgeflow/` is the single source of truth for shared templates and skills

## Current Improvement Direction / 今後の改善軸

This repository should optimize for:

- faster intent alignment
- lower workflow variance between runs
- safer install and export behavior
- clearer onboarding for first-time users

直近では次が重要です。

- install / update / uninstall の lifecycle を CLI に寄せる
- README の first-run 体験をさらに短くする
- workflow gate を `doctor` でさらに厳密にする
- install banner / logo を最終導線に合わせて入れる
