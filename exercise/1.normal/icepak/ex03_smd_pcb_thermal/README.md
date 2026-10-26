# 演習3: PCB表面実装部品の熱解析（モデル作成〜解析実行）

**目安時間: 60分**

題材: 社内で作成されたIcepak熱流体解析のPCB表面実装チップ部品（SMD）サンプルモデルを着想元に、
このプロジェクト向けに構成を単純化して独自に作成。

> 面IDの特定方法（`get_faceid_from_position()`）は
> [1.normal/icepak/ex01_heatsink/](../ex01_heatsink/) で練習済みの前提で進める。

> この演習は「Icepak熱解析シリーズ」の3問目。基板上に複数の薄い層を積み重ねる
> モデリング手法と、`MeshRegion`による部位別メッシュ制御、方向ごとに異なるパディング種別を
> 指定するRegion作成、対流熱伝達係数（HTC）で壁面を定義する`assign_stationary_wall_with_htc()`を
> 新たに扱う。

## 学習目標

- 基板（PCB）の上に、銅箔・パッド・はんだ・部品本体・ダイという複数の薄い層を
  順番に積み重ねてモデル化する手法を学ぶ
- `MeshRegion`で、特定のオブジェクト群を内包するメッシュ細分化領域を作成し、
  部位ごとに異なるメッシュサイズ・最大分割レベルを指定する方法を学ぶ
- `create_region()`で、面ごとに異なる絶対値パディングを`Absolute Offset`で指定する方法を学ぶ
  （Icepakデザイン作成時に自動生成される既定の`"Region"`を削除してから作り直す点に注意）
- `assign_stationary_wall_with_htc()`で、対流熱伝達係数（HTC）を指定した壁面境界条件を
  割り当てる方法を学ぶ（`ex01_heatsink`の固定温度壁`assign_stationary_wall()`との違いに注意）
- Setupの`Radiation Model`に`"Discrete Ordinates Model"`を指定し、放射伝熱を考慮した
  解析を設定する方法を学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。
寸法・値はすべてmm単位（特記のあるものを除く）。

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

4. メッシュリージョンを3つ作成する（**Regionより先に作成する**。Regionの`Percentage Offset`
   パディングは、メッシュリージョンを含むモデル全体のbboxを基準に計算されるため）。
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
   設定し、XY面の2Dマルチレベルを指定する（PCBのような平坂形状に適した設定）。

5. 解析領域（`"Region"`）を作り直す。`Icepak`デザイン作成時に自動生成される既定の
   `"Region"`を `ipk.modeler["Region"].delete()` でいったん削除してから、
   `create_region(pad_type=["Absolute Offset"] * 6, pad_value=["25mm", "25mm", "25mm",
   "25mm", "50mm", "10mm"])` で絶対値パディングのRegionを作成する
   （パディングの並びは+X, -X, +Y, -Y, +Z, -Z。+Z方向だけ`"50mm"`、-Z方向だけ`"10mm"`、
   ±X/±Y方向は`"25mm"`という非対称な絶対値指定）。
6. Siダイ（`"Box8"`）に `assign_solid_block(object_name="Box8", power_assignment="0.05W",
   boundary_name="Block1")` で総発熱量0.05Wを割り当てる。
7. `modeler["Region"].bounding_box` から6面の中心座標を計算し、`get_faceid_from_position()`
   で各面の面IDを特定する。
8. Regionの+Z面（上面）に `assign_pressure_free_opening(assignment=[+Z面],
   boundary_name="Opening1", no_reverse_flow=True)` で圧力開口を割り当てる。
9. Regionの±X, ±Y面（4面）に `assign_pressure_free_opening(assignment=[4面],
   boundary_name="Opening2", no_reverse_flow=False)` で圧力開口を割り当てる。
