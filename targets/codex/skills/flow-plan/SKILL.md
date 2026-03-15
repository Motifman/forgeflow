---
name: "flow-plan"
description: "アイデアを feature に昇格し、関連コード調査・phase 分割・成功条件整理を行って実装計画を作る"
---

# Flow Plan

<objective>
idea を、実装可能で追跡可能な feature plan に変換する。
</objective>

<context>
- `forgeflow setup-project` で project 側 `.ai-workflow/` を初期化してある前提
- runtime artifact: `.ai-workflow/features/<slug>/`
- 補助 CLI: `forgeflow init-feature --slug <slug>`
</context>

<process>
1. 対応する idea artifact がある場合は読む
2. feature 用ディレクトリを作成する
3. 関連モジュール、既存の実装パターン、既存テストを調査する
4. 再利用できる継承関係、例外、イベント、value object、repository 契約を洗い出す
5. 懸念点、未確定点、実装順序の制約を整理し、暫定の phase 案を作る
6. 必ず 1 回は alignment loop を回し、「この順序でよいか」「重い実装を含めるか」「何をもって成功とするか」をユーザーと合わせる
7. 反応を受けて phase 分け、成功条件、コスト感を修正する
8. 各 phase について scope、依存、成功条件を明文化する
9. 実装に入る準備が整ったら、専用ブランチに乗る前提を整える
</process>

<interaction_rules>
- draft plan を作ったら、そのまま確定せず一度ユーザーにぶつける
- 特にコストが重い箇所、順序に迷いがある箇所、成功条件が曖昧な箇所を質問対象にする
- 「コード上はここが重そう」「順序はこの方が安全そう」といった判断根拠を添える
- alignment loop の結果は `Alignment Loop` セクションに残す
</interaction_rules>
