# 演習1: 半波長ダイポールアンテナ（S11・遠方界のポスト処理）

**目安時間: 90分**

題材: [PyAEDT Examples - Dipole antenna](https://examples.aedt.docs.pyansys.com/) を着想元に、
このプロジェクト向けに構成を単純化して独自に作成。

> セットアップ作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex3_setup_basics/](../../../0.easy/common_3d/ex3_setup_basics/) を確認するとよい。

> この演習は「ダイポールアンテナシリーズ」の hard レベル。モデル作成〜解析実行だけのものが
> `1.normal/hfss/ex1_dipole_antenna/`、さらにPyVista/CSV入出力を追加したものが
> `3.expert/hfss/ex1_dipole_s11_postprocessing/` にある。

## 学習目標

- normalと同じモデル（組み込み3Dコンポーネントのダイポール）に対して、目的別に周波数掃引を使い分ける
  （S11用のInterpolating掃引、遠方界用のフィールド保存Discrete掃引）
- S11（リターンロス）のレポートを作成する
- 遠方界（Far Field）のゲインパターンをElevation面でレポート作成する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Hfss(solution_type="Modal", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. 設計変数 `l_dipole = "10.2cm"` と、中心周波数 `center_freq = "1.5GHz"` を定義する。
3. 組み込み3Dコンポーネント `"Dipole_Antenna_DM"` を挿入する（`dipole_length` パラメータを `l_dipole` に紐づける）。
4. `create_open_region(frequency=center_freq)` で解析領域を作成する。
5. セットアップ `"MySetup"` を作成する（`MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"]`, `MaximumPasses=2`）。
6. 周波数掃引を2つ追加する。
   - `"DiscreteSweep"`（`sweep_type="Discrete"`, `RangeStart="1GHz"`, `RangeEnd="2GHz"`, `RangeStep="0.5GHz"`,
     `SaveFields=True`）: 遠方界レポートに使うフィールドデータを各周波数点で保存する。
   - `"InterpolatingSweep"`（`sweep_type="Interpolating"`, `RangeStart="1GHz"`, `RangeEnd="2GHz"`,
     `SaveFields=False`）: S11の広帯域応答を高速に計算する。
7. `setup.analyze()` で解析を実行する。
8. `hfss.create_scattering(plot="Return Loss", sweep=interp_sweep.name)` でS11のレポートを作成する。
9. 中心周波数における Elevation 面のゲインパターン（`db(GainTheta)`）をレポート作成する。
   `hfss.available_variations.nominal_values` を取得し、`Freq`/`Theta`/`Phi` を上書きしてから
   `hfss.post.create_report(..., setup_sweep_name=disc_sweep.name, context="Elevation",
   report_category="Far Fields", plot_type="Radiation Pattern")` に渡す。
10. プロジェクトを保存し、`hfss.release_desktop()` でAEDTを終了する。

## ヒント

- 遠方界のレポートは、フィールドを保存した Discrete 掃引（`SaveFields=True`）を参照する必要がある。
  Interpolating掃引はSパラメータの高速計算用で、フィールドは保存されない。
- `hfss.available_variations.nominal_values` は、現在のモデルのノミナル変数値（Freq/Theta/Phiなど）を
  辞書として返す。この辞書のキーを書き換えてから `create_report` の `variations` 引数に渡す。
- `context="Elevation"` は、HFSSが既定で用意しているカットプレーン名（球面座標のΦ=0/90面）。

## 評価基準

- [ ] AEDTが起動し、`Dipole_Antenna_DM` コンポーネントが挿入されている
- [ ] Discrete/Interpolating の2つの周波数掃引が作成されている
- [ ] 解析がエラーなく完走している
- [ ] S11（Return Loss）のレポートが作成され、1.5GHz付近で十分に低い値（目安: -10dB以下）になっている
- [ ] Elevation面のゲインパターン（Radiation Pattern）レポートが作成されている

## 発展課題（任意）

- 3D極座標の Realized Gain レポート（`hfss.post.reports_by_category.far_field(...)`, 球面名 `"3D"`）を
  追加作成してみてください。
- PyVistaでの3D可視化やCSV入出力を試したい場合は、`3.expert/hfss/ex1_dipole_s11_postprocessing/`
  （このシリーズのexpert）に進んでみてください。
