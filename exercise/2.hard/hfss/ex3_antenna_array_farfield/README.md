# 演習3: ダイポールアレイアンテナ（S/遠方界のポスト処理）

**目安時間: 90分**

題材: [PyAEDT Examples - Dipole antenna](https://examples.aedt.docs.pyansys.com/) を着想元に、
単一素子の解析（`2.hard/hfss/ex1_dipole_farfield/`）をアレイ構成に拡張して独自に作成。

> セットアップ作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex3_setup_basics/](../../../0.easy/common_3d/ex3_setup_basics/) を確認するとよい。

> この演習は「ダイポールアレイアンテナシリーズ」の hard レベル。モデル作成〜解析実行だけのものが
> `1.normal/hfss/ex3_antenna_array/`、さらにPyVista/CSV入出力（ビームステアリング）を追加したものが
> `3.expert/hfss/ex3_antenna_array_beamsteering/` にある。

## 学習目標

- normalと同じアレイモデルに対して、目的別に周波数掃引を使い分ける
  （Sパラメータ用のInterpolating掃引、遠方界用のフィールド保存Discrete掃引）
- 複数ポート間の自己反射・相互結合（マチュアルカップリング）をSパラメータレポートで確認する
- アレイ全体の合成放射パターンをElevation面でレポート作成する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Hfss(solution_type="Modal", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. 設計変数 `l_dipole = "10.2cm"`, `element_spacing = "15cm"` と、中心周波数 `center_freq = "1.5GHz"` を定義する。
3. `1.normal/hfss/ex3_antenna_array/solution.py` と同じ手順で、`NUM_ELEMENTS`（既定4）個の
   `Dipole_Antenna_DM` を、素子ごとのローカル座標系に配置する。
4. `create_open_region(frequency=center_freq)` で解析領域を作成する。
5. セットアップ `"MySetup"` を作成する（`MultipleAdaptiveFreqsSetup=["1GHz", "2GHz"]`, `MaximumPasses=2`）。
6. 周波数掃引を2つ追加する。
   - `"DiscreteSweep"`（`sweep_type="Discrete"`, `RangeStep="0.5GHz"`, `SaveFields=True`）: 遠方界レポート用。
   - `"InterpolatingSweep"`（`sweep_type="Interpolating"`, `SaveFields=False`）: Sパラメータ用。
7. `setup.analyze()` で解析を実行する。
8. `hfss.excitation_names` の全組み合わせ（`itertools.product(excitations, repeat=2)`）を
   `ports`/`ports_excited` として `hfss.create_scattering()` に渡し、自己反射（S11, S22, ...）と
   相互結合（S21, S31, ...）を含むSパラメータレポートを作成する。
9. 中心周波数における Elevation 面のアレイ全体のゲインパターン（`db(GainTheta)`）をレポート作成する
   （手順は `2.hard/hfss/ex1_dipole_farfield/` と同様）。
10. プロジェクトを保存し、`hfss.release_desktop()` でAEDTを終了する。

## ヒント

- `create_scattering()` に `ports`/`ports_excited` を渡さないと、既定では対角成分（各ポートの自己反射）
  しか作られない。素子間の結合まで見たい場合は、すべてのポートの組み合わせを明示的に渡す必要がある。
- `itertools.product(excitations, repeat=2)` は、`excitations` の全要素同士の組み合わせ（重複あり）を
  タプルのイテレータとして返す。`ports=[p for p, _ in pairs]`, `ports_excited=[q for _, q in pairs]` の
  ように分解して渡す。
- アレイの各素子は既定で等振幅・同位相（0deg）で励振されるため、遠方界レポートはそのまま
  「ブロードサイド（正面）方向にビームが向いたアレイパターン」になる。位相を変えたビームステアリングは
  expertで扱う。

## 評価基準

- [ ] AEDTが起動し、4素子のアレイモデルが作成されている
- [ ] Discrete/Interpolating の2つの周波数掃引が作成されている
- [ ] 解析がエラーなく完走している
- [ ] 自己反射・相互結合を含むSパラメータレポートが作成されている
- [ ] Elevation面のアレイ全体ゲインパターン（Radiation Pattern）レポートが作成されている

## 発展課題（任意）

- `element_spacing` を変えて、相互結合（S21等）や放射パターンのサイドローブがどう変化するか確認してください。
- 各素子の励振位相を変えてビームステアリングを試したい場合は、
  `3.expert/hfss/ex3_antenna_array_beamsteering/`（このシリーズのexpert）に進んでみてください。
