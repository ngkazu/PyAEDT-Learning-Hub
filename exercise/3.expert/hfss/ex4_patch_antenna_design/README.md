# 演習4: プローブ給電パッチアンテナの設計計算とPython後処理

**目安時間: 90分以上**

題材: 演習「2.hard/hfss/ex4_patch_antenna_farfield」で作成したモデルを土台に、パッチの寸法を
**Pythonで理論計算してからモデルに適用する**点に重点を置く（`docs/difficulty-criteria.md` の
expert レベルに相当）。

> このプロジェクトの各演習は独立して実行できるように作られている。本演習は
> `2.hard/hfss/ex4_patch_antenna_farfield` のモデルをこのスクリプト内で作り直した上で、
> パッチの幅・長さを固定値ではなく設計式から計算する（hardの演習を先にやっていなくても単体で進められる）。
> モデル作成の基本操作は
> [0.easy/common_3d/ex1_basic_operations/](../../../0.easy/common_3d/ex1_basic_operations/) で先に練習できる。

## 学習目標

- `csv.DictReader` で設計条件CSV（`design_conditions.csv`）を読み込み、設計目標（周波数・誘電率・基板厚）を取得する
- マイクロストリップパッチアンテナの伝送線路モデル（transmission-line model）をPythonで実装し、
  パッチの幅・長さを理論計算する
- 計算した寸法をAEDTモデルにそのまま適用し、設計値の妥当性を実際のS11・放射パターンで検証する
- 計算結果をCSVファイルに出力する
- `hfss.get_antenna_data()` と PyVista で3D放射パターンを可視化する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 同じフォルダにある `design_conditions.csv`（`design_freq_ghz`, `eps_r`, `substrate_thickness_mm` の
   列を持つ1行のCSV）を `csv.DictReader` で読み込み、各値を取得する。
2. 伝送線路モデルで、パッチの幅 `width_mm`・長さ `length_mm` を計算する。
   - `width = (c / (2*f0)) * sqrt(2/(eps_r+1))`
   - `eps_reff = (eps_r+1)/2 + (eps_r-1)/2 * (1+12*h/width)**-0.5`
   - `delta_L = 0.412*h*(eps_reff+0.3)*(width/h+0.264) / ((eps_reff-0.258)*(width/h+0.8))`
   - `length = c/(2*f0*sqrt(eps_reff)) - 2*delta_L`
   （`c` は光速 `3e8 m/s`、`f0` は設計周波数[Hz]、`h` は基板厚[m]。単位に注意して計算すること）
3. 計算結果（設計条件と `eps_reff`, `patch_width_mm`, `patch_length_mm`）をCSVファイル
   （`results_patch_dimensions.csv`）に出力する。
4. `Hfss(solution_type="Terminal", ...)` で起動し、`1.normal/hfss/ex4_patch_antenna/solution.py` と
   同じ手順でパッチアンテナを作成する。ただし `patch_width`/`patch_length` には固定値ではなく、
   手順2で計算した `width_mm`/`length_mm` を使う。
5. セットアップ `"MySetup"`（`Frequency=f"{design_freq_ghz}GHz"`）と、設計周波数の±20%の範囲の
   周波数スイープ（Interpolating）を作成する。
6. `setup.analyze()` で解析を実行する。
7. `hfss.get_antenna_data()` で遠方界データ（`FfdSolutionDataExporter`）を取得し、
   `ffdata.farfield_data.plot_3d(quantity="RealizedGain", output_file=..., show=False)` で
   PyVistaによる3D放射パターンを画像ファイルとして出力する。
8. 同じ `ffdata.farfield_data` に対して、今度は `output_file` を渡さず `show=True` で
   `plot_3d(quantity="RealizedGain", show=True)` を呼び、インタラクティブなPyVistaウィンドウ
   （マウスで回転・拡大できる）を表示する。
9. プロジェクトを保存し、`release_desktop()` で終了する。

## ヒント

- 伝送線路モデルの式はすべてSI単位（メートル・ヘルツ）で計算し、最後にAEDTモデル用にミリメートルへ
  変換するとよい（単位を混在させると計算結果が大きく狂うので注意）。
- `design_conditions.csv` の `eps_r=2.2` は `Duroid (tm)` 材料の比誘電率にほぼ相当する
  （`1.normal/hfss/ex4_patch_antenna/` で固定値として使っていた `patch_length=9.57`,
  `patch_width=9.25` は、ほぼ同じ設計条件から得られる値のはずなので、計算結果と比較してみるとよい）。
- 計算したパッチが正しければ、S11の共振点が設計周波数（`design_freq_ghz`）付近に現れる。
  大きくずれる場合は式の単位変換を見直す。

## 評価基準

- [ ] `design_conditions.csv` の値が正しく読み込まれている
- [ ] パッチの幅・長さが伝送線路モデルの式通りに計算されている
- [ ] 計算結果がCSVファイルに出力されている
- [ ] 計算した寸法でモデルが作成され、解析がエラーなく完走している
- [ ] 遠方界の3D放射パターンがPyVistaで画像出力されている
- [ ] 3D放射パターンがインタラクティブなPyVistaウィンドウで表示され、マウスで回転できる

## 発展課題（任意）

- `design_conditions.csv` の `design_freq_ghz` や `eps_r` を変えて、計算される寸法とAEDTでの
  実際の共振周波数がどの程度一致するか比較してみてください。
- `2.hard/hfss/ex4_patch_antenna_farfield/` のS11レポート作成コードを本演習に追加し、
  設計値の妥当性をより定量的に確認してみてください。
