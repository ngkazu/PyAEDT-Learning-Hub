# 演習2: 小型筐体のファン冷却解析（モデル作成〜解析実行）

**目安時間: 60分**

題材: 社内で作成されたIcepak熱流体解析の小型筐体サンプルモデル（ファン冷却・native Fan
コンポーネントを含む）を着想元に、このプロジェクト向けに構成を簡略化して独自に作成
（筐体は省略し、PCB・発熱部品・ヒートシンク・Fanコンポーネントを解析領域内に直接配置）。

> ヒートシンクのフィン作成（`duplicate_along_line()`）や面IDの特定方法は
> [1.normal/icepak/ex01_heatsink/](../ex01_heatsink/) で練習済みの前提で進める。
> 解析領域の作成（`create_region()`）の基本操作は
> [0.easy/common_3d/ex19_create_region/](../../../0.easy/common_3d/ex19_create_region/) で練習できる。

> この演習は「Icepak熱解析シリーズ」の2問目。`ex01_heatsink`とは異なる境界条件
> （`assign_solid_block()`、`assign_conducting_plate_with_thickness()`）と、
> native Fanコンポーネント（`create_fan()`）を新たに扱う。
> 同じモデルに温度フィールドプロット・モニタを追加したものが
> [2.hard/icepak/ex02_small_cabinet_fan_fieldplot/](../../../2.hard/icepak/ex02_small_cabinet_fan_fieldplot/)、
> さらにPython後処理（CSV入出力・PyVista可視化）を追加したものが
> [3.expert/icepak/ex02_small_cabinet_fan_postprocessing/](../../../3.expert/icepak/ex02_small_cabinet_fan_postprocessing/)
> にある。

## 学習目標

- `assign_solid_block()`で、ソリッド形状そのものに総発熱量を割り当てる方法を学ぶ
  （`ex01_heatsink`の`assign_source()`は面への割り当てだった点との違いに注意）
- `assign_conducting_plate_with_thickness()`で、薄いダイアタッチ層を厚み・材料を指定した
  伝導板として簡略化してモデル化する方法を学ぶ
- `create_fan()`で、native Fanコンポーネント（送風機）を解析領域内に配置する方法を学ぶ
- Fanコンポーネントの`props["NativeComponentDefinitionProvider"]`を直接書き換えて、
  流量圧力特性曲線（ファンカーブ）を`update()`で反映する方法を学ぶ
- Setupの`Flow Regime`（乱流/層流）・`Radiation Model`・`Include Gravity`の組み合わせを変えて
  解析条件を設定する方法を学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。
寸法・値はすべてmm単位（特記のあるものを除く）。

1. `Icepak(design="IcepakDesign1", solution_type="SteadyState", version=AEDT_VERSION,
   new_desktop=True, non_graphical=False)` で起動し、`modeler.model_units = "mm"` を設定する。
2. `edit_design_settings(ambient_temperature="20cel", gravity_dir=2)` で、周囲温度20℃・
   重力方向-Zを設定する。
3. PCB基板（`"Box5"`）を `origin=[15, 5, 5]`, `sizes=[70, 70, 1.6]`, `material="fr4_epoxy"` で
   作成する。
4. 発熱部品（`"Box6"`）を `origin=[50, 40, 6.6]`, `sizes=[20, 20, 4]`,
   `material="ceramic_material"` で作成する。
5. 発熱部品の上面（Z=10.6の位置）に、ダイアタッチ割り当て用の20×20mmシート
   （`"Box6_ObjectFromFace1"`）を `create_rectangle(orientation="XY",
   origin=[50, 40, 10.6], sizes=[20, 20])` で作成する。
6. ヒートシンクを作成する（`ex01_heatsink`と同じ要領）。
   - ベース（`"Box7"`）: `origin=[40, 30, 10.6]`, `sizes=[40, 40, 5]`, `material="al-extruded"`
   - フィン1枚目（`"Box8"`）: `origin=[40, 30, 15.6]`, `sizes=[40, 1.5, 15]`,
     `material="al-extruded"`。`duplicate_along_line(assignment="Box8",
     vector=[0, 5.5, 0], clones=8)` でY方向にピッチ5.5mmで8枚に複製する。
7. 解析領域（`"Region"`）を作り直す。Icepakデザイン作成時に自動生成される既定の
   `"Region"`を `ipk.modeler["Region"].delete()` でいったん削除してから、
   `create_region(pad_value=[58, 58, 48, 48, 28, 28], pad_type="Absolute Offset")` で
   作成する（パディングの並びは+X, -X, +Y, -Y, +Z, -Z。`create_fan()`が許容する`radius`上限は
   作成時点のRegion・モデル全体の寸法に依存するため、**必ずFanより先にRegionを作る**）。
