# 演習3: マイクロストリップ線路（モデル作成〜解析実行）

**目安時間: 60分**

題材: `AEDT-AI-Assistant/examples/hfss/field_overlay.py`（Terminalソリューションのマイクロストリップ線路、
AEDT 2026.1 / PyAEDT 1.3.0 で動作検証済みの例）を着想元に、このプロジェクト向けに構成を単純化して作成。

> モデル作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex01_basic_operations/](../../../0.easy/common_3d/ex01_basic_operations/) を確認するとよい。

> この演習は「マイクロストリップ線路シリーズ」の normal レベル。同じモデルにポスト処理を追加したものが
> `2.hard/hfss/ex03_microstrip_line_fieldplot/`、さらにPyVista/CSV入出力を追加したものが
> `3.expert/hfss/ex03_microstrip_line_postprocessing/` にある。

## 学習目標

- 2Dシート（`create_rectangle`）には `Material` プロパティが無く、導体として振る舞わせるには
  `assign_finite_conductivity()` を明示的に割り当てる必要があることを理解する
- Wave Port・輻射境界など、複数の境界条件が同じ形状に重複しないよう、面単位で割り当てを制御する
- `hfss.validate_full_design()` でモデルの妥当性を確認する習慣を身につける
- `hfss.create_linear_count_sweep()`（`hfss`側のメソッド。`setup`のメソッドではない）で周波数スイープを追加する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Hfss(solution_type="Terminal", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動し、
   `hfss.modeler.model_units = "mm"` を設定する。
2. 基板（3Dソリッド）を `origin=[0, -SUB_W/2, 0]`, `sizes=[LINE_L, SUB_W, SUB_H]`,
   `material="alumina_96pct"` で作成する。
3. GND と信号線を2Dシート（`modeler.create_rectangle()`）として作成する。
   - GND: `orientation=Plane.XY`, `origin=[0, -SUB_W/2, 0]`, `sizes=[LINE_L, SUB_W]`
   - Line: `orientation=Plane.XY`, `origin=[0, -LINE_W/2, SUB_H]`, `sizes=[LINE_L, LINE_W]`
   - それぞれに `hfss.assign_finite_conductivity(assignment=..., material="copper", name=...)` を割り当てる。
4. エアボックスを、基板の上面（`z=SUB_H`）から `sizes=[LINE_L, SUB_W, AIR_H]`, `material="vacuum"` で作成する。
5. エアボックスの両端面（YZ平面のシート）に Wave Port（`modes=1`, `renormalize=True`, `impedance=50`）を
   `hfss.wave_port()` で作成する。
6. エアボックスの6面のうち、下面（GND/Lineと接する面）と両端面（Wave Portの面）を除いた面だけに、
   `hfss.assign_radiation_boundary_to_faces()` で輻射境界を割り当てる。
7. `hfss.validate_full_design()` でモデルを検証する。
8. セットアップ `"Setup1"`（`Frequency="10GHz"`, `MaxDeltaS=0.02`, `MaximumPasses=6`）を作成し、
   `hfss.create_linear_count_sweep(setup="Setup1", unit="GHz", start_frequency=0.1, stop_frequency=10,
   num_of_freq_points=201, name="Sweep", sweep_type="Interpolating")` で周波数スイープを追加する。
9. `setup.analyze()` で解析を実行する。
10. プロジェクトを保存し、`hfss.release_desktop()` でAEDTを終了する（**レポート作成などのポスト処理は
    行わない**。ポスト処理はhard以降で追加する）。

## ヒント

- `create_rectangle()` で作った2Dシートに `assign_material()` を呼んでも、エラーにはならないが
  実質的に何も起こらない（シートに `Material` プロパティ自体が存在しない）。導体として扱うには
  `assign_finite_conductivity()`（有限導電率）や `assign_perfect_e()`（完全導体）を使う。
- `assign_radiation_boundary_to_objects("AirBox")` は6面すべてに輻射境界を割り当てるため、
  GND/Line（下面）やWave Port（両端面）と境界が重複してしまう。`airbox.faces` を走査し、
  各面の中心座標（`face.center`）から下面・端面を判定して除外する。
- 境界の重複などの問題は、作成時にはエラーにならず `validate_full_design()` で初めて警告される
  ことがある。手動で境界を割り当てたときは必ず検証する習慣をつける。
- `create_linear_count_sweep()` は `setup.add_sweep()` とは異なり、`hfss`（アプリオブジェクト）側の
  メソッドとして呼び出す（`setup="Setup1"` のように名前で対象セットアップを指定する）。

## 評価基準

- [ ] AEDTがTerminalソリューションで起動し、基板・GND・信号線・エアボックスが作成されている
- [ ] GND・信号線に `assign_finite_conductivity()` が割り当てられている
- [ ] Wave Portが両端に作成され、輻射境界がエアボックスの上面・側面のみに割り当てられている
- [ ] `validate_full_design()` でエラー・警告がない（あった場合は原因を修正している）
- [ ] セットアップと周波数スイープが作成されている
- [ ] 解析がエラーなく完走し、プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `line_w`（信号線幅）を変えて、特性インピーダンスがどう変化するか（S11の変化から）確認してください。
- S21やフィールド分布を確認したい場合は、`2.hard/hfss/ex03_microstrip_line_fieldplot/`
  （このシリーズのhard）に進んでみてください。
