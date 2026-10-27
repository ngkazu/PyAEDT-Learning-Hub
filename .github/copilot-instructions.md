# PyAEDT-Learning-Hub — Copilot Instructions

## プロジェクトの目的

PyAEDT（`ansys.aedt.core` / `pyedb`）を使った**課題集**を作成するプロジェクト。
`docs/` に方針・テンプレート、`exercise/` に難易度別の課題本体、`memo/` に課題作成者向けの内部メモを置く。

計画・検討経緯の詳細は `memo/plan-pyaedtLearningHub.md` を参照（このファイルは課題実施者には見せない）。

## 言語（必須）

`docs/`, `exercise/`, `memo/` 配下のドキュメント類（README.md、starter/solution 内のコメント等）は
**すべて日本語で作成する（必須）**。ただし、コード自体・API名・引数名・識別子・ファイルパスは
原文（英語）のまま維持する。

## フォルダ構造

```
exercise/{0.easy|1.normal|2.hard|3.expert}/<app_slug>/exNN_<slug>/
  README.md      課題文・学習目標・要件・ヒント・評価基準・発展課題
  starter.py     TODO穴埋め用のひな形
  solution.py    模範解答（starter.py と同一フォルダに配置）
```

- easy はアプリ非依存でよく、モデリングのパラダイム別に以下3フォルダへ共通化する:
  - `exercise/0.easy/common_3d/`（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）
  - `exercise/0.easy/common_2d/`（Maxwell 2D, 2D Extractor）
  - `exercise/0.easy/common_circuit/`（Circuit, EMIT, Twin Builder）
- `hfss_3d_layout` と `edb` は easy 対象外（normal から開始）。
- 対象アプリフォルダ（13個）: `hfss`, `hfss_3d_layout`, `maxwell_3d`, `maxwell_2d`, `icepak`, `q3d`,
  `2d_extractor`, `circuit`, `emit`, `twin_builder`, `edb`, `misc`, `mechanical`

## 製品名の表記統一

ドキュメント内で製品名を書く際は以下に統一する（フォルダ名/slugは小文字のまま変更しない）。

| slug | 表示名 |
|---|---|
| `hfss` | HFSS |
| `maxwell_3d` | Maxwell 3D |
| `maxwell_2d` | Maxwell 2D |
| `icepak` | Icepak |
| `q3d` | Q3D Extractor |
| `2d_extractor` | 2D Extractor |
| `hfss_3d_layout` | HFSS 3D Layout |
| `circuit` | Circuit |
| `emit` | EMIT |
| `rmxprt` | RMxprt |
| `mechanical` | IcepakFEA（PyAEDTクラス名は `Mechanical`。表示名と異なる点に注意） |
| `twin_builder` | Twin Builder（PyAEDTクラス名は `TwinBuilder`、1語） |

## 難易度基準（概要。詳細は `docs/difficulty-criteria.md`）

対象読者は「Pythonの基本文法は習得済みで、ドキュメントを参照しながらコードを書ける人」を全難易度共通の前提とする。
難易度は **Pythonの難しさではなく、AEDT/PyAEDTドメインの複雑さ** で決める（時間目安は多少の逸脱を許容）。

- **easy（目安30分）**: AEDTの基本操作（起動→何かする→保存→終了）。アプリ非依存でよい。
- **normal（目安60分）**: アプリ別。モデル作成→Setup作成→解析実行まで（ポスト処理は行わない）。
- **hard（目安90分）**: normalと同じモデルにAEDT内部のポスト処理（Report/Field Plot）を追加する。
  複数アプリの連成はここでのみ任意採用可。
- **expert（目安90分以上）**: hardの内容にPyVista可視化・CSV入出力を追加する。matplotlib等を使った
  Python側のカスタムデータ処理を重視する。

normal/hard/expert は「シリーズ」構成（同じ `exNN_<slug>` が同一モデルを段階的に拡張する）を基本とする。
詳細は `docs/difficulty-criteria.md` の「難易度のシリーズ設計」節と `docs/exercise-template.md` の
「シリーズ番号（exNN）の付け方」を参照。

## 題材の作り方

- 公式サンプル（https://examples.aedt.docs.pyansys.com/）は**着想元として参照するのみ**。
  コードの丸写しはせず、学習目的で独自に作り直す（著作権・学習効果の両観点）。
- 引数名・戻り値・内部実装が不明なAPIは推測しない。以下を確認する:
  - `D:\+Projects\repos\pyaedt\src\ansys\aedt\core\` / `D:\+Projects\repos\pyedb\src\pyedb\` を grep/参照
  - `inspect.signature()` 等での実行時検証
- `docs/app-selection.md` にアプリ選択（`from ansys.aedt.core import ...` のクラス名対応表）をまとめ、
  easy課題の README/starter.py からはこれを参照する（重複記載しない）。

## `memo/` フォルダについて

課題作成者向けの内部メモ専用。課題実施者（学習者）には見せない。
`docs/` や `exercise/` などの学習者向け成果物には `memo/` の内容を転記・参照させない。

## `lecture/` フォルダについて

課題（`exercise/`）の前に行う45分の講義資料を置く学習者向けフォルダ。
`docs/`（方針・テンプレート）や `exercise/`（手を動かす課題）とは別の成果物として扱う。
流れは「講義 → 課題（easyから）」。講義内容とeasy課題の内容が一部重複してもよい（復習として有益）。
構成: `lecture/README.md`（構成・時間配分）、`lecture/01_pyaedt_lecture.md`（発表者用台本風の講義ノート）、
`lecture/demo/`（実行可能なデモ.pyスクリプト）。

## `skills/` フォルダについて（AIエージェント向け作業手順）

`skills/pyaedt-learning-hub-exercise-authoring/SKILL.md` に、このプロジェクトで課題
（`exercise/` の README.md/starter.py/solution.py 3点セット）を新規作成・修正する際の
実行手順・コードパターン・既知の落とし穴（PyEDB/HFSS 3D Layoutのポート選定ミス、API名の誤り、
差動Sパラメータの`context`必須、AEDTライブ検証からの教材化ワークフロー等）をまとめている。

**AIエージェント（Copilot/Autopilot等）は、`exercise/` 配下の課題を新規作成・修正する作業を
行う前に、必ず `skills/pyaedt-learning-hub-exercise-authoring/SKILL.md` を読み込むこと。**
このファイルとSKILL.mdの内容が矛盾する場合は、このファイル（`.github/copilot-instructions.md`）
と `docs/` 配下の方針ドキュメントを正とする。

## 進め方（フェーズ）

1. **Phase A**: `docs/` の6ドキュメント + ルート `README.md` を整備（コード実装なし）。
2. **Phase B**: HFSS（+ `common_3d`）でテンプレートを検証するパイロット実装。
3. **Phase C**: `docs/roadmap/coverage.md` を進捗管理台帳として、Tier順に残りアプリへ段階的にロールアウト。

詳細・最新の決定事項は必ず `memo/plan-pyaedtLearningHub.md` の「背景・決定事項」を正とする。
