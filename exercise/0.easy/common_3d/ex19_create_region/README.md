# 演習19: 解析領域（Region）を作る（create_region）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/icepak/ex01_heatsink/` をはじめ、ほぼすべての
3D熱流体・電磁界解析課題で使う `modeler.create_region()` の基本操作だけを切り出して練習する演習。

## アプリケーションの選び方

このフォルダの課題は、3Dモデラー系アプリ（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）に共通する
基本操作を学ぶ。使いたいアプリケーションのクラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照し、`starter.py` 冒頭の import とアプリ生成部分を書き換える。

## 学習目標

- `modeler.create_region(pad_value, pad_type, name)` で、形状全体を囲む解析領域（Region）を
  作成する方法を学ぶ
- `pad_type="Percentage Offset"`（モデル全体のサイズに対する割合）と
  `"Absolute Offset"`（絶対値）の違いを理解する
- `pad_value`/`pad_type`はスカラー1つなら全6面に同じ値が適用され、6要素のリストで渡すと
  `[+X, -X, +Y, -Y, +Z, -Z]`の順に面ごとに異なる値を指定できることを知る
- Icepakでは、デザイン作成時に既定で`"Region"`オブジェクトが自動生成されていることを知り、
  作り直す場合は先に削除してから`create_region()`を呼ぶ必要があることを学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../docs/app-selection.md) から使いたいアプリケーションを選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動し、
   `modeler.model_units = "mm"` を設定する。
3. 対象の形状（`"MyBox"`）を `origin=[0, 0, 0]`, `sizes=[20, 20, 10]`, `material="copper"` で
   作成する。
4. Icepakでは既定で`"Region"`オブジェクトが自動生成されるため、
   `if "Region" in modeler.object_names: modeler["Region"].delete()` で、作り直す前に
   いったん削除する（他のアプリではこの手順は不要な場合がある）。
5. `create_region(pad_value=100, pad_type="Percentage Offset")` で、形状全体を囲む解析領域
   （`"Region"`）を、全方向100%のパーセントオフセットで作成する。
6. `modeler["Region"].bounding_box` でRegionのバウンディングボックスを取得する（確認用）。
7. プロジェクトを保存する。
8. `release_desktop()` でアプリケーションを終了する。

## ヒント

- `pad_type="Percentage Offset"`で`pad_value=100`を指定すると、各方向にモデル全体のサイズの
  100%分の余白が追加される（`"MyBox"`が20mm角なら、Regionは各方向に+20mmずつ広がる）。
- `pad_value`/`pad_type`は、面ごとに異なる値・種別を指定したい場合、どちらも6要素のリストで
  渡す（例: `pad_value=[10, 10, 10, 10, 20, 5]`, `pad_type="Absolute Offset"`）。並びは
  `[+X, -X, +Y, -Y, +Z, -Z]`。
- Icepakはソリューションの性質上、デザイン作成時点で既定の`"Region"`（空気領域）が自動生成
  されている。これに気づかず`create_region()`を呼ぶと、名前の衝突で作成が失敗する
  （エラーは出ず静かに失敗するため気づきにくい）。HFSS/Maxwell 3D/Q3D Extractorでは
  この既定Regionは生成されない。

## 評価基準

- [ ] 選んだアプリケーションが起動し、`modeler.model_units = "mm"` が設定されている
- [ ] `"MyBox"`という名前のBoxが作成されている
- [ ] `"Region"`という名前の解析領域が、`"MyBox"`を囲むサイズで作成されている
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- `pad_value`/`pad_type`を6要素のリストに変えて、面ごとに異なるパディング（例えば+Z方向だけ
  大きく余白を取る）を指定してみてください。
- `pad_type="Absolute Offset"`に変えて、`pad_value="10mm"`のような絶対値指定でRegionを
  作り直してみてください。
