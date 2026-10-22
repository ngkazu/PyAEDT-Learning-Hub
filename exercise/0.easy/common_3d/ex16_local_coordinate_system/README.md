# 演習16: ローカル座標系を作る（create_coordinate_system→set_working_coordinate_system）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/maxwell_3d/ex02_asymmetric_conductor/` で使う
`modeler.create_coordinate_system()`の基本操作だけを切り出して練習する演習。

## アプリケーションの選び方

このフォルダの課題は、3Dモデラー系アプリ（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）に共通する
基本操作を学ぶ。使いたいアプリケーションのクラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照し、`starter.py` 冒頭の import とアプリ生成部分を書き換える。

## 学習目標

- `modeler.create_coordinate_system()` で、グローバル座標系とは別の原点を持つローカル座標系を作成する
- `modeler.set_working_coordinate_system()` で、形状作成の基準となる作業座標系を切り替える
- ローカル座標系上で作成した形状の原点が、グローバル座標系から見てどこに位置するかを理解する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 好きな3Dモデラー系アプリケーションを起動する。
2. `modeler.create_coordinate_system(origin=[10, 10, 10], reference_cs="Global", name="MyCS")` で、
   グローバル座標系の原点から`[10, 10, 10]`だけ離れた位置にローカル座標系を作成する。
3. `modeler.set_working_coordinate_system("MyCS")` で、作業座標系をローカル座標系に切り替える。
4. `modeler.create_box(origin=[0, 0, 0], sizes=["10mm", "10mm", "10mm"], name="BoxOnLocalCS",
   material="aluminum")` で箱を作成する（指定する`origin=[0, 0, 0]`は、ローカル座標系`MyCS`上の
   位置であり、グローバル座標系で見ると`[10, 10, 10]`の位置になる）。
5. `modeler.set_working_coordinate_system("Global")` で、作業座標系をグローバルに戻す。
6. プロジェクトを保存し、アプリケーションを終了する。

## ヒント

- `create_coordinate_system()`の`reference_cs`引数は「このローカル座標系が、どの座標系から見た
  相対位置・向きで定義されるか」を指定する。`"Global"`を指定すれば、グローバル座標系からの
  オフセットとして定義される。
- `set_working_coordinate_system()`を呼ばずに形状を作成すると、常にグローバル座標系基準で
  配置される。ローカル座標系を作っただけでは座標系は切り替わらない点に注意。
- 作業座標系を切り替えたままにしておくと、以降に作成する形状がすべて意図しない位置に
  配置されてしまう。形状作成が終わったら忘れずにグローバルへ戻す。

## 評価基準

- [ ] アプリケーションが起動し、ローカル座標系`MyCS`が作成されている
- [ ] 作業座標系がローカル座標系に切り替わった状態で箱が作成されている
- [ ] 作業座標系がグローバルに戻されている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `mode="view"`や`mode="axisrotation"`など、他の座標系定義モードを調べて、向きを回転させた
  ローカル座標系を作成してみてください。
- 実際にTEAM7問題のコイル形状作成で使われている様子を見たい場合は、
  [1.normal/maxwell_3d/ex02_asymmetric_conductor/](../../../1.normal/maxwell_3d/ex02_asymmetric_conductor/)
  に進んでみてください。
