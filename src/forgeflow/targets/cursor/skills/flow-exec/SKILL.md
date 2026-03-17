---
name: flow-exec
description: feature の現在 phase を実装し、テスト・artifact 更新・phase 単位コミットまで行う。
---

# Flow Exec

1. `PLAN.md` と `PROGRESS.md` を読み、現在 phase を特定する
2. 関連コードと既存テストを再確認する
3. 現在 phase の scope だけを実装する
4. テストを追加または更新し、対象テストを実行する
5. 実装中の観測情報を整理し、元の plan 想定と何がズレたかを見る
6. phase 完了時に plan revision check を行い、future phase 見直しの要否を判定する
7. 見直しが必要なら、future phase 修正や新 phase 追加の前に user の許可を取る
8. user が許可した場合だけ `PLAN.md` を更新し、plan 変更が発生したらその差分をコミットする
9. findings、plan revision check、user approval、plan updates、goal check、scope delta、handoff summary、next-phase impact を artifact に反映する
10. phase ごとにコミットする

plan revision が必要な明確な基準:

- 新しい発見により、全体 goal 達成に必須な作業が既存 future phase に入っていない
- success criteria が不十分、観測不能、または誤っていると分かった
- phase の依存や順序前提が壊れ、後続 phase の並び替えや分割が必要になった
- 既存 scope では吸収できない必須の設計変更、例外処理、移行、検証作業が出た
- コスト、リスク、影響範囲が大きく変わり、user の再確認なしに進めるのが危険になった
