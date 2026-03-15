---
name: "flow-idea"
description: "アイデアを対話と軽いコード調査で具体化し、.ai-workflow/ideas に日付付き Markdown として残す"
---

# Flow Idea

<objective>
ユーザーの雑なアイデアを、後で計画に昇格できる実装候補まで具体化する。

この段階の目的は「今すぐ実装すること」ではなく、以下を明確にすること。

- 何を実現したいのか
- 現状のコードのどこが関係しそうか
- 何が未確定で、何を聞くべきか
- どの条件を満たせば planning に進めるか
</objective>

<context>
- `forgeflow setup-project` で project 側 `.ai-workflow/` を初期化してある前提
- runtime artifact: `.ai-workflow/ideas/`
- 補助 CLI: `forgeflow new-idea --slug <slug>`
</context>

<process>
1. ユーザーのアイデアを一文で言い換え、目的を取り違えていないか確認する
2. 関連しそうなコード、テスト、既存パターンを軽く調査する
3. 必ず 1 回は alignment loop を回し、「何を作りたいか」「何をもって成功か」「今回やらないことは何か」を聞く
4. コード調査で見えたコストや制約があれば、解釈のズレが起きそうな点として質問に織り込む
5. 回答を反映し、実装候補としての価値、制約、関連コード、未解決点を整理する
6. `.ai-workflow/ideas/` に日付付きの idea artifact を作成または更新する
7. planning に進める条件を明文化する
</process>

<interaction_rules>
- ユーザーがかなり具体的でも、idea では少なくとも 1 回は確認質問を行う
- 質問は自由作文ではなく、なるべく選択肢や比較の形にする
- 「こう理解している」「コード上はここが重そう」という暫定解釈を先に示してから聞く
- alignment loop の結果は `Success Signals`、`Non-Goals`、`Alignment Notes` に残す
</interaction_rules>

<guardrails>
- 明示的な依頼がない限り、この段階ではブランチを切らない
- scope が膨らんだら別 idea として分離する
- 会話だけで終わらせず、必ず artifact に残す
</guardrails>
