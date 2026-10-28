# 演習1: EDB の基本構造（スタックアップ → ネット → トレース → ビア）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。HFSS 3D Layout（レイヤー/ECAD 構造）のジオメトリ作成を担う
**PyEDB** の基本操作を、自分の手で組み立てて身につける。

## アプリケーションの選び方

この演習は **PyEDB**（`from pyedb import Edb`）だけを使い、AEDT アプリケーションの起動も解析も行わない。
HFSS 3D Layout では、ジオメトリ（スタックアップ・配線・ビアなど ECAD 構造）を PyEDB で作り、
解析を PyAEDT の `Hfss3dLayout` で行う。この easy 課題はその前半（EDB 構造の作成）に集中する。
クラス名は [docs/app-selection.md](../../../../docs/app-selection.md) を参照（3D Layout は `Hfss3dLayout`、EDB は `Edb`）。

> この演習は PyEDB（HFSS 3D Layout のジオメトリ作成を担う）の easy レベル。解析は行わず、
> EDB の基本構造を作る手順だけを学ぶ。
> ポート配置やセットアップ・解析の実行は normal（`1.normal/hfss_3d_layout/`）に進んでから扱う。

## 学習目標

- PyEDB で EDB を作成・保存する一連の流れを身につける
- スタックアップ（信号層・誘電体層）を下から順に積み上げる
- ネット（配線の論理名）を作成する
- トレース（信号配線）と GND プレーン（矩形）を作成する
- パッドスタック定義を作り、ビア（層をまたぐ縦の接続）を配置する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください（**解析は行わない**）。

1. `Edb(edbpath=AEDB_PATH, version=AEDT_VERSION)` で EDB を作成する（座標の単位は **メートル**）。
2. スタックアップを `add_layer` で作る（下から順に積層）:
   - `TOP`（signal, copper, 35um）
   - `Diel`（dielectric, FR4_epoxy, 0.2mm, `base_layer="TOP", method="add_on_top"`）
   - `BOTTOM`（signal, copper, 35um, `base_layer="Diel", method="add_on_top"`）
3. ネットを2つ作る（`find_or_create_net`）: `SIG` と `GND`。
4. `TOP` 層に信号トレースを作る（`create_trace`、`net_name="SIG"`、長さ `TRACE_LEN`・幅 `TRACE_WIDTH`）。
5. `BOTTOM` 層に GND プレーン（矩形）を作る（`create_rectangle`、`net_name="GND"`）。
6. パッドスタック定義 `VIA_SIG` を作る（`padstacks.create`、穴径 0.2mm / パッド径 0.4mm /
   アンチパッド径 0.6mm、`start_layer="TOP"`, `stop_layer="BOTTOM"`）。
7. トレース終端 `[TRACE_LEN, 0]` にビアを配置する（`padstacks.place`、`definition_name="VIA_SIG"`,
   `net_name="SIG"`）。
8. `edb.save()` → `edb.close()` で保存して閉じる。

## ヒント

- PyEDB の座標は **メートル**（`0.010` = 10mm）。層厚やビア寸法は `"35um"` / `"0.2mm"` のように
  単位付き文字列で指定できる。
- `add_layer` は最初の層（`TOP`）だけ `base_layer` / `method` を付けない。2層目以降は
  `base_layer="直前の層名", method="add_on_top"` を付けると上に積み上げられる。
- `create_trace(path_list, layer_name, width, net_name)` の `path_list` は `[[x0,y0],[x1,y1]]` の座標列。
- ビアは「定義」と「配置」の2段階。まず `padstacks.create(...)` で **パッドスタック定義**
  （穴・パッド・貫通範囲）を作り、次に `padstacks.place(position=..., definition_name=..., net_name=...)`
  でその定義を位置に **配置** する。
- `find_or_create_net` は同名ネットがあれば再利用、なければ新規作成する。

## 評価基準

- [ ] EDB が作成され、`edb_basics.aedb` として保存されている
- [ ] 3層のスタックアップ（signal 2 / dielectric 1: TOP / Diel / BOTTOM）が作成されている
- [ ] ネット `SIG` と `GND` が作成されている
- [ ] `TOP` に信号トレース、`BOTTOM` に GND プレーンが作成されている
- [ ] パッドスタック定義 `VIA_SIG` が作られ、トレース終端にビアが1本配置されている

## 発展課題（任意）

- トレースを分岐させて複数のビアを配置し、配線が層をまたいで繋がる様子を作ってみてください。
- 生成した `edb_basics.aedb` を `Hfss3dLayout(project=AEDB_PATH, ...)` で開き、GUI 上で
  スタックアップやビアがどう見えるか確認してみてください（normal 課題への橋渡し）。
