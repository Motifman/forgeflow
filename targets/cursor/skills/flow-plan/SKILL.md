---
name: flow-plan
description: アイデアを feature に昇格し、関連コード調査・phase 分割・成功条件整理を行って実装計画を作る。
---

# Flow Plan

1. 対応する idea artifact を読む
2. `forgeflow init-feature --slug <slug>` で feature 骨組みを作る
3. 既存コード、例外、イベント、テスト、再利用パターンを調査する
4. 暫定の phase 案を作る
5. 少なくとも 1 回は alignment loop を回し、phase 順序、重い実装を含めるか、成功条件を確認する
6. 各 phase の scope、依存、成功条件、懸念点を `PLAN.md` に書く
