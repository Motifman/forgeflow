# AI Workflow Artifacts

このディレクトリは `forgeflow` により生成・管理される runtime artifact 置き場です。

ここには workflow 定義そのものではなく、各 project で実際に作られた成果物を置きます。

## 置くもの

- `ideas/`
  - 日付付きのアイデアメモ
- `features/`
  - feature ごとの `IDEA.md`, `PLAN.md`, `PROGRESS.md`, `REVIEW.md`, `SUMMARY.md`
- `MANAGED_BY_FORGEFLOW`
  - forgeflow が runtime を初期化した印

## 置かないもの

- global skill 定義
- 共通 template
- 共通 reference

それらは `forgeflow` repository 側で管理する。

## 運用メモ

- artifact は narrative ではなく、意思決定の証跡として扱う
- `proposal`、`selected option`、`assumptions`、`reopen alignment if` を埋める
- review artifact では blocker だけでなく、minor な気づきや polish 候補も残す
- ship artifact では review 後に適用した polish と defer した polish を区別して残す
- `forgeflow doctor` は空欄や stage gate 違反を workflow defect として扱う
