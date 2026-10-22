# 演習2: TEAM7非対称導体（$B_z$ラインレポート）

**目安時間: 90分**

題材: [1.normal/maxwell_3d/ex02_asymmetric_conductor/](../../../1.normal/maxwell_3d/ex02_asymmetric_conductor/)
と同じモデル・Setupに、AEDT内部のポスト処理（Fields Calculator式・ラインレポート・フィールドプロット）を
追加する。

> この演習は「TEAM7非対称導体シリーズ」の hard レベル。normalの内容は
> [1.normal/maxwell_3d/ex02_asymmetric_conductor/](../../../1.normal/maxwell_3d/ex02_asymmetric_conductor/)
> を参照。さらに公開実測データと比較したものが
> [3.expert/maxwell_3d/ex02_asymmetric_conductor_benchmark/](../../../3.expert/maxwell_3d/ex02_asymmetric_conductor_benchmark/)
> にある。

> 非モデル（non_model）形状の作り方だけを練習したい場合は
> [0.easy/common_3d/ex17_non_model/](../../../0.easy/common_3d/ex17_non_model/) を先に確認するとよい。

## 学習目標

- `post.fields_calculator.add_expression()` で、磁束密度ベクトルからZ成分を取り出し位相評価する
  カスタム式（$B_z$、Gauss換算）を定義する（生のベクトル成分はCalculatorで式を登録しないと
  レポートの式として使えない点に注意）
- 評価用のライン（`create_polyline()`で2点を結んだだけの線）を板の上に作成し、Fields Calculator式の
  評価コンテキストとして使う
- `report_category="Fields"` で、ライン上の$|B_z|$分布をレポートとして作成する
- `setup.add_eddy_current_sweep()` で、既存のSetupに追加の周波数ポイントを足す方法を学ぶ
- `post.create_fieldplot_surface()` で、板表面のB磁束密度（`Mag_B`）のフィールドプロットを作成する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析・ポスト処理を完成させてください
（モデル作成部分はnormalと同じ内容です）。

1. normalと同じ手順でモデルを作成したうえで、セットアップ`"Setup1"`に
   `setup.add_eddy_current_sweep(sweep_type="SinglePoints", start_frequency=50, units="Hz",
   clear=True)` を追加し、200Hzに加えて50Hzでも解けるようにする。
2. 解析を実行する。
3. $B_z$（磁束密度Z成分、Gauss換算）を評価するFields Calculator式を定義し、
   `post.fields_calculator.add_expression(bz, None)` で登録する（式の内容は下記参照）。
4. 板の上に、評価用のライン`"Line_A1_B1"`・`"Line_A2_B2"`と、局所的なメッシュ細分化用の円柱を、
   どちらも`create_polyline(..., non_model=True)`で作成する。円柱には
   `set_crosssection_properties(section="Circle", width="2mm")` で断面を設定する。
5. 各ラインについて、`post.create_report(expressions="mag(Bz)", variations={"Distance": ["All"],
   "Freq": ["All"], "Phase": ["0deg"]}, primary_sweep_variable="Distance", report_category="Fields",
   context=line_name, plot_name=...)` でレポートを作成する。
6. `post.create_fieldplot_surface(assignment=plate.name, quantity="Mag_B", setup=f"{setup.name} :
   LastAdaptive", intrinsics={"Freq": "200Hz", "Phase": "0deg"}, plot_name="PlateMagB")` で、
   板表面のフィールドプロットを作成する。
7. プロジェクトを保存し、`m3d.release_desktop()` でAEDTを終了する。

## $B_z$計算式（Fields Calculator）

```python
bz = {
    "name": "Bz",
    "description": "Z component of B in Gauss",
    "design_type": ["Maxwell 3D"],
    "fields_type": ["Fields"],
    "primary_sweep": "Distance",
    "assignment": "",
    "assignment_type": ["Line"],
    "operations": [
        "NameOfExpression('<Bx,By,Bz>')",
        "Operation('ScalarZ')",
        "Scalar_Function(FuncValue='Phase')",
        "Operation('AtPhase')",
        "Scalar_Constant(10000)",
        "Operation('*')",
        "Operation('Smooth')",
    ],
    "report": ["Field_3D"],
}
```

## ヒント

- このラインと式は、TEAM7問題の公開実測データ（距離ごとの$B_z$測定値）と比較するために用意されている。
  2本のライン（`Line_A1_B1`、`Line_A2_B2`）は、板の表面上の異なる位置を通る。
- 評価用のラインとメッシュ細分化用の円柱はどちらも`non_model=True`を付けて作成する。
  どちらもソリッド・シートのような「解析対象のモデル形状」ではなく、
  レポート評価・メッシュヒント用の補助形状であることを明示するため。
- `"Bz"`のような生のベクトル成分は、`create_report()`の`expressions`に直接渡せる標準の量ではない
  （pyaedtのテスト・サンプルでも使われているのは`"Mag_B"`/`"Mag_E"`のような大きさ系の量のみ）。
  ベクトルの特定成分を取り出したい場合は、Fields Calculatorで式を明示的に登録する必要がある。
- `Scalar_Constant(10000)` による乗算は、Tesla単位の磁束密度をGauss単位に変換するため
  （$1\ \text{T} = 10000\ \text{Gauss}$）。
- ラインは2点を結ぶだけの単純な形状でよい（断面を持つ必要はない。メッシュ細分化用の円柱は
  ラインとは別オブジェクトとして重ねて作る）。

## 評価基準

- [ ] normalと同じモデル・励振・Region・渦電流設定がエラーなく解析完了している
- [ ] セットアップに50Hzのスイープ点が追加されている
- [ ] $B_z$のFields Calculator式が登録されている
- [ ] 2本の評価ラインが作成されている
- [ ] 各ラインに沿った$|B_z|$のレポートが作成されている
- [ ] 板表面のMag_Bフィールドプロットが作成されている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- 公開されているTEAM7の実測データとシミュレーション結果を比較したい場合は、このシリーズのexpert
  （[3.expert/maxwell_3d/ex02_asymmetric_conductor_benchmark/](../../../3.expert/maxwell_3d/ex02_asymmetric_conductor_benchmark/)）
  に進んでみてください。
