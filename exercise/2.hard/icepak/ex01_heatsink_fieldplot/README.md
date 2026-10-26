# 演習1: ヒートシンク熱解析（温度フィールドプロット・モニタ）

**目安時間: 90分**

題材: [1.normal/icepak/ex01_heatsink/](../../1.normal/icepak/ex01_heatsink/) で
作成したヒートシンクモデルに、AEDT内部のポスト処理（温度ポイントモニタ・温度フィールドプロット）
を追加する。

> この演習は「ヒートシンク熱解析シリーズ」の hard レベル。normalで作ったモデルに
> `assign_point_monitor_in_object()`と`post.create_fieldplot_surface()`を追加する。
> さらにPython側の集計・CSV入出力・PyVista可視化を追加したものが
> [3.expert/icepak/ex01_heatsink_postprocessing/](../../3.expert/icepak/ex01_heatsink_postprocessing/)
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
寸法・値はすべてmm単位（特記のあるものを除く）。手順1〜13は
[1.normal/icepak/ex01_heatsink/](../../1.normal/icepak/ex01_heatsink/)
と同じモデル・境界条件・Setupなので、そちらのREADMEも参照しながら進める。

1. `Icepak(design="IcepakDesign1", solution_type="SteadyState", version=AEDT_VERSION,
   new_desktop=True, non_graphical=False)` で起動し、`modeler.model_units = "mm"` を設定する。
2. `edit_design_settings(ambient_temperature="20cel", gravity_dir=2)` で、周囲温度20℃・
   重力方向-Zを設定する。
3. ベース（`"base"`）を `origin=[0, -50, -50]`, `sizes=[10, 100, 100]`,
   `material="Al-Extruded"` で作成する。
4. `assign_point_monitor_in_object(name="base", monitor_type="Temperature",
   monitor_name="Monitor_base")` で、ベースに温度ポイントモニタを割り当てる
   （**解析実行前に**割り当てること）。
5. フィン1枚目（`"fin"`）を `origin=[10, -50, -50]`, `sizes=[40, 5, 100]`,
   `material="Al-Extruded"` で作成し、`_ok, fin_clone_names = duplicate_along_line(
   assignment="fin", vector=[0, 9.5, 0], clones=11)` でY方向にピッチ9.5mmで11枚に複製する。
   戻り値の複製オブジェクト名リストを使って`fin_names = ["fin"] + fin_clone_names`を
   作っておく（手順14で使う）。
6. 発熱面シート（`"Rectangle1"`）を `create_rectangle(orientation="YZ",
   origin=[0, -50, -50], sizes=[100, 100])` で作成する。
7. 解析領域（`"Region"`）を `create_region(pad_value=[25, 25, 50, 50, 50, 50],
   pad_type="Absolute Offset")` で作成する。
8. `assign_source(assignment="Rectangle1", thermal_condition="Total Power",
   assignment_value="20W", boundary_name="Source1", radiate=False)` で発熱面に
   総発熱量20Wの熱源を割り当てる。
9. Regionの6面（±X, ±Y, ±Z）の中心座標から `get_faceid_from_position()` で面IDを特定する。
10. Regionの+Z面に `assign_pressure_free_opening(assignment=[+Z面],
    boundary_name="Opening1", no_reverse_flow=True)`、-Z面に
    `assign_pressure_free_opening(assignment=[-Z面], boundary_name="Opening2",
    no_reverse_flow=False)` で圧力開口を割り当てる。
11. Regionの±X, ±Y面（4面）に `assign_stationary_wall(geometry=[4面],
    boundary_condition="Temperature", name="StationaryWall1", temperature="AmbientTemp",
    material="Al-Extruded", radiate=True)` で固定温度壁を割り当てる。
12. セットアップ `"Setup1"` を作成し、`setup.props["Flow Regime"] = "Laminar"`、
    `setup.props["Include Gravity"] = True`、
    `setup.props["Convergence Criteria - Max Iterations"] = 500` を設定する。
13. `setup.analyze()` で解析を実行する。
14. `ipk.post.create_fieldplot_surface(assignment=["base"] + fin_names,
    quantity="Temperature", setup=f"{setup.name} : {ipk.solution_type}",
    plot_name="HeatsinkTemperature")` で、ヒートシンク表面（base+フィン11枚）の
    温度フィールドプロットを作成する。
15. プロジェクトを保存し、`release_desktop()` でAEDTを終了する。

## ヒント

- 点モニタ・面モニタは、解析実行（`setup.analyze()`）より**前に**割り当てる必要がある。
  後から追加しても、既存の解析結果には反映されない。
- `create_fieldplot_surface()`の`setup`引数は`"セットアップ名 : ソリューション種別"`の形式
  （例: `"Setup1 : SteadyState"`）で指定する。`f"{setup.name} : {ipk.solution_type}"`で
  組み立てられる。
- `duplicate_along_line()`は`(成功フラグ, 複製されたオブジェクト名のリスト)`のタプルを返す。
  このリストを使うと、個々のフィン名を手で列挙しなくてもフィールドプロットの対象に含められる。

## 評価基準

- [ ] AEDTがIcepak SteadyStateで起動し、`ex01_heatsink`（normal）と同じモデル・境界条件・
      Setupが作成されている
- [ ] ベース（base）に温度ポイントモニタ（`Monitor_base`）が解析実行前に割り当てられている
- [ ] 解析がエラーなく完走している
- [ ] ヒートシンク表面（base+フィン11枚）の温度フィールドプロット
      （`HeatsinkTemperature`）が作成されている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- フィールドプロットの`quantity`を`"Velocity Vector"`や`"Pressure"`に変えて、
  ヒートシンク周辺の流れ場を可視化してみてください。
- モニタを発熱面（Rectangle1）にも追加し、発熱面とベースの温度差を比較してみてください。
