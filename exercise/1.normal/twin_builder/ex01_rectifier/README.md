# 演習1: ブリッジ整流回路+コンデンサフィルタの過渡解析（モデル作成〜解析実行）

**目安時間: 60分**

題材: [PyAEDT Examples - Twin Builder（ブリッジ整流回路）](https://examples.aedt.docs.pyansys.com/)
を着想元に、回路の主要パラメータ（電圧振幅・周波数・フィルタ容量・負荷抵抗）を設計変数化し、
ハードコードしないよう独自に構成。

> 回路図への部品配置・配線がまだ不安な場合は、先に
> [0.easy/common_circuit/ex01_circuit_basics/](../../../0.easy/common_circuit/ex01_circuit_basics/)
> で起動〜配置〜配線〜保存の基本操作を練習するとよい（Circuit/Twin Builder共通の操作）。

> この演習は「整流回路シリーズ」の normal レベル。交流電源 → ダイオードブリッジ → コンデンサ
> 平滑フィルタ → 負荷抵抗、というAC-DC変換回路をモデル化し、過渡解析まで実行する。
> hard（[`2.hard/twin_builder/ex01_rectifier_waveforms`](../../../2.hard/twin_builder/ex01_rectifier_waveforms/README.md)）
> では入出力波形のAEDT内ポスト処理を追加し、expert
> （[`3.expert/twin_builder/ex01_rectifier_postprocessing`](../../../3.expert/twin_builder/ex01_rectifier_postprocessing/README.md)）
> ではさらに Python 後処理（CSV・matplotlib・リプル率算出）を追加する。

## アプリケーションの選び方

この課題は Twin Builder（Simplorer由来のシステムシミュレータ）を使う。`common_circuit` グループ
（Circuit / EMIT / Twin Builder）のうち、回路図の基本操作自体は Circuit と共通だが、
Twin Builder はシステムレベルの電気回路・制御系の時間領域シミュレーションに向く。クラス名は
[docs/app-selection.md](../../../../docs/app-selection.md) を参照（`from ansys.aedt.core import TwinBuilder`）。

## 学習目標

- 回路図（schematic）に電圧源・ダイオード・コンデンサ・抵抗・GND を座標指定で配置する
- 回路の主要パラメータを**設計変数**として定義し、部品の `value`/`amplitude`/`freq` 引数に
  変数名の文字列を渡す（値をハードコードしない）
- ダイオードブリッジ（全波整流）の配線パターンを組む
- 過渡解析（Transient）の終了時間を設定し、解析を実行する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `TwinBuilder(design="Rectifier", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. 回路の設計変数を4つ定義する: `V_AMPL`（電源振幅, `"100V"`）、`AC_FREQ`（周波数, `"50Hz"`）、
   `C_FILTER`（フィルタ容量, `"1uF"`）、`R_LOAD`（負荷抵抗, `"100kohm"`）。
3. `sch.create_voltage_source("V_AC", "ESINE", "V_AMPL", "AC_FREQ", location=[-1*G, 0])` で
   交流電源を配置する（`amplitude`/`freq` 引数に変数名の文字列を渡す）。
4. `sch.create_diode(name=..., location=[...], angle=270)` を4回呼び、ブリッジ整流用のダイオード
   D1〜D4 を配置する（座標は solution.py のコメントを参照）。
5. `sch.create_capacitor(name="C_FILT", value="C_FILTER", ...)` と
   `sch.create_resistor(name="RL", value="R_LOAD", ...)` で、変数名を `value` に渡してフィルタと
   負荷を配置する。`sch.create_gnd(...)` で接地も配置する。
6. `create_wire()` でダイオードブリッジを組み、電源・フィルタ・負荷・GND を接続する
   （配線パターンは solution.py を参照）。
7. `tb.set_end_time("100ms")` で過渡解析の終了時間を設定し、`tb.analyze_setup("TR")` で解析を実行する。
8. プロジェクトを保存し、`tb.release_desktop()` でAEDTを終了する（**レポート作成などのポスト処理は
   行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- **変数名 `"FREQ"` は Twin Builder の内部予約語と衝突して登録されない。** 周波数の設計変数には
  `"AC_FREQ"` のような別名を使うこと（`tb["FREQ"] = "50Hz"` としても `tb.variable_manager`
  に反映されない、という分かりにくい失敗パターンなので注意）。
- 部品の `value`（コンデンサ・抵抗）や `amplitude`/`freq`（電圧源）には、数値だけでなく
  **変数名の文字列**（例: `"V_AMPL"`）をそのまま渡せる。渡した変数名は部品のプロパティ
  （例えば電圧源の `AMPL` プロパティ）にそのまま式として設定される。
- 回路図のコンポーネント作成は `tb.modeler.schematic` のメソッド群
  （`create_voltage_source` / `create_diode` / `create_capacitor` / `create_resistor` /
  `create_gnd` / `create_wire`）で行う。引数名・既定値は `inspect.signature()` で確認できる。
- 部品の `location` はグリッド間隔 `G = 0.00254`（m）の倍数で指定するのが一般的。
- 配線は `create_wire(points=[...])` に座標のリストを渡す。途中で曲げたい場合は中間点を挟む
  （例: `[始点, [x, y], 終点]`）。部品のピン座標は `component.pins[i].location` で取得する。

## 評価基準

- [ ] AEDTが起動し、電源・ダイオード4個・コンデンサ・抵抗・GND が配置されている
- [ ] 電源振幅・周波数・フィルタ容量・負荷抵抗が設計変数として定義され、各部品の値が
      その変数名を参照している（数値のハードコードではない）
- [ ] ダイオードブリッジが正しく配線され、閉回路になっている
- [ ] 過渡解析がエラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `R_LOAD` の値を変えて、負荷抵抗を大きく/小さくするとフィルタ後の電圧のリプル（脈動）が
  どう変わるか予想してください（波形の確認はこのシリーズの
  [hard](../../../2.hard/twin_builder/ex01_rectifier_waveforms/README.md) で扱います）。
- `C_FILTER` を大きくすると、平滑後の電圧がどう変化するか考えてください。
- 単相全波整流ではなく、半波整流（ダイオード1個のみ）にすると波形がどう変わるか試してみてください。
