# 演習3: PCB表面実装部品の熱解析（温度フィールドプロット・モニタ）

**目安時間: 90分**

題材: [1.normal/icepak/ex03_smd_pcb_thermal/](../../1.normal/icepak/ex03_smd_pcb_thermal/) で
作成したPCB表面実装部品モデルに、AEDT内部のポスト処理（温度ポイントモニタ・温度フィールド
プロット）を追加する。

> この演習は「Icepak熱解析シリーズ」の3問目・hardレベル。normalで作ったモデルに
> `assign_point_monitor_in_object()`と`post.create_fieldplot_surface()`を追加する。
> さらにPython側の集計・CSV入出力・PyVista可視化を追加したものが
> [3.expert/icepak/ex03_smd_pcb_thermal_postprocessing/](../../3.expert/icepak/ex03_smd_pcb_thermal_postprocessing/)
> にある。

## 学習目標

- `assign_point_monitor_in_object()`で、非常に小さいオブジェクト（Siダイ）にも温度ポイント
  モニタを割り当てられることを学ぶ（モニタは解析実行前に割り当てる必要がある点に注意）
- `post.create_fieldplot_surface()`で、積層構造（PCB・部品本体・ダイ）の複数オブジェクトの
  表面温度フィールドプロットを作成する方法を学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。
寸法・値はすべてmm単位（特記のあるものを除く）。手順1〜13は
[1.normal/icepak/ex03_smd_pcb_thermal/](../../1.normal/icepak/ex03_smd_pcb_thermal/)
と同じモデル・境界条件・Setupなので、そちらのREADMEも参照しながら進める。

1. `Icepak(design="IcepakDesign1", solution_type="SteadyState", version=AEDT_VERSION,
   new_desktop=True, non_graphical=False)` で起動し、`modeler.model_units = "mm"` を設定する。
2. `edit_design_settings(ambient_temperature="20cel", gravity_dir=2)` で、周囲温度20℃・
   重力方向-Zを設定する。
3. PCB基板とその上の層を、下から順にBoxで積み重ねて作成する。

   | 名前 | 役割 | `origin` | `sizes` | `material` |
   |---|---|---|---|---|
   | `"Box1"` | PCB基板 | `[0, 0, 0]` | `[50, 50, 1.6]` | `fr4_epoxy` |
   | `"Box2"` | ベタ銅箔 | `[0, 0, 0]` | `[50, 50, 0.035]` | `copper` |
   | `"Box3"` | 表面パッドA | `[24.5, 0, 1.565]` | `[1, 24.5, 0.035]` | `copper` |
   | `"Box4"` | 表面パッドB | `[24.5, 25.5, 1.565]` | `[1, 24.5, 0.035]` | `copper` |
   | `"Box5"` | はんだA | `[24.5, 24, 1.6]` | `[1, 0.5, 0.05]` | `solder` |
   | `"Box6"` | はんだB | `[24.5, 25.5, 1.6]` | `[1, 0.5, 0.05]` | `solder` |
   | `"Box7"` | 部品本体 | `[24.5, 24, 1.65]` | `[1, 2, 0.5]` | `ceramic_material` |
   | `"Box8"` | Siダイ（発熱源） | `[24.7, 24.5, 1.9]` | `[0.6, 1, 0.02]` | `si-typical_ref` |

4. `assign_point_monitor_in_object(name="Box8", monitor_type="Temperature",
   monitor_name="Monitor_Box8")` で、Siダイに温度ポイントモニタを割り当てる
   （**解析実行前に**割り当てること）。
5. メッシュリージョンを3つ作成する（**Regionより先に作成する**）。
   `from ansys.aedt.core.modules.mesh_icepak import MeshRegion` をインポートし、
   各リージョンごとに `MeshRegion(ipk, parts, name)` でインスタンスを作成する。作成後、
   `mr.assignment.padding_types` / `mr.assignment.padding_values` で6面分のパディング
   （すべて`"Absolute Offset"`）を設定し、`mr.manual_settings = True` にしたうえで
   `mr.settings["MaxElementSizeX/Y/Z"]` と `mr.settings["MaxLevels"]` でメッシュサイズ・
   最大分割レベルを指定し、最後に`mr.update()`を呼んで適用する。

   | 名前 | 対象オブジェクト | パディング`[+X,-X,+Y,-Y,+Z,-Z]` | メッシュサイズ | 最大レベル |
   |---|---|---|---|---|
   | `"MeshRegion1"` | `["Box1"]`（PCB） | `[0, 0, 0, 0, 0, 0]` | `1mm` | `1` |
   | `"MeshRegion2"` | `["Box5", "Box6", "Box7", "Box8"]`（部品群） | `[0.4, 0.4, 0.4, 0.4, 0.4, 0]` | `0.2mm` | `3` |
   | `"MeshRegion3"` | `["Box1"]`〜`["Box8"]`（全体） | `[4, 4, 4, 4, 4.4, 4]` | `1mm` | `1` |

   `"MeshRegion1"`はさらに2Dマルチレベルメッシュ（MLM）を有効化する。
   `mr.settings["EnforeMLMType"] = "2D"`、`mr.settings["2DMLMType"] = "2DMLM_XY"` を追加で
   設定し、XY面の2Dマルチレベルを指定する。
