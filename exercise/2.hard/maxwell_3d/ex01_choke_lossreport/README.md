# 演習1: コモンモードチョーク（巻線損失・コア損失レポート、Bフィールドプロット）

**目安時間: 90分**

題材: [1.normal/maxwell_3d/ex01_choke/](../../../1.normal/maxwell_3d/ex01_choke/) と同じモデル・Setup・解析に、
AEDT内部のポスト処理（損失レポート・フィールドプロット）を追加する。

> この演習は「チョークシリーズ」の hard レベル。normalの内容は
> [1.normal/maxwell_3d/ex01_choke/](../../../1.normal/maxwell_3d/ex01_choke/) を参照。
> さらにPython側での損失集計とPyVista/CSV入出力を追加したものが
> [3.expert/maxwell_3d/ex01_choke_postprocessing/](../../../3.expert/maxwell_3d/ex01_choke_postprocessing/) にある。

## 学習目標

- `post.create_report()` で、損失（`SolidLoss`：巻線のオーミック損失、`CoreLoss`：コアの磁心損失）を
  「Data Table」形式のレポートとして作成する
- `post.create_fieldplot_surface()` で、コア表面のB磁束密度（`Mag_B`）のフィールドプロットを作成する
- EddyCurrentソルバーの解析結果（単一周波数の定常値）に対するポスト処理の基本パターンを学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たす解析・ポスト処理を完成させてください
（モデル作成〜解析実行までは [1.normal/maxwell_3d/ex01_choke/](../../../1.normal/maxwell_3d/ex01_choke/)
と同じ内容です）。

1. [1.normal/maxwell_3d/ex01_choke/](../../../1.normal/maxwell_3d/ex01_choke/) と同じ手順で、次を順に行う
   （Regionがないと解析が失敗する点に注意）。
   - `choke_descriptor` 辞書（コア・巻線2本、単層、差動モード）を定義し、`modeler.check_choke_values()` で
     検証後、`modeler.create_choke(input_file=choke_fn)` でチョークを作成する。
   - `modeler.create_air_region(x_pos=100, y_pos=100, z_pos=100, x_neg=100, y_neg=100, z_neg=0)` で
     解析領域を作成する。
   - `modeler.get_object_faces()` で各巻線の両端面を取得し、`assign_current()` で振幅1000A・
     位相0deg/180degの電流励振を割り当てる。
   - セットアップ `"MySetup"` を作成し、`setup.props["Frequency"] = "150kHz"` を設定する。
   - `setup.analyze()` で解析を実行する。
2. `post.create_report(expressions=["SolidLoss"], report_category="Fields", plot_type="Data Table",
   plot_name="WindingLoss")` で、巻線のオーミック損失をデータテーブルレポートとして作成する。
3. `post.create_report(expressions=["CoreLoss"], report_category="Fields", plot_type="Data Table",
   plot_name="CoreLoss")` で、コアの磁心損失をデータテーブルレポートとして作成する。
4. `post.create_fieldplot_surface(assignment=core.name, quantity="Mag_B", setup=f"{setup.name} :
   LastAdaptive", intrinsics={"Freq": "150kHz", "Phase": "0deg"}, plot_name="CoreMagB")` で、
   コア表面のB磁束密度のフィールドプロットを作成する。
5. プロジェクトを保存し、`m3d.release_desktop()` でAEDTを終了する。

## ヒント

- `report_category="Fields"` は、周波数スイープを伴わない単一周波数の値（損失など）を
  「Data Table」形式で確認する際によく使う組み合わせ。
- `create_fieldplot_surface()` の `setup` 引数は `"SetupName : SetupSweep"` の形式で指定する。
  周波数スイープを追加していない場合は `"LastAdaptive"` を使う。
- `intrinsics` にはEddyCurrentソルバーで必要な周波数・位相（`Freq`/`Phase`）を指定する。
  Setupで設定した周波数（`150kHz`）と一致させる。

## 評価基準

- [ ] normalと同じモデル・Region・励振・Setup・解析がエラーなく完走している
- [ ] `WindingLoss`（SolidLoss）と`CoreLoss`のデータテーブルレポートが作成されている
- [ ] コア表面のMag_Bフィールドプロットが作成されている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- 巻線表面のMag_Bフィールドプロットも追加し、コアと巻線の磁束密度分布を比較してください。
- 損失・フィールドデータをPythonで取得・CSV出力・PyVista可視化したい場合は、
  このシリーズのexpert（`3.expert/maxwell_3d/ex01_choke_postprocessing/`、準備中）に進んでみてください。
