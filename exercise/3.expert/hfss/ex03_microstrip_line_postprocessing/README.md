# 演習3: マイクロストリップ線路 S/フィールドデータの Python 後処理

**目安時間: 90分以上**

題材: 演習「2.hard/hfss/ex03_microstrip_line_fieldplot」で作成したモデルを土台に、AEDT側の操作は最小限に
とどめ、**Pythonでのカスタムデータ処理とCSV入出力、PyVistaでの可視化**に重点を置く
（`docs/difficulty-criteria.md` の expert レベルに相当）。

> このプロジェクトの各演習は独立して実行できるように作られている。本演習は
> `2.hard/hfss/ex03_microstrip_line_fieldplot` のモデルをこのスクリプト内で作り直した上で、
> S11・S21データをCSVに出力し、フィールドプロットをPyVistaで可視化する
> （hardの演習を先にやっていなくても単体で進められる）。モデル作成の基本操作は
> [0.easy/common_3d/ex01_basic_operations/](../../../0.easy/common_3d/ex01_basic_operations/) で先に練習できる。

## 学習目標

- `csv.DictReader` で条件CSV（`conditions.csv`）を読み込み、モデルの寸法パラメータに反映する
- Terminalソリューションの2ポートSパラメータを `post.get_solution_data()` で取得する
  （`report_category="Terminal Solution Data"` を指定する点がModalソリューションと異なる）
- 取得した周波数特性をCSVファイルに出力する
- `post.plot_field_from_fieldplot()` を使い、フィールドプロットをPyVistaで画像・インタラクティブ表示する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 同じフォルダにある `conditions.csv`（`line_w_mm`, `line_l_mm` の列を持つ1行のCSV）を
   `csv.DictReader` で読み込み、各値を取得する。
2. `1.normal/hfss/ex03_microstrip_line/` と同じ手順で、次を順に行う（導体幅・長さはCSVから読み込んだ
   `line_w_mm`/`line_l_mm` の値を使う。それ以外は固定値 `SUB_W=6.0mm`, `SUB_H=1.0mm`, `AIR_H=3.0mm`）。
   - 基板（3Dソリッド）を `origin=[0, -SUB_W/2, 0]`, `sizes=[line_l_mm, SUB_W, SUB_H]`,
     `material="alumina_96pct"` で作成する。
   - GND・信号線を `modeler.create_rectangle()` で2Dシートとして作成し、それぞれに
     `hfss.assign_finite_conductivity(material="copper")` を割り当てる（信号線幅は `line_w_mm`）。
   - 基板上面からエアボックス（`sizes=[line_l_mm, SUB_W, AIR_H]`, `material="vacuum"`）を作成する。
   - エアボックスの両端面に `hfss.wave_port(modes=1, renormalize=True, impedance=50)` でWave Portを作成する。
   - エアボックスの下面・両端面を除く面に `hfss.assign_radiation_boundary_to_faces()` で輻射境界を割り当てる。
   - `hfss.validate_full_design()` でモデルを検証する。
   - セットアップ `"Setup1"`（`Frequency="10GHz"`, `MaxDeltaS=0.02`, `MaximumPasses=6`）を作成し、
     `hfss.create_linear_count_sweep(...)` で周波数スイープを追加後、`setup.analyze()` で解析する。
3. `sorted(hfss.excitation_names)` からポート名を取得し、S11・S21の2つの式について
   `hfss.post.get_solution_data(expressions=[...], setup_sweep_name=hfss.nominal_sweep,
   report_category="Terminal Solution Data")` で `SolutionData` を取得する。
4. `get_expression_data(formula="db20")` を使って、周波数・S11[dB]・S21[dB]をNumPy形式で取り出す。
5. 周波数・S11[dB]・S21[dB]の3列を持つCSVファイル（`results_s_parameters.csv`）に結果を出力する。
6. `hfss.post.create_fieldplot_surface(assignment=[gnd.name, line.name], quantity="Mag_E",
   setup="Setup1 : LastAdaptive", plot_name="MagE_Surface")` でフィールドプロットを作成する。
7. `hfss.post.plot_field_from_fieldplot(plot_name="MagE_Surface", project_path=str(script_dir),
   image_format="png", view="isometric", log_scale=True, show=False)` を使い、フィールドプロットを
   PyVistaで画像ファイルとして出力する。
8. 同じフィールドプロットに対し、今度は `project_path` を渡さず `show=True` で
   `plot_field_from_fieldplot(plot_name="MagE_Surface", view="isometric", log_scale=True, show=True)` を
   呼び、インタラクティブなPyVistaウィンドウ（マウスで回転・拡大できる）を表示する。
9. プロジェクトを保存し、`release_desktop()` で終了する。

## ヒント

- Terminalソリューションの `get_solution_data()` は `report_category="Terminal Solution Data"` を
  指定する（`hfss.create_scattering()` の内部実装でも、ソリューションタイプに応じてこの
  `report_category` を自動的に切り替えている）。
- `plot_field_from_fieldplot()` の `log_scale=True` を使うと、`export_image` 経由の対数スケール設定
  （`folder_settings.scale_settings.log = True`）と同様に、電界強度の桁違いな分布を見やすくできる。
- `plot_field_from_fieldplot()` は `project_path` を渡すと画面表示なしでその場所に画像を保存し、
  `project_path` を渡さず `show=True` にすると `auto_close` されないインタラクティブウィンドウが開く。

## 評価基準

- [ ] `conditions.csv` の値がモデルの寸法（`line_w_mm`, `line_l_mm`）に反映されている
- [ ] S11・S21のデータが `SolutionData` として取得できている
- [ ] S11・S21の結果がCSVファイルに出力されている
- [ ] 電界（Mag_E）のフィールドプロットが作成されている
- [ ] フィールドプロットがPyVistaで画像ファイルとして出力されている
- [ ] フィールドプロットがインタラクティブなPyVistaウィンドウで表示され、マウスで回転できる

## 発展課題（任意）

- `conditions.csv` に複数行の条件（`line_w_mm` の異なる値など）を用意し、行ごとにループして解析し、
  導体幅と特性インピーダンス（S11から推定）の関係を比較するCSV/グラフを作ってみてください。
