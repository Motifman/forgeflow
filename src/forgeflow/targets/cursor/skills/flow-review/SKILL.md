---
name: flow-review
description: DDD・例外処理・仮実装禁止・テスト厳密性の観点で feature を厳しくレビューし、結果を REVIEW.md に残す。
---

# Flow Review

1. `PLAN.md` と `PROGRESS.md` を読み、実装意図を把握する
2. 実装ファイルと対応テストをレビューする
3. DDD 境界、例外処理、仮実装の有無、テストの厳しさを点検する
4. blocking issue だけでなく、non-blocking な気づき、改善余地、残留リスクも `REVIEW.md` に具体的に残す
5. findings は severity 順に並べ、可能なら対象ファイル、挙動、影響、推奨アクションを書く
6. `Ship ready: yes` にできる場合でも、minor な polish 候補を見つけたら省略せず残す
7. minor な改善は「今このまま直す候補」か「ship 後に回してよいもの」かを分けて書く
8. 本質的な gap があれば phase 追加か差し戻しを判断する
9. `Ship ready: yes/no` を明記する
