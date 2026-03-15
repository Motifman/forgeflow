---
name: flow-review
description: DDD・例外処理・仮実装禁止・テスト厳密性の観点で feature を厳しくレビューし、結果を REVIEW.md に残す。
---

# Flow Review

1. `PLAN.md` と `PROGRESS.md` を読み、実装意図を把握する
2. 実装ファイルと対応テストをレビューする
3. DDD 境界、例外処理、仮実装の有無、テストの厳しさを点検する
4. findings を severity 順に `REVIEW.md` に残す
5. 本質的な gap があれば phase 追加か差し戻しを判断する
6. `Ship ready: yes/no` を明記する
