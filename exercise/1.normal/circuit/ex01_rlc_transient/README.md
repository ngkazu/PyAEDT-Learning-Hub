# 演習1: RLC直列回路の過渡解析（モデル作成〜解析実行）

**目安時間: 60分**

題材: [PyAEDT Examples - Circuit](https://examples.aedt.docs.pyansys.com/) を着想元に、
回路図API（コンポーネント配置・配線・過渡解析）の基本を学べるよう独自に構成。

> 回路図への部品配置・配線がまだ不安な場合は、先に
> [0.easy/common_schematic/ex01_circuit_basics/](../../../0.easy/common_schematic/ex01_circuit_basics/)
> で起動〜配置〜配線〜保存の基本操作を練習するとよい。

> この演習は「RLC回路シリーズ」の normal レベル。回路図（Nexxim）の自動化に初めて触れる人向け。
> hard（[`2.hard/circuit/ex01_rlc_filter_sparams`](../../../2.hard/circuit/ex01_rlc_filter_sparams/README.md)）
> では同じ R/L/C を2ポートのローパスフィルタとして構成し直し、**S パラメータ解析（S21/S11レポート）**
> を追加する。expert（[`3.expert/circuit/ex01_rlc_filter_postprocessing`](../../../3.expert/circuit/ex01_rlc_filter_postprocessing/README.md)）
> ではさらに Python 後処理（カットオフ算出・CSV・matplotlib・Touchstone出力）を追加する。

## アプリケーションの選び方

この課題は Circuit（Nexxim 回路シミュレータ）を使う。`common_schematic` グループ
（Circuit / EMIT / Twin Builder）のうち、回路図作成の基本は Circuit で学ぶ。クラス名は
[docs/app-selection.md](../../../../docs/app-selection.md) を参照（`from ansys.aedt.core import Circuit`）。

## 学習目標

- 回路図（schematic）に R・L・C・電圧源・GND を座標指定で配置する
- 部品のピン位置（`component.pins[i].location`）を使って配線する
- パルス電圧源を定義する
- 過渡解析（Transient）セットアップを作成し、解析を実行する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Circuit(design="RLC_Transient", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. 直列 RLC を横一列に配置する。`sch.create_resistor`（R1, 50ohm, `location=[0.02, 0.0]`）、
   `sch.create_inductor`（L1, 1nH=`1e-9`, `location=[0.04, 0.0]`）、
   `sch.create_capacitor`（C1, 1pF=`1e-12`, `location=[0.06, 0.0]`）。
3. `create_wire()` で R→L→C を直列に配線する（R右-L左、L右-C左）。
   各部品の左右ピン座標は `left_right()` ヘルパー（ピンを X 座標でソート）で取得できる。
4. `sch.create_voltage_pulse(name="V1", value_lists=[0, 1, 0, "1us", "1ns", "1ns", "5us", "10us"], location=[0.0, 0.0])`
   でパルス電圧源を配置する（引数は `[初期値, パルス値, 遅延, 立上り, 立下り, パルス幅, 周期]`）。
5. `sch.create_gnd(location=[0.0, -0.03])` で接地を配置する。
6. 電源+ → R左、C右 → GND、電源- → GND を配線して閉ループにする。
7. `cir.create_setup(name="Transient", setup_type="NexximTransient")` で過渡解析セットアップを作成し、
   `setup.props["TransientData"] = ["0.01us", "10us"]`（時間ステップ, 終了時間）を設定して `setup.update()` する。
8. `setup.analyze()` で解析を実行する。
9. プロジェクトを保存し、`cir.release_desktop()` でAEDTを終了する（**レポート作成などのポスト処理は
   行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- 回路図のコンポーネント作成は `cir.modeler.schematic` のメソッド群
  （`create_resistor` / `create_inductor` / `create_capacitor` / `create_voltage_pulse` /
  `create_gnd` / `create_wire`）で行う。引数名・既定値は `inspect.signature()` で確認できる。
- **ピン名は部品種類ごとに異なる**（抵抗=`terminals_0`/`terminals_1`、インダクタ=`n1`/`n2`、
  コンデンサ=`positive`/`negative`）。名前で配線すると部品ごとに分岐が必要になるため、
  `starter.py` の `left_right()` のように**ピンの座標 `pin.location` で左右を判定**すると共通化できる。
- `create_wire()` は座標のリストを受け取る。途中で曲げたい場合は中間点を挟む
  （例: `[始点, [x, y], 終点]`）。
- 過渡解析のセットアップ種別は `setup_type="NexximTransient"`。`TransientData` は
  `[時間ステップ, 終了時間]` の2要素リストで指定する。

## 評価基準

- [ ] AEDTが起動し、R1・L1・C1・V1・GND が配置されている
- [ ] 直列 RLC が電源・GND と閉ループに配線されている
- [ ] 過渡解析（NexximTransient）セットアップが作成されている
- [ ] 解析がエラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `value_lists` のパルス幅・立上り時間を変えて、回路の過渡応答がどう変わるか考えてください。
- R の値を変えて、直列RLCの減衰（オーバーダンプ/アンダーダンプ）がどう変わるか予想してください
  （共振周波数 `f = 1/(2*pi*sqrt(L*C))`、減衰の目安 `R` と `2*sqrt(L/C)` の大小）。
- 周波数ドメインでの特性（S パラメータ）を見たい場合は、このシリーズの
  [hard](../../../2.hard/circuit/ex01_rlc_filter_sparams/README.md) に進んでください。
