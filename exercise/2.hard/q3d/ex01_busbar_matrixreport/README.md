# 演習1: ブスバー解析（縮退行列・キャパシタンス/インダクタンスレポート）

**目安時間: 90分**

題材: [1.normal/q3d/ex01_busbar/](../../../1.normal/q3d/ex01_busbar/) と同じモデル・Setupに、
AEDT内部のポスト処理（縮退行列演算・レポート作成）を追加する。

> この演習は「ブスバー解析シリーズ」の hard レベル。normalの内容は
> [1.normal/q3d/ex01_busbar/](../../../1.normal/q3d/ex01_busbar/) を参照。さらにPython側での
> データ集計とPyVista/CSV入出力を追加したものが
> [3.expert/q3d/ex01_busbar_postprocessing/](../../../3.expert/q3d/ex01_busbar_postprocessing/)
> にある（準備中）。

## 学習目標

- `insert_reduced_matrix()` で `JoinSeries`/`JoinParallel` の縮退行列演算を行い、複数バーを束ねた
  等価回路（合成ネット）を作る
- `Matrix.add_operation()` で、既存の縮退行列に追加の演算を重ねる方法を学ぶ
- `get_sources_for_plot()` で、レポート用の自己/相互容量・インダクタンスの式リストを自動生成する
- `post.create_report()` で、キャパシタンス（元の行列）・ACL（交流インダクタンス、縮退行列）の
  Data Tableレポートを作成する
- `post.create_fieldplot_surface()` で、ブスバー表面のAC電流密度（`Mag_SurfaceJac`）の
  フィールドプロット（コントア図）を作成する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析・ポスト処理を完成させてください
（モデル作成〜解析実行部分はnormalと同じ内容です）。

1. [1.normal/q3d/ex01_busbar/](../../../1.normal/q3d/ex01_busbar/) と同じ手順で、次を順に行う。
   - 3本のブスバー（Bar1/Bar2/Bar3）＋基板を作成する。
   - `auto_identify_nets()` でネットを識別する。
   - Bar1/Bar2/Bar3にソース・シンクを割り当てる（`Source1`/`Sink1`, `Source2`/`Sink2`, `Source3`/`Sink3`）。
   - セットアップ（`AdaptiveFreq="1000MHz"`）＋周波数スイープ（`sweep_type="Discrete"`,
     `save_fields=True`, 0〜10GHz, step 1GHz）を作成する（`Interpolating`だと`SaveFields`が常に
     `False`になり、本演習のマトリクスデータ取得ができなくなるため）。
2. `mr_series = q3d.insert_reduced_matrix(operation_name="JoinSeries", assignment=["Sink1", "Source2"],
   reduced_matrix="MR_Series", new_net_name="Series1")` で、Bar1とBar2を直列結合した縮退行列を作る。
3. `mr_series.add_operation(operation_type="JoinParallel", source_names=["Source1", "Source3"],
   new_net_name="SeriesPar", new_source_name="src_par", new_sink_name="snk_par")` で、
   Bar3を並列結合として追加する。
4. `q3d.analyze()` で解析を実行する。
5. 元の行列（Original）の自己容量・相互容量をレポート化する。
   - `original_self = q3d.matrices[0].get_sources_for_plot(get_self_terms=True, get_mutual_terms=False)`
   - `original_mutual = q3d.matrices[0].get_sources_for_plot(get_self_terms=False, get_mutual_terms=True)`
   - `post.create_report(expressions=original_self, plot_name="Original, Self Capacitances")`
   - `post.create_report(expressions=original_mutual, context="Original",
     plot_name="Original, Mutual Capacitances")`
6. 縮退行列（MR_Series）の自己インダクタンス（ACLカテゴリ）をレポート化する。
   - `reduced_self = mr_series.get_sources_for_plot(get_self_terms=True, get_mutual_terms=False,
     category="ACL")`
   - `post.create_report(expressions=reduced_self, context="MR_Series",
     plot_name="MR_Series, Self Inductances")`
7. `q3d.post.create_fieldplot_surface(assignment=["Bar1", "Bar2", "Bar3"], quantity="Mag_SurfaceJac",
   setup=f"{setup.name} : LastAdaptive", intrinsics={"Freq": "1GHz"}, plot_name="BusbarCurrentDensity")` で、
   3本のブスバー表面のAC電流密度（表皮効果による偏り）をフィールドプロット（コンター図）として作成する。
8. プロジェクトを保存し、`q3d.release_desktop()` でAEDTを終了する。

## ヒント

- `insert_reduced_matrix()` の `assignment` には、結合したいソース・シンクの名前リストを渡す
  （`JoinSeries` は「シンク→ソース」の経路を直列接続、`JoinParallel` は複数ソースを並列結合する）。
- `Matrix` オブジェクト（`mr_series`）に対して `add_operation()` を呼ぶと、同じ縮退行列の中に
  演算を積み重ねられる（新しい `Matrix` を作り直す必要はない）。
- `get_sources_for_plot()` の `category` 引数は、キャパシタンス（`"C"`、既定）・ACL（交流インダクタンス）・
  ACR（交流抵抗）などを切り替える。
- 縮退行列に対するレポートは `context=<縮退行列名>` を指定する（既定のOriginal行列とは別の
  コンテキストとして扱われる点に注意）。
- `Mag_SurfaceJac` は Q3D Extractorが内部的に保持するAC表面電流密度の量名（`reports_by_category.rl_fields()`
  のドキュメント例でも使われている）。AC RL解（本演習のセットアップは既定でAC RLが有効）が
  解けていれば参照できる。
- `create_fieldplot_surface()` の `setup` 引数は `"SetupName : LastAdaptive"` の形式で指定する。
  `intrinsics={"Freq": "1GHz"}` は `AdaptiveFreq="1000MHz"` と一致させる（アダプティブメッシュの解は
  必ずフィールドデータが保存されるため、周波数スイープの点を指定するより確実）。

## 評価基準

- [ ] normalと同じモデル・ソース・シンク・Setup・解析がエラーなく完了している
- [ ] 縮退行列（JoinSeries＋JoinParallel）が作成されている
- [ ] 元の行列の自己容量・相互容量レポートが作成されている
- [ ] 縮退行列の自己インダクタンス（ACL）レポートが作成されている
- [ ] ブスバー表面のAC電流密度（`Mag_SurfaceJac`）フィールドプロット（コントア図）が作成されている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `category="ACR"`（交流抵抗）のレポートも追加して、周波数依存性を比較してください。
- レポートの数値をPythonで取得し、CSV出力・周波数特性プロットまで行いたい場合は、このシリーズの
  expert（[3.expert/q3d/ex01_busbar_postprocessing/](../../../3.expert/q3d/ex01_busbar_postprocessing/)、
  準備中）に進んでみてください。
