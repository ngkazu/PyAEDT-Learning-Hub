# 演習2: 導波管インダクティブアイリスフィルタ（高度なポスト処理）

**目安時間: 90分**

題材: [PyAEDT Examples - Inductive iris waveguide filter](https://examples.aedt.docs.pyansys.com/) を
着想元に、このプロジェクト向けに構成を単純化して独自に作成。

> ブーリアン演算（Subtract）の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex2_boolean_subtract/](../../../0.easy/common_3d/ex2_boolean_subtract/) を確認するとよい。

> この演習は「導波管アイリスフィルタシリーズ」の hard レベル。同じモデルでSetup作成〜解析実行までの
> ものが `1.normal/hfss/ex2_iris_filter/`、さらにPyVista/CSV入出力を追加したものが
> `3.expert/hfss/ex2_iris_filter_postprocessing/` にある。

## 学習目標

- `modeler.create_waveguide()` を使い、標準規格の矩形導波管（WR-90 / WG16）を作成する
- ブーリアン演算（`subtract`）で、導波管内部にインダクティブアイリス（金属フィン）を作成する
- Wave Port を2つ使った2ポート回路の S パラメータ解析を行う
- **高度なポスト処理**として、導波管内の電界分布をカットプレーンでフィールドプロットする
  （`docs/difficulty-criteria.md` の hard レベルにおける「AEDT内部ポスト処理の高度化」に相当）

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
7. セットアップを作成し（中心周波数 `10GHz` 付近）、`SaveFields=True` の周波数掃引を追加する
   （フィールドプロットにはフィールドデータの保存が必要）。
8. 解析を実行する。
9. `hfss.create_scattering()` で S11・S21 のレポートを作成する。
10. **高度なポスト処理**: 導波管の中心を通るXZ平面（y = 5.08mm）の断面に、電界強度（`Mag_E`）の
    フィールドプロットを作成する。カットプレーン用に、`modeler.create_plane()` で作成した Plane オブジェクトを
    `hfss.post.create_fieldplot_cutplane()` に渡す。
11. プロジェクトを保存し、`release_desktop()` で終了する。

## ヒント

- `create_waveguide()` の戻り値は `(waveguide_object, port1_sheet, port2_sheet)`。
  内部の空気領域は導波管作成時に自動生成・消費されるため、アイリスは自分で座標を計算して新規に作成する。
- アイリスの「穴」は、全体を覆う板から小さい板を `modeler.subtract(大きい板, 小さい板, keep_originals=False)`
  でくり抜くことで作れる。
- Wave Portの名前は `wave_port(name=...)` で指定した通りになるが、Sパラメータレポートで参照する際の
  モード名（例: `Port1:1`）が自動付与される場合がある。ポート名を手打ちするより、
  `hfss.excitation_names` で実際の励振名一覧を取得して `create_scattering()` に渡す方が安全。
- カットプレーン用のシートは `modeler.create_plane()` で作成する。**AEDTの「CutPlane」は、座標系上の
  平面（基準点＋法線ベクトル）を指す概念であり、シートオブジェクト（`create_rectangle` 等）は指定できない**。
  自作の面（シート）へのプロットには別の `post.create_fieldplot_surface()` を使う必要がある。
- フィールドプロットの `intrinsics` には解析済みの周波数（例: `{"Freq": "10GHz"}`）を指定する。
- フィールドデータは **Interpolating掃引の各周波数では保存されない**。`SaveFields=True` で保存されるのは
  アダプティブメッシュの周波数（今回は10GHz）のみなので、`create_fieldplot_cutplane` の `setup` には
  `f"{setup.name} : LastAdaptive"` を指定する（掃引名を指定するとデータが見つからずプロットが作成されない）。

## 評価基準

- [ ] WR-90（WG16）導波管が作成され、2つの開口部にWave Portが割り当てられている
- [ ] 導波管内部に2枚のインダクティブアイリスが、対称な開口部を持つ形状で作成されている
- [ ] 解析が完走し、S11・S21のレポートが作成されている
- [ ] 中心周波数付近での電界分布のフィールドプロットが作成されている

## 発展課題（任意）

- アイリスの開口部（`iris_aperture`）を変えて、S21の周波数特性がどう変わるか比較してください。
- PyVistaでの可視化やCSV入出力を試したい場合は、`3.expert/hfss/ex2_iris_filter_postprocessing/`
  （このシリーズのexpert）に進んでみてください。
