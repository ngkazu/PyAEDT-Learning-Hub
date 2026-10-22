# 演習1: ダイポールアンテナ S11・遠方界データの Python 後処理（VSWR・帯域幅算出・CSV入出力）

**目安時間: 90分以上**

題材: 演習「1.normal/hfss/ex01_dipole_antenna」で作成したモデルを土台に、AEDT側の操作は最小限にとどめ、
**Pythonでのカスタムデータ処理とCSV入出力、PyVistaでの可視化**に重点を置く
（`docs/difficulty-criteria.md` の expert レベルに相当）。

> このプロジェクトの各演習は独立して実行できるように作られている。本演習は
> `1.normal/hfss/ex01_dipole_antenna` のモデルをこのスクリプト内で作り直した上で、
> S11・遠方界データをPythonで解析する（normalの演習を先にやっていなくても単体で進められる）。
> 同じモデルでS11・遠方界のAEDT内部レポートのみを作成するものが
> `2.hard/hfss/ex01_dipole_farfield/`（このシリーズのhard）にある。モデル作成の基本操作は
> [0.easy/common_3d/ex01_basic_operations/](../../../0.easy/common_3d/ex01_basic_operations/)、
> セットアップ作成の基本操作は
> [0.easy/common_3d/ex03_setup_basics/](../../../0.easy/common_3d/ex03_setup_basics/) で先に練習できる。

## 学習目標

- `csv.DictReader` で条件CSV（`conditions.csv`）を読み込み、モデルのパラメータに反映する
- `post.get_solution_data()` で解析結果を Python 側（NumPy配列）として取得する
- S11（dB）から反射係数・VSWR（電圧定在波比）を自分で計算する
- -10dB帯域幅（S11が-10dBを下回る周波数範囲）をPythonのロジックで自動的に求める
- matplotlib で S11 と VSWR を1つの図に重ねてプロットし、帯域幅の範囲を注釈する
- S11・VSWRの計算結果をCSVファイルに出力する
- `hfss.get_antenna_data()` と PyVista で遠方界の3D放射パターンを画像出力する
- PyVistaのインタラクティブウィンドウで3D放射パターンをマウス操作（回転・拡大）しながら確認する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 同じフォルダにある `conditions.csv`（`l_dipole`, `center_freq` の列を持つ1行のCSV）を
   `csv.DictReader` で読み込み、`l_dipole` / `center_freq` の値を取得する。
2. `1.normal/hfss/ex01_dipole_antenna/solution.py` と同じ手順で、ダイポールアンテナを作成・解析する
   （変数、3Dコンポーネント挿入、Open Region、セットアップ、周波数スイープ、解析実行まで。長さと中心周波数は
   手順1でCSVから読み込んだ値を使う）。
3. `hfss.post.get_solution_data(expressions=..., setup_sweep_name=hfss.nominal_sweep, report_category="Modal Solution Data")`
   で S11の解析結果（`SolutionData`）を取得する。ポート名は `"Dipole1_1"` のように決め打ちせず、
   `hfss.excitation_names[0]` で実際の励振名を取得して式を組み立てる。
   （`hfss.post.get_solution_data()` のスイープ指定引数名は `setup_sweep_name` であり、`Setup` オブジェクト自体の
   `get_solution_data()`（引数名 `sweep`）とは別のメソッドなので混同しないよう注意）。
4. `get_expression_data()` を使って、周波数（x軸）と S11 の dB値（`formula="db20"`）を NumPy配列として取り出す。
5. dB値から線形の反射係数の絶対値 `|Γ| = 10 ** (S11_dB / 20)` を計算し、
   VSWR `= (1 + |Γ|) / (1 - |Γ|)` を求める（NumPyでベクトル演算する）。
6. S11が `-10dB` を下回る周波数範囲（-10dB帯域幅）を、配列を走査して自動的に求める。
7. matplotlib で以下を1つの図（2軸: 左にS11[dB]、右にVSWR）にプロットする。
   - S11 [dB] vs 周波数
   - VSWR vs 周波数
   - -10dB帯域幅の範囲を `axvspan` 等で網掛け表示する
