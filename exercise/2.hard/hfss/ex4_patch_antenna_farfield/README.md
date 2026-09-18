# 演習4: プローブ給電パッチアンテナ（S11・遠方界のポスト処理）

**目安時間: 90分**

題材: `AEDT-AI-Assistant/examples/hfss/patch.py` を着想元に、このプロジェクト向けに構成を単純化して
独自に作成。

> セットアップ作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex3_setup_basics/](../../../0.easy/common_3d/ex3_setup_basics/) を確認するとよい。

> この演習は「パッチアンテナシリーズ」の hard レベル。モデル作成〜解析実行だけのものが
> `1.normal/hfss/ex4_patch_antenna/`、さらにPyVista/CSV入出力を追加したものが
> `3.expert/hfss/ex4_patch_antenna_design/` にある。

## 学習目標

- normalと同じパッチアンテナモデルに対して、目的別に周波数掃引を使い分ける
  （S11用のInterpolating掃引、遠方界用のフィールド保存Discrete掃引）
- S11（リターンロス）のレポートを作成する
- 遠方界（Far Field）のゲインパターンをElevation面でレポート作成する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Hfss(solution_type="Terminal", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. `1.normal/hfss/ex4_patch_antenna/solution.py` と同じ手順で、`Stackup3D`・パッチ・プローブ給電ポートまでを
   作成する。
3. セットアップ `"MySetup"`（`setup_type="HFSSDriven"`, `Frequency="10GHz"`）を作成する。
4. 周波数掃引を2つ追加する。
   - `"DiscreteSweep"`（`sweep_type="Discrete"`, `start_frequency=8`, `stop_frequency=12`,
     `num_of_freq_points=9`, `save_fields=True`）: 遠方界レポートに使うフィールドデータを保存する。
   - `"InterpolatingSweep"`（`sweep_type="Interpolating"`, `start_frequency=8`, `stop_frequency=12`,
     `save_fields=False`）: S11の広帯域応答を高速に計算する。
5. `setup.analyze()` で解析を実行する。
6. `hfss.create_scattering(plot="Return Loss", sweep=interp_sweep.name)` でS11のレポートを作成する。
7. `sphere = hfss.insert_infinite_sphere(theta_start=-180, theta_stop=180, theta_step=5, phi_start=0,
   phi_stop=180, phi_step=5)` で、遠方界の基準となる無限球面を作成する（`1.normal/hfss/ex4_patch_antenna/`
   で使った `create_region()`+`assign_radiation_boundary_to_objects()` だけでは無限球面が作られないため、
   遠方界レポートを作成する前に明示的に追加する必要がある）。
8. 中心周波数（10GHz）におけるゲインパターン（`db(GainTheta)`）をレポート作成する。
   `hfss.available_variations.nominal_values` を取得し、`Freq`/`Theta`/`Phi` を上書きしてから
   `hfss.post.create_report(..., setup_sweep_name=disc_sweep.name, context=sphere.name,
   report_category="Far Fields", plot_type="Radiation Pattern")` に渡す（`context` には手順7で作った
   無限球面の名前を指定する）。
9. プロジェクトを保存し、`hfss.release_desktop()` でAEDTを終了する。

## ヒント

- `create_frequency_sweep()` はSetupHFSSクラスのメソッドで、`add_sweep()` と似ているが引数名が異なる
  （`unit`/`start_frequency`/`stop_frequency`/`num_of_freq_points` など）。戻り値の `.name` 属性で
  掃引名を取得できる点は `add_sweep()` と同じ。
- 遠方界のレポートは、フィールドを保存した Discrete 掃引（`save_fields=True`）を参照する必要がある。
- `create_report()` の `context` 引数は、遠方界レポートの場合「無限球面の名前」を指定する仕様（APIドキュメントに明記）。
  `insert_infinite_sphere()` の戻り値（`sphere`）の `.name` をそのまま渡せばよい。
- **無限球面（Infinite Sphere）が存在しないと、遠方界レポートは正しく作成されず、
  レポート名にアクセスした際に `Invalid PropServer` のようなAEDT側スクリプトエラーになることがある。**
  `create_open_region()` は輻射境界と同時に既定の無限球面も作るが、`create_region()`+
  `assign_radiation_boundary_to_objects()` だけでは無限球面が作られないため、`insert_infinite_sphere()`
  を明示的に呼ぶ必要がある。

## 評価基準

- [ ] AEDTがTerminalソリューションで起動し、パッチアンテナモデルが作成されている
- [ ] Discrete/Interpolating の2つの周波数掃引が作成されている
- [ ] 解析がエラーなく完走している
- [ ] S11（Return Loss）のレポートが作成され、10GHz付近で十分に低い値（目安: -10dB以下）になっている
- [ ] Elevation面のゲインパターン（Radiation Pattern）レポートが作成されている

## 発展課題（任意）

- `patch.create_probe_port()` の `rel_x_offset` を変えて、S11の整合状態がどう変化するか確認してください。
- PyVistaでの3D可視化やCSV入出力を試したい場合は、`3.expert/hfss/ex4_patch_antenna_design/`
  （このシリーズのexpert）に進んでみてください。
