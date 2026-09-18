# 演習3: ダイポールアレイアンテナ ビームステアリングの Python 後処理

**目安時間: 90分以上**

題材: 演習「2.hard/hfss/ex3_antenna_array_farfield」で作成したモデルを土台に、AEDT側の操作は最小限にとどめ、
**Pythonでのカスタムデータ処理（理論アレイファクタ計算）とCSV入出力、PyVistaでの可視化**に重点を置く
（`docs/difficulty-criteria.md` の expert レベルに相当）。

> このプロジェクトの各演習は独立して実行できるように作られている。本演習は
> `2.hard/hfss/ex3_antenna_array_farfield` のモデルをこのスクリプト内で作り直した上で、
> 位相重み（ビームステアリング条件）をCSVから読み込んで適用する
> （hardの演習を先にやっていなくても単体で進められる）。モデル作成の基本操作は
> [0.easy/common_3d/ex1_basic_operations/](../../../0.easy/common_3d/ex1_basic_operations/) で先に練習できる。

## 学習目標

- `csv.DictReader` で位相重みCSV（`phase_weights.csv`）を読み込み、素子ごとの励振位相に反映する
- `hfss.edit_sources()` で、解を再計算せずに各ポートの励振振幅・位相を変更する
  （ビームステアリングの基本原理: 素子間に線形位相差を与えるとビーム方向が傾く）
- NumPyでアレイファクタ（Array Factor）の理論式を実装し、シミュレーション結果と比較する
- `hfss.get_antenna_data()` と PyVista で、位相重み適用後の3D放射パターンを可視化する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 同じフォルダにある `phase_weights.csv`（`element_index`, `phase_deg` の列を持つ、素子数分の行のCSV）を
   `csv.DictReader` で読み込み、`element_index` の昇順にソートした `phase_deg` のリストを作る。
2. `1.normal/hfss/ex3_antenna_array/solution.py` と同じ手順で、`NUM_ELEMENTS`（既定4）個の
   `Dipole_Antenna_DM` を配置し、セットアップを作成して解析を実行する。
3. `sorted(hfss.excitation_names)` と手順1の `phases_deg` を素子番号順に対応させ、
   `hfss.edit_sources({name: ("1W", f"{phase}deg") for name, phase in zip(...)})` で、
   各ポートの励振位相を変更する（振幅はすべて `"1W"` で固定）。
4. NumPyで理論上のアレイファクタを計算する。
   `array_factor(theta) = sum_n exp(j * (k * ELEMENT_SPACING_M * n * sin(theta) + phase_n))`
   （`k = 2*pi/wavelength`）の絶対値を `20*log10(...)` でdB化し、`theta` を `-90度〜90度` で走査する。
5. 理論アレイファクタを横軸 `theta`、縦軸dBでmatplotlibにプロットし、ピーク角度を線で示す。
6. 図を `.png` ファイルとして保存し、`theta_deg`/`array_factor_db` の2列を持つCSVファイル
   （`results_array_factor.csv`）に結果を出力する。
7. `hfss.get_antenna_data()` で遠方界データ（`FfdSolutionDataExporter`）を取得し、
   `ffdata.farfield_data.plot_3d(quantity="RealizedGain", output_file=..., show=False)` で
   PyVistaによる3D放射パターンを画像ファイルとして出力する（`edit_sources()` で設定した位相重みが
   反映され、ビームが傾いたパターンが得られる）。
8. 同じ `ffdata.farfield_data` に対して、今度は `output_file` を渡さず `show=True` で
   `plot_3d(quantity="RealizedGain", show=True)` を呼び、インタラクティブなPyVistaウィンドウ
   （マウスで回転・拡大できる）を表示する。
9. プロジェクトを保存し、`release_desktop()` で終了する。

## ヒント

- `edit_sources()` は解析済みのフィールドデータを重み付けして再合成するだけなので、`setup.analyze()` を
  やり直す必要はない（ポート励振の変更が高速に反映される）。
- `hfss.excitation_names` の並び順は保証されないため、`sorted()` で並べ替えてから
  `phase_weights.csv` の `element_index` 順（0, 1, 2, ...）と対応させる。
- アレイファクタの理論式はあくまで簡易的な1次元モデル（素子はX軸上に等間隔・無指向性と仮定）であり、
  実際のダイポール素子パターンや3Dモデルの角度定義とは厳密には一致しない。傾向の比較用と考えること。
- `phase_weights.csv` の位相差を大きくするほど、理論上のビーム方向（ピーク角度）が正面（0度）からずれる。
  実際のPyVista表示でも同じ傾向（ビームが傾く）が確認できるはずである。

## 評価基準

- [ ] `phase_weights.csv` の値が読み込まれ、`hfss.edit_sources()` で各ポートの励振位相に反映されている
- [ ] 理論アレイファクタがNumPyで正しく計算されている
- [ ] 理論アレイファクタのグラフが作成され、画像ファイルとして保存されている
- [ ] 理論アレイファクタの結果がCSVファイルに出力されている
- [ ] 位相重み適用後の3D放射パターンがPyVistaで画像出力されている
- [ ] 3D放射パターンがインタラクティブなPyVistaウィンドウで表示され、マウスで回転できる

## 発展課題（任意）

- `phase_weights.csv` の位相差を変えて、理論上のピーク角度と実際のPyVista表示のビーム方向が
  対応しているか比較してみてください。
- 位相だけでなく振幅（テーパー）も変えて、サイドローブレベルがどう変化するか確認してみてください。
