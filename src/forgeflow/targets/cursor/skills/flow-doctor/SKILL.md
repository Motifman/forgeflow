---
name: flow-doctor
description: artifact 不足や plan 構造不足など、flow-* ワークフローの抜け漏れを検知する。
---

# Flow Doctor

1. `forgeflow doctor [--slug <slug>]` を実行する
2. fail している箇所を列挙する
3. 各 fail に対する修復アクションを案内する
4. stage gate 違反があれば、次 skill に進まず先に修復する
