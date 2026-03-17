# Review Standard

`flow-review` では、以下を最低ラインとして確認する。

- blocking issue だけでなく、ship を止めない改善余地や残留リスクも拾う
- レビューは「問題があるか」だけでなく「何に気づいたか」を多めに残す
- `Ship ready: yes` は「これ以上何も改善できない」ではなく「blocking な懸念がない」を意味する
- minor な改善は、今ここで直す候補と defer してよい候補を分けて扱う

## 実装

- DDD の責務境界が崩れていない
- 継承や interface 利用が既存パターンと整合している
- 例外処理が十分で、握りつぶしや曖昧な失敗がない
- temporary implementation や placeholder がない
- TODO や「あとで対応」が実質的な未実装になっていない

## テスト

- 正常系だけでなく、異常系と境界ケースも見る
- 対応する実装変更に対して十分なテストがある
- 既存の厳しいテスト群と比べて明らかに甘くなっていない
- 例外ケースや validation failure を取りこぼしていない

## 出力

- findings を先に出す
- 可能なら対象ファイル、挙動、影響、推奨アクションを書く
- 問題がなければその旨を明言する
- 問題がなくても、気づいた改善余地や review note を残してよい
- 残留リスクや testing gap があれば併記する
- minor な改善は `Apply-now polish` と `Deferred polish` に分ける
- release gate として `Ship ready: yes/no` を明記する
