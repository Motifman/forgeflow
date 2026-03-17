---
name: "flow-ship"
description: "review 済み feature の出荷準備を整え、SUMMARY.md と最終 git 動線をまとめる"
---

# Flow Ship

- review 完了と test evidence を確認する
- `SUMMARY.md` に outcome、delivered、remaining work、evidence を書く
- PR か main 直 merge かを整理する
- `REVIEW.md` に apply-now minor polish が残っている場合は、そのまま見送らず短い polishing loop を回してよい
- polishing loop を回した場合は、修正、再確認、artifact 更新まで行い、`SUMMARY.md` の evidence と remaining work に反映する
- 未解決事項があれば隠さず残す
- `REVIEW.md` が `Ship ready: yes` でない場合は出荷扱いにしない
