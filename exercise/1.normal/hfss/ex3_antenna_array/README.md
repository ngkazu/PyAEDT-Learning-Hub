# 演習3: ダイポールアレイアンテナ（モデル作成〜解析実行）

**目安時間: 60分**

題材: [PyAEDT Examples - Dipole antenna](https://examples.aedt.docs.pyansys.com/) を着想元に、
単一素子（`1.normal/hfss/ex1_dipole_antenna/`）を複数並べたアレイ構成へ拡張して独自に作成。

> モデル作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex1_basic_operations/](../../../0.easy/common_3d/ex1_basic_operations/) と
> [1.normal/hfss/ex1_dipole_antenna/](../ex1_dipole_antenna/) を確認するとよい。

> この演習は「ダイポールアレイアンテナシリーズ」の normal レベル。同じモデルにポスト処理を追加したものが
> `2.hard/hfss/ex3_antenna_array_farfield/`、さらにPyVista/CSV入出力（ビームステアリング）を追加したものが
> `3.expert/hfss/ex3_antenna_array_beamsteering/` にある。

## 学習目標

- `modeler.create_coordinate_system()` でローカル座標系を作り、3Dコンポーネントを任意の位置に配置する
- 同じ3Dコンポーネントを複数回挿入し、線形アレイ（等間隔に並んだアンテナ素子群）を構成する
- 複数ポートを持つモデルのSetup作成・解析実行を行う

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Hfss(solution_type="Modal", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. 設計変数 `l_dipole = "10.2cm"`, `element_spacing = "15cm"` を定義する。
3. `NUM_ELEMENTS`（`starter.py` 冒頭で `4` に設定済み）回ループし、素子ごとに次を行う。
   - `modeler.create_coordinate_system(origin=[f"{i}*element_spacing", 0, 0], name=f"CS_Element{i}")` で、
     X軸方向に `i * element_spacing` だけずらしたローカル座標系を作成する。
   - `hfss.get_component_variables("Dipole_Antenna_DM")` で取得したパラメータ辞書の `dipole_length` を
     `"l_dipole"` に書き換え、`coordinate_system=cs_name` を指定して `insert_3d_component()` で挿入する
     （`name=f"Dipole_{i}"` のように素子ごとに名前を変える）。
4. 中心周波数 `1.5GHz` で `create_open_region()` を実行し、Airboxと輻射境界を作成する。
5. セットアップ `"MySetup"` を作成する。`MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"]`、`MaximumPasses=2` とする。
6. 周波数掃引 `"Sweep1"`（`sweep_type="Interpolating"`, `RangeStart="1GHz"`, `RangeEnd="2GHz"`）を追加する。
7. `setup.analyze()` で解析を実行する。
8. プロジェクトを保存し、`hfss.release_desktop()` でAEDTを終了する（**レポート作成などのポスト処理は
   行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- `create_coordinate_system()` の `origin` には、数値のリストだけでなく `f"{i}*element_spacing"` のような
  変数式の文字列も渡せる（`i` はPythonのループ変数であり、HFSS側の変数ではない点に注意）。
- `insert_3d_component()` の `coordinate_system` 引数に作成したローカル座標系名を渡すと、
  そのローカル座標系の原点にコンポーネントが配置される（`origin` 引数はinsert_3d_component自体にはない）。
- 素子数を増やすと解析時間・メッシュ数が増える。まずは `NUM_ELEMENTS = 4` のまま進め、
  余裕があれば増減して比較するとよい。

## 評価基準

- [ ] AEDTが起動し、4つの `Dipole_Antenna_DM` コンポーネントが等間隔（`element_spacing`）に並んで配置されている
- [ ] Airboxと輻射境界（Open Region）が作成されている
- [ ] セットアップと周波数掃引が作成されている
- [ ] 解析がエラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `element_spacing` の値を変えて、素子間の結合（近接効果）がモデル形状にどう影響するか確認してください。
- 各素子のS11・S21（結合）や、アレイ全体の放射パターンを確認したい場合は、
  `2.hard/hfss/ex3_antenna_array_farfield/`（このシリーズのhard）に進んでみてください。
