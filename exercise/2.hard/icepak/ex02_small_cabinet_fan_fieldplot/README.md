# 演習2: 小型筐体のファン冷却解析（温度フィールドプロット・モニタ）

**目安時間: 90分**

題材: [1.normal/icepak/ex02_small_cabinet_fan/](../../1.normal/icepak/ex02_small_cabinet_fan/) で
作成したPCB+発熱部品+ヒートシンク+Fanモデルに、AEDT内部のポスト処理（温度ポイントモニタ・
温度フィールドプロット）を追加する。

> この演習は「Icepak熱解析シリーズ」の2問目・hardレベル。normalで作ったモデルに
> `assign_point_monitor_in_object()`と`post.create_fieldplot_surface()`を追加する。
> さらにPython側の集計・CSV入出力・PyVista可視化を追加したものが
> [3.expert/icepak/ex02_small_cabinet_fan_postprocessing/](../../3.expert/icepak/ex02_small_cabinet_fan_postprocessing/)
> にある。

## 学習目標

- `assign_point_monitor_in_object()`で、オブジェクトの重心に温度ポイントモニタを割り当てる
  方法を学ぶ（モニタは解析実行前に割り当てる必要がある点に注意）
- `post.create_fieldplot_surface()`で、複数オブジェクトの表面温度フィールドプロットを
  作成する方法を学ぶ
- `duplicate_along_line()`の戻り値（複製されたオブジェクト名のリスト）を、後続のフィールド
  プロット割り当てに再利用する方法を学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。
寸法・値はすべてmm単位（特記のあるものを除く）。手順1〜14は
[1.normal/icepak/ex02_small_cabinet_fan/](../../1.normal/icepak/ex02_small_cabinet_fan/)
と同じモデル・境界条件・Setupなので、そちらのREADMEも参照しながら進める。

1. `Icepak(design="IcepakDesign1", solution_type="SteadyState", version=AEDT_VERSION,
   new_desktop=True, non_graphical=False)` で起動し、`modeler.model_units = "mm"` を設定する。
2. `edit_design_settings(ambient_temperature="20cel", gravity_dir=2)` で、周囲温度20℃・
   重力方向-Zを設定する。
3. PCB基板（`"Box5"`）を `origin=[15, 5, 5]`, `sizes=[70, 70, 1.6]`, `material="fr4_epoxy"` で
   作成する。
4. 発熱部品（`"Box6"`）を `origin=[50, 40, 6.6]`, `sizes=[20, 20, 4]`,
   `material="ceramic_material"` で作成する。
5. `assign_point_monitor_in_object(name="Box6", monitor_type="Temperature",
   monitor_name="Monitor_Box6")` で、発熱部品に温度ポイントモニタを割り当てる
   （**解析実行前に**割り当てること）。
6. 発熱部品の上面（Z=10.6の位置）に、ダイアタッチ割り当て用の20×20mmシート
   （`"Box6_ObjectFromFace1"`）を `create_rectangle(orientation="XY",
   origin=[50, 40, 10.6], sizes=[20, 20])` で作成する。
7. ヒートシンクを作成する。
   - ベース（`"Box7"`）: `origin=[40, 30, 10.6]`, `sizes=[40, 40, 5]`, `material="al-extruded"`
   - フィン1枚目（`"Box8"`）: `origin=[40, 30, 15.6]`, `sizes=[40, 1.5, 15]`,
     `material="al-extruded"`。`_, fin_clone_names = duplicate_along_line(assignment="Box8",
     vector=[0, 5.5, 0], clones=8)` でY方向にピッチ5.5mmで8枚に複製し、戻り値の
     複製オブジェクト名リストを`fin_clone_names`に保持しておく（手順15で使う）。
