# 演習1: 半波長ダイポールアンテナ（モデル作成〜解析実行）

**目安時間: 60分**

題材: [PyAEDT Examples - Dipole antenna](https://examples.aedt.docs.pyansys.com/) を着想元に、
このプロジェクト向けに構成を単純化して独自に作成。

> 起動〜変数〜形状〜保存の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex1_basic_operations/](../../../0.easy/common_3d/ex1_basic_operations/) を、
> セットアップ作成の基本操作は
> [0.easy/common_3d/ex3_setup_basics/](../../../0.easy/common_3d/ex3_setup_basics/) を確認するとよい。

> この演習は「ダイポールアンテナシリーズ」の normal レベル。同じモデルにポスト処理を追加したものが
> `2.hard/hfss/ex1_dipole_farfield/`、さらにPyVista/CSV入出力を追加したものが
> `3.expert/hfss/ex1_dipole_s11_postprocessing/` にある。

## 学習目標

- 組み込み3Dコンポーネントを挿入し、コンポーネント側のパラメータを設計変数に紐づける
- `create_open_region()` で解析領域（Airbox + 輻射境界）を一括作成する
- Setupと周波数掃引を作成し、解析を実行する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Hfss(solution_type="Modal", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. 設計変数 `l_dipole = "10.2cm"` を定義する。
3. 組み込み3Dコンポーネント `"Dipole_Antenna_DM"` を挿入する。挿入前に
   `hfss.get_component_variables("Dipole_Antenna_DM")` でコンポーネントが公開しているパラメータの
   デフォルト値を辞書として取得し、長さに関係するパラメータ（`dipole_length`）の値を `"l_dipole"` に
   書き換えてから挿入する。
4. 中心周波数 `1.5GHz` で `create_open_region()` を実行し、Airboxと輻射境界を作成する。
5. セットアップ `"MySetup"` を作成する。`MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"]`（帯域の両端でアダプティブ
   メッシュを行う）、`MaximumPasses=2` とする。
6. 上記セットアップに、周波数掃引 `"Sweep1"`（`sweep_type="Interpolating"`, `RangeStart="1GHz"`,
   `RangeEnd="2GHz"`）を追加する。
7. `setup.analyze()` で解析を実行する。
8. プロジェクトを保存し、`hfss.release_desktop()` でAEDTを終了する（**レポート作成などのポスト処理は
   行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- `hfss.components3d` は、登録済みの組み込み3Dコンポーネント名 → ファイルパスの辞書。
  `hfss.components3d["Dipole_Antenna_DM"]` でファイルパスが取れる。
- `hfss.get_component_variables(name)` はコンポーネントが公開しているパラメータのデフォルト値を
  辞書で返す。このキーを書き換えてから `hfss.modeler.insert_3d_component(input_file=..., geometry_parameters=...)`
  に渡す（実際のパラメータ名はAEDTのGUIで3Dコンポーネントの編集画面からも確認できる）。
- セットアップの作成は `hfss.create_setup(name="MySetup", MultipleAdaptiveFreqsSetup=[...], MaximumPasses=...)`
  のように、`create_setup` の `**kwargs` にネイティブAPIのプロパティ名をそのまま渡す方法を使う
  （作成後に `setup.props[...] = ...` としてから `setup.update()` する方法もあるが、プロパティの組み合わせに
  よっては期待通りに反映されないことがあるため、作成時にまとめて指定する方が確実）。
- 周波数掃引は `setup.add_sweep(name=..., sweep_type=..., RangeStart=..., RangeEnd=...)` で追加する。

## 評価基準

- [ ] AEDTが起動し、`Dipole_Antenna_DM` コンポーネントが挿入されている
- [ ] Airboxと輻射境界（Open Region）が作成されている
- [ ] セットアップと周波数掃引が作成されている
- [ ] 解析がエラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `l_dipole` の値を変えて共振周波数がどう変化するか確認してください（半波長の式 `l = c0 / (2f)` と比較）。
- S11の値を確認したい場合は、`2.hard/hfss/ex1_dipole_farfield/`（このシリーズのhard）に進んでみてください。
