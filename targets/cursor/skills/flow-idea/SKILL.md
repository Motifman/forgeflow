---
name: flow-idea
description: アイデアを対話と軽いコード調査で具体化し、.ai-workflow/ideas に日付付き Markdown として残す。
---

# Flow Idea

1. 関連するコードやテストを軽く調査する
2. 少なくとも 1 回は alignment loop を回し、「何を作りたいか」「何をもって成功か」「今回やらないことは何か」を聞く
3. コード調査で見えたコストや制約があれば、解釈のズレが起きそうな点として質問に入れる
4. 価値、制約、関連コード、未解決点を整理する
5. `forgeflow new-idea --slug <slug>` または同等の処理で idea artifact を残す
