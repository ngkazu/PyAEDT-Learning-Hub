# 演習1: ヒートシンク熱解析 温度データのPython後処理（CSV入出力・PyVista可視化）

**目安時間: 90分以上**

題材: [2.hard/icepak/ex01_heatsink_fieldplot/](../../../2.hard/icepak/ex01_heatsink_fieldplot/)
で作成した温度ポイントモニタ・温度フィールドプロットに、Python側の数値集計・CSV入出力・
PyVista可視化を追加する。

> この演習は「ヒートシンク熱解析シリーズ」の expertレベル。hardの内容に加えて、
> `conditions.csv`から発熱量を読み込み、`evaluate_monitor_quantity()`で取得した温度を
> CSVに出力し、`plot_field_from_fieldplot()`で温度フィールドプロットをPNG画像・
> インタラクティブなPyVistaウィンドウの両方で可視化する。

## 学習目標

- `conditions.csv`から設計パラメータ（発熱量）を読み込み、モデルに反映する方法を学ぶ
- `post.evaluate_monitor_quantity()`で、温度ポイントモニタの解析結果（Min/Max/Mean/Stdev）を
  Pythonの辞書として取得する方法を学ぶ
- 取得した数値をCSVファイルに書き出し、設計条件と解析結果を対応付けて記録する方法を学ぶ
- `post.plot_field_from_fieldplot()`で、AEDTのフィールドプロットをPyVista経由で
  PNG画像化・インタラクティブ表示する方法を学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。
寸法・値はすべてmm単位（特記のあるものを除く）。手順2〜14は
[2.hard/icepak/ex01_heatsink_fieldplot/](../../../2.hard/icepak/ex01_heatsink_fieldplot/)
と同じモデル・境界条件・Setupなので、そちらのREADMEも参照しながら進める
（発熱量のみCSVから読み込んだ値を使う点が異なる）。

1. `conditions.csv`（`power_w`列、値`20`）を読み込み、`power_w`を`float`として取得する。
2. `Icepak(design="IcepakDesign1", solution_type="SteadyState", version=AEDT_VERSION,
   new_desktop=True, non_graphical=False)` で起動し、`modeler.model_units = "mm"` を設定する。
3. `edit_design_settings(ambient_temperature="20cel", gravity_dir=2)` で、周囲温度20℃・
   重力方向-Zを設定する。
4. ベース（`"base"`）を `origin=[0, -50, -50]`, `sizes=[10, 100, 100]`,
   `material="Al-Extruded"` で作成する。
5. `assign_point_monitor_in_object(name="base", monitor_type="Temperature",
   monitor_name="Monitor_base")` で、ベースに温度ポイントモニタを割り当てる。
6. フィン1枚目（`"fin"`）を `origin=[10, -50, -50]`, `sizes=[40, 5, 100]`,
   `material="Al-Extruded"` で作成し、`_ok, fin_clone_names = duplicate_along_line(
   assignment="fin", vector=[0, 9.5, 0], clones=11)` でY方向にピッチ9.5mmで11枚に複製する。
7. 発熱面シート（`"Rectangle1"`）を `create_rectangle(orientation="YZ",
   origin=[0, -50, -50], sizes=[100, 100])` で作成する。
8. 解析領域（`"Region"`）を `create_region(pad_value=[25, 25, 50, 50, 50, 50],
   pad_type="Absolute Offset")` で作成する。
9. `assign_source(assignment="Rectangle1", thermal_condition="Total Power",
   assignment_value=f"{power_w}W", boundary_name="Source1", radiate=False)` で、
   CSVから読み込んだ発熱量を発熱面に割り当てる。
10. Regionの6面（±X, ±Y, ±Z）の中心座標から `get_faceid_from_position()` で面IDを特定する。
11. Regionの+Z面に `assign_pressure_free_opening(assignment=[+Z面],
    boundary_name="Opening1", no_reverse_flow=True)`、-Z面に
    `assign_pressure_free_opening(assignment=[-Z面], boundary_name="Opening2",
    no_reverse_flow=False)` で圧力開口を割り当てる。
12. Regionの±X, ±Y面（4面）に `assign_stationary_wall(geometry=[4面],
    boundary_condition="Temperature", name="StationaryWall1", temperature="AmbientTemp",
    material="Al-Extruded", radiate=True)` で固定温度壁を割り当てる。
13. セットアップ `"Setup1"` を作成し、`setup.props["Flow Regime"] = "Laminar"`、
    `setup.props["Include Gravity"] = True`、
    `setup.props["Convergence Criteria - Max Iterations"] = 500` を設定する。
14. `setup.analyze()` で解析を実行し、`setup_sweep = f"{setup.name} : {ipk.solution_type}"`
    を作っておく。
15. `ipk.post.evaluate_monitor_quantity(monitor="Monitor_base", quantity="Temperature",
    setup_name=setup_sweep)` で、ベースの温度モニタ値（`"Min"`/`"Max"`/`"Mean"`/
    `"Stdev"`/`"Unit"`を持つ辞書）を取得する。
16. `power_w`・温度モニタの最大値・温度単位を、ヘッダー付きで`results_thermal.csv`に
    書き出す。
17. `ipk.post.create_fieldplot_surface(assignment=["base"] + fin_names,
    quantity="Temperature", setup=setup_sweep, plot_name="HeatsinkTemperature")` で、
    ヒートシンク表面の温度フィールドプロットを作成する。
18. `ipk.post.plot_field_from_fieldplot(plot_name="HeatsinkTemperature",
    project_path=str(script_dir), image_format="png", view="isometric",
    log_scale=False, show=False)` で、フィールドプロットをPNG画像として出力する。
19. `ipk.post.plot_field_from_fieldplot(plot_name="HeatsinkTemperature", view="isometric",
    log_scale=False, show=True)` で、同じフィールドプロットをインタラクティブな
    PyVistaウィンドウで表示する。
20. プロジェクトを保存し、`release_desktop()` でAEDTを終了する。

## ヒント

- `evaluate_monitor_quantity()`の戻り値は、点モニタの場合`{"Min", "Max", "Mean", "Stdev",
  "Unit"}`を持つ辞書になる（単一点モニタではMin=Max=Meanになる）。
- `plot_field_from_fieldplot()`の`log_scale`は既定で`True`だが、温度分布のように値の桁が
  揃っている量では線形スケール（`log_scale=False`）の方が見やすいことが多い。
- `show=False`はPNG画像をファイルに保存するだけで、GUIウィンドウは開かない。`show=True`は
  インタラクティブなPyVistaウィンドウを開く（自動テストやバッチ実行では`show=False`のみを
  使うのが安全）。

## 評価基準

- [ ] `conditions.csv`から`power_w`を読み込み、モデルの発熱量に反映している
- [ ] AEDTがIcepak SteadyStateで起動し、`ex01_heatsink_fieldplot`（hard）と同じモデル・
      境界条件・Setup・モニタが作成され、解析がエラーなく完走している
- [ ] ベースの温度モニタ最大値が`results_thermal.csv`に書き出されている
- [ ] ヒートシンク表面の温度フィールドプロットが作成され、PNG画像として出力されている
- [ ] 同じフィールドプロットがインタラクティブなPyVistaウィンドウで表示できる

## 発展課題（任意）

- `conditions.csv`に複数行の発熱量を用意し、それぞれについて解析を実行して
  `results_thermal.csv`に追記し、発熱量と最大温度の関係をmatplotlibでグラフ化してみてください。
- フィンの枚数やピッチを変えて、ベース温度がどう変化するか比較してみてください。
