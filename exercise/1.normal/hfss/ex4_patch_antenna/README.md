# 演習4: プローブ給電パッチアンテナ（モデル作成〜解析実行）

**目安時間: 60分**

題材: `AEDT-AI-Assistant/examples/hfss/patch.py`（`Stackup3D` を使ったプローブ給電パッチアンテナの例）を
着想元に、このプロジェクト向けに構成を単純化して独自に作成。

> モデル作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex1_basic_operations/](../../../0.easy/common_3d/ex1_basic_operations/) を確認するとよい。

> この演習は「パッチアンテナシリーズ」の normal レベル。同じモデルにポスト処理を追加したものが
> `2.hard/hfss/ex4_patch_antenna_farfield/`、さらにPyVista/CSV入出力を追加したものが
> `3.expert/hfss/ex4_patch_antenna_design/` にある。

## 学習目標

- `Stackup3D` クラスで、地板（ground）→誘電体基板（dielectric）→信号層（signal）の積層構造を作る
- 信号層にパッチ（矩形パッチアンテナ）を作成し、誘電体・地板をパッチサイズに合わせて自動リサイズする
- 同軸プローブ給電ポート（`create_probe_port`）を割り当て、Terminalソリューションで解析する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Hfss(solution_type="Terminal", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動し、
   `hfss.modeler.model_units = "mm"` を設定する。
2. `Stackup3D(hfss)` を作成し、次の順にレイヤーを積み上げる。
   - `stackup.add_ground_layer("ground", material="copper", thickness=0.035, fill_material="air")`
   - `stackup.add_dielectric_layer("dielectric", thickness="0.5mm", material="Duroid (tm)")`
   - `stackup.add_signal_layer("signal", material="copper", thickness=0.035, fill_material="air")`
3. `signal.add_patch(patch_length=9.57, patch_width=9.25, patch_name="Patch", frequency=1e10)` で
   信号層にパッチを作成する。
4. `stackup.resize_around_element(patch)` で、誘電体基板・地板をパッチサイズに合わせて自動リサイズする。
5. `hfss.modeler.create_region(pad_value=[3, 3, 3, 3, 3, 3], pad_type="Absolute Offset", name="Region")` で
   解析領域（Airbox）を作成し、`hfss.assign_radiation_boundary_to_objects(region)` で輻射境界を割り当てる。
6. `patch.create_probe_port(ground, rel_x_offset=0.485)` で、パッチに同軸プローブ給電ポートを割り当てる。
7. セットアップ `"MySetup"`（`setup_type="HFSSDriven"`, `Frequency="10GHz"`）を作成し、
   `setup.create_frequency_sweep(unit="GHz", name="Sweep1", start_frequency=8, stop_frequency=12,
   sweep_type="Interpolating")` で周波数掃引を追加する。
8. `setup.analyze()` で解析を実行する。
9. プロジェクトを保存し、`hfss.release_desktop()` でAEDTを終了する（**レポート作成などのポスト処理は
   行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- プローブ（同軸コネクタ）給電はAEDTの仕様上 **Terminal ソリューション** を使う（Modalではない）。
  ダイポール・アレイ・導波管フィルタの演習（Modalソリューション）とはこの点が異なる。
- `Stackup3D` はレイヤーの積層順を「地板→誘電体→信号層」のように呼び出した順で管理する。
  信号層は必ず誘電体層の直後（真上）に追加する必要がある。
- `add_patch()` の `frequency` 引数はパッチの設計目標周波数（Hz単位）。ここでは10GHz(`1e10`)を想定した
  寸法（`patch_length=9.57mm`, `patch_width=9.25mm`）を直接指定している。
- `create_region()` の引数名は `pad_value`/`pad_type`（`pad_length`/`is_percentage` という古い引数名も
  後方互換で動くが、本演習では現行の引数名を使う）。

## 評価基準

- [ ] AEDTがTerminalソリューションで起動し、地板・誘電体・信号層・パッチが作成されている
- [ ] Airboxと輻射境界が作成されている
- [ ] プローブ給電ポートが割り当てられている
- [ ] セットアップと周波数掃引が作成されている
- [ ] 解析がエラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `patch_length`/`patch_width` の値を変えて、共振周波数がどう変化するか確認してください。
- S11の値や放射パターンを確認したい場合は、`2.hard/hfss/ex4_patch_antenna_farfield/`
  （このシリーズのhard）に進んでみてください。
