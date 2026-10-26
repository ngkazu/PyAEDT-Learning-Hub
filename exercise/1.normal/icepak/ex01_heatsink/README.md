# 演習1: ヒートシンク熱解析（モデル作成〜解析実行）

**目安時間: 60分**

題材: 社内で作成されたIcepak熱流体解析のヒートシンクサンプルモデルを着想元に、このプロジェクト
向けに構成を整理して独自に作成。

> モデル作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex01_basic_operations/](../../../0.easy/common_3d/ex01_basic_operations/) を確認するとよい。
> 面の取得（`get_object_faces()`）の考え方は
> [0.easy/common_3d/ex11_get_faces/](../../../0.easy/common_3d/ex11_get_faces/) も参考になる
> （本演習では座標から面IDを求める `get_faceid_from_position()` を使う点が異なる）。

> この演習は「ヒートシンク熱解析シリーズ」の normal レベル。同じモデルにポスト処理を追加したものが
> `2.hard/icepak/ex01_heatsink_fieldplot/`、さらにPyVista/CSV入出力を追加したものが
> `3.expert/icepak/ex01_heatsink_postprocessing/` にある（いずれも準備中）。
> 別の境界条件（`assign_solid_block()`、`assign_conducting_plate_with_thickness()`）や
> native Fanコンポーネントを扱う演習は
> [1.normal/icepak/ex02_small_cabinet_fan/](../ex02_small_cabinet_fan/)、
> 多層基板モデリングとHTC壁面を扱う演習は
> [1.normal/icepak/ex03_smd_pcb_thermal/](../ex03_smd_pcb_thermal/) にある。

## 学習目標

- Icepakの`SteadyState`（定常熱流体）ソリューションタイプの基本的な使い方を学ぶ
- `duplicate_along_line()`で、等間隔に並んだ繰り返し形状（放熱フィン）を作る
- `assign_source()`で、面に総発熱量（Total Power）を割り当てる
- `assign_pressure_free_opening()`/`assign_stationary_wall()`で、解析領域（Region）の境界条件
  （圧力開口・固定温度壁）を設定する
- `edit_design_settings()`で、周囲温度・重力方向など設計全体の設定を行う

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。
寸法・値はすべてmm単位（特記のあるものを除く）。

1. `Icepak(design="IcepakDesign1", solution_type="SteadyState", version=AEDT_VERSION,
   new_desktop=True, non_graphical=False)` で起動し、`modeler.model_units = "mm"` を設定する。
2. `edit_design_settings(ambient_temperature="20cel", gravity_dir=2)` で、周囲温度20℃・
   重力方向-Zを設定する。
3. ベース（`"base"`）を `create_box(origin=[0, -50, -50], sizes=[10, 100, 100],
   material="Al-Extruded")` で作成する（X=0〜10が厚み、Y/Zは-50〜50の100mm角）。
4. フィンの1枚目（`"fin"`）を `create_box(origin=[10, -50, -50], sizes=[40, 5, 100],
   material="Al-Extruded")` で作成する（X=10〜50が高さ、厚み(Y)=5mm）。
   `modeler.duplicate_along_line(assignment="fin", vector=[0, 9.5, 0], clones=11)` で、
   Y方向にピッチ9.5mmで合計11枚になるよう複製する（戻り値は `(成功フラグ, 複製名のリスト)`）。
5. 発熱面シート（`"Rectangle1"`）を `create_rectangle(orientation="YZ",
   origin=[0, -50, -50], sizes=[100, 100])` で作成する（X=0のYZ平面、ベースと同じ100mm角）。
6. 解析領域（`"Region"`）を `create_region(pad_value=[25, 25, 50, 50, 50, 50],
   pad_type="Absolute Offset")` で作成する（パディングの並びは+X, -X, +Y, -Y, +Z, -Z）。
7. 発熱面に `assign_source(assignment="Rectangle1", thermal_condition="Total Power",
   assignment_value="20W", boundary_name="Source1", radiate=False)` で、総発熱量20Wの
   熱源を割り当てる。
8. `modeler["Region"].bounding_box` から得られる座標範囲を使って、Regionの6面（±X, ±Y, ±Z）
   それぞれの中心座標を計算し、`get_faceid_from_position()` で各面の面IDを特定する。
9. Regionの+Z面に `assign_pressure_free_opening(boundary_name="Opening1",
   no_reverse_flow=True)`、-Z面に `assign_pressure_free_opening(boundary_name="Opening2",
   no_reverse_flow=False)` で、それぞれ圧力開口を割り当てる（`temperature`/`pressure`は
   既定値の`"AmbientTemp"`/`"AmbientPressure"`のままでよい）。
10. Regionの±X, ±Y面（4面まとめて）に `assign_stationary_wall(geometry=<4面のリスト>,
    boundary_condition="Temperature", name="StationaryWall1", temperature="AmbientTemp",
    material="Al-Extruded", radiate=True)` で、固定温度壁を割り当てる。
11. セットアップ `"Setup1"` を作成し、`setup.props["Flow Regime"] = "Laminar"`、
    `setup.props["Include Temperature"] = True`、`setup.props["Include Flow"] = True`、
    `setup.props["Include Gravity"] = True`、
    `setup.props["Convergence Criteria - Max Iterations"] = 500` を設定する。
12. `setup.analyze()` で解析を実行する。
13. プロジェクトを保存し、`release_desktop()` でAEDTを終了する（**モニタ割り当て・レポート作成
    などのポスト処理は行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- `duplicate_along_line()` の戻り値は `(成功フラグ, 複製されたオブジェクト名のリスト)` の
  タプル。元の `"fin"` 自体は複製名のリストに含まれないため、`["fin"] + clone_names` のように
  まとめておくと、hard以降でフィン全体をまとめて参照する際に扱いやすい。
- `get_faceid_from_position(position, assignment="Region")` は、指定した座標に最も近い面の
  IDを返す。Regionの `bounding_box`（`[xmin, ymin, zmin, xmax, ymax, zmax]`）から中心座標
  （`(xmin+xmax)/2` など）を計算し、6面それぞれの中心座標を求めてから渡す。
- `assign_stationary_wall()` の `geometry` 引数は、単一の面ID・オブジェクト名だけでなく、
  リストも渡せる（複数の面をまとめて1つの境界条件にできる）。
- Icepakの解析設定は、GUIのプロパティ名（例: `"Flow Regime"`、`"Include Temperature"`）を
  そのまま `setup.props[...]` のキーとして使う。

## 評価基準

- [ ] AEDTがIcepak SteadyStateで起動し、ベース・11枚のフィン・発熱面シートが作成されている
- [ ] 解析領域（Region）が作成されている
- [ ] 発熱面にTotal Power 20Wの熱源が割り当てられている
- [ ] Regionの±Z面に圧力開口、±X/±Y面（4面）に固定温度壁が割り当てられている
- [ ] セットアップが作成され、解析がエラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- フィンの枚数（`FIN_COUNT`）やピッチ（`FIN_PITCH`）を変えて、ベース温度や排熱量がどう変化するか
  予想してみてください。
- フィン表面・ベースの温度分布を確認したい場合は、このシリーズのhard
  （`2.hard/icepak/ex01_heatsink_fieldplot/`、準備中）に進んでみてください。
