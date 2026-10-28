# 演習2: 小型筐体のファン冷却解析 温度データのPython後処理（CSV入出力・PyVista可視化）

**目安時間: 90分以上**

題材: [2.hard/icepak/ex02_small_cabinet_fan_fieldplot/](../../../2.hard/icepak/ex02_small_cabinet_fan_fieldplot/)
で作成した温度ポイントモニタ・温度フィールドプロットに、Python側の数値集計・CSV入出力・
PyVista可視化を追加する。

> この演習は「Icepak熱解析シリーズ」の2問目・expertレベル。hardの内容に加えて、
> `conditions.csv`から発熱量を読み込み、`evaluate_monitor_quantity()`・
> `get_fans_operating_point()`で取得した数値をCSVに出力し、`plot_field_from_fieldplot()`で
> 温度フィールドプロットをPNG画像・インタラクティブなPyVistaウィンドウの両方で可視化する。

## 学習目標

- `conditions.csv`から設計パラメータ（発熱量）を読み込み、モデルに反映する方法を学ぶ
- `post.evaluate_monitor_quantity()`で、温度ポイントモニタの解析結果（Min/Max/Mean/Stdev）を
  Pythonの辞書として取得する方法を学ぶ
- `post.get_fans_operating_point()`で、Fanコンポーネントの動作点（流量・圧力上昇）を
  CSVファイルおよびPython辞書として取得する方法を学ぶ
- 取得した数値をCSVファイルに書き出し、設計条件と解析結果を対応付けて記録する方法を学ぶ
- `post.plot_field_from_fieldplot()`で、AEDTのフィールドプロットをPyVista経由で
  PNG画像化・インタラクティブ表示する方法を学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。
寸法・値はすべてmm単位（特記のあるものを除く）。手順2〜15は
[2.hard/icepak/ex02_small_cabinet_fan_fieldplot/](../../../2.hard/icepak/ex02_small_cabinet_fan_fieldplot/)
と同じモデル・境界条件・Setupなので、そちらのREADMEも参照しながら進める
（発熱量のみCSVから読み込んだ値を使う点が異なる）。

1. `conditions.csv`（`power_w`列、値`10`）を読み込み、`power_w`を`float`として取得する。
2. `Icepak(design="IcepakDesign1", solution_type="SteadyState", version=AEDT_VERSION,
   new_desktop=True, non_graphical=False)` で起動し、`modeler.model_units = "mm"` を設定する。
3. `edit_design_settings(ambient_temperature="20cel", gravity_dir=2)` で、周囲温度20℃・
   重力方向-Zを設定する。
4. PCB基板（`"Box5"`）を `origin=[15, 5, 5]`, `sizes=[70, 70, 1.6]`, `material="fr4_epoxy"` で
   作成する。
5. 発熱部品（`"Box6"`）を `origin=[50, 40, 6.6]`, `sizes=[20, 20, 4]`,
   `material="ceramic_material"` で作成する。
6. `assign_point_monitor_in_object(name="Box6", monitor_type="Temperature",
   monitor_name="Monitor_Box6")` で、発熱部品に温度ポイントモニタを割り当てる。
7. 発熱部品の上面（Z=10.6の位置）に、ダイアタッチ割り当て用の20×20mmシート
   （`"Box6_ObjectFromFace1"`）を `create_rectangle(orientation="XY",
   origin=[50, 40, 10.6], sizes=[20, 20])` で作成する。
8. ヒートシンクを作成する。
   - ベース（`"Box7"`）: `origin=[40, 30, 10.6]`, `sizes=[40, 40, 5]`, `material="al-extruded"`
   - フィン1枚目（`"Box8"`）: `origin=[40, 30, 15.6]`, `sizes=[40, 1.5, 15]`,
     `material="al-extruded"`。`_, fin_clone_names = duplicate_along_line(assignment="Box8",
     vector=[0, 5.5, 0], clones=8)` でY方向にピッチ5.5mmで8枚に複製する。
9. 解析領域（`"Region"`）を作り直す。`ipk.modeler["Region"].delete()` で既定の`"Region"`を
   削除してから、`create_region(pad_value=[58, 58, 48, 48, 28, 28],
   pad_type="Absolute Offset")` で作成する（**必ずFanより先に**Regionを作ること）。
10. `create_fan(name="Fan1", shape="Circular", cross_section="YZ", radius="10mm",
    hub_radius="5mm", origin=[0, 60, 20])` で送風機を配置し、
    `fan.props["NativeComponentDefinitionProvider"]`
    の`"DimUnits"`を`["m3_per_s", "pascal"]`、`"X"`を`["0", "0.005", "0.01", "0.015"]`、
    `"Y"`を`["50", "40", "20", "0"]`に書き換えて流量圧力カーブを設定し、`fan.update()`で
    反映する。
11. 発熱部品に `assign_solid_block(object_name="Box6", power_assignment=f"{power_w}W",
    boundary_name="Block1")` で、CSVから読み込んだ発熱量を割り当てる。
