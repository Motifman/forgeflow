# forgeflow

`forgeflow` は、Codex と Cursor の両方で使う実装ワークフローを単一の正本として管理するための repository です。

目的は 2 つです。

- workflow 定義を project repository から分離し、ワークツリーやブランチに依存しない形で運用する
- Codex と Cursor の両方に同じ workflow を配布しつつ、runtime artifact は各 project に生成する

## 構成

```text
forgeflow/
  README.md
  shared/
    templates/
    references/
    runtime/
  targets/
    codex/
      skills/
    cursor/
      skills/
  scripts/
    forgeflow.py
    install_codex.sh
    export_cursor_skills.sh
    bootstrap_project.sh
```

## 役割分担

### この repo に置くもの

- workflow の説明
- skill 定義
- template
- reference
- install / export / setup script

### 各 project に生成するもの

- `.ai-workflow/ideas/`
- `.ai-workflow/features/`
- `.ai-workflow/README.md`
- 実際の `IDEA.md`, `PLAN.md`, `PROGRESS.md`, `REVIEW.md`, `SUMMARY.md`

## インストール方針

### Codex

- `install_codex.sh` で global skill を symlink install する
- 同時に `forgeflow` CLI を `~/.local/bin/forgeflow` に置く

### Cursor

- Cursor には Codex と同等の global skill directory は前提にしない
- `export_cursor_skills.sh` で project の `.cursor/skills/` へ同期する
- 同じく `forgeflow` CLI を使って project bootstrap を行う

## セットアップ

### 1. forgeflow repo を clone する

```bash
git clone <your-forgeflow-repo>
cd forgeflow
```

### 2. Codex に global install する

```bash
./scripts/install_codex.sh
```

### 3. project を bootstrap する

```bash
forgeflow setup-project --project /path/to/project
```

Cursor でもすぐ使いたい場合:

```bash
forgeflow setup-project --project /path/to/project --export-cursor
```

または:

```bash
./scripts/bootstrap_project.sh /path/to/project
```

## 代表コマンド

```bash
python forgeflow/scripts/forgeflow.py setup-project --project /path/to/project
python forgeflow/scripts/forgeflow.py setup-project --project /path/to/project --export-cursor
python forgeflow/scripts/forgeflow.py new-idea --project /path/to/project --slug guild-market
python forgeflow/scripts/forgeflow.py init-feature --project /path/to/project --slug guild-market
python forgeflow/scripts/forgeflow.py status --project /path/to/project --slug guild-market
python forgeflow/scripts/forgeflow.py doctor --project /path/to/project --slug guild-market
```

## 設計メモ

- static workflow definition と runtime artifact は分ける
- 質問ループと alignment loop は skill 側の責務
- project 側 `.ai-workflow` は成果物置き場として保つ
- CLI は project をまたいで再利用できるよう、共有 template を repo 内から読む
- Cursor は project ごと export、Codex は global install という非対称モデルを採る
