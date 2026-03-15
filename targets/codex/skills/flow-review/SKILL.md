---
name: "flow-review"
description: "DDD・例外処理・仮実装禁止・テスト厳密性の観点で feature を厳しくレビューし、結果を REVIEW.md に残す"
---

# Flow Review

feature の変更全体を見直し、実装の後回し、仮置き、テスト不足、DDD 逸脱を検出する。

- `PLAN.md` と `PROGRESS.md` を読み、実装意図を把握する
- 実装ファイルと対応テストをレビューする
- DDD 境界、例外処理、仮実装の有無、テストの厳しさを点検する
- findings を severity 順に `REVIEW.md` に残す
- 本質的な gap があれば phase 追加か差し戻しを判断する
