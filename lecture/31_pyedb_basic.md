# PyEDBの基礎（スタックアップ・ネット・配線・ビア）

[00_environment_setup.md](00_environment_setup.md)〜[14_post_processing.md](14_post_processing.md) は
**PyAEDT**（`ansys.aedt.core`）を中心に扱うノートでした。このノートは、レイアウト・基板（ECAD）領域を
扱う別パッケージ **PyEDB**（`pyedb`）に絞った基礎ノートです。番号を `31` として独立させているのは、
PyAEDTの基本講義（`00`・`01`・`11`〜`14`）とは別トラックで、HFSS 3D Layout を使う人だけが読めばよい内容だからです
（`exercise/0.easy/common_3d` などPyAEDT側だけの課題を進める人は読む必要がありません）。

対応する演習は [exercise/0.easy/pyedb/ex01_edb_basics/](../exercise/0.easy/pyedb/ex01_edb_basics/)
（easy、解析なし）と [exercise/1.normal/hfss_3d_layout/ex01_diff_pair/](../exercise/1.normal/hfss_3d_layout/ex01_diff_pair/)
（normal、ポート配置〜解析実行）です。このノートを読んでから演習に進むと理解しやすくなります。

---

## 1. PyEDBとは何か

### 1.1 PyAEDTとの役割分担

PyAEDTのアプリオブジェクト（`Hfss`, `Maxwell3d` など）は、AEDTの「3D Modeler」でジオメトリを
作ることを前提にした設計です。一方、HFSS 3D Layout が扱うのはPCB・パッケージ・ICのような
**レイヤー構造（ECAD: Electronics Computer-Aided Design）**で、スタックアップ・配線パターン・
ビア・コンポーネントといった、3D Modelerとは全く異なる概念で構成されています。

この「レイヤー構造の作成・編集」を担当するのが **PyEDB**（`pyedb` パッケージ、`from pyedb import Edb`）
です。PyEDBは**EDB（Electronics Database）**と呼ばれるデータベース形式（`.aedb` フォルダ）を直接
操作します。`.aedb` は HFSS 3D Layout がプロジェクトとして開くファイル形式そのものです。

```
PyEDB（pyedb）          … EDB(.aedb) の作成・編集（スタックアップ、ネット、配線、ビア、ポート）
PyAEDT の Hfss3dLayout … EDB(.aedb) を開いて解析（セットアップ作成、解析実行、結果の後処理）
```

典型的な流れは次の通りです。

```python
from pyedb import Edb
from ansys.aedt.core import Hfss3dLayout

# 1. PyEDBでジオメトリ（EDB構造）を作る
edb = Edb(edbpath="my_board.aedb", version="2026.1")
# ... スタックアップ、ネット、配線、ビア、ポートを作る ...
edb.save()
edb.close()

# 2. PyAEDTのHfss3dLayoutで開いて解析する
h3d = Hfss3dLayout(project="my_board.aedb", version="2026.1")
h3d.create_setup(name="MySetup")
h3d.analyze_setup(name="MySetup")
```

**重要**: PyEDBでの作業が終わったら必ず `edb.save()` → `edb.close()` を呼んでから
`Hfss3dLayout` で開くこと。`close()` を呼ばずに終了すると `.aedt.lock` が残り、
次に開こうとしたときに「Project is locked」エラーになる（詳しくは §5）。

### 1.2 座標の単位はメートル

PyAEDTの3D Modelerでは `"10mm"` のような単位付き文字列で寸法を指定できますが、PyEDBの
**座標（位置）は基本的にメートル単位の数値**です。層の厚みなど一部のプロパティは
`"35um"` のような単位付き文字列も使えます。

```python
LENGTH = 0.040   # 40mm を意味する（メートル）
WIDTH = 0.0002   # 0.2mm を意味する
```

単位を書き忘れてミリメートルのつもりで `40` と書いてしまうと、意図せず40メートルの
配線になってしまう、というのがPyEDBで最初につまずきやすいポイントです。

---

## 2. スタックアップ（層構造）

PCBやパッケージは、信号層・誘電体層・GND層などが積み重なった「層構造」を持ちます。
PyEDBではこれを `edb.stackup.add_layer(...)` で下から順に積み上げて定義します。

```python
edb.stackup.add_layer(
    "TOP", layer_type="signal", material="copper", thickness="35um"
)
edb.stackup.add_layer(
    "Diel",
    base_layer="TOP",
    method="add_on_top",
    layer_type="dielectric",
    material="FR4_epoxy",
    thickness="0.2mm",
)
edb.stackup.add_layer(
    "BOTTOM",
    base_layer="Diel",
    method="add_on_top",
    layer_type="signal",
    material="copper",
    thickness="35um",
)
```

