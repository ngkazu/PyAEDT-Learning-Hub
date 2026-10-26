# 演習1: RLCローパスフィルタ Sパラメータの Python 後処理（CSV入出力・matplotlib）

**目安時間: 90分以上**

題材: `2.hard/circuit/ex01_rlc_filter_sparams/`（RLCローパスフィルタの S パラメータ解析）と
同じモデル・解析に、Python での後処理（CSV入出力・matplotlib 可視化）を追加する。

> この演習は「RLC回路シリーズ」の expert レベル。hard（S パラメータ解析）と同じ 2ポート
> RLC ローパスフィルタを解析し、**S21 データを Python で取り出して CSV・画像に保存し、
> カットオフ周波数を自動算出**する。各課題は自己完結させるため、モデル作成〜解析のコードは
> hard と重複して含んでいる（他の難易度のファイルを import しない）。

## 学習目標

- `get_solution_data()` で得た S パラメータを Python（numpy 配列）として扱う
- S21 データを CSV ファイルに保存する
- カットオフ周波数（S21 が −3dB になる周波数）を線形補間で自動算出する
- matplotlib（headless: `Figure` + `FigureCanvasAgg`）で特性を画像（PNG）に保存する
- S パラメータを Touchstone（.s2p）にエクスポートする

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください
（モデル作成〜解析の部分は hard と同じものが既に書いてある）。

1. `cir.post.get_solution_data(expressions="dB(S(Port2,Port1))", setup_sweep_name="LNA", domain="Sweep")`
   で S21 の solution data を取得し、`data.get_expression_data("dB(S(Port2,Port1))")` で
   `(freq_ghz, s21_db)` の2つの numpy 配列を得る。
2. `freq_ghz` と `s21_db` を CSV（ヘッダ `Freq_GHz, S21_dB`）に書き出す（`csv` モジュール）。
3. カットオフ周波数を算出する。DC（配列先頭）の S21 値を基準に `threshold = s21_dc - 3.0` とし、
   `s21_db` が初めて `threshold` を下回る区間を**線形補間**してクロス周波数 `cutoff_ghz` を求める。
4. matplotlib で S21 対周波数をプロットし、`-3dB` ライン・カットオフ線を重ねて PNG 保存する。
   **`Figure` + `FigureCanvasAgg` を使い、`plt.show()` / `plt.subplots()` は使わない**
   （ヘッドレス環境でハングしないため）。
5. `cir.export_touchstone(output_file=...)` で S パラメータを `.s2p` に保存する。
6. プロジェクトを保存し、`cir.release_desktop()` で終了する。

## ヒント

- `get_expression_data(式)` は `(x配列, y配列)` のタプルを返す（x=周波数[GHz], y=S21[dB]）。
  返り値は numpy 配列なので、`if xs:` のような真偽評価は避け、`len(xs)` で長さを見る。
- 線形補間: 区間 `(f0,y0)-(f1,y1)` を threshold が横切るとき
  `fc = f0 + (threshold - y0) * (f1 - f0) / (y1 - y0)`。
- matplotlib の headless 利用:
  ```python
  from matplotlib.figure import Figure
  from matplotlib.backends.backend_agg import FigureCanvasAgg
  fig = Figure(figsize=(8, 5)); FigureCanvasAgg(fig)
  ax = fig.add_subplot(111); ax.plot(freq_ghz, s21_db)
  fig.savefig("s21.png", dpi=150)
  ```
- `export_touchstone(output_file=...)` は拡張子（2ポートなら `.s2p`）で形式が決まる。

## 評価基準

- [ ] S21 データが取得でき、CSV（`s21.csv`）が出力されている
- [ ] カットオフ周波数（約 2.4GHz 付近）が算出・表示されている
- [ ] S21 特性の画像（`s21.png`）が `Figure`+`FigureCanvasAgg` で保存されている
- [ ] Touchstone（`rlc_lowpass.s2p`）がエクスポートされている
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- L や C の値を変えて、算出されるカットオフ周波数が理論値
  `fc = 1 / (2*pi*sqrt(L*C))` にどれだけ近いか比較してください。
- 出力した `.s2p` を scikit-rf（skrf）で読み込み、群遅延やインピーダンスなど別の指標も
  プロットしてみてください。