8. 図を `.png` ファイルとして保存する。
9. 周波数・S11[dB]・VSWRの3列を持つCSVファイル（`results_s11_vswr.csv`）に結果を出力する。
10. `hfss.get_antenna_data()` で遠方界データ（`FfdSolutionDataExporter`）を取得し、
    `ffdata.farfield_data.plot_3d(quantity="RealizedGain", output_file=..., show=False)` で
    PyVistaによる3D放射パターンを画像ファイルとして出力する。
11. 同じ `ffdata.farfield_data` に対して、今度は `output_file` を渡さず `show=True` で
    `plot_3d(quantity="RealizedGain", show=True)` を呼び、インタラクティブなPyVistaウィンドウ
    （マウスで回転・拡大できる）を表示する。ウィンドウを閉じると次のステップに進む。
12. プロジェクトを保存し、`release_desktop()` で終了する。

## ヒント

- `csv.DictReader` はヘッダー行をキーにした辞書を1行ずつ返す。`next(reader)` で最初の1行を取得できる。
- `SolutionData.get_expression_data(expression, formula="db20")` は `(x配列, y配列)` のタプルを返す。
  `formula="real"`/`"imag"`/`"mag"`/`"db20"` などが選べる。
- `get_solution_data()` は `report_category` を明示しないと、Modal解析のSパラメータ式が見つからず
  例外になることがある。`report_category="Modal Solution Data"` を指定する。
- VSWR は理論上 `|Γ| < 1` の範囲でのみ定義できる（`|Γ| >= 1` になる場合は入力データやポート名を見直す）。
- -10dB帯域幅は、`numpy.where(s11_db <= -10)` のようにブールインデックスで対象周波数を抽出し、
  その最小値・最大値を取ればよい。
- matplotlib で左右2軸のグラフを作るには `ax1 = plt.subplots()` の後 `ax2 = ax1.twinx()` を使う。
- 画像保存のみで画面表示はしないため、`import matplotlib.pyplot as plt` の前に
  `matplotlib.use("Agg")` を呼び、GUIバックエンド（TkAgg等）が自動選択されるのを防ぐ。
- CSV出力は `csv.writer` で `zip(freq, s11_db, vswr)` を1行ずつ書き込めばよい。
- `hfss.get_antenna_data()` は `setup`/`sphere` を省略すると、`nominal_adaptive` と
  既存（なければ自動作成）の無限球面を使う。追加のセットアップ変更は不要。
- `plot_3d()` は `output_file` を渡すと画面表示なしでスクリーンショットのみ保存し、`output_file` を渡さず
  `show=True` にすると `auto_close=False` のインタラクティブウィンドウが開く（マウスで自由に視点を変えられる）。
  同じ結果を画像保存と画面確認の両方で使いたい場合は、このように2回呼び出すのが手軽。

## 評価基準

- [ ] `conditions.csv` の値がモデルのパラメータ（`l_dipole`, 解析領域の中心周波数）に反映されている
- [ ] S11データが `SolutionData` として取得できている
- [ ] VSWRがNumPyの配列演算で正しく計算されている（`|Γ|>=1` になる異常値がないか確認する）
- [ ] -10dB帯域幅が自動的に求められている
- [ ] S11とVSWRを重ねたグラフが作成され、帯域幅の範囲が視覚的に分かるようになっている
- [ ] グラフが画像ファイルとして保存されている
- [ ] S11・VSWRの結果がCSVファイルに出力されている
- [ ] 遠方界の3D放射パターンがPyVistaで画像出力されている
- [ ] 遠方界の3D放射パターンがインタラクティブなPyVistaウィンドウで表示され、マウスで回転できる

## 発展課題（任意）

- `conditions.csv` に複数行の条件（`l_dipole` の異なる値など）を用意し、行ごとにループして解析し、
  共振周波数とVSWR帯域幅の関係を比較するグラフを作ってみてください。
- `plot_3d` の `quantity` を `"rETotal"` などに変えて、異なる物理量の放射パターンを比較してみてください。
