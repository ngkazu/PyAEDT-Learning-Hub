# 演習1: 差動ペア伝送線路（HFSS 3D Layout, モデル作成〜解析実行）

**目安時間: 60分**

題材: [PyAEDT Examples](https://examples.aedt.docs.pyansys.com/) の 3D Layout / EDB 系サンプルを
着想元に、差動ペア（ストリップライン）を PyEDB で作って HFSS 3D Layout で解析する構成を独自に作成。

> この演習は「差動ペア伝送線路シリーズ」の normal レベル。
> HFSS 3D Layout 自体の easy 課題（解析あり）はないが、前段として PyEDB で EDB の基本構造
> （スタックアップ・ネット・トレース・ビア）を作る easy 課題
> [`0.easy/pyedb/ex01_edb_basics`](../../../0.easy/pyedb/ex01_edb_basics/README.md) を用意している。
> EDB の組み立てに不安があれば、先にそちらを済ませてからこの課題に進むとよい。
> hard 以降では差動 S パラメータ（SDD21 など）のレポート・後処理を追加していく予定。

## 使用するパッケージ

HFSS 3D Layout（レイヤー/ECAD 構造）は、ジオメトリ作成を **PyEDB**（`from pyedb import Edb`）で行い、
解析を **PyAEDT の `Hfss3dLayout`** で行う。クラス名は
[docs/app-selection.md](../../../../docs/app-selection.md) を参照（3D Layout は `Hfss3dLayout`、EDB は `Edb`）。

## 学習目標

- PyEDB で PCB スタックアップ（信号層・誘電体層・GND 層）を定義する
- 差動ペア（平行トレース2本）と GND プレーンを作成する
- 各信号線の端に vertical gap ポートを配置する（ストリップラインに適したポート種別の選択）
- HFSS 3D Layout でセットアップと周波数スイープを作成し、解析を実行する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Edb(edbpath=AEDB_PATH, version=AEDT_VERSION)` で EDB を作成する（座標の単位は **メートル**）。
2. スタックアップを `add_layer` で作る（下から順に積層）:
   - `GND_TOP`（signal, copper, 35um）
   - `Diel_1`（dielectric, FR4_epoxy, 0.2mm, `base_layer="GND_TOP", method="add_on_top"`）
   - `SIG`（signal, copper, 35um, `base_layer="Diel_1"`）
   - `Diel_2`（dielectric, FR4_epoxy, 0.2mm, `base_layer="SIG"`）
   - `GND_BOT`（signal, copper, 35um, `base_layer="Diel_2"`）
3. SIG 層に差動ペアを2本作る（`create_trace`）。`DIFF_P` を `y=+GAP/2`、`DIFF_N` を `y=-GAP/2` に、
   長さ `LENGTH`・幅 `WIDTH` で配置する。
4. `GND_TOP` と `GND_BOT` に GND プレーン（矩形）を作る（`create_rectangle`、`net_name="GND"`）。
5. 各信号線の端に vertical gap ポートを配置する（`create_edge_port_vertical`、`hfss_type="Gap"`,
   `reference_layer="GND_TOP"`）。P 側（`trace_p`）と N 側（`trace_n`）それぞれ x=0 と x=LENGTH の
   計4ポート（例: `P_in`, `P_out`, `N_in`, `N_out`）。
   - **なぜ wave port ではないのか**: ストリップライン端の wave port は内部で同軸(coax)ポート扱いに
     なり、ポート領域内に via か bondwire を要求する。via の無い平面トレースではターミナルを形成できず
     メッシュ生成が失敗する。via 不要の vertical gap port が正しい選択。
6. `edb.save()` → `edb.close()` で保存して閉じる。
7. `Hfss3dLayout(project=AEDB_PATH, ...)` で開く。
8. `create_setup(name="MySetup")` と、`create_linear_count_sweep(setup=..., unit="GHz",
   start_frequency=0, stop_frequency=20, num_of_freq_points=201, sweep_type="Interpolating")`
   でセットアップと周波数スイープを作る。
9. `h3d.analyze_setup(name="MySetup")` で解析を実行する。
10. プロジェクトを保存し、`h3d.release_desktop()` で終了する（**ポスト処理は行わない**。hard 以降で追加）。

## ヒント

- PyEDB の座標は **メートル**（`0.040` = 40mm）。レイヤー厚は `"35um"` のように単位付き文字列でも可。
- `add_layer` の2層目以降は `base_layer="直前の層名", method="add_on_top"` を付けると積み上げられる。
- `create_trace(path_list, layer_name, width, net_name)` の `path_list` は `[[x0,y0],[x1,y1]]` の座標列。
- vertical gap ポートは `create_edge_port_vertical(prim_id=trace.id, point_on_edge=[x, y],
  port_name=..., reference_layer="GND_TOP", hfss_type="Gap")`。`prim_id` には `create_trace` の
  戻り値の `.id` を渡す。`point_on_edge` はトレース端の座標（入力端は x=0、出力端は x=LENGTH）。
- `create_linear_count_sweep` の周波数単位引数は **`unit`**（`units` ではない）。
- ストリップライン端に wave port を使うとメッシュ生成でエラーになる
  （`could not find suitable geometry to form the terminal of the coax port`）。
  ポート種別は構造に合わせて選ぶこと。

## 評価基準

- [ ] PyEDB で 5 層のスタックアップ（signal 3 / dielectric 2）が作成されている
- [ ] 差動ペア（DIFF_P / DIFF_N）と GND プレーンが作成されている
- [ ] 各信号線の端に vertical gap ポート（P_in / P_out / N_in / N_out の4ポート）が配置されている
- [ ] HFSS 3D Layout でセットアップと周波数スイープが作成されている
- [ ] 解析がエラーなく完走し、プロジェクトが保存されている

## 発展課題（任意）

- 差動線間隔 `GAP` や線幅 `WIDTH` を変えて、差動インピーダンスがどう変わるか考えてください。
- 差動 S パラメータ（SDD21 など）を見たい場合は、このシリーズの hard に進んでください。
