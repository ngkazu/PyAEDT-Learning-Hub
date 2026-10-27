# 演習1: ブリッジ整流回路+コンデンサフィルタの波形ポスト処理（AEDT内ポスト処理）

**目安時間: 90分**

題材: `1.normal/twin_builder/ex01_rectifier/`（整流回路の過渡解析）と同じ回路に、
入力交流電圧・出力DC電圧の波形レポートを追加する。

> この演習は「整流回路シリーズ」の hard レベル。normal（モデル作成〜解析実行）で作った
> 回路に、**AEDT内ポスト処理（波形レポート）** を追加する。さらに Python 後処理
> （CSV入出力・matplotlib・リプル率算出）を追加したものが
> `3.expert/twin_builder/ex01_rectifier_postprocessing/`。

## 使用するパッケージ

normal と同じく `TwinBuilder`（`from ansys.aedt.core import TwinBuilder`）を使う。

## 学習目標

- 過渡解析（Time domain）の波形データをAEDT内レポートとして作成する
- 入力交流電圧と、整流・平滑後の出力DC電圧を比較できるようにする
- Twin Builderのポスト処理特有の注意点（`report_category`の明示）を理解する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください
（モデル作成部分は normal 課題と同じ。迷ったら
`1.normal/twin_builder/ex01_rectifier/solution.py` を参考にしてよい）。

1. normal と同じ手順で回路を作る（設計変数4つ、電源・ダイオード4個・コンデンサ・抵抗・GND、配線）。
2. `tb.set_end_time("100ms")` と `tb.analyze_setup("TR")` で過渡解析を実行する。
3. **AEDT内ポスト処理**として、入力交流電圧（`V_AC.V`）と出力DC電圧（`RL.V`）の波形レポートを
   `report_category="Standard"` 付きで作成する。

## ヒント

- **`create_report()` / `get_solution_data()` に `report_category="Standard"` を指定しないと、
  式の文法が正しくてもデータが取得できない（空/Falseが返る）。** これはTwin Builderの
  過渡解析データ特有の注意点で、HFSS等の3Dソルバーとは挙動が異なる。
- `setup_sweep_name` は単純に `"TR"`（セットアップ名そのもの）でよい（HFSS 3D Layoutのように
  `"セットアップ名 : スイープ名"` の形式にする必要はない。過渡解析には周波数スイープが無いため）。
- 式の名前は `部品のInstanceName.物理量`（例: `V_AC.V`, `RL.V`）。利用可能な式一覧は
  `tb.post.available_report_quantities(solution="TR")` で確認できる。

## 評価基準

- [ ] normal と同じ回路（設計変数4つ・電源・ダイオード4個・コンデンサ・抵抗・GND）が作成されている
- [ ] 過渡解析がエラーなく完走している
- [ ] 入力交流電圧（`V_AC.V`）と出力DC電圧（`RL.V`）の波形レポートが
      `report_category="Standard"` 付きで作成されている（`.aedt` に保存されている）

## 発展課題（任意）

- 各ダイオードの電流波形（`D1.I` など）もレポートに追加し、整流の瞬間にどのダイオードに
  電流が流れているか確認してみてください。
- 波形データをPythonで取り出してリプル率を自動算出したい場合は、このシリーズの
  expert（`3.expert/twin_builder/ex01_rectifier_postprocessing/`）に進んでください。
