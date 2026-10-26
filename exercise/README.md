# 課題一覧

このプロジェクトの課題本体。難易度別に `0.easy/` → `1.normal/` → `2.hard/` → `3.expert/` の順に取り組む。
各フォルダの構成・進め方は [ルートREADME](../README.md) と [docs/exercise-template.md](../docs/exercise-template.md)
を参照。

## 前提

- [lecture/](../lecture/) の講義資料に目を通していること（推奨。必須ではない）
- [lecture/00_environment_setup.md](../lecture/00_environment_setup.md) の環境構築が完了していること
- [docs/app-selection.md](../docs/app-selection.md) で使いたいアプリケーションのクラス名を確認しておくこと

## 難易度別の学び方

| 難易度 | 目安時間 | 何を学ぶか |
|---|---|---|
| [0.easy/](0.easy/) | 30分 | AEDTの基本操作（起動→何かする→保存→終了）。`common_3d`/`common_2d`/`common_circuit` からアプリを選んで進める |
| [1.normal/](1.normal/) | 60分 | アプリ別の自動化基本（モデル作成→Setup作成→解析実行まで。ポスト処理は行わない） |
| [2.hard/](2.hard/) | 90分 | normalと同じモデルにAEDT内部ポスト処理（Report/Field Plot）を追加。複数アプリの連成解析は任意でここのみ扱う |
| [3.expert/](3.expert/) | 90分以上 | hardの内容にPyVista可視化・CSV入出力を追加。matplotlib等を使ったPythonデータ処理も重視 |

難易度の詳しい判断基準は [docs/difficulty-criteria.md](../docs/difficulty-criteria.md) を参照。

## 現在の演習一覧（Phase B パイロット: HFSS）

`1.normal/` → `2.hard/` → `3.expert/` は「シリーズ」構成になっている。同じ `exNN_*` 番号のフォルダは、
normalで作ったモデルにhardでポスト処理を追加し、expertでさらにPyVista可視化・CSV入出力を追加した
ステップアップ形式（詳細は [docs/difficulty-criteria.md](../docs/difficulty-criteria.md) の
「難易度のシリーズ設計」を参照）。

