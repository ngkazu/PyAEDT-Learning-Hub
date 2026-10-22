# 演習1: ブスバー解析 容量・インダクタンスデータのPython後処理（CSV入出力・PyVista可視化）

**目安時間: 90分以上**

題材: 演習「[2.hard/q3d/ex01_busbar_matrixreport/](../../../2.hard/q3d/ex01_busbar_matrixreport/)」で
作成したモデルを土台に、AEDT側の操作は最小限にとどめ、**Pythonでのカスタムデータ処理とCSV入出力、
PyVistaでの可視化**に重点を置く（`docs/difficulty-criteria.md` の expert レベルに相当）。

> この演習は「ブスバー解析シリーズ」の expert レベル。normal/hardの内容は
> [1.normal/q3d/ex01_busbar/](../../../1.normal/q3d/ex01_busbar/) /
> [2.hard/q3d/ex01_busbar_matrixreport/](../../../2.hard/q3d/ex01_busbar_matrixreport/) を参照。

## 学習目標

- `conditions.csv` から解析条件（Bar1の長さ）を読み込み、モデルに反映する
- `post.get_solution_data()` で、周波数スイープに沿った自己容量（元の行列）・自己インダクタンス
  （縮退行列、ACL）の値をPython側（NumPy配列）として取得する
- 取得した周波数特性をCSVファイルに出力する
- matplotlibで、自己容量・自己インダクタンスの周波数特性をグラフ化する
- `post.create_fieldplot_surface()` でブスバー表面のAC電流密度（`Mag_SurfaceJac`）のコンター図を作成し、
  `post.plot_field_from_fieldplot()` でPyVista画像出力・インタラクティブ表示する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 同じフォルダにある `conditions.csv`（`bar1_length_mm` の1列1行）を `csv.DictReader` で読み込み、
   `bar1_length_mm` の値を取得する。
2. [2.hard/q3d/ex01_busbar_matrixreport/](../../../2.hard/q3d/ex01_busbar_matrixreport/) と同じ手順で、
   次を順に行う。ただしBar1の経路の終点Xは、CSVから読み込んだ `bar1_length_mm` を使って
   `[-bar1_length_mm, 0, 0]` とする（Bar2/Bar3の寸法は固定値のまま）。
   - 3本のブスバー（Bar1/Bar2/Bar3）＋基板を作成する。
   - `auto_identify_nets()` でネットを識別し、各バーにソース・シンクを割り当てる。
   - セットアップ（`AdaptiveFreq="1000MHz"`）＋周波数スイープ（`sweep_type="Discrete"`,
     `save_fields=True`, 0〜10GHz, step 1GHz）を作成する。
   - `insert_reduced_matrix()`（`JoinSeries`）＋`add_operation()`（`JoinParallel`）で縮退行列を作る。
3. `q3d.analyze()` で解析を実行する。
4. `q3d.post.create_fieldplot_surface(assignment=["Bar1", "Bar2", "Bar3"], quantity="Mag_SurfaceJac",
   setup=f"{setup.name} : LastAdaptive", intrinsics={"Freq": "1GHz"}, plot_name="BusbarCurrentDensity")` で、
   3本のブスバー表面のAC電流密度をフィールドプロット（コンター図）として作成する。
5. `original_self = q3d.matrices[0].get_sources_for_plot(get_self_terms=True, get_mutual_terms=False)`
   （`C(Source1,Source1)` 等、3本分の自己容量の式リスト）と、
   `reduced_self = mr_series.get_sources_for_plot(get_self_terms=True, get_mutual_terms=False,
   category="ACL")`（縮退後の自己インダクタンスの式リスト）を用意する。
6. `post.get_solution_data(expressions=original_self, context="Original")` と
   `post.get_solution_data(expressions=reduced_self, context="MR_Series")` で、それぞれの
   `SolutionData` を取得する。
7. `get_expression_data(expression=..., formula="mag")` を使って、各式について周波数・値をNumPy配列
   として取り出す（容量・インダクタンスはQ3Dの内部表現上複素数になり得るため、絶対値`"mag"`を使う）。
8. 周波数・各自己容量（3列）・自己インダクタンス（1列）を `results_q3d_busbar.csv` に出力する。
9. matplotlibで、自己容量（3本分）を1つのグラフに、自己インダクタンスをもう1つのグラフに重ねてプロットし、
   画像ファイルとして保存する。
10. `post.plot_field_from_fieldplot(plot_name="BusbarCurrentDensity", project_path=..., image_format="png",
    view="isometric", show=False)` で、電流密度コンター図をPyVista画像として出力する。
11. 同じフィールドプロットに対して、今度は `project_path` を渡さず `show=True` で
    `post.plot_field_from_fieldplot(plot_name="BusbarCurrentDensity", view="isometric", show=True)` を呼び、
    インタラクティブなPyVistaウィンドウ（マウスで回転・拡大できる）を表示する。
12. プロジェクトを保存し、`q3d.release_desktop()` でAEDTを終了する。

## ヒント

- `csv.DictReader` はヘッダー行をキーにした辞書を1行ずつ返す。`next(reader)` で最初の1行を取得できる。
- `get_expression_data()` は `(x配列, y配列)` のタプルを返す。容量・インダクタンスはスカラー量なので
  `formula="mag"`（絶対値）を使う（`"db20"` はSパラメータ等の比率量向けで、ここでは不適切）。
- `get_sources_for_plot()` が返す式は `"C(Source1,Source1)"` のような文字列。CSV列名にそのまま使うと
  分かりやすい。
- CSV出力は `csv.writer` で、周波数配列と各expressionの値配列を `zip()` してまとめて書き込む。
- `Mag_SurfaceJac` はQ3D Extractorが内部的に保持するAC表面電流密度の量名。`create_fieldplot_surface()`の
  `setup`引数は`"SetupName : LastAdaptive"`の形式で指定し、`intrinsics={"Freq": "1GHz"}`は
  `AdaptiveFreq="1000MHz"`と一致させる（アダプティブメッシュの解は必ずフィールドデータが保存されるため）。
- `post.plot_field_from_fieldplot()` は「AEDT内部で作成したフィールドプロット結果をPyVistaで再構築して画像化する」
  メソッド。`plot_name`には`create_fieldplot_surface()`で作成したフィールドプロット名をそのまま渡す。
  `project_path`を渡すと画面表示なしでその場所に画像を保存し、`project_path`を渡さず`show=True`にすると
  `auto_close`されないインタラクティブウィンドウが開く（他の演習のフィールドプロットと同じパターン）。

## 評価基準

- [ ] `conditions.csv` の値（`bar1_length_mm`）がBar1の経路に反映されている
- [ ] hardと同じモデル・縮退行列・Setup・解析がエラーなく完了している
- [ ] 自己容量（3本分）・自己インダクタンスの周波数特性データがPython側に取得できている
- [ ] `results_q3d_busbar.csv` に結果が出力されている
- [ ] 周波数特性グラフが画像ファイルとして保存されている
- [ ] 電流密度（`Mag_SurfaceJac`）コンター図のPyVista画像出力・インタラクティブ表示ができている

## 発展課題（任意）

- `conditions.csv` に複数行の条件（Bar1の長さの組み合わせなど）を追加し、ループで解析・比較してください。
- 相互容量（Mutual Capacitance）も取得し、バー間のクロストークを定量的に評価してみてください。