ポイント:

- **最初の層だけ** `base_layer` / `method` を付けない。2層目以降は
  `base_layer="直前の層名", method="add_on_top"` を指定すると、その層の上に積み上げられる。
- `layer_type` は `"signal"`（導体層。トレースやプレーンを置く）と `"dielectric"`（誘電体層。
  信号層の間を埋める絶縁材）の2種類が基本。
- 層名（`"TOP"`, `"BOTTOM"` など）は以降、配線やビアを配置するときに `layer_name` として参照する。
- 作成済みの層一覧は `edb.stackup.layers`（辞書、キーが層名）で確認できる。

GND層と信号層の間に誘電体層を挟んだ「signal / dielectric / signal / dielectric / signal」
という5層構成にすると、信号層が上下をGNDで挟まれた**ストリップライン**構造になります
（[exercise/1.normal/hfss_3d_layout/ex01_diff_pair/](../exercise/1.normal/hfss_3d_layout/ex01_diff_pair/)
で扱う構造）。

---

## 3. ネット（配線の論理名）

**ネット**は、配線やプレーンに付ける論理的な名前です。同じネット名を持つ配線・プレーン・ビアは、
電気的に同じ信号（または同じ電位）として扱われます。PyAEDTの設計変数とは別物で、
回路図のネットリストに近い概念です。

```python
edb.nets.find_or_create_net(net_name="SIG")
edb.nets.find_or_create_net(net_name="GND")
```

`find_or_create_net` は「同名のネットが既にあればそれを返し、なければ新規作成する」という
挙動なので、何度呼んでも安全です（重複作成されない）。実際には、配線やプレーンを作成する際に
`net_name=` 引数で指定すれば、そのネットが自動的に作られるため、明示的に先に呼ばなくても
動作することが多いですが、「このEDBにどんなネットがあるべきか」を最初に整理しておくと
設計の見通しがよくなります。

作成済みネット一覧は `edb.nets.nets`（辞書、キーがネット名）で確認できます。

---

## 4. 配線（トレース）とプレーン

### 4.1 トレース（信号配線）

信号層の上に引く線状の配線は `edb.modeler.create_trace(...)` で作成します。

```python
edb.modeler.create_trace(
    [[0, 0], [0.010, 0]],   # [[x0, y0], [x1, y1]] の座標列（メートル）
    layer_name="TOP",
    width="0.2mm",
    net_name="SIG",
)
```

- 第1引数は経路の座標列。2点なら直線、3点以上なら折れ線になる。
- `width` は線幅。文字列（単位付き）でも数値（メートル）でも指定できる。
- 戻り値はトレースを表すプリミティブオブジェクトで、`.id` 属性を持つ（後述のビア配置や
  ポート作成で、どのトレースの、どの位置に作業するかを指定するために使う）。

### 4.2 プレーン（GNDなどの面）

GNDプレーンのような面形状は `edb.modeler.create_rectangle(...)` で作成します。

```python
edb.modeler.create_rectangle(
    "TOP",
    net_name="GND",
    lower_left_point=[-0.005, -0.005],
    upper_right_point=[0.045, 0.005],
)
```

第1引数は層名、`lower_left_point` / `upper_right_point` で矩形の対角2点を指定します
（こちらもメートル単位）。円形や多角形のプレーンが必要な場合は `create_circle` や
`create_polygon` といった類似メソッドもあります。

---

## 5. ビア（層をまたぐ縦の接続）

ビアは、層をまたいで配線を接続する縦方向の導体です。PyEDBでは**「定義」と「配置」の2段階**で
作成します。

### 5.1 パッドスタック定義を作る

まず、穴径・パッド径・アンチパッド径などを決めた「パッドスタック定義」を1つ作ります。

```python
edb.padstacks.create(
    padstackname="VIA_SIG",
    holediam="0.2mm",       # ドリル穴径
    paddiam="0.4mm",        # パッド径（ビアのランド）
    antipaddiam="0.6mm",    # アンチパッド径（プレーン層でのクリアランス穴）
    start_layer="TOP",
    stop_layer="BOTTOM",
)
```

- `start_layer` / `stop_layer` で、このビアがどの層からどの層まで貫通するかを決める。
- 同じ定義（例えば「標準的な0.2mm径のビア」）を基板中で何度も使い回すのが普通なので、
  定義自体は配置と切り離されている。

### 5.2 定義を使ってビアを配置する

作った定義を使って、具体的な座標にビアを配置します。

```python
edb.padstacks.place(
    position=[0.010, 0],      # [x, y]（メートル）
    definition_name="VIA_SIG",
    net_name="SIG",
)
```

