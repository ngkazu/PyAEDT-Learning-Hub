# 演習1: コモンモードチョーク 損失・Bフィールドデータの Python 後処理（CSV入出力・PyVista可視化）

**目安時間: 90分以上**

題材: 演習「[2.hard/maxwell_3d/ex01_choke_lossreport/](../../../2.hard/maxwell_3d/ex01_choke_lossreport/)」で
作成したモデルを土台に、AEDT側の操作は最小限にとどめ、Python側でのデータ取得・CSV入出力・PyVista可視化を追加する。

> この演習は「チョークシリーズ」の expert レベル。normal/hardの内容は
> [1.normal/maxwell_3d/ex01_choke/](../../../1.normal/maxwell_3d/ex01_choke/) /
> [2.hard/maxwell_3d/ex01_choke_lossreport/](../../../2.hard/maxwell_3d/ex01_choke_lossreport/) を参照。

> モデル作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex10_choke_geometry/](../../../0.easy/common_3d/ex10_choke_geometry/) を確認するとよい。

## 学習目標

- `conditions.csv` から解析条件（巻数・周波数）を読み込み、モデルに反映する
- `post.get_solution_data()` で、損失レポート（`SolidLoss`/`CoreLoss`）の数値データを取得する
- `SolutionData.get_expression_data()` で、損失の値をPython側の配列として取り出す
- 損失データをCSVファイルに出力する
- `post.plot_field_from_fieldplot()` で、コア表面のBフィールドプロットをPyVistaで画像出力・インタラクティブ表示する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. `conditions.csv`（`turns`, `frequency_khz` の2列）を読み込む。
2. [1.normal/maxwell_3d/ex01_choke/](../../../1.normal/maxwell_3d/ex01_choke/) と同じ手順でチョークを作成し、
   Region作成・電流励振の割り当て・Setup作成・解析を行う。ただし `"Outer Winding"` の `"Turns"` と
   `setup.props["Frequency"]` は、CSVから読み込んだ `turns`/`frequency_khz` の値を使う。
3. `m3d.post.get_solution_data(expressions=["SolidLoss", "CoreLoss"], setup_sweep_name=m3d.nominal_sweep,
   report_category="Fields")` で、巻線のオーミック損失・コア損失のSolutionDataを取得する。
4. `solution_data.get_expression_data(expression="SolidLoss", formula="real")` と
   `get_expression_data(expression="CoreLoss", formula="real")` で、損失の値を取得する。
5. `turns`・`frequency_khz`・巻線損失・コア損失を `results_losses.csv` に出力する。
6. `m3d.post.create_fieldplot_surface(assignment=core.name, quantity="Mag_B", setup=f"{setup.name} :
   LastAdaptive", intrinsics={"Freq": f"{frequency_khz}kHz", "Phase": "0deg"}, plot_name="CoreMagB")` で、
   コア表面のB磁束密度のフィールドプロットを作成する。
7. `m3d.post.plot_field_from_fieldplot(plot_name="CoreMagB", project_path=str(script_dir),
   image_format="png", view="isometric", log_scale=True, show=False)` で、PyVistaによる画像を出力する。
8. `project_path` を渡さず `show=True` で同じ `plot_field_from_fieldplot()` を呼び、
   インタラクティブなPyVistaウィンドウ（マウスで回転可能）で表示する。
9. プロジェクトを保存し、`m3d.release_desktop()` でAEDTを終了する。

## ヒント

- `get_solution_data()` の `report_category="Fields"` は、hard演習で作成した
  `report_category="Fields", plot_type="Data Table"` のレポートと同じカテゴリを指定する。
- `get_expression_data()` の `formula` はSパラメータのような複素量なら `"db20"` 等を使うが、
  損失（`SolidLoss`/`CoreLoss`）はスカラーの実数値なので `"real"` を使う。
- `get_expression_data()` は `(x配列, y配列)` のタプルを返す。単一周波数・単一ポイントの解析なので、
  配列の最初の要素（`[0]`）を使えばよい。
- `plot_field_from_fieldplot()` は1回目（`show=False`）で画像ファイルに出力し、2回目（`show=True`）で
  インタラクティブウィンドウを開く、という2段階の呼び出しパターンがHFSS側の演習と共通。

## 評価基準

- [ ] `conditions.csv` の値（巻数・周波数）がモデルに反映されている
- [ ] normalと同じモデル・Region・励振・Setup・解析がエラーなく完走している
- [ ] 巻線損失・コア損失の値がPython側で取得できている
- [ ] `results_losses.csv` に損失データが出力されている
- [ ] コア表面のMag_Bフィールドプロットの画像ファイルが出力されている
- [ ] インタラクティブなPyVistaウィンドウが表示される

## 発展課題（任意）

- `conditions.csv` に複数行の条件（巻数・周波数の組み合わせ）を追加し、ループで解析・結果比較してください。
- 巻線損失とコア損失の比率を計算し、matplotlibで棒グラフにしてみてください。
