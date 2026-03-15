---
name: "flow-exec"
description: "feature の現在 phase を実装し、テスト・artifact 更新・phase 単位コミットまで行う"
---

# Flow Exec

<objective>
`PLAN.md` の現在 phase を、既存コードに自然に溶け込む品質で実装する。
</objective>

<context>
- runtime artifact: `.ai-workflow/features/<slug>/PLAN.md`
- runtime artifact: `.ai-workflow/features/<slug>/PROGRESS.md`
</context>

<process>
1. feature の `PLAN.md` と `PROGRESS.md` を読み、現在 phase を特定する
2. 関連コード、既存テスト、既存の例外やイベントの形式を再確認する
3. 現在 phase の scope だけを実装する
4. 関連テストを追加または更新し、必要なテストを実行する
5. 実装中に得た観測情報を列挙し、元の plan 想定と何がズレたかを整理する
6. 全体目的と success criteria を見直し、その差分を `PLAN.md` に反映する
7. `PROGRESS.md` に開始時刻、完了時刻、テスト、findings、plan updates、goal check、next-phase impact、commit を残す
8. phase 単位でコミットする
</process>

<feedback_loop>
- phase 完了時に、内部モデルの更新を artifact へ外在化する
- 「何を学んだか」「次 phase の前提がどう変わったか」を必ず書く
- 実装の都合で全体目的からずれていないかを見直す
</feedback_loop>