| フォルダ | タイトル | 目安時間 |
|---|---|---|
| [0.easy/common_3d/ex01_basic_operations/](0.easy/common_3d/ex01_basic_operations/) | AEDTの基本操作（起動→変数→形状→保存→終了） | 30分 |
| [0.easy/common_3d/ex02_boolean_subtract/](0.easy/common_3d/ex02_boolean_subtract/) | ブーリアン演算（Subtract）で中空の箱を作る | 30分 |
| [0.easy/common_3d/ex03_setup_basics/](0.easy/common_3d/ex03_setup_basics/) | セットアップ（解析条件）を作ってみる | 30分 |
| [0.easy/common_3d/ex04_sheets/](0.easy/common_3d/ex04_sheets/) | シート形状（矩形・円）を作る | 30分 |
| [0.easy/common_3d/ex05_unite/](0.easy/common_3d/ex05_unite/) | ブーリアン演算（Unite）で2つの箱を結合する | 30分 |
| [0.easy/common_3d/ex06_move_rotate/](0.easy/common_3d/ex06_move_rotate/) | 形状の移動（Move）と回転（Rotate） | 30分 |
| [0.easy/common_3d/ex07_plane/](0.easy/common_3d/ex07_plane/) | Planeを作る | 30分 |
| [0.easy/common_3d/ex08_cad_import/](0.easy/common_3d/ex08_cad_import/) | CADのインポート（エクスポート→インポートの往復） | 30分 |
| [0.easy/common_3d/ex09_variables/](0.easy/common_3d/ex09_variables/) | プロジェクト変数とデザイン変数を作る・変更する | 30分 |
| [0.easy/common_3d/ex10_choke_geometry/](0.easy/common_3d/ex10_choke_geometry/) | チョークのジオメトリを作る（check_choke_values→create_choke） | 30分 |
| [0.easy/common_3d/ex11_get_faces/](0.easy/common_3d/ex11_get_faces/) | 面（Face）を取得する（get_object_faces→get_face_center/get_face_area） | 30分 |
| [0.easy/common_3d/ex12_export_import_config/](0.easy/common_3d/ex12_export_import_config/) | デザイン設定のJSON入出力（configurations.export_config→import_config） | 30分 |
| [0.easy/common_3d/ex13_custom_material/](0.easy/common_3d/ex13_custom_material/) | カスタム材料を作る（add_material→conductivity/permeability設定） | 30分 |
| [0.easy/common_3d/ex14_section_terminal/](0.easy/common_3d/ex14_section_terminal/) | 断面を切ってターミナル面を作る（section→separate_bodies→delete） | 30分 |
| [0.easy/common_3d/ex15_polyline_duplicate/](0.easy/common_3d/ex15_polyline_duplicate/) | ポリラインの回転複製で環状形状を作る（create_polyline→duplicate_around_axis→unite） | 30分 |
| [0.easy/common_3d/ex16_local_coordinate_system/](0.easy/common_3d/ex16_local_coordinate_system/) | ローカル座標系を作る（create_coordinate_system→set_working_coordinate_system） | 30分 |
| [0.easy/common_3d/ex17_non_model/](0.easy/common_3d/ex17_non_model/) | 非モデル（non_model）形状を作る | 30分 |
| [0.easy/common_3d/ex18_duplicate_along_line/](0.easy/common_3d/ex18_duplicate_along_line/) | 直線方向への複製（duplicate_along_line）でフィン列を作る | 30分 |
| [0.easy/common_3d/ex19_create_region/](0.easy/common_3d/ex19_create_region/) | 解析領域（Region）を作る（create_region） | 30分 |
| [1.normal/hfss/ex01_dipole_antenna/](1.normal/hfss/ex01_dipole_antenna/) | 半波長ダイポールアンテナ（モデル作成〜解析実行） | 60分 |
| [1.normal/hfss/ex02_iris_filter/](1.normal/hfss/ex02_iris_filter/) | 導波管インダクティブアイリスフィルタ（モデル作成〜解析実行） | 60分 |
| [2.hard/hfss/ex01_dipole_farfield/](2.hard/hfss/ex01_dipole_farfield/) | 半波長ダイポールアンテナ（S11・遠方界のポスト処理） | 90分 |
| [2.hard/hfss/ex02_iris_filter/](2.hard/hfss/ex02_iris_filter/) | 導波管インダクティブアイリスフィルタ（高度なポスト処理） | 90分 |
| [3.expert/hfss/ex01_dipole_s11_postprocessing/](3.expert/hfss/ex01_dipole_s11_postprocessing/) | ダイポールアンテナ S11・遠方界データのPython後処理（VSWR・帯域幅算出・CSV入出力） | 90分以上 |
| [3.expert/hfss/ex02_iris_filter_postprocessing/](3.expert/hfss/ex02_iris_filter_postprocessing/) | 導波管インダクティブアイリスフィルタ S/フィールドデータのPython後処理（CSV入出力・PyVista可視化） | 90分以上 |
| [1.normal/hfss/ex03_microstrip_line/](1.normal/hfss/ex03_microstrip_line/) | マイクロストリップ線路（モデル作成〜解析実行） | 60分 |
| [1.normal/hfss/ex04_patch_antenna/](1.normal/hfss/ex04_patch_antenna/) | プローブ給電パッチアンテナ（モデル作成〜解析実行） | 60分 |
| [2.hard/hfss/ex03_microstrip_line_fieldplot/](2.hard/hfss/ex03_microstrip_line_fieldplot/) | マイクロストリップ線路（S/フィールドのポスト処理） | 90分 |
| [2.hard/hfss/ex04_patch_antenna_farfield/](2.hard/hfss/ex04_patch_antenna_farfield/) | プローブ給電パッチアンテナ（S11・遠方界のポスト処理） | 90分 |
| [3.expert/hfss/ex03_microstrip_line_postprocessing/](3.expert/hfss/ex03_microstrip_line_postprocessing/) | マイクロストリップ線路S/フィールドデータのPython後処理（CSV入出力・PyVista可視化） | 90分以上 |
| [3.expert/hfss/ex04_patch_antenna_design/](3.expert/hfss/ex04_patch_antenna_design/) | プローブ給電パッチアンテナの設計計算とPython後処理（CSV入出力・PyVista可視化） | 90分以上 |

他のアプリケーション（Maxwell 3D, Icepak, Q3D Extractor など）や、HFSSの追加シリーズ（パッチアンテナ、
チョークコイル、フレキシブルケーブルなど）の課題は、
[docs/roadmap/coverage.md](../docs/roadmap/coverage.md) の進捗表に沿って順次追加されます。

## 現在の演習一覧（Phase C: Maxwell 3D）

