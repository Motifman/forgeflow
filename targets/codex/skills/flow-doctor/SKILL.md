---
name: "flow-doctor"
description: "artifact 不足や plan 構造不足など、flow-* ワークフローの抜け漏れを検知する"
---

# Flow Doctor

- `forgeflow doctor [--slug <slug>]` を実行する
- fail している箇所を列挙する
- 各 fail に対する修復アクションを案内する

fail は任意ではなく workflow defect として扱う。
