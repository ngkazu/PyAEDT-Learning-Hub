# 演習1: パルス電圧源とインターフェースポートの配置（起動 → 配置 → 配線 → 保存 → 終了）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。Circuit固有の操作（パルス電圧源、インターフェースポート）
を自分の手で体験する。

> この演習は Circuit 専用の easy 課題。[0.easy/common_schematic/ex01_circuit_basics/](../../common_schematic/ex01_circuit_basics/)
> （R/L/C配置・配線。Circuit/Twin Builder共通）を先に済ませてから進めるとよい。
> ここで練習するインターフェースポートは、このシリーズの
> [1.normal/circuit/ex01_rlc_transient/](../../../1.normal/circuit/ex01_rlc_transient/)（過渡解析）や
> [2.hard/circuit/ex01_rlc_filter_sparams/](../../../2.hard/circuit/ex01_rlc_filter_sparams/)
> （Sパラメータ解析の入出力ポート）でそのまま使う。

## アプリケーションの選び方

この課題は Circuit（Nexxim 回路シミュレータ）専用（Twin Builderでは`create_voltage_pulse`の
挙動が異なるため代替不可）。クラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照（`from ansys.aedt.core import Circuit`）。

## 学習目標

- パルス波形を持つ電圧源（`create_voltage_pulse`）を配置する
- 回路の入出力インターフェース（インターフェースポート）を配置する
- インターフェースポートの戻り値型（`Excitations`）が通常の部品（`CircuitComponent`）と
  異なる点を理解する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. `Circuit(design="PulsePort", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. `sch.create_voltage_pulse(name="V1", value_lists=[0, 5, 0, "1ns", "1ns", "10ns", "20ns"],
   location=[0.0, 0.0])` でパルス電圧源を配置する。
3. `sch.create_resistor(name="R1", value=50, location=[0.02, 0.0])` で抵抗を配置する。
4. `sch.create_interface_port(name="Port1", location=[-0.02, 0.0])` と
   `sch.create_interface_port(name="Port2", location=[0.04, 0.0])` でインターフェースポートを
   2つ配置する。
5. `sch.create_gnd(location=[0.02, -0.02])` で接地を配置する。
6. 配線する: `Port1` → 電源の正極、電源の負極 → `GND`、`Port1` → `R1`左、`R1`右 → `Port2`。
7. プロジェクトを保存し、`cir.release_desktop()` でAEDTを終了する。

**解析（Setup 作成・analyze）は行わない**。それはこのグループの normal/hard 課題で扱う。

## ヒント

- `create_voltage_pulse` の `value_lists` は `[初期値, パルス値, 遅延, 立上り, 立下り, パルス幅, 周期]`
  の7要素リスト。
- **`create_interface_port()` の戻り値は `CircuitComponent` ではなく `Excitations` 型。**
  `component.parameters["InstanceName"]` にはポート名が入らない（`None`のまま）ので、
  ポート名を確認したい場合は `.name` 属性を直接使う（例: `p1.name` で `"Port1"` が取れる）。
  配線に使う `pins[i].location` は通常の部品と同じように使える。
- パルス電圧源のピンは、Y座標でソートして上下（正極/負極）を判定できる
  （`sorted(v.pins, key=lambda p: p.location[1])`）。

## 評価基準

- [ ] AEDTが起動し、V1・R1・Port1・Port2・GND が配置されている
- [ ] Port1-電源-R1-Port2-GND が正しく配線され、閉回路になっている
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- `value_lists` の立上り時間・パルス幅を変えて、パルス波形がどう変わるかGUIで確認してください。
- このシリーズの次のステップとして、
  [1.normal/circuit/ex01_rlc_transient/](../../../1.normal/circuit/ex01_rlc_transient/) に進み、
  RLC回路の過渡解析を実行してみてください。