| フォルダ | タイトル | 目安時間 |
|---|---|---|
| [1.normal/maxwell_3d/ex01_choke/](1.normal/maxwell_3d/ex01_choke/) | コモンモードチョーク（モデル作成〜解析実行） | 60分 |
| [2.hard/maxwell_3d/ex01_choke_lossreport/](2.hard/maxwell_3d/ex01_choke_lossreport/) | コモンモードチョーク（巻線損失・コア損失レポート、Bフィールドプロット） | 90分 |
| [3.expert/maxwell_3d/ex01_choke_postprocessing/](3.expert/maxwell_3d/ex01_choke_postprocessing/) | コモンモードチョーク 損失・BフィールドデータのPython後処理（CSV入出力・PyVista可視化） | 90分以上 |
| [1.normal/maxwell_3d/ex02_asymmetric_conductor/](1.normal/maxwell_3d/ex02_asymmetric_conductor/) | TEAM7非対称導体（モデル作成〜解析実行） | 60分 |
| [1.normal/maxwell_3d/ex03_coil_core/](1.normal/maxwell_3d/ex03_coil_core/) | コイル・コア電磁石（モデル作成〜解析実行） | 60分 |
| [2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/](2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/) | TEAM7非対称導体（$B_z$ラインレポート） | 90分 |
| [2.hard/maxwell_3d/ex03_coil_core_fieldplot/](2.hard/maxwell_3d/ex03_coil_core_fieldplot/) | コイル・コア電磁石（インダクタンスレポート、Bフィールドプロット） | 90分 |
| [3.expert/maxwell_3d/ex02_asymmetric_conductor_benchmark/](3.expert/maxwell_3d/ex02_asymmetric_conductor_benchmark/) | TEAM7非対称導体 実測データとの比較（CSV入出力・PyVista可視化） | 90分以上 |
| [3.expert/maxwell_3d/ex03_coil_core_postprocessing/](3.expert/maxwell_3d/ex03_coil_core_postprocessing/) | コイル・コア電磁石 インダクタンスデータのPython後処理（CSV入出力・PyVista可視化） | 90分以上 |
## 現在の演習一覧（Phase C: Q3D Extractor）

| フォルダ | タイトル | 目安時間 |
|---|---|---|
| [1.normal/q3d/ex01_busbar/](1.normal/q3d/ex01_busbar/) | ブスバー解析（モデル作成〜解析実行） | 60分 |
| [2.hard/q3d/ex01_busbar_matrixreport/](2.hard/q3d/ex01_busbar_matrixreport/) | ブスバー解析（縮退行列・キャパシタンス/インダクタンスレポート） | 90分 |
| [3.expert/q3d/ex01_busbar_postprocessing/](3.expert/q3d/ex01_busbar_postprocessing/) | ブスバー解析 容量・インダクタンスデータのPython後処理（CSV入出力・PyVista可視化） | 90分以上 |

## 現在の演習一覧（Phase C: Icepak）

| フォルダ | タイトル | 目安時間 |
|---|---|---|
| [1.normal/icepak/ex01_heatsink/](1.normal/icepak/ex01_heatsink/) | ヒートシンク熱解析（モデル作成〜解析実行） | 60分 |
| [1.normal/icepak/ex02_small_cabinet_fan/](1.normal/icepak/ex02_small_cabinet_fan/) | 小型筐体のファン冷却解析（モデル作成〜解析実行） | 60分 |
| [1.normal/icepak/ex03_smd_pcb_thermal/](1.normal/icepak/ex03_smd_pcb_thermal/) | PCB表面実装部品の熱解析（モデル作成〜解析実行） | 60分 |
| [2.hard/icepak/ex01_heatsink_fieldplot/](2.hard/icepak/ex01_heatsink_fieldplot/) | ヒートシンク熱解析（温度フィールドプロット・モニタ） | 90分 |
| [2.hard/icepak/ex02_small_cabinet_fan_fieldplot/](2.hard/icepak/ex02_small_cabinet_fan_fieldplot/) | 小型筐体のファン冷却解析（温度フィールドプロット・モニタ） | 90分 |
| [2.hard/icepak/ex03_smd_pcb_thermal_fieldplot/](2.hard/icepak/ex03_smd_pcb_thermal_fieldplot/) | PCB表面実装部品の熱解析（温度フィールドプロット・モニタ） | 90分 |
| [3.expert/icepak/ex01_heatsink_postprocessing/](3.expert/icepak/ex01_heatsink_postprocessing/) | ヒートシンク熱解析 温度データのPython後処理（CSV入出力・PyVista可視化） | 90分以上 |
| [3.expert/icepak/ex02_small_cabinet_fan_postprocessing/](3.expert/icepak/ex02_small_cabinet_fan_postprocessing/) | 小型筐体のファン冷却解析 温度データのPython後処理（CSV入出力・PyVista可視化） | 90分以上 |
| [3.expert/icepak/ex03_smd_pcb_thermal_postprocessing/](3.expert/icepak/ex03_smd_pcb_thermal_postprocessing/) | PCB表面実装部品の熱解析 温度データのPython後処理（CSV入出力・PyVista可視化） | 90分以上 |

## 進め方

1. 各課題フォルダの `README.md` を読み、課題内容・学習目標・評価基準を確認する。
2. `starter.py` をコピーして自分の作業ファイルとし、`# TODO` を埋めていく。
3. AEDTを起動して実行し、GUIで形状・境界条件・結果を確認する。
4. 詰まったら `README.md` の「ヒント」を見る。それでも分からなければ `solution.py` と該当箇所だけ見比べる。
5. 実行できたら、各演習の「発展課題」にも挑戦する（時間があれば）。

## 共通の評価基準

各課題固有の評価基準に加えて、[docs/review-checklist.md](../docs/review-checklist.md) の項目も満たすことを
目指す（実行可否、`release_desktop()` の呼び出し、日本語ドキュメントの徹底など）。
