# 演習2: 導波管インダクティブアイリスフィルタ S/フィールドデータの Python 後処理

**目安時間: 90分以上**

題材: 演習「2.hard/hfss/ex2_iris_filter」で作成したモデルを土台に、AEDT側の操作は最小限にとどめ、
**Pythonでのカスタムデータ処理とCSV入出力、PyVistaでの可視化**に重点を置く
（`docs/difficulty-criteria.md` の expert レベルに相当）。

> このプロジェクトの各演習は独立して実行できるように作られている。本演習は
> `2.hard/hfss/ex2_iris_filter` のモデルをこのスクリプト内で作り直した上で、
> S11・S21データをCSVに出力し、フィールドプロットをPyVistaで画像出力する
> （hardの演習を先にやっていなくても単体で進められる）。ブーリアン演算の基本操作は
> [0.easy/common_3d/ex2_boolean_subtract/](../../../0.easy/common_3d/ex2_boolean_subtract/) で先に練習できる。

## 学習目標

- `csv.DictReader` で条件CSV（`conditions.csv`）を読み込み、モデルの寸法パラメータに反映する
- 2ポート回路のS11・S21データを `post.get_solution_data()` で取得する
- 取得した周波数特性をCSVファイルに出力する
- `post.create_fieldplot_cutplane()` で作成したフィールドプロットを、
  `post.plot_field_from_fieldplot()` を使ってPyVistaで画像出力する
- PyVistaのインタラクティブウィンドウでフィールドプロットをマウス操作（回転・拡大）しながら確認する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 同じフォルダにある `conditions.csv`（`wg_length`, `iris_thickness`, `iris_aperture` の列を持つ1行のCSV）を
   `csv.DictReader` で読み込み、各値を取得する。
2. `2.hard/hfss/ex2_iris_filter/solution.py` と同じ手順で、導波管・アイリス・Wave Port・セットアップ・
   周波数掃引・解析実行までを行う（寸法はCSVから読み込んだ値を使う）。
3. `hfss.excitation_names` から実際の励振名を取得し、S11・S21の2つの式について
   `hfss.post.get_solution_data(expressions=[...], setup_sweep_name=hfss.nominal_sweep,
   report_category="Modal Solution Data")` で `SolutionData` を取得する。
4. `get_expression_data(formula="db20")` を使って、周波数・S11[dB]・S21[dB]をNumPy配列として取り出す。
5. 周波数・S11[dB]・S21[dB]の3列を持つCSVファイル（`results_s_parameters.csv`）に結果を出力する。
6. `modeler.create_plane()` で導波管中心を通るXZ平面（y = 5.08mm）を作成し、
   `hfss.post.create_fieldplot_cutplane()` で電界強度（`Mag_E`）のフィールドプロットを作成する。
7. `hfss.post.plot_field_from_fieldplot(plot_name=..., project_path=str(script_dir), image_format="png",
   view="xz", show=False)` を使い、フィールドプロットをPyVistaで画像ファイルとして出力する。
8. 同じフィールドプロットに対し、今度は `project_path` を渡さず `show=True` で
   `post.plot_field_from_fieldplot(plot_name=..., view="xz", show=True)` を呼び、
   インタラクティブなPyVistaウィンドウ（マウスで回転・拡大できる）を表示する。
9. プロジェクトを保存し、`release_desktop()` で終了する。

## ヒント

- `csv.DictReader` はヘッダー行をキーにした辞書を1行ずつ返す。`next(reader)` で最初の1行を取得できる。
- `get_solution_data()` の `expressions` にはリストを渡せる（複数の式を1回でまとめて取得できる）。
  `get_expression_data(expression=...)` で式ごとに個別のデータを取り出す。
- `post.plot_field_from_fieldplot()` は「AEDTのGUI上のフィールドプロット結果をPyVistaで再構築して画像化する」
  メソッド。`plot_name` にはAEDT側で作成したフィールドプロット名（`create_fieldplot_cutplane` の
  `plot_name` 引数で指定した名前）を渡す。
- `view="xz"` はXZ平面から見た視点。等角視点で見たい場合は `view="isometric"` にする。
- `plot_field_from_fieldplot()` は `project_path` を渡すと画面表示なしでその場所に画像を保存し、
  `project_path` を渡さず `show=True` にすると `auto_close` されないインタラクティブウィンドウが開く。
  画像保存と画面確認の両方をしたい場合は、このように2回呼び出すのが手軽。

## 評価基準

- [ ] `conditions.csv` の値がモデルの寸法（`wg_length`, `iris_thickness`, `iris_aperture`）に反映されている
- [ ] S11・S21のデータが `SolutionData` として取得できている
- [ ] S11・S21の結果がCSVファイルに出力されている
- [ ] 電界分布のフィールドプロットが作成されている
- [ ] フィールドプロットがPyVistaで画像ファイルとして出力されている
- [ ] フィールドプロットがインタラクティブなPyVistaウィンドウで表示され、マウスで回転できる

## 発展課題（任意）

- `conditions.csv` に複数行の条件（`iris_aperture` の異なる値など）を用意し、行ごとにループして解析し、
  通過帯域とアイリス寸法の関係を比較するCSV/グラフを作ってみてください。
- `view` を `"isometric"` に変えて、3D的な電界分布を確認してみてください。
