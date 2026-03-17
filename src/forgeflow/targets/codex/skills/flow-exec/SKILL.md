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
6. phase 完了時に plan revision check を行い、将来 phase の見直し要否を判定する
7. plan revision check で見直しが必要なら、以降の phase 修正や新 phase 追加の前に user の許可を取る
8. user が許可した場合だけ `PLAN.md` の future phase と change log を更新し、plan 変更が発生した場合はその差分をコミットする
9. `PROGRESS.md` に開始時刻、完了時刻、テスト、findings、plan revision check、user approval、plan updates、goal check、scope delta、handoff summary、next-phase impact、commit を残す
10. phase 実装を phase 単位でコミットする
</process>

<feedback_loop>
- phase 完了時に、内部モデルの更新を artifact へ外在化する
- 「何を学んだか」「次 phase の前提がどう変わったか」を必ず書く
- 実装の都合で全体目的からずれていないかを見直す
- 次のどれかに当てはまるなら plan revision が必要:
  - 新しい発見により、全体 objective を満たすための必須作業が既存 future phase に入っていない
  - success criteria が不十分、観測不能、または誤っていると分かった
  - phase の依存や順序前提が壊れ、後続 phase の並び替えや分割が必要になった
  - 既存の scope contract では吸収できない必須の設計変更、例外処理、移行、検証作業が出た
  - コスト、リスク、影響範囲が大きく変わり、user の期待値調整なしに進めるのが危険になった
- plan revision が不要なら、その理由を artifact に明記する
- success criteria 崩壊、コスト急増、phase 順序変更が必要な場合は alignment を再開する
</feedback_loop>