同じ `definition_name="VIA_SIG"` を使って、何個でもビアを配置できます。これが
「定義（1個）」と「配置（N個）」を分ける理由です。

### 5.3 よくあるつまずき

PyEDBのビア関連APIは、名前が似ていて混同しやすいので注意してください。

| 誤り | 正しい |
|---|---|
| `edb.padstacks.create_padstack(...)` | `edb.padstacks.create(...)` |
| `edb.padstacks.place_padstack(...)` | `edb.padstacks.place(...)` |

存在しないメソッド名を呼ぶとすぐに `AttributeError` になるので気づけますが、
「それっぽい名前」を推測で書かず、`dir(edb.padstacks)` でメソッド名を確認してから
書くことを勧めます（§7「APIの調べ方」も参照）。

---

## 6. ポート（励振）とメッシュ生成の落とし穴

解析のための励振（ポート）の配置は PyEDB の `edb.source_excitation` 以下のメソッドで行います。
ポート種別の選び方は構造によって変わり、**選び方を間違えるとメッシュ生成が失敗します**。

### 6.1 なぜ構造によって選ぶ必要があるのか

HFSS 3D Layout の wave port は、内部的に**同軸（coax）ポート**として扱われ、ポート領域の中に
via かボンドワイヤが存在することを前提にしています。平面トレースの端（via のない単純な
ストリップライン端など）に wave port 系のAPI（`create_wave_port`, `create_differential_wave_port`
など）を使うと、ポートのターミナル（参照導体への接続）を形成できず、次のようなエラーで
メッシュ生成に失敗します。

```
[error] could not find suitable geometry to form the terminal of the coax port;
        a via or bondwire must fall within the port region.
```

ストリップライン構造（signal層の上下をGND層で挟んだ構造）のトレース端には、via を必要としない
**vertical gap port**（`create_edge_port_vertical` に `hfss_type="Gap"` を指定）を使うのが適切です。

```python
edb.source_excitation.create_edge_port_vertical(
    prim_id=trace.id,              # create_trace の戻り値の .id
    point_on_edge=[0, 0],          # トレース端の座標
    port_name="P_in",
    reference_layer="GND_TOP",     # 参照するGND層
    hfss_type="Gap",
)
```

### 6.2 ポート種別の選び方（まとめ）

| 構造 | 適したポート種別 |
|---|---|
| ストリップライン（上下GND挟み）のトレース端 | vertical gap port（`create_edge_port_vertical`, `hfss_type="Gap"`） |
| via・ボンドワイヤを伴うパッド | wave port / coax port |
| コンポーネントのピン | コンポーネントポート（`create_port_on_component` 等） |

迷ったら「このポート領域の中に via か bondwire があるか？」を自問すると判断しやすくなります。
ない場合は wave port 系を避けてください。

---

## 7. APIの調べ方（推測しない）

PyEDBは `pyedb.grpc.database...` 以下に多数のクラスが定義されており、メソッド名が
似通っていたり、引数名がバージョンによって変わったりすることがあります。
[11_pyaedt_lecture.md](11_pyaedt_lecture.md) §2.4 と同様、推測せずその場で確認する習慣が重要です。

```python
# そのオブジェクトが持つメソッド名を確認する
print([m for m in dir(edb.padstacks) if not m.startswith("_")])

# 関数シグネチャとdocstringを確認する
import inspect
print(inspect.signature(edb.padstacks.create))
print(edb.padstacks.create.__doc__)
```

このノートに出てくるAPI（`stackup.add_layer`, `nets.find_or_create_net`, `modeler.create_trace`,
`modeler.create_rectangle`, `padstacks.create`, `padstacks.place`,
`source_excitation.create_edge_port_vertical`）は、実際にEDBを作成して動作確認した上で
書いています。

---

## 次に読むもの

- 実際に手を動かして復習する: [exercise/0.easy/pyedb/ex01_edb_basics/](../exercise/0.easy/pyedb/ex01_edb_basics/)
  （スタックアップ・ネット・トレース・ビアの作成。解析なし）
- ポート配置と解析実行まで進める: [exercise/1.normal/hfss_3d_layout/ex01_diff_pair/](../exercise/1.normal/hfss_3d_layout/ex01_diff_pair/)
  （差動ペア伝送線路、vertical gap port、セットアップ・解析実行）
- PyAEDT本体（3D Modeler系）の基本構造に戻る場合は [13_pyaedt_architecture.md](13_pyaedt_architecture.md) を参照。
- PyEDBのHelp サイト・GitHubリポジトリの歩き方は [01_help_site_guide.md](01_help_site_guide.md) §3・§4.2を参照。
- 演習を再開する場合は [exercise/README.md](../exercise/README.md) に戻ってください。