10. Regionの-Z面（底面）に `assign_stationary_wall_with_htc(geometry=-Z面,
    name="StationaryWall1", thickness="30mm", material="Epoxy Resin-JSME",
    htc="10w_per_m2kel", ref_temperature="AmbientTemp", shell_conduction=True)` で、
    対流熱伝達係数10 W/m²Kの壁面境界条件を割り当てる。
11. セットアップ `"Setup1"` を作成し、`setup.props["Flow Regime"] = "Laminar"`、
    `setup.props["Include Gravity"] = True`、
    `setup.props["Radiation Model"] = "Discrete Ordinates Model"`、
    `setup.props["Convergence Criteria - Max Iterations"] = 500`、
    `setup.props["Convergence Criteria - Flow"] = "0.001"`、
    `setup.props["Convergence Criteria - Energy"] = "1e-07"`、
    `setup.props["Linear Solver Type - Pressure"] = "V"` を設定する。
12. `setup.analyze()` で解析を実行する。
13. プロジェクトを保存し、`release_desktop()` でAEDTを終了する（**ポスト処理は行わない**）。

## ヒント

- メッシュリージョンは必ずRegion作成前に作る。順序を逆にすると、Regionの
  `Percentage Offset`系パディングがメッシュリージョンを含まないbboxで計算され、
  元モデルより一回り小さい解析領域になってしまう（本演習のRegionは`Absolute Offset`
  のみを使うため影響はないが、他の演習・実務でPercentage系を使う場合は要注意）。
- `Icepak`デザインを作成すると既定で`"Region"`オブジェクトが自動生成される。
  パディングの種別・値を変えたRegionを作り直す場合は、先に
  `ipk.modeler["Region"].delete()` で削除してから`create_region()`を呼ぶ。
- `MeshRegion`の`parts`引数には実在するオブジェクト名のリストを渡す。`mr.assignment`は
  その部位を包含する`SubRegion`オブジェクトを返し、`padding_types`/`padding_values`で
  6面分のパディング（`[+X,-X,+Y,-Y,+Z,-Z]`の順）を指定する。
- `create_region()`の`pad_value`/`pad_type`は、面ごとに異なる値を指定したい場合、
  どちらも6要素のリストで渡す（スカラー1つを渡すと全面に同じ値が適用される）。
  `"Absolute Offset"`は絶対値（単位付き文字列、例えば`"25mm"`）を表す。
- `assign_stationary_wall_with_htc()`は、壁の向こう側の環境との熱のやり取りを、固定温度では
  なく「熱伝達係数（HTC）× 温度差」でモデル化する。`ex01_heatsink`の
  `assign_stationary_wall(boundary_condition="Temperature", ...)`（壁面を直接指定温度にする）
  との違いを意識する。
- `Radiation Model`に`"Discrete Ordinates Model"`を指定すると、放射伝熱を考慮した解析になる
  （`ex02_small_cabinet_fan`では`"Off"`にして放射を無視していた点と対比するとよい）。

## 評価基準

- [ ] AEDTがIcepak SteadyStateで起動し、PCB基板の上に銅箔・パッド・はんだ・部品本体・ダイが
      正しく積み重なって作成されている
- [ ] メッシュリージョン（MeshRegion1〜3）がRegion作成前に作成されている
- [ ] 既定で生成される`"Region"`が削除され、絶対値パディング（`Absolute Offset`）で
      作り直されている
- [ ] Siダイに総発熱量0.05Wが割り当てられている
- [ ] Regionの+Z面・±X/±Y面に圧力開口、-Z面にHTC壁面境界条件が割り当てられている
- [ ] セットアップ（Laminar、Gravity有効、Discrete Ordinates Model）が作成され、解析が
      エラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- Siダイの発熱量（`0.05W`）や、底面のHTC（`10w_per_m2kel`）を変えて、ダイ温度がどう変化するか
  予想してみてください。
- `Radiation Model`を`"Off"`に変えて解析し直し、放射伝熱の有無で結果にどの程度差が出るか
  比較してみてください。
