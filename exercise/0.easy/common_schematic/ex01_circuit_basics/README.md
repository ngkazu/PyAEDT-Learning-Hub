# 演習1: 回路要素の配置と配線（起動 → 配置 → 配線 → 保存 → 終了）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。回路図（schematic）の最も基本的な操作
（部品配置・ピン配線）を自分の手で体験する。

> この演習は `common_schematic` グループの基礎課題。ここで練習する部品配置・配線は、
> `1.normal/circuit/ex01_rlc_transient/`（RLC直列回路の過渡解析）でそのまま使う。

## アプリケーションの選び方

この演習は回路図（schematic）を扱うアプリケーションで進める。
[docs/app-selection.md](../../../../docs/app-selection.md) の `common_schematic` 分類のうち、
**Circuit** または **Twin Builder** を選ぶこと（どちらも `modeler.schematic` の
部品作成API（`create_resistor` など）が共通で、同じコードで進められる）。
`starter.py` 冒頭の import とアプリ生成部分を書き換えてから進めること。以降の説明では例として
`Circuit` を使う。

> 注: EMIT は同じ `common_schematic` グループだが、アンテナ/無線機器の共存干渉解析用で、
> R・L・C を配置する回路図とは性質が異なる。この課題では Circuit か Twin Builder を選ぶこと。

## 学習目標

- PyAEDTで回路図系アプリを起動し、正しく終了するまでの一連の流れを身につける
- 回路図に抵抗・インダクタ・コンデンサ・接地（GND）を座標指定で配置する
- 部品のピン座標（`component.pins[i].location`）を使って部品どうしを配線する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../../docs/app-selection.md) から Circuit または Twin Builder を選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動する。
3. 抵抗 `R1`（`100`）を `location=[0.02, 0.0]` に配置する（`sch.create_resistor`）。
4. インダクタ `L1`（`1e-6` = 1uH）を `location=[0.04, 0.0]` に配置する（`sch.create_inductor`）。
5. コンデンサ `C1`（`1e-9` = 1nF）を `location=[0.06, 0.0]` に配置する（`sch.create_capacitor`）。
6. `create_wire()` で R→L→C を直列に配線する（R右-L左、L右-C左）。
   各部品の左右ピン座標は `left_right()` ヘルパー（ピンを X 座標でソート）で取得できる。
7. `sch.create_gnd(location=[0.06, -0.03])` で接地を配置する。
8. プロジェクトを保存する。
9. `release_desktop()` でAEDTを終了する（プロジェクト・プロセスの両方を閉じる）。

**解析（Setup 作成・analyze）は行わない**。それはこのグループの normal 課題
（`1.normal/circuit/ex01_rlc_transient/`）で扱う。

## ヒント

- 回路図のコンポーネント作成は `app.modeler.schematic` のメソッド群
  （`create_resistor` / `create_inductor` / `create_capacitor` / `create_gnd` / `create_wire`）で行う。
- **ピン名は部品種類ごとに異なる**（抵抗=`terminals_0`/`terminals_1`、インダクタ=`n1`/`n2`、
  コンデンサ=`positive`/`negative`）。名前で配線すると部品ごとに分岐が必要になるため、
  `starter.py` の `left_right()` のように**ピンの座標 `pin.location` で左右を判定**すると共通化できる。
- `create_wire()` は座標のリストを受け取る。2点をつなぐなら `[始点, 終点]`、
  途中で曲げたいなら中間点を挟む（例: `[始点, [x, y], 終点]`）。
- 部品の値は数値で渡す（`100`、`1e-6`、`1e-9`）。単位付き文字列（`"100ohm"`）でも指定できる。

## 評価基準

- [ ] 選んだアプリケーション（Circuit または Twin Builder）が起動している
- [ ] R1・L1・C1・GND が回路図に配置されている
- [ ] R→L→C が直列に配線されている
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- 配置した部品の値を変えてみて、GUI のプロパティに反映されることを確認してください。
- アプリ固有の操作も練習したい場合は、Circuit なら
  [0.easy/circuit/ex01_pulse_port/](../../circuit/ex01_pulse_port/)（パルス電圧源・
  インターフェースポート）、Twin Builder なら
  [0.easy/twin_builder/ex01_halfwave_diode/](../../twin_builder/ex01_halfwave_diode/)
  （波形タイプ・ダイオード）に進んでください。
- このシリーズの次のステップとして、`1.normal/circuit/ex01_rlc_transient/` に進み、
  電源・GND を加えて閉ループにし、過渡解析を実行してみてください。
