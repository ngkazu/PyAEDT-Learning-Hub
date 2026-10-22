# 演習13: カスタム材料を作る（add_material→conductivity/permeability設定）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/maxwell_3d/ex02_asymmetric_conductor/`（`team7_aluminium`）や
`1.normal/maxwell_3d/ex03_coil_core/`（`core_steel`）で使う`materials.add_material()`の基本操作だけを
切り出して練習する演習。

## アプリケーションの選び方

このフォルダの課題は、3Dモデラー系アプリ（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）に共通する
基本操作を学ぶ。使いたいアプリケーションのクラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照し、`starter.py` 冒頭の import とアプリ生成部分を書き換える。

## 学習目標

- `materials.add_material()` で、既存ライブラリにない新しい材料を定義する
- 作成した材料オブジェクトの `conductivity`（導電率）・`permeability.value`（比透磁率）を設定する
- カスタム材料を形状の `material` 引数に割り当てる

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 好きな3Dモデラー系アプリケーションを起動する。
2. `materials.add_material(name="my_custom_material")` でカスタム材料を追加する。
3. 追加した材料オブジェクトの `conductivity = 3.526e7`、`permeability.value = 1000` を設定する。
4. `modeler.create_box(origin=[0, 0, 0], sizes=["10mm", "10mm", "10mm"], name="MyBox",
   material=my_material.name)` で、作成した材料を割り当てた箱を作成する。
5. プロジェクトを保存し、アプリケーションを終了する。

## ヒント

- `add_material()` の戻り値（材料オブジェクト）のプロパティに直接代入する形でパラメータを設定する
  （`材料名.conductivity = 値` のように）。`material=` 引数には材料名の文字列（`.name`）を渡す。
- `permeability.value` は比透磁率（真空に対する相対値）。非磁性材料なら `1`、強磁性体なら
  数百〜数千程度の値を設定する。
- 既存ライブラリ材料（`"copper"`や`"ferrite"`など）をそのまま使うのではなく、独自の数値で
  材料特性を定義したいときに使うパターン。

## 評価基準

- [ ] アプリケーションが起動し、カスタム材料が追加されている
- [ ] 材料の導電率・比透磁率が設定されている
- [ ] 箱が作成され、カスタム材料が割り当てられている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `conductivity`/`permeability.value`の値を変えて、材料ライブラリ上でどう表示されるか確認してください。
- 実際にMaxwell 3Dの解析で使ってみたい場合は、
  [1.normal/maxwell_3d/ex02_asymmetric_conductor/](../../../1.normal/maxwell_3d/ex02_asymmetric_conductor/) や
  [1.normal/maxwell_3d/ex03_coil_core/](../../../1.normal/maxwell_3d/ex03_coil_core/) に進んでみてください。
