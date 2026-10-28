# 演習1: ブスバー解析（モデル作成〜解析実行）

**目安時間: 60分**

題材: `AEDT-AI-Assistant/examples/q3d/busbar.py`（Q3D Extractorでのブスバー抵抗・インダクタンス・
キャパシタンス抽出の例）を着想元に、このプロジェクト向けに構成を単純化して独自に作成。

> モデル作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex01_basic_operations/](../../../0.easy/common_3d/ex01_basic_operations/) を確認するとよい。

> この演習は「ブスバー解析シリーズ」の normal レベル。同じモデルに縮退行列・レポート作成を追加したものが
> [2.hard/q3d/ex01_busbar_matrixreport/](../../../2.hard/q3d/ex01_busbar_matrixreport/)、さらにPyVista/CSV入出力を追加したものが
> [3.expert/q3d/ex01_busbar_postprocessing/](../../../3.expert/q3d/ex01_busbar_postprocessing/) にある。

## 学習目標

- Q3D Extractorのモデリング手法（`create_polyline()`の矩形断面オプションで線状導体を作る）を理解する
- `auto_identify_nets()`でネットを自動識別し、`source()`/`sink()`で電流の入出力端子を割り当てる方法を学ぶ
- Q3D Extractor特有の`AdaptiveFreq`ベースのSetup・`create_linear_step_sweep()`によるスイープ作成パターンを学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Q3d(version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動し、
   `q3d.modeler.model_units = "mm"` を設定する。
2. 3本のブスバーを `create_polyline(points=..., xsection_type="Rectangle", xsection_width="5mm",
   xsection_height="1mm", material=...)` で作成する。寸法・経路は下表の通り（Z座標はすべて0）。

   | バー | 名前 | 材質 | 経路（mm） |
   |---|---|---|---|
   | Bar1 | `"Bar1"` | `copper` | `[0, 0, 0]` → `[-100, 0, 0]` |
   | Bar2 | `"Bar2"` | `aluminum` | `[0, -15, 0]` → `[-150, -15, 0]` |
   | Bar3 | `"Bar3"` | `copper` | `[0, -30, 0]` → `[-175, -30, 0]` → `[-175, -10, 0]` |

3. 基板を `modeler.create_box(origin=[50, 30, -0.5], sizes=[-250, -100, -3], name="substrate",
   material="FR4_epoxy")` で作成する。
4. `q3d.auto_identify_nets()` でネットを自動識別する。
5. 各バーにソース・シンクを割り当てる（`direction` は `q3d.axis_directions` の列挙値を使う）。

   | バー | ソース（名前・方向） | シンク（名前・方向） |
   |---|---|---|
   | Bar1 | `"Source1"` / `XPos` | `"Sink1"` / `XNeg` |
   | Bar2 | `"Source2"` / `XPos` | `"Sink2"` / `XNeg` |
   | Bar3 | `"Source3"` / `XPos` | `"Sink3"` / `YPos` |

6. セットアップを `q3d.create_setup(name="MySetup", props={"AdaptiveFreq": "1000MHz"})` で作成する。
7. `setup.create_linear_step_sweep(name="my_sweep", unit="GHz", start_frequency=0, stop_frequency=10,
   step_size=1, sweep_type="Discrete", save_fields=True)` で周波数スイープを追加する
   （`sweep_type="Interpolating"`は各点を実解析せず補間するため`SaveFields`が常に`False`に強制され、
   hard以降でマトリクスデータを周波数ごとに取得できなくなる。`Discrete`＋`save_fields=True`にしておく）。
8. `q3d.analyze()` で解析を実行する。
9. プロジェクトを保存し、`q3d.release_desktop()` でAEDTを終了する（**縮退行列作成・レポート作成などの
   ポスト処理は行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- `create_polyline()` の `xsection_type="Rectangle"` は、矩形断面を持つ線状導体（ブスバーやケーブルの
  芯線など）を作る際の定型パターン。断面サイズは `xsection_width`/`xsection_height` で指定する。
- `source()`/`sink()` の `assignment` にはオブジェクト名をそのまま渡せる。`direction` には
  `q3d.axis_directions.XPos` のように、`Analysis` クラスが公開する軸方向の列挙値
  （`XNeg`/`YNeg`/`ZNeg`/`XPos`/`YPos`/`ZPos`）を使う。面IDを自分で調べなくても、
  「指定した軸方向で最大/最小になる面」が自動的に選ばれる。
- Q3D Extractorの `create_setup()` は、他ソルバーの `create_setup(name=..., **kwargs)` と違い、
  `props` 辞書でプロパティをまとめて渡す使い方がより確実（`AdaptiveFreq` はこの辞書のキーとして渡す）。
- `create_linear_step_sweep()` は `setup.add_sweep()` と異なり、開始・終了周波数とステップ幅を
  そのまま引数で渡せる専用メソッド（`SetupQ3D` 固有）。
- `create_linear_step_sweep()` は `sweep_type="Interpolating"` の場合、各周波数点を個別に解かず補間で
  済ませるため、`save_fields` に何を渡しても内部的に `SaveFields` は `False` に強制される（PyAEDTの実装上の仕様）。
  hard以降でマトリクスデータ（容量・インダクタンス）を周波数ごとに取得したいため、本演習では
  `sweep_type="Discrete"` と `save_fields=True` を使う。

## 評価基準

- [ ] AEDTがQ3D Extractorで起動し、3本のブスバー・基板が作成されている
- [ ] `auto_identify_nets()` でネットが識別されている
- [ ] 各バーにソース・シンクが割り当てられている
- [ ] セットアップと周波数スイープが作成されている
- [ ] 解析がエラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- バーの間隔・断面寸法を変えて、キャパシタンス・インダクタンスの値がどう変化するか予想してみてください。
- 複数バーを束ねた等価回路（縮退行列）やレポート作成をしたい場合は、このシリーズのhard
  （[2.hard/q3d/ex01_busbar_matrixreport/](../../../2.hard/q3d/ex01_busbar_matrixreport/)）に進んでみてください。
