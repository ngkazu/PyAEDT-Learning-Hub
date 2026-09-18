# 演習2: 導波管インダクティブアイリスフィルタ（モデル作成〜解析実行）

**目安時間: 60分**

題材: [PyAEDT Examples - Inductive iris waveguide filter](https://examples.aedt.docs.pyansys.com/) を
着想元に、このプロジェクト向けに構成を単純化して独自に作成。

> ブーリアン演算（Subtract）の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex2_boolean_subtract/](../../../0.easy/common_3d/ex2_boolean_subtract/) を、
> セットアップ作成の基本操作は
> [0.easy/common_3d/ex3_setup_basics/](../../../0.easy/common_3d/ex3_setup_basics/) を確認するとよい。

> この演習は「導波管アイリスフィルタシリーズ」の normal レベル。同じモデルにポスト処理を追加したものが
> `2.hard/hfss/ex2_iris_filter/`、さらにPyVista/CSV入出力を追加したものが
> `3.expert/hfss/ex2_iris_filter_postprocessing/` にある。

## 学習目標

- `modeler.create_waveguide()` を使い、標準規格の矩形導波管（WR-90 / WG16）を作成する
- ブーリアン演算（`subtract`）で、導波管内部にインダクティブアイリス（金属フィン）を作成する
- Wave Port を2つ使った2ポート回路のセットアップを作成し、解析を実行する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Hfss(solution_type="Modal", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. 変数 `wg_length = "60mm"`, `iris_thickness = "2mm"`, `iris_aperture = "5mm"` を定義する。
3. `hfss.modeler.create_waveguide()` で、`wgmodel="WG16"`（WR-90, 内寸22.86mm×10.16mm）、
   `wg_direction_axis=2`（Z軸方向）、`wg_length="wg_length"`、`create_sheets_on_openings=True` として
   導波管を作成する。戻り値の3つ（導波管本体、開口部シート×2）を変数に保持しておく
   （開口部シートは後でWave Portに使う）。
4. 導波管の内部（内寸22.86mm×10.16mm）に、インダクティブアイリス（金属フィン）を2枚作成する。
   1枚のアイリスは以下の2ステップで作る:
   - 内寸全体を覆う銅の板（`sizes=[22.86mm, 10.16mm, iris_thickness]`）を、導波管の長さ方向の
     1/3 の位置に作成する。
   - その板から、幅22.86mm・高さ`iris_aperture`（y方向中央に配置）の穴を `subtract` でくり抜く
     （上下対称に金属が残り、中央に開口部ができる ＝ インダクティブアイリスの形状）。
   同様に、長さ方向の 2/3 の位置にも2枚目のアイリスを作成する。
5. 導波管の内部（内寸22.86mm×10.16mm）と同じサイズの空気ボリューム（`material="vacuum"`）を
   作成し、手順4で作った2枚のアイリスを `subtract`（`keep_originals=True`）でくり抜く。
   （`create_waveguide()` が内部に作った空気領域は導波管作成時の`subtract`で消えてしまうため、
   このステップを行わないと Solve Inside=True の実体がモデルに存在せず、解析が
   「At least one material assignment should have solve inside set!」で失敗する）。
6. 手順3,4で保持した2つの開口部シートに対し、`hfss.wave_port()` でそれぞれ Wave Port（`Port1`, `Port2`）を
   割り当てる。
7. セットアップを作成し（中心周波数 `10GHz` 付近）、`SaveFields=True` の周波数掃引を追加する。
   - `hfss.create_setup(name="MySetup", Frequency="10GHz", MaximumPasses=8)`
   - `setup.add_sweep(name="Sweep1", sweep_type="Interpolating", RangeStart="8GHz", RangeEnd="12GHz", SaveFields=True)`
8. `setup.analyze()` で解析を実行する。
9. プロジェクトを保存し、`hfss.release_desktop()` でAEDTを終了する（**レポート作成・フィールドプロットなどの
   ポスト処理は行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- `create_waveguide()` の戻り値は `(waveguide_box, port1_sheet, port2_sheet)` の3要素タプル。
- アイリスの位置は `z_position_expr` に `"wg_length/3"` のような変数式をそのまま渡せる。
- `subtract(blank, tool, keep_originals=...)` は `blank` から `tool` の形状をくり抜く。
  `keep_originals=False` にすると `tool` 側のオブジェクトは削除される。
- `SaveFields=True` は本演習では未使用だが、hardで同じモデルに対しフィールドプロットを追加する際に
  必要になるため、ここで付けておく。

## 評価基準

- [ ] AEDTが起動し、導波管とアイリスが作成されている
- [ ] AirRegion（空気ボリューム）がアイリスとの重複なく作成されている
- [ ] Wave Port（Port1, Port2）が割り当てられている
- [ ] セットアップと周波数掃引が作成されている
- [ ] 解析がエラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `iris_aperture` の値を変えて、通過帯域の中心周波数や帯域幅がどう変化するか確認してみてください。
- S11/S21のレポートやフィールドプロットを見たい場合は、`2.hard/hfss/ex2_iris_filter/`
  （このシリーズのhard）に進んでみてください。
