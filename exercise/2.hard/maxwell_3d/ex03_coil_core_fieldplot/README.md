# 演習3: コイル・コア電磁石（インダクタンスレポート、Bフィールドプロット）

**目安時間: 90分**

題材: [1.normal/maxwell_3d/ex03_coil_core/](../../../1.normal/maxwell_3d/ex03_coil_core/) と
同じモデル・Setupに、AEDT内部のポスト処理（インダクタンスレポート・フィールドプロット）を追加する。

> この演習は「コイル・コア電磁石シリーズ」の hard レベル。normalの内容は
> [1.normal/maxwell_3d/ex03_coil_core/](../../../1.normal/maxwell_3d/ex03_coil_core/) を参照。
> さらにPython側でのCSV入出力・PyVista可視化を追加したものが
> [3.expert/maxwell_3d/ex03_coil_core_postprocessing/](../../../3.expert/maxwell_3d/ex03_coil_core_postprocessing/)
> にある。

## 学習目標

- `MatrixMagnetostatic`/`SourceMagnetostatic` を使って、Windingにインダクタンス計算用の
  Matrixを割り当てる
- `post.create_report()` で、自己インダクタンス（`Matrix1.L(Winding1,Winding1)`）を
  データテーブルレポートとして作成する
- `post.create_fieldplot_surface()` で、コア表面のB磁束密度（`Mag_B`）のフィールドプロットを作成する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析・ポスト処理を完成させてください
（モデル作成部分はnormalと同じ内容です）。

1. normalと同じ手順でモデルを作成する。
2. `SourceMagnetostatic(name="Winding1")` を `signal_sources` とした
   `MatrixMagnetostatic(signal_sources=sources, group_sources=[], matrix_name="Matrix1")` を作り、
   `assign_matrix()` でWindingに割り当てる。
3. セットアップを作成し、解析を実行する（normalと同じ設定）。
4. `post.create_report(expressions=["Matrix1.L(Winding1,Winding1)"], plot_type="Data Table",
   plot_name="Inductance")` で、自己インダクタンスをデータテーブルレポートとして作成する。
5. `post.create_fieldplot_surface(assignment="Core", quantity="Mag_B", setup=f"{setup.name} :
   LastAdaptive", plot_name="CoreMagB")` で、コア表面のB磁束密度のフィールドプロットを作成する。
6. プロジェクトを保存し、`m3d.release_desktop()` でAEDTを終了する。

## ヒント

- `assign_matrix()`はWinding（励振）を割り当てた後に呼ぶ必要がある（励振が存在しないと
  計算対象の信号源を指定できない）。
- `Matrix1.L(Winding1,Winding1)`は「Winding1に対するWinding1自身の自己インダクタンス」を表す式。
  巻線が複数ある場合は`Matrix1.L(巻線A,巻線B)`で相互インダクタンスも取得できる。
- `plot_type="Data Table"`は、周波数スイープのような連続変化がない単一の値を確認する際に使う
  （choke演習の損失レポートと同じ考え方）。

## 評価基準

- [ ] normalと同じモデル・励振・Setup・解析がエラーなく完走している
- [ ] Windingにインダクタンス計算用のMatrixが割り当てられている
- [ ] 自己インダクタンスのデータテーブルレポートが作成されている
- [ ] コア表面のMag_Bフィールドプロットが作成されている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `amp_turns`の値を変えて再解析し、インダクタンスの値が（線形材料なので）変化しないことを
  確認してください（非線形材料であれば電流によって透磁率が変わり、インダクタンスも変化する）。
- インダクタンスの値をPythonで取得し、CSV出力・PyVista可視化まで行いたい場合は、このシリーズの
  expert（[3.expert/maxwell_3d/ex03_coil_core_postprocessing/](../../../3.expert/maxwell_3d/ex03_coil_core_postprocessing/)）
  に進んでみてください。
