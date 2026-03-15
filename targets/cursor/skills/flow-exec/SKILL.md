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
6. findings、plan updates、goal check、next-phase impact を artifact に反映する
7. phase ごとにコミットする
