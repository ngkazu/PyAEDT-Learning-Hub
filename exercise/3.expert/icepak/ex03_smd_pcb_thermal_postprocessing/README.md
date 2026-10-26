# 演習3: PCB表面実装部品の熱解析 温度データのPython後処理（CSV入出力・PyVista可視化）

**目安時間: 90分以上**

題材: [2.hard/icepak/ex03_smd_pcb_thermal_fieldplot/](../../2.hard/icepak/ex03_smd_pcb_thermal_fieldplot/)
で作成した温度ポイントモニタ・温度フィールドプロットに、Python側の数値集計・CSV入出力・
PyVista可視化を追加する。

> この演習は「Icepak熱解析シリーズ」の3問目・expertレベル。hardの内容に加えて、
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
[2.hard/icepak/ex03_smd_pcb_thermal_fieldplot/](../../2.hard/icepak/ex03_smd_pcb_thermal_fieldplot/)
と同じモデル・境界条件・Setupなので、そちらのREADMEも参照しながら進める
（発熱量のみCSVから読み込んだ値を使う点が異なる）。

1. `conditions.csv`（`power_w`列、値`0.05`）を読み込み、`power_w`を`float`として取得する。
2. `Icepak(design="IcepakDesign1", solution_type="SteadyState", version=AEDT_VERSION,
   new_desktop=True, non_graphical=False)` で起動し、`modeler.model_units = "mm"` を設定する。
3. `edit_design_settings(ambient_temperature="20cel", gravity_dir=2)` で、周囲温度20℃・
   重力方向-Zを設定する。
4. PCB基板とその上の層を、下から順にBoxで積み重ねて作成する（具体的な`origin`/`sizes`/
   `material`は[2.hard/icepak/ex03_smd_pcb_thermal_fieldplot/](../../2.hard/icepak/ex03_smd_pcb_thermal_fieldplot/)
   のREADMEの表を参照）。
5. `assign_point_monitor_in_object(name="Box8", monitor_type="Temperature",
   monitor_name="Monitor_Box8")` で、Siダイに温度ポイントモニタを割り当てる。
6. メッシュリージョンを3つ作成する（**Regionより先に作成する**。詳細はhardのREADMEを参照）。
7. 解析領域（`"Region"`）を作り直す。`ipk.modeler["Region"].delete()` で既定の`"Region"`を
   削除してから、`create_region(pad_type=["Absolute Offset"] * 6, pad_value=["25mm",
   "25mm", "25mm", "25mm", "50mm", "10mm"])` で作成する。
8. `assign_solid_block(object_name="Box8", power_assignment=f"{power_w}W",
   boundary_name="Block1")` で、CSVから読み込んだ発熱量をSiダイに割り当てる。
9. `modeler["Region"].bounding_box` から6面の中心座標を計算し、`get_faceid_from_position()`
   で各面の面IDを特定する。
10. Regionの+Z面（上面）に `assign_pressure_free_opening(assignment=[+Z面],
    boundary_name="Opening1", no_reverse_flow=True)` で圧力開口を割り当てる。
11. Regionの±X, ±Y面（4面）に `assign_pressure_free_opening(assignment=[4面],
    boundary_name="Opening2", no_reverse_flow=False)` で圧力開口を割り当てる。
12. Regionの-Z面（底面）に `assign_stationary_wall_with_htc(geometry=-Z面,
    name="StationaryWall1", thickness="30mm", material="Epoxy Resin-JSME",
    htc="10w_per_m2kel", ref_temperature="AmbientTemp", shell_conduction=True)` で、
    対流熱伝達係数10 W/m²Kの壁面境界条件を割り当てる。
13. セットアップ `"Setup1"` を作成し、`setup.props["Flow Regime"] = "Laminar"`、
    `setup.props["Include Gravity"] = True`、
    `setup.props["Radiation Model"] = "Discrete Ordinates Model"`、
    `setup.props["Convergence Criteria - Max Iterations"] = 500`、
    `setup.props["Convergence Criteria - Flow"] = "0.001"`、
    `setup.props["Convergence Criteria - Energy"] = "1e-07"`、
    `setup.props["Linear Solver Type - Pressure"] = "V"` を設定する。
14. `setup.analyze()` で解析を実行し、`setup_sweep = f"{setup.name} : {ipk.solution_type}"`
    を作っておく。
15. `ipk.post.evaluate_monitor_quantity(monitor="Monitor_Box8", quantity="Temperature",
    setup_name=setup_sweep)` で、Siダイの温度モニタ値（`"Min"`/`"Max"`/`"Mean"`/
    `"Stdev"`/`"Unit"`を持つ辞書）を取得する。
16. `power_w`・温度モニタの最大値・温度単位を、ヘッダー付きで`results_thermal.csv`に
    書き出す。
17. `ipk.post.create_fieldplot_surface(assignment=["Box1", "Box7", "Box8"],
    quantity="Temperature", setup=setup_sweep, plot_name="PcbTemperature")` で、
    PCB・部品本体・Siダイ表面の温度フィールドプロットを作成する。
18. `ipk.post.plot_field_from_fieldplot(plot_name="PcbTemperature",
    project_path=str(script_dir), image_format="png", view="isometric",
    log_scale=False, show=False)` で、フィールドプロットをPNG画像として出力する。
19. `ipk.post.plot_field_from_fieldplot(plot_name="PcbTemperature", view="isometric",
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
- [ ] AEDTがIcepak SteadyStateで起動し、`ex03_smd_pcb_thermal_fieldplot`（hard）と同じ
      モデル・境界条件・Setup・モニタが作成され、解析がエラーなく完走している
- [ ] Siダイの温度モニタ最大値が`results_thermal.csv`に書き出されている
- [ ] PCB・部品本体・Siダイ表面の温度フィールドプロットが作成され、PNG画像として
      出力されている
- [ ] 同じフィールドプロットがインタラクティブなPyVistaウィンドウで表示できる

## 発展課題（任意）

- `conditions.csv`に複数行の発熱量を用意し、それぞれについて解析を実行して
  `results_thermal.csv`に追記し、発熱量と最大温度の関係をmatplotlibでグラフ化してみてください。
- 底面のHTC（`10w_per_m2kel`）を変えて、Siダイの最大温度がどう変化するか比較してみてください。
