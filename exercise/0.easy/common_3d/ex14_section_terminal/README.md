# 演習14: 断面を切ってターミナル面を作る（section→separate_bodies→delete）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/maxwell_3d/ex02_asymmetric_conductor/` や
`1.normal/maxwell_3d/ex03_coil_core/` で使う「ソリッド導体に電流励振を割り当てるためのターミナル面を作る」
定型パターンだけを切り出して練習する演習。

## アプリケーションの選び方

このフォルダの課題は、3Dモデラー系アプリ（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）に共通する
基本操作を学ぶ。使いたいアプリケーションのクラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照し、`starter.py` 冒頭の import とアプリ生成部分を書き換える。

## 学習目標

- `modeler.section()` で、3Dオブジェクトを平面で断面切断する
- 断面切断で生じた離れた2つの面を `modeler.separate_bodies()` で別オブジェクトに分離する
- 不要な片方を `modeler.delete()` で削除し、電流励振などに使う片側だけの面を残す

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 好きな3Dモデラー系アプリケーションを起動する。
2. 外円柱（`radius="20mm"`, `name="Ring"`）と内円柱（`radius="12mm"`, `name="Ring_hole"`）を作成し、
   `modeler.subtract(blank_list=["Ring"], tool_list=["Ring_hole"], keep_originals=False)` で
   円環（リング形状）にする。
3. `modeler.section(assignment="Ring", plane="ZX")` で、円環をZX平面で断面切断する。
4. `modeler.separate_bodies(["Ring_Section1"])` で、断面切断によって生じた離れた2枚の面
   （円環なので左右に分かれる）を、別々のオブジェクトに分離する。
5. `modeler.delete("Ring_Section1_Separate1")` で、分離によって生成された片方を削除し、
   `Ring_Section1`（片側だけ）を残す。
6. プロジェクトを保存し、アプリケーションを終了する。

## ヒント

- `section()` の `plane` 引数に使える正式な値は `"XY"`/`"YZ"`/`"ZX"` の3つ。
- 円環（閉じた輪）を1枚の平面で切ると、物理的に繋がっていない2つの面ができる。これを
  `separate_bodies()` で別オブジェクトに分けないと、片方だけを選んで電流を流すといった操作ができない。
- `separate_bodies()` で分離されたオブジェクトの名前は、元の名前に `_Separate1`、`_Separate2`...
  という連番が付く。

## 評価基準

- [ ] アプリケーションが起動し、円環（リング）が作成されている
- [ ] 円環がZX平面で断面切断されている
- [ ] 分離・削除の結果、片側だけの面（`Ring_Section1`）が残っている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- 残った片側の面に `assign_coil()`/`assign_current()` で電流励振を割り当て、実際に解析まで
  行いたい場合は、
  [1.normal/maxwell_3d/ex02_asymmetric_conductor/](../../../1.normal/maxwell_3d/ex02_asymmetric_conductor/) や
  [1.normal/maxwell_3d/ex03_coil_core/](../../../1.normal/maxwell_3d/ex03_coil_core/) に進んでみてください。