12. ダイアタッチシートに `assign_conducting_plate_with_thickness(obj_plate=
    "Box6_ObjectFromFace1", boundary_name="ConductingPlate1", total_power="0W",
    thickness="0.02mm", solid_material="Die_attach_material")` で、厚さ0.02mmの
    伝導板を割り当てる。
13. Regionの±X面を`get_faceid_from_position()`で特定し、
    `assign_pressure_free_opening(assignment=[+X面, -X面], boundary_name="Opening1",
    no_reverse_flow=False)` で圧力開口を割り当てる。
14. セットアップ `"Setup1"` を作成し、`setup.props["Flow Regime"] = "Turbulent"`、
    `setup.props["Include Gravity"] = False`、`setup.props["Radiation Model"] = "Off"`、
    `setup.props["Convergence Criteria - Max Iterations"] = 500` を設定する。
15. `setup.analyze()` で解析を実行し、`setup_sweep = f"{setup.name} : {ipk.solution_type}"`
    を作っておく。
16. `ipk.post.evaluate_monitor_quantity(monitor="Monitor_Box6", quantity="Temperature",
    setup_name=setup_sweep)` で、発熱部品の温度モニタ値（`"Min"`/`"Max"`/`"Mean"`/
    `"Stdev"`/`"Unit"`を持つ辞書）を取得する。
17. `_, flow_label, pressure_label, fan_operating_points =
    ipk.post.get_fans_operating_point(setup_name=setup_sweep)` で、Fanの動作点を取得し、
    `fan_operating_points[fan.name]` から流量・圧力上昇の値を取り出す。
18. `power_w`・温度モニタの最大値・温度単位・Fan流量・Fan圧力上昇を、ヘッダー付きで
    `results_thermal.csv` に書き出す。
19. `ipk.post.create_fieldplot_surface(assignment=["Box7", "Box8"] + fin_clone_names,
    quantity="Temperature", setup=setup_sweep, plot_name="HeatsinkTemperature")` で、
    ヒートシンク表面の温度フィールドプロットを作成する。
20. `ipk.post.plot_field_from_fieldplot(plot_name="HeatsinkTemperature",
    project_path=str(script_dir), image_format="png", view="isometric",
    log_scale=False, show=False)` で、フィールドプロットをPNG画像として出力する。
21. `ipk.post.plot_field_from_fieldplot(plot_name="HeatsinkTemperature", view="isometric",
    log_scale=False, show=True)` で、同じフィールドプロットをインタラクティブな
    PyVistaウィンドウで表示する。
22. プロジェクトを保存し、`release_desktop()` でAEDTを終了する。

## ヒント

- `evaluate_monitor_quantity()`の戻り値は、点モニタの場合`{"Min", "Max", "Mean", "Stdev",
  "Unit"}`を持つ辞書になる（単一点モニタではMin=Max=Meanになる）。
- `get_fans_operating_point()`の戻り値は`[CSVファイルパス, 流量の列名, 圧力の列名,
  {Fanインスタンス名: [流量, 圧力]}]`の4要素タプル。Fanインスタンス名は`create_fan()`の
  `name`引数と一致しない場合がある（AEDTが内部的にサフィックスを付けることがあるため）ので、
  `fan.name`（作成時に返されたオブジェクトのプロパティ）を使ってルックアップする。
- `plot_field_from_fieldplot()`の`log_scale`は既定で`True`だが、温度分布のように値の桁が
  揃っている量では線形スケール（`log_scale=False`）の方が見やすいことが多い。
- `show=False`はPNG画像をファイルに保存するだけで、GUIウィンドウは開かない。`show=True`は
  インタラクティブなPyVistaウィンドウを開く（自動テストやバッチ実行では`show=False`のみを
  使うのが安全）。

## 評価基準

- [ ] `conditions.csv`から`power_w`を読み込み、モデルの発熱量に反映している
- [ ] AEDTがIcepak SteadyStateで起動し、`ex02_small_cabinet_fan_fieldplot`（hard）と
      同じモデル・境界条件・Setup・モニタが作成され、解析がエラーなく完走している
- [ ] 温度モニタの最大値とFanの動作点（流量・圧力上昇）が`results_thermal.csv`に
      書き出されている
- [ ] ヒートシンク表面の温度フィールドプロットが作成され、PNG画像として出力されている
- [ ] 同じフィールドプロットがインタラクティブなPyVistaウィンドウで表示できる

## 発展課題（任意）

- `conditions.csv`に複数行の発熱量を用意し、それぞれについて解析を実行して
  `results_thermal.csv`に追記し、発熱量と最大温度の関係をmatplotlibでグラフ化してみてください。
- Fanの流量圧力カーブ（`"X"`/`"Y"`）を変えて、動作点（`get_fans_operating_point()`の結果）が
  どう変化するか確認してみてください。