8. 解析領域（`"Region"`）を作り直す。Icepakデザイン作成時に自動生成される既定の
   `"Region"`を `ipk.modeler["Region"].delete()` でいったん削除してから、
   `create_region(pad_value=[58, 58, 48, 48, 28, 28], pad_type="Absolute Offset")` で
   作成する（`create_fan()`が許容する`radius`上限はRegion・モデル全体のサイズに依存するため、
   **必ずFanより先にRegionを作る**）。
9. `create_fan(name="Fan1", shape="Circular", cross_section="YZ", radius="10mm",
   hub_radius="5mm", origin=[0, 60, 20])` で送風機（Fanコンポーネント）を配置する。続けて
   `fan.props["NativeComponentDefinitionProvider"]`
   の`"DimUnits"`を`["m3_per_s", "pascal"]`、`"X"`を`["0", "0.005", "0.01", "0.015"]`、
   `"Y"`を`["50", "40", "20", "0"]`に書き換えて流量圧力カーブを設定し、`fan.update()`で
   反映する（`Radius`/`HubRadius`はここで変更しない）。
10. 発熱部品に `assign_solid_block(object_name="Box6", power_assignment="10W",
    boundary_name="Block1")` で総発熱量10Wを割り当てる。
11. ダイアタッチシートに `assign_conducting_plate_with_thickness(obj_plate=
    "Box6_ObjectFromFace1", boundary_name="ConductingPlate1", total_power="0W",
    thickness="0.02mm", solid_material="Die_attach_material")` で、厚さ0.02mmの
    伝導板を割り当てる。
12. Regionの±X面を`get_faceid_from_position()`で特定し、
    `assign_pressure_free_opening(assignment=[+X面, -X面], boundary_name="Opening1",
    no_reverse_flow=False)` で圧力開口を割り当てる。
13. セットアップ `"Setup1"` を作成し、`setup.props["Flow Regime"] = "Turbulent"`、
    `setup.props["Include Gravity"] = False`、`setup.props["Radiation Model"] = "Off"`、
    `setup.props["Convergence Criteria - Max Iterations"] = 500` を設定する。
14. `setup.analyze()` で解析を実行する。
15. `ipk.post.create_fieldplot_surface(assignment=["Box7", "Box8"] + fin_clone_names,
    quantity="Temperature", setup=f"{setup.name} : {ipk.solution_type}",
    plot_name="HeatsinkTemperature")` で、ヒートシンク表面（ベース+フィン8枚）の
    温度フィールドプロットを作成する。
16. プロジェクトを保存し、`release_desktop()` でAEDTを終了する。

## ヒント

- 点モニタ・面モニタは、解析実行（`setup.analyze()`）より**前に**割り当てる必要がある。
  後から追加しても、既存の解析結果には反映されない。
- `create_fieldplot_surface()`の`setup`引数は`"セットアップ名 : ソリューション種別"`の形式
  （例: `"Setup1 : SteadyState"`）で指定する。`f"{setup.name} : {ipk.solution_type}"`で
  組み立てられる。
- `duplicate_along_line()`は`(成功フラグ, 複製されたオブジェクト名のリスト)`のタプルを返す
  （`ex01_heatsink`で既習）。このリストを使うと、個々のフィン名を手で列挙しなくても
  フィールドプロットの対象に含められる。

## 評価基準

- [ ] AEDTがIcepak SteadyStateで起動し、`ex02_small_cabinet_fan`（normal）と同じモデル・
      境界条件・Setupが作成されている
- [ ] 発熱部品（Box6）に温度ポイントモニタ（`Monitor_Box6`）が解析実行前に割り当てられている
- [ ] 解析がエラーなく完走している
- [ ] ヒートシンク表面（ベース+フィン8枚）の温度フィールドプロット（`HeatsinkTemperature`）が
      作成されている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- フィールドプロットの`quantity`を`"Velocity Vector"`や`"Pressure"`に変えて、
  ヒートシンク周辺の流れ場を可視化してみてください。
- モニタをヒートシンクのベース（Box7）にも追加し、発熱部品とベースの温度差を比較してみてください。