6. 解析領域（`"Region"`）を作り直す。`ipk.modeler["Region"].delete()` で既定の`"Region"`を
   削除してから、`create_region(pad_type=["Absolute Offset"] * 6, pad_value=["25mm",
   "25mm", "25mm", "25mm", "50mm", "10mm"])` で作成する。
7. Siダイ（`"Box8"`）に `assign_solid_block(object_name="Box8", power_assignment="0.05W",
   boundary_name="Block1")` で総発熱量0.05Wを割り当てる。
8. `modeler["Region"].bounding_box` から6面の中心座標を計算し、`get_faceid_from_position()`
   で各面の面IDを特定する。
9. Regionの+Z面（上面）に `assign_pressure_free_opening(assignment=[+Z面],
   boundary_name="Opening1", no_reverse_flow=True)` で圧力開口を割り当てる。
10. Regionの±X, ±Y面（4面）に `assign_pressure_free_opening(assignment=[4面],
    boundary_name="Opening2", no_reverse_flow=False)` で圧力開口を割り当てる。
11. Regionの-Z面（底面）に `assign_stationary_wall_with_htc(geometry=-Z面,
    name="StationaryWall1", thickness="30mm", material="Epoxy Resin-JSME",
    htc="10w_per_m2kel", ref_temperature="AmbientTemp", shell_conduction=True)` で、
    対流熱伝達係数10 W/m²Kの壁面境界条件を割り当てる。
12. セットアップ `"Setup1"` を作成し、`setup.props["Flow Regime"] = "Laminar"`、
    `setup.props["Include Gravity"] = True`、
    `setup.props["Radiation Model"] = "Discrete Ordinates Model"`、
    `setup.props["Convergence Criteria - Max Iterations"] = 500`、
    `setup.props["Convergence Criteria - Flow"] = "0.001"`、
    `setup.props["Convergence Criteria - Energy"] = "1e-07"`、
    `setup.props["Linear Solver Type - Pressure"] = "V"` を設定する。
13. `setup.analyze()` で解析を実行する。
14. `ipk.post.create_fieldplot_surface(assignment=["Box1", "Box7", "Box8"],
    quantity="Temperature", setup=f"{setup.name} : {ipk.solution_type}",
    plot_name="PcbTemperature")` で、PCB・部品本体・Siダイ表面の温度フィールドプロットを
    作成する。
15. プロジェクトを保存し、`release_desktop()` でAEDTを終了する。

## ヒント

- 点モニタは、解析実行（`setup.analyze()`）より**前に**割り当てる必要がある。
  後から追加しても、既存の解析結果には反映されない。
- Siダイ（Box8）は`0.6×1×0.02mm`と非常に小さいオブジェクトだが、
  `assign_point_monitor_in_object()`はオブジェクトの重心に監視点を置くため、
  サイズによらず問題なく動作する。
- `create_fieldplot_surface()`の`setup`引数は`"セットアップ名 : ソリューション種別"`の形式
  （例: `"Setup1 : SteadyState"`）で指定する。`f"{setup.name} : {ipk.solution_type}"`で
  組み立てられる。

## 評価基準

- [ ] AEDTがIcepak SteadyStateで起動し、`ex03_smd_pcb_thermal`（normal）と同じモデル・
      境界条件・Setupが作成されている
- [ ] Siダイ（Box8）に温度ポイントモニタ（`Monitor_Box8`）が解析実行前に割り当てられている
- [ ] 解析がエラーなく完走している
- [ ] PCB・部品本体・Siダイ表面の温度フィールドプロット（`PcbTemperature`）が作成されている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- フィールドプロットの`quantity`を`"Pressure"`や`"Velocity Vector"`に変えて、
  PCB表面の流れ場を可視化してみてください。
- モニタをPCB基板（Box1）にも追加し、ダイとPCBの温度差（熱抵抗の目安）を比較してみてください。