8. `create_fan(name="Fan1", shape="Circular", cross_section="YZ", radius="10mm",
   hub_radius="5mm", origin=[0, 60, 20])` で送風機（Fanコンポーネント）を配置する。
   続けて `fan.props["NativeComponentDefinitionProvider"]`
   の`"DimUnits"`を`["m3_per_s", "pascal"]`、`"X"`を`["0", "0.005", "0.01", "0.015"]`、
   `"Y"`を`["50", "40", "20", "0"]`に書き換えて流量圧力カーブを設定し、`fan.update()`で
   反映する（`Radius`/`HubRadius`はここで変更しない）。
9. 発熱部品に `assign_solid_block(object_name="Box6", power_assignment="10W",
   boundary_name="Block1")` で総発熱量10Wを割り当てる。
10. ダイアタッチシートに `assign_conducting_plate_with_thickness(obj_plate=
    "Box6_ObjectFromFace1", boundary_name="ConductingPlate1", total_power="0W",
    thickness="0.02mm", solid_material="Die_attach_material")` で、厚さ0.02mmの
    伝導板を割り当てる。
11. Regionの±X面を`get_faceid_from_position()`で特定し、
    `assign_pressure_free_opening(assignment=[+X面, -X面], boundary_name="Opening1",
    no_reverse_flow=False)` で圧力開口を割り当てる。
12. セットアップ `"Setup1"` を作成し、`setup.props["Flow Regime"] = "Turbulent"`、
    `setup.props["Include Gravity"] = False`、`setup.props["Radiation Model"] = "Off"`、
    `setup.props["Convergence Criteria - Max Iterations"] = 500` を設定する。
13. `setup.analyze()` で解析を実行する。
14. プロジェクトを保存し、`release_desktop()` でAEDTを終了する（**ポスト処理は行わない**）。

## ヒント

- `assign_solid_block()`は面ではなくオブジェクト名（ソリッド全体）に対して発熱量を割り当てる。
  `ex01_heatsink`の`assign_source()`（面に対する総発熱量）との使い分けを意識する。
- `assign_conducting_plate_with_thickness()`は、実際には薄すぎてメッシュ化が難しい層
  （ダイアタッチ・TIM等）を、厚み・熱伝導率を指定した仮想的な伝導層として近似するための機能。
- `create_fan()`は、流量-圧力特性曲線やケース形状を細かくカスタマイズする引数を持たない
  簡略版のAPI。`radius`には上限があり、**作成時点でのRegion（またはモデル全体）の
  バウンディングボックスが小さいほど、許容される`radius`上限も小さくなる**という
  ネイティブコンポーネントの既知の制約がある。そのため本演習ではRegionをFanより先に作成し、
  Regionを削除したおた【Fanを作らないようにする。流量圧力カーブを変更したい場合は、
  戻り値（`NativeComponentObject`）の`props["NativeComponentDefinitionProvider"]`辞書を
  直接書き換えて`update()`を呼ぶ。ただし`Radius`/`HubRadius`は作成後に変更すると、
  Fanのケース形状（`*_Case`）と流路形状（`*_Passage`）の寸法が食い違い
  「Parts ... and ... intersect」「The fan flow region is bigger than the case」という
  検証エラーになるため、**形状サイズは作成時の値から変更しない**。
- `cross_section="YZ"`は、Fanの円盤面がYZ平面上にあり、X方向に送風することを意味する。
- Icepakデザインを作成すると既定で`"Region"`オブジェクトが自動生成される。
  パディングの種別・値を変えたRegionを作り直す場合は、先に
  `ipk.modeler["Region"].delete()`で削除してから`create_region()`を呼ぶ。
- Setupの`Radiation Model`を`"Off"`にすると放射伝熱を計算しない（`ex01_heatsink`の
  固定温度壁での`radiate=True`とは対照的な設定）。

## 評価基準

- [ ] AEDTがIcepak SteadyStateで起動し、PCB・発熱部品・ヒートシンク（ベース+フィン8枚）が
      作成されている
- [ ] 解析領域（Region）が、既定Regionを削除したうえで、Fanより先に作り直されている
- [ ] Fanコンポーネントが配置され、流量圧力カーブ（`DimUnits`/`X`/`Y`）が設定されている
- [ ] 発熱部品にBlock（総発熱量10W）、ダイアタッチシートにConducting Plateが割り当てられている
- [ ] Regionの±X面に圧力開口が割り当てられている
- [ ] セットアップ（Turbulent、Gravity無効、Radiation無効）が作成され、解析がエラーなく完走し、
      プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- Fanの`radius`や配置位置を変えて、筐体内の温度分布がどう変化するか予想してみてください。
- `assign_conducting_plate_with_thickness()`の`thickness`や`solid_material`を変えて、
  ダイアタッチの熱抵抗の影響を確認してみてください。
