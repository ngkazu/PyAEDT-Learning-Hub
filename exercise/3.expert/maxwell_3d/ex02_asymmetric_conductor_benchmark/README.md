# 演習2: TEAM7非対称導体 実測データとの比較（CSV入出力・PyVista可視化）

**目安時間: 90分以上**

題材: 演習「[2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/](../../../2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/)」
で作成したモデルを土台に、AEDT側の操作は最小限にとどめ、Python側でのデータ取得・公開実測データとの比較・
CSV入出力・PyVista可視化を追加する。TEAM7問題の公開実測データ（`team7_measured_bz.csv`）は
[COMPUMAG TEAM Workshop problem 7](https://www.compumag.org/wp/wp-content/uploads/2018/06/problem7.pdf)
の測定結果（200Hz・位相0度）を収録している。

> この演習は「TEAM7非対称導体シリーズ」の expert レベル。normal/hardの内容は
> [1.normal/maxwell_3d/ex02_asymmetric_conductor/](../../../1.normal/maxwell_3d/ex02_asymmetric_conductor/) /
> [2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/](../../../2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/)
> を参照。

## 学習目標

- `post.get_solution_data()` で、ラインに沿った$B_z$分布のSolutionDataを取得する
- `numpy.interp()` で、シミュレーション結果（連続的な距離サンプル）を実測データと同じ距離点に補間する
- シミュレーション値・実測値・誤差をCSVファイルに出力する
- matplotlibで、シミュレーション結果と公開実測データを重ね描きして比較する
- `post.plot_field_from_fieldplot()` で、板表面のBフィールドをPyVistaで画像出力・インタラクティブ表示する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. `team7_measured_bz.csv`（`distance_mm`, `bz_a1b1_gauss`, `bz_a2b2_gauss` の3列）を読み込む。
2. [2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/](../../../2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/)
   と同じ手順で、次を順に行う。
   - normalと同じ手順でコイル・アルミ板・Region・渦電流設定を作成し、セットアップ `"Setup1"`
     （200Hz＋`add_eddy_current_sweep()`で50Hzを追加）を作成する。
   - `setup.analyze()` で解析を実行する。
   - $B_z$（Gauss換算）のFields Calculator式を `post.fields_calculator.add_expression(bz, None)` で登録する。
   - 評価用ライン `"Line_A1_B1"`（`[0,72,34]mm`→`[288,72,34]mm`）・`"Line_A2_B2"`
     （`[0,144,34]mm`→`[288,144,34]mm`）を `create_polyline(..., non_model=True)` で作成する。
3. 200Hz・位相0度における、各ラインに沿った$|B_z|$のSolutionDataを
   `post.get_solution_data(expressions="mag(Bz)", variations={"Distance": ["All"], "Freq": ["200Hz"],
   "Phase": ["0deg"]}, primary_sweep_variable="Distance", report_category="Fields",
   context=line_name)` で取得する。
4. `get_expression_data(expression="mag(Bz)", formula="real")` で取得したシミュレーション結果
   （連続的な距離サンプル）を、`np.interp()` で実測データと同じ距離点に補間する。
5. シミュレーション値・実測値を `results_benchmark_comparison.csv` に出力する。
6. シミュレーション結果と実測値をmatplotlibで重ね描きし、画像ファイルに保存する。
7. `post.create_fieldplot_surface(assignment=plate.name, quantity="Mag_B", ...)` で板表面の
   フィールドプロットを作成し、`post.plot_field_from_fieldplot()` で画像出力（`show=False`）と
   インタラクティブ表示（`show=True`）の両方を行う。
8. プロジェクトを保存し、`m3d.release_desktop()` でAEDTを終了する。

## ヒント

- **重要**: AEDTが返す`Distance`軸の単位（m/mm）は実行環境・バージョンによって変わる場合がある。
  実行結果の`sim_distance`配列の値を確認し、`measured_distance_mm`（mm単位）とスケールが
  合っているか確認すること。合っていなければ、どちらかを単位変換してから`np.interp()`を使う。
- シミュレーション結果はメッシュに応じた密な距離サンプルになるため、実測データの17点の距離と
  正確には一致しない。`np.interp(x_measured, x_sim, y_sim)` で、実測データの距離点における
  シミュレーション値を補間して求める。
- `np.interp()`は`x_sim`が昇順になっている必要がある。ライン上の距離サンプルは通常始点から
  終点に向かって単調増加するはずだが、念のため確認すること。

## 評価基準

- [ ] 実測データCSVが読み込まれている
- [ ] hardと同じモデル・Setup・解析・$B_z$計算式・評価ラインが再現されている
- [ ] シミュレーション結果がPythonに取得され、実測データの距離点に補間されている
- [ ] `results_benchmark_comparison.csv` に比較データが出力されている
- [ ] シミュレーションと実測値を重ね描きした画像が出力されている
- [ ] 板表面のMag_Bフィールドプロットの画像出力・インタラクティブ表示ができている

## 発展課題（任意）

- シミュレーション値と実測値の誤差（絶対誤差・相対誤差）を計算し、CSVに追加の列として出力してください。
- 50Hzのデータについても同様の比較を行い、周波数による一致度の違いを確認してください。
