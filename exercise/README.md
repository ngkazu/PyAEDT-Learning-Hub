# 課題一覧

このプロジェクトの課題本体。難易度別に `0.easy/` → `1.normal/` → `2.hard/` → `3.expert/` の順に取り組む。
各フォルダの構成・進め方は [ルートREADME](../README.md) と [docs/exercise-template.md](../docs/exercise-template.md)
を参照。

## 前提

- [lecture/](../lecture/) の講義資料に目を通していること（推奨。必須ではない）
- [docs/setup.md](../docs/setup.md) の環境構築が完了していること
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
| [0.easy/common_3d/ex1_basic_operations/](0.easy/common_3d/ex1_basic_operations/) | AEDTの基本操作（起動→変数→形状→保存→終了） | 30分 |
| [0.easy/common_3d/ex2_boolean_subtract/](0.easy/common_3d/ex2_boolean_subtract/) | ブーリアン演算（Subtract）で中空の箱を作る | 30分 |
| [0.easy/common_3d/ex3_setup_basics/](0.easy/common_3d/ex3_setup_basics/) | セットアップ（解析条件）を作ってみる | 30分 |
| [1.normal/hfss/ex1_dipole_antenna/](1.normal/hfss/ex1_dipole_antenna/) | 半波長ダイポールアンテナ（モデル作成〜解析実行） | 60分 |
| [1.normal/hfss/ex2_iris_filter/](1.normal/hfss/ex2_iris_filter/) | 導波管インダクティブアイリスフィルタ（モデル作成〜解析実行） | 60分 |
| [2.hard/hfss/ex1_dipole_farfield/](2.hard/hfss/ex1_dipole_farfield/) | 半波長ダイポールアンテナ（S11・遠方界のポスト処理） | 90分 |
| [2.hard/hfss/ex2_iris_filter/](2.hard/hfss/ex2_iris_filter/) | 導波管インダクティブアイリスフィルタ（高度なポスト処理） | 90分 |
| [3.expert/hfss/ex1_dipole_s11_postprocessing/](3.expert/hfss/ex1_dipole_s11_postprocessing/) | ダイポールアンテナ S11・遠方界データのPython後処理（VSWR・帯域幅算出・CSV入出力） | 90分以上 |
| [3.expert/hfss/ex2_iris_filter_postprocessing/](3.expert/hfss/ex2_iris_filter_postprocessing/) | 導波管インダクティブアイリスフィルタ S/フィールドデータのPython後処理（CSV入出力・PyVista可視化） | 90分以上 |
| [1.normal/hfss/ex3_antenna_array/](1.normal/hfss/ex3_antenna_array/) | ダイポールアレイアンテナ（モデル作成〜解析実行） | 60分 |
| [2.hard/hfss/ex3_antenna_array_farfield/](2.hard/hfss/ex3_antenna_array_farfield/) | ダイポールアレイアンテナ（S/遠方界のポスト処理） | 90分 |
| [3.expert/hfss/ex3_antenna_array_beamsteering/](3.expert/hfss/ex3_antenna_array_beamsteering/) | ダイポールアレイアンテナ ビームステアリングのPython後処理（CSV入出力・PyVista可視化） | 90分以上 |

他のアプリケーション（Maxwell 3D, Icepak, Q3D Extractor など）や、HFSSの追加シリーズ（パッチアンテナ、
チョークコイル、フレキシブルケーブルなど）の課題は、
[docs/roadmap/coverage.md](../docs/roadmap/coverage.md) の進捗表に沿って順次追加されます。

## 進め方

1. 各課題フォルダの `README.md` を読み、課題内容・学習目標・評価基準を確認する。
2. `starter.py` をコピーして自分の作業ファイルとし、`# TODO` を埋めていく。
3. AEDTを起動して実行し、GUIで形状・境界条件・結果を確認する。
4. 詰まったら `README.md` の「ヒント」を見る。それでも分からなければ `solution.py` と該当箇所だけ見比べる。
5. 実行できたら、各演習の「発展課題」にも挑戦する（時間があれば）。

## 共通の評価基準

各課題固有の評価基準に加えて、[docs/review-checklist.md](../docs/review-checklist.md) の項目も満たすことを
目指す（実行可否、`release_desktop()` の呼び出し、日本語ドキュメントの徹底など）。
