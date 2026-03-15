---
name: "flow-status"
description: "flow-* ワークフロー上で feature の現在地を要約し、次の具体的アクションを案内する"
---

# Flow Status

- `forgeflow status [--slug <slug>]` を実行する
- artifact ベースで現在地を短く要約する
- 次の最小アクションを案内する
- `forgeflow doctor` が fail なら、その修復を最小アクションとして優先する
