# 演習3: コイル・コア電磁石 インダクタンスデータのPython後処理（CSV入出力・PyVista可視化）

**目安時間: 90分以上**

題材: 演習「[2.hard/maxwell_3d/ex03_coil_core_fieldplot/](../../../2.hard/maxwell_3d/ex03_coil_core_fieldplot/)」
で作成したモデルを土台に、AEDT側の操作は最小限にとどめ、Python側でのデータ取得・CSV入出力・
PyVista可視化を追加する。

> この演習は「コイル・コア電磁石シリーズ」の expert レベル。normal/hardの内容は
> [1.normal/maxwell_3d/ex03_coil_core/](../../../1.normal/maxwell_3d/ex03_coil_core/) /
> [2.hard/maxwell_3d/ex03_coil_core_fieldplot/](../../../2.hard/maxwell_3d/ex03_coil_core_fieldplot/)
> を参照。

## 学習目標

- `conditions.csv` から解析条件（起磁力・コア半径）を読み込み、モデルに反映する
- `post.get_solution_data()` で、インダクタンスのデータテーブル値を取得する
- インダクタンスの値をCSVファイルに出力する
- `post.plot_field_from_fieldplot()` で、コア表面のBフィールドをPyVistaで画像出力・インタラクティブ表示する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. `conditions.csv`（`amp_turns`, `core_r_mm` の2列）を読み込む。
2. [2.hard/maxwell_3d/ex03_coil_core_fieldplot/](../../../2.hard/maxwell_3d/ex03_coil_core_fieldplot/)
   と同じ手順でモデルを作成し、Matrix割り当て・Setup作成・解析を行う。ただし`"amp_turns"`と
   `"core_r"`はCSVから読み込んだ値を使う。
3. `post.get_solution_data(expressions=["Matrix1.L(Winding1,Winding1)"])` で自己インダクタンスの
   SolutionDataを取得し、`get_expression_data(formula="real")` で値を取得する。
4. `amp_turns`・`core_r_mm`・インダクタンスの値を `results_inductance.csv` に出力する。
5. `post.create_fieldplot_surface(assignment="Core", quantity="Mag_B", setup=f"{setup.name} :
   LastAdaptive", plot_name=...)` でコア表面のフィールドプロットを作成する。
6. `post.plot_field_from_fieldplot(plot_name=..., project_path=str(script_dir), image_format="png",
   view="isometric", log_scale=True, show=False)` で、PyVistaによる画像を出力する。
7. `project_path`を渡さず`show=True`で同じ`plot_field_from_fieldplot()`を呼び、インタラクティブな
   PyVistaウィンドウ（マウスで回転可能）で表示する。
8. プロジェクトを保存し、`m3d.release_desktop()` でAEDTを終了する。

## ヒント

- `get_solution_data()`はDate Table系の単一値レポートにも使える。`variations`を指定しなくても
  既定のノミナル値が使われる。
- `get_expression_data()`は`(x配列, y配列)`のタプルを返す。単一値の解析なので、配列の最初の
  要素（`[0]`）を使えばよい。

## 評価基準

- [ ] `conditions.csv`の値（起磁力・コア半径）がモデルに反映されている
- [ ] hardと同じモデル・Matrix・Setup・解析がエラーなく完走している
- [ ] 自己インダクタンスの値がPython側で取得できている
- [ ] `results_inductance.csv`にインダクタンスデータが出力されている
- [ ] コア表面のMag_Bフィールドプロットの画像ファイルが出力されている
- [ ] インタラクティブなPyVistaウィンドウが表示される

## 発展課題（任意）

- `conditions.csv`に複数行の条件（コア半径の組み合わせ）を追加し、ループで解析・インダクタンスの
  変化をmatplotlibでグラフ化してください。
