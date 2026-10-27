# 演習1: 半波整流回路（単一ダイオード）の配置（起動 → 配置 → 配線 → 保存 → 終了）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。Twin Builder固有の操作（波形タイプ指定の電圧源、
ダイオード）を自分の手で体験する。

> この演習は Twin Builder 専用の easy 課題。[0.easy/common_schematic/ex01_circuit_basics/](../../common_schematic/ex01_circuit_basics/)
> （R/L/C配置・配線。Circuit/Twin Builder共通）を先に済ませてから進めるとよい。
> ここで練習するダイオード配置は、このシリーズの
> [1.normal/twin_builder/ex01_rectifier/](../../../1.normal/twin_builder/ex01_rectifier/)
> （ブリッジ整流回路。ダイオード4個の全波整流）の前段にあたる。

## アプリケーションの選び方

この課題は Twin Builder 専用（`create_diode`はTwin Builder固有で、Circuitの基底クラスには
存在しない）。クラス名は [docs/app-selection.md](../../../../docs/app-selection.md) を参照
（`from ansys.aedt.core import TwinBuilder`）。

## 学習目標

- `create_voltage_source` の `source_type` 引数で、波形タイプ（`"EPULSE"` = 矩形パルス波）を
  指定して電圧源を配置する
- ダイオード（非線形素子）を配置する
- 電源・ダイオード・負荷・GND を直列に配線し、半波整流回路の形を作る

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. `TwinBuilder(design="HalfWave", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. `sch.create_voltage_source("V_IN", "EPULSE", 10.0, 1000.0, location=[0, 0])` で
   矩形パルス波形の電圧源を配置する（`source_type="EPULSE"`, 振幅10V, 周波数1000Hz）。
3. `sch.create_diode(name="D1", location=[10*G, 0], angle=0)` でダイオードを1個配置する
   （`G = 0.00254`、グリッド間隔）。
4. `sch.create_resistor(name="RL", value=1000, location=[20*G, 0])` で負荷抵抗を配置する。
5. `sch.create_gnd(location=[10*G, -10*G])` で接地を配置する。
6. 電源 → ダイオード → 負荷抵抗 → GND → 電源、という直列ループに配線する。
7. プロジェクトを保存し、`tb.release_desktop()` でAEDTを終了する。

**解析（Setup 作成・analyze）は行わない**。それはこのグループの normal 課題で扱う。

## ヒント

- `create_voltage_source` の `source_type` には複数の波形タイプが指定できる:
  `"E"`（定数/DC）、`"ESINE"`（正弦波）、`"EPULSE"`（矩形パルス波）、`"ETRIANG"`（三角波）。
  このシリーズのnormal課題（整流回路）では`"ESINE"`（交流電源）を使っているが、ここでは
  `"EPULSE"`で違いを体験する。
- **配置した部品は全て配線すること。** 未接続のピンが1つでもあると
  `Netlist error due to unconnected pin` でエラーになる（解析を行わないこの課題では
  エラーメッセージとしては出ないが、normal以降で解析する際に必ず問題になる）。
- 部品のピン座標は `component.pins[i].location` で取得する。`left_right()` ヘルパー
  （ピンをX座標でソート）で左右のピンを判定できる。

## 評価基準

- [ ] AEDTが起動し、V_IN（EPULSE）・D1・RL・GND が配置されている
- [ ] 電源 → D1 → RL → GND → 電源、が直列に配線され、閉回路になっている
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- `source_type` を `"ESINE"`（正弦波）や `"ETRIANG"`（三角波）に変えて、GUIで波形の違いを
  比較してみてください。
- このシリーズの次のステップとして、
  [1.normal/twin_builder/ex01_rectifier/](../../../1.normal/twin_builder/ex01_rectifier/) に進み、
  ダイオード4個のブリッジ（全波整流）+コンデンサフィルタに発展させ、過渡解析を実行してみてください。
