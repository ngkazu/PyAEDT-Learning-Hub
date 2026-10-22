# 演習3: マイクロストリップ線路（S/フィールドのポスト処理）

**目安時間: 90分**

題材: `AEDT-AI-Assistant/examples/hfss/field_overlay.py` を着想元に、このプロジェクト向けに構成を単純化して
独自に作成。

> セットアップ作成の基本操作がまだ不安な場合は、先に
> [0.easy/common_3d/ex03_setup_basics/](../../../0.easy/common_3d/ex03_setup_basics/) を確認するとよい。

> この演習は「マイクロストリップ線路シリーズ」の hard レベル。モデル作成〜解析実行だけのものが
> `1.normal/hfss/ex03_microstrip_line/`、さらにPyVista/CSV入出力を追加したものが
> `3.expert/hfss/ex03_microstrip_line_postprocessing/` にある。

## 学習目標

- normalと同じマイクロストリップモデルに対して、S11・S21のレポートを作成する
- `post.create_fieldplot_surface()` で、指定した面（GND・信号線）上の電界分布をフィールドプロットする
- フィールドプロットの凡例を対数スケールに切り替え、AEDTのネイティブ機能で画像エクスポートする

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析を完成させてください。

1. `Hfss(solution_type="Terminal", version=AEDT_VERSION, new_desktop=True, non_graphical=False)` で起動する。
2. `1.normal/hfss/ex03_microstrip_line/` と同じ手順で、次を順に行う
   （`SUB_W=6.0mm`, `SUB_H=1.0mm`, `LINE_W=1.5mm`, `LINE_L=10.0mm`, `AIR_H=3.0mm`）。
   - 基板（3Dソリッド）を `origin=[0, -SUB_W/2, 0]`, `sizes=[LINE_L, SUB_W, SUB_H]`,
     `material="alumina_96pct"` で作成する。
   - GND・信号線を `modeler.create_rectangle()` で2Dシートとして作成し、それぞれに
     `hfss.assign_finite_conductivity(material="copper")` を割り当てる。
   - 基板上面からエアボックス（`sizes=[LINE_L, SUB_W, AIR_H]`, `material="vacuum"`）を作成する。
   - エアボックスの両端面に `hfss.wave_port(modes=1, renormalize=True, impedance=50)` でWave Portを作成する。
   - エアボックスの下面・両端面を除く面に `hfss.assign_radiation_boundary_to_faces()` で輻射境界を割り当てる。
   - `hfss.validate_full_design()` でモデルを検証する。
   - セットアップ `"Setup1"`（`Frequency="10GHz"`, `MaxDeltaS=0.02`, `MaximumPasses=6`）を作成し、
     `hfss.create_linear_count_sweep(unit="GHz", start_frequency=0.1, stop_frequency=10,
     num_of_freq_points=201, sweep_type="Interpolating")` で周波数スイープを追加する。
   - `setup.analyze()` で解析を実行する。
3. `hfss.create_scattering(plot="S Parameters")` でS11・S21のレポートを作成する。
4. `hfss.post.create_fieldplot_surface(assignment=[gnd.name, line.name], quantity="Mag_E",
   setup="Setup1 : LastAdaptive", plot_name="MagE_Surface")` で、GND・信号線の表面に電界強度の
   フィールドプロットを作成する。
5. `field_plot.folder_settings.scale_settings.log = True` にしてから
   `field_plot.folder_settings.update()` を呼び、凡例を対数スケールに切り替える。
6. `hfss.modeler.fit_all()` でビューをモデル全体に合わせてから、
   `field_plot.export_image(full_path=..., width=1920, height=1080, orientation="isometric")` で
   画像としてエクスポートする。
7. プロジェクトを保存し、`release_desktop()` で終了する。

## ヒント

- `create_fieldplot_surface()` の `setup` には `"Setup1 : LastAdaptive"` を指定する。Interpolatingスイープは
  既定で `SaveFields=True` になっていても、各周波数点でフィールドを保存するわけではないため、
  スイープ名を指定するとデータが見つからずプロットが作成されない。
- `field_plot.folder_settings` は、プロジェクトを保存した後の `.aedt` ファイルからプロット設定を
  読み込む。作成直後・未保存の状態では `None` が返ることがあるため、フィールドプロット作成後に
  一度 `hfss.save_project()` を呼んでから `folder_settings` にアクセスする。
- `export_image()` の前に `hfss.modeler.fit_all()` を呼ばないと、カメラが対象物から外れて
  真っ黒な画像がエクスポートされることがある。
- マイクロストリップ線路の電界は、導体端付近で非常に強く、それ以外の領域では弱いため、
  線形スケールの凡例では分布が潰れて見える。対数スケールにすると分布全体が見やすくなる。

## 評価基準

- [ ] AEDTが起動し、normalと同じモデルが作成され、解析が完走している
- [ ] S11・S21のレポートが作成されている
- [ ] GND・信号線表面の電界（Mag_E）フィールドプロットが作成されている
- [ ] フィールドプロットの凡例が対数スケールになっている
- [ ] フィールドプロットが画像ファイルとしてエクスポートされている

## 発展課題（任意）

- `quantity` を `"Mag_H"`（磁界強度）に変えて、電界分布との違いを確認してみてください。
- PyVistaでの可視化やCSV入出力を試したい場合は、`3.expert/hfss/ex03_microstrip_line_postprocessing/`
  （このシリーズのexpert）に進んでみてください。
