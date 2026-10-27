# 演習1: 差動ペア伝送線路 Sパラメータの Python 後処理（CSV入出力・matplotlib・Touchstone出力）

**目安時間: 90分以上**

題材: `2.hard/hfss_3d_layout/ex01_diff_pair_sparams/`（差動Sパラメータ解析）と同じモデル・解析に、
Python でのデータ抽出・帯域算出・可視化・Touchstoneエクスポートを追加する。

> この演習は「差動ペア伝送線路シリーズ」の expert レベル。hard（AEDT内ポスト処理）で作った
> 差動Sパラメータ解析に、Python後処理（CSV・matplotlib・Touchstone出力）を追加する。
> この課題は CPython 実行環境で動かす（matplotlib を使うため）。

## 使用するパッケージ

normal/hard と同じく、ジオメトリ作成を **PyEDB**、解析を **PyAEDT の `Hfss3dLayout`** で行う。
加えて、`csv`（標準ライブラリ）と `matplotlib`（headless構成）を使う。

## 学習目標

- 差動Sパラメータ（Sdd21・Sdd11）の生データを `get_solution_data()` + `context="Differential Pairs"`
  で取得する
- 取得したデータを CSV に保存する
- 伝送線路の実用帯域（Sdd21 が −3dB 下がる周波数）を Python で算出する
- matplotlib（headless: `Figure` + `FigureCanvasAgg`）でグラフを画像保存する
- 差動Sパラメータを Touchstone（`.s4p`）にエクスポートする

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください
（モデル作成・差動ペア設定・解析部分は hard 課題と同じ。迷ったら
`2.hard/hfss_3d_layout/ex01_diff_pair_sparams/solution.py` を参考にしてよい）。

1. hard と同じ手順でモデルを作り、差動ペア（`Diff_In`/`Diff_Out`）を設定して解析する。
2. `get_solution_data(expressions="dB(S(Diff_Out,Diff_In))", setup_sweep_name=...,
   context="Differential Pairs")` で Sdd21 の生データ（周波数配列・dB配列）を取得する。
   同様に Sdd11（`dB(S(Diff_In,Diff_In))`）も取得する。
3. 取得したデータを `sdd_parameters.csv`（列: `Freq_GHz`, `Sdd21_dB`, `Sdd11_dB`）に保存する。
4. Sdd21 が DC 値（1点目）から −3dB 下がる周波数を、隣接点の線形補間で算出する
   （`3.expert/circuit/ex01_rlc_filter_postprocessing/` のカットオフ算出と同じ考え方）。
5. matplotlib（headless構成: `Figure` + `FigureCanvasAgg`、`plt.show()` は使わない）で
   Sdd21・Sdd11 を1枚のグラフに重ねてプロットし、`sdd_parameters.png` に保存する。
   −3dBのしきい値線と、算出した周波数の縦線も描く。
6. `export_touchstone(setup="MySetup", sweep=sweep.name, output_file=...)` で
   差動Sパラメータを `diff_pair.s4p` にエクスポートする。
7. プロジェクトを保存し、`h3d.release_desktop()` で終了する。

## ヒント

- `get_solution_data()` の戻り値（`SolutionData`）から実際の配列を取り出すには
  `data.get_expression_data("式の文字列そのまま")` を呼ぶ（`get_expression_data()` の戻り値は
  `(周波数配列, 値配列)` のタプル）。**`SolutionData` オブジェクト自体を `if data:` のように
  真偽値評価しないこと**（内部がnumpy配列のため `ValueError` になる）。戻り値が得られたかどうかは
  `data is not None` 等で確認する。
- `export_touchstone` の `sweep` 引数には、`create_linear_count_sweep` の**戻り値の `.name`**
  （`sweep.name`）を渡す。文字列として決め打ちしないこと（スイープ名はAEDTが自動生成する）。
- matplotlib は `plt.figure()` / `plt.show()` を使わず、`Figure` + `FigureCanvasAgg(fig)` の
  オブジェクト指向APIで書く（headless環境でクラッシュしないため）。
- CSVの書き込みは標準ライブラリの `csv.writer` でよい（`with open(path, "w", newline="") as f:`）。
- カットオフ（−3dB点）の算出は、しきい値をまたぐ隣接2点から線形補間で求める
  （RLCフィルタのexpert課題と同じアルゴリズム）。

## 評価基準

- [ ] hard と同じモデル・差動ペア設定・解析が行われている
- [ ] `sdd_parameters.csv` に Sdd21・Sdd11 の周波数特性データが保存されている
- [ ] −3dBとなる周波数が算出され、コンソールに表示されている
- [ ] `sdd_parameters.png` にSdd21・Sdd11のグラフが保存されている（headless matplotlib、クラッシュなし）
- [ ] `diff_pair.s4p`（Touchstone）が出力されている

## 発展課題（任意）

- コモンモード（Scc21）やモード変換（Sdc21, Scd21）のデータも取得してCSV・グラフに追加してみてください。
- 線路長 `LENGTH` や間隔 `GAP` を変えて、−3dB周波数がどう変化するか比較してみてください。
- 出力した `.s4p` を Circuit 設計にインポートし、差動ドライバ・レシーバを繋いだ系全体の
  アイダイアグラムなど、更なる解析に発展させることもできます（本シリーズの範囲外）。
