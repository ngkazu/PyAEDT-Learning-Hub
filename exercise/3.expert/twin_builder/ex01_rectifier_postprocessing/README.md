# 演習1: ブリッジ整流回路+コンデンサフィルタの Python 後処理（CSV入出力・matplotlib・リプル率算出）

**目安時間: 90分以上**

題材: `2.hard/twin_builder/ex01_rectifier_waveforms/`（波形ポスト処理）と同じモデル・解析に、
Python でのデータ抽出・リプル率算出・可視化を追加する。

> この演習は「整流回路シリーズ」の expert レベル。hard（AEDT内ポスト処理）で作った
> 波形解析に、Python後処理（CSV・matplotlib・リプル率算出）を追加する。
> この課題は CPython 実行環境で動かす（matplotlib を使うため）。

## 使用するパッケージ

normal/hard と同じく `TwinBuilder` を使う。加えて `csv`（標準ライブラリ）と
`matplotlib`（headless構成）を使う。

## 学習目標

- 過渡解析の波形データを `get_solution_data()` で取得し、CSVに保存する
- 時間軸の単位（ns）を人間が読みやすい単位（ms）に変換する
- 整流回路の実用指標である**リプル率**（出力電圧の脈動の割合）をPythonで算出する
- matplotlib（headless: `Figure` + `FigureCanvasAgg`）で入出力波形を比較するグラフを保存する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください
（モデル作成・解析部分は hard 課題と同じ。迷ったら
`2.hard/twin_builder/ex01_rectifier_waveforms/solution.py` を参考にしてよい）。

1. hard と同じ手順でモデルを作り、過渡解析を実行する。
2. `get_solution_data(expressions="V_AC.V", setup_sweep_name="TR", domain="Time",
   report_category="Standard")` で入力交流電圧の生データ（時間配列・電圧配列）を取得する。
   同様に出力DC電圧（`RL.V`）も取得する。
3. 時間配列の単位は **ns** なので、**ms に変換**してからCSV・グラフに使う
   （`time_ms = [t / 1.0e6 for t in time_ns]`）。
4. 取得したデータを `rectifier_waveforms.csv`（列: `Time_ms`, `V_AC_V`, `V_RL_V`）に保存する。
5. 出力DC電圧の後半50%（定常状態）から、最大値・最小値・平均値を求め、
   **リプル率** `(Vmax - Vmin) / Vmean * 100` [%] を算出する。
6. matplotlib（headless構成）で入力交流電圧と出力DC電圧を1枚のグラフに重ねてプロットし、
   `rectifier_waveforms.png` に保存する。
7. プロジェクトを保存し、`tb.release_desktop()` で終了する。

## ヒント

- `get_solution_data()` の戻り値（`SolutionData`）から実際の配列を取り出すには、
  `data.get_expression_data("式の文字列そのまま")` を呼ぶ（戻り値は `(時間配列, 値配列)` のタプル）。
  時間配列は `data.intrinsics["Time"]` でも取得できる。
- **時間の単位はns（ナノ秒）であって、ミリ秒ではない。** `tb.set_end_time("100ms")` で
  設定した終了時間は、`get_solution_data`経由では`1e8`（ns単位の数値）として返ってくる。
  グラフやCSVに出す前に `/ 1.0e6` で ms に変換すること（忘れると「桁が明らかにおかしいグラフ」になる）。
- リプル率の算出では、起動直後（コンデンサが充電されるまでの過渡応答）を含めると数値が不正確に
  なるため、**後半50%（定常状態）だけを評価に使う**のがポイント（RLCフィルタのカットオフ算出と
  同様、過渡現象を除いてから指標を計算する考え方）。
- matplotlib は `plt.figure()` / `plt.show()` を使わず、`Figure` + `FigureCanvasAgg(fig)` の
  オブジェクト指向APIで書く（headless環境でクラッシュしないため）。

## 評価基準

- [ ] hard と同じモデル・解析が行われている
- [ ] `rectifier_waveforms.csv` に時間(ms)・入力電圧・出力電圧のデータが保存されている
- [ ] リプル率が算出され、コンソールに表示されている
- [ ] `rectifier_waveforms.png` に入出力波形の比較グラフが保存されている（headless matplotlib、
      クラッシュなし）

## 発展課題（任意）

- `C_FILTER`（フィルタ容量）や `R_LOAD`（負荷抵抗）を変えて、リプル率がどう変化するか
  比較してみてください（容量を大きくする、または負荷抵抗を大きくする＝電流を減らすと
  リプルは小さくなるはず）。
- 半波整流（ダイオード1個のみ）に変更し、全波整流と比べてリプル率がどう変わるか試してみてください。
