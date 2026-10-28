# Plan: PyAEDT-Learning-Hub 課題プロジェクトの構築

## 背景・決定事項（ヒアリング済み）
- 対象アプリ: 公式サイト（https://examples.aedt.docs.pyansys.com/）の11カテゴリ。ただし Q3D Extractor と 2D Extractor
  はフォルダとして別々（`q3d` / `2d_extractor`）に分割し、さらに **Mechanical**（構造/熱FEA。通称
  「IcepakFEA」とも呼ばれる。IcepakのCFDソルバーとは別の有限要素法ソルバー）を追加するため、
  実際のアプリフォルダは13個となる:
  hfss, hfss_3d_layout, maxwell_3d, maxwell_2d, icepak, q3d, 2d_extractor, circuit, emit, twin_builder, edb, misc, mechanical
- フォルダ構造: 難易度が先。`exercise/{0.easy|1.normal|2.hard|3.expert}/<app_slug>/exNN_<slug>/`
  easyはアプリ非依存でよく、モデリングのパラダイムごとに以下3つのグループで共通化する:
  - `exercise/0.easy/common_3d/`: 3Dモデラー系（hfss, maxwell_3d, icepak, q3d, mechanical）
  - `exercise/0.easy/common_2d/`: 2Dモデラー系（maxwell_2d, 2D Extractor）
  - `exercise/0.easy/common_schematic/`: 回路・スキーマ系（circuit, emit, twin_builder）
  **hfss_3d_layout と edb は easy の対象から除外し、normalから開始する**（レイヤー/ECAD操作は3D/2D/回路の
  いずれにもなじまず、common化するメリットが小さいため）。
  既存の空フォルダ `exercise/HFSS/`, `exercise/HFSS_3DLayout/` は削除する（難易度先方式に統一のため不要）。
- `memo/` フォルダ: 課題作成者向けの内部メモ専用フォルダ。課題作成時の確認事項・決定事項・検討過程を保存する場であり、
  **課題実施者（学習者）には見せない**。`docs/`（学習者も読む方針・テンプレート文書）や `exercise/`（課題本体）とは
  明確に区別し、学習者向け成果物からは参照させない。
- `lecture/` フォルダ（新規）: 課題の前に行う45分の講義資料を置く学習者向けフォルダ。
  `docs/`（方針・テンプレート）や `exercise/`（手を動かす課題）とは別の性質の成果物（一回限りの発表内容）として分ける。
  流れは「講義→課題（easyから）」。講義内容とeasy課題の内容が一部重複しても良い（復習として有益、
  課題作成側は講義内容を考慮不要）。構成は以下:
  - `lecture/README.md` — 講義の目的・構成（45分の時間配分）・進め方
  - `lecture/11_pyaedt_lecture.md` — 発表者用台本風の講義ノート（Markdown、スライド形式ではない）。
    内容: (1) PyAEDTの位置づけと主なクラス/関数の紹介、(2) 基本操作（開く・箱を作る・保存・閉じる）、
    (3) AEDT内蔵Script（記録スクリプト）→PyAEDTへの変換方法。
  - `lecture/demo/` — 講義中に実行するデモ.pyスクリプト一式（基本操作デモ、変換前後のコード例）。
- 課題フォーマット: `README.md`（課題文・学習目標・要件・ヒント・評価基準・発展課題）+ `starter.py`（TODO穴埋め）+ `solution.py`（模範解答）。
  `d:\+Projects\+2026\...\2026.PyAnsysTraning_inJapan\WorkShop\HFSS\ex1_dipole\` を書式テンプレートとして踏襲する。
- 題材の作り方: 公式サンプルは着想元として参照するのみ。コードの丸写しはせず、学習目的で独自に作り直す（著作権・学習効果の両観点）。
- 言語: `docs/`, `exercise/`, `memo/` 配下のドキュメント類（README.md、starter/solution内のコメント等）は
  **必ず日本語で作成する（必須）**。ただしコード自体・ API名・引数名・識別子・ファイルパスは原文（英語）のまま維持する。
- 表記統一（ドキュメント内の製品名表示）: `hfss`→HFSS, `maxwell_3d`→Maxwell 3D, `maxwell_2d`→Maxwell 2D,
  `icepak`→Icepak, `q3d`→Q3D Extractor, `2d_extractor`→2D Extractor, `hfss_3d_layout`→HFSS 3D Layout,
  `circuit`→Circuit, `emit`→EMIT, `rmxprt`→RMxprt, `mechanical`→IcepakFEA, `twin_builder`→Twin Builder。
  フォルダ名（slug）は上記の小文字表記のまま変更しない。※ `mechanical`（表示名 IcepakFEA）の PyAEDT
  クラス名は `Mechanical` であり、表示名とクラス名が一致しない点に注意。
- docs/ に用意するドキュメント（6点）:
  1. `docs/difficulty-criteria.md` — 難易度基準
  2. `docs/exercise-template.md` — 課題テンプレート・執筆スタイルガイド
  3. `docs/roadmap/coverage.md` — アプリ×難易度のカバレッジ表（進捗トラッキング）
  4. `docs/setup.md` — 環境構築ガイド
  5. `docs/review-checklist.md` — レビュー・品質チェックリスト
  6. `docs/app-selection.md` — アプリケーション選択リファレンス（`ansys.aedt.core` のクラス名対応表）

## 規模感と方針
11アプリ × 4難易度 × 2〜3問 ≒ 88〜132問规模。1セッションで全問作成するのは非現実的なため、
**基盤整備 → パイロット実装 → 段階的ロールアウト**の3フェーズに分割し、`coverage.md` で進捗を追跡することで
複数セッションにまたがる作業を可能にする。

---

## Phase A: 基盤整備（最初に実行・全体の前提）

1. リポジトリ直下に `README.md` を新規作成。プロジェクトの目的（PyAEDT課題集）、`exercise/` の構造、
   `docs/` への導線、進め方（README→starter→solution の順で学習）を記載。
2. `docs/setup.md` を作成。Python 3.10+、`pip install "pyaedt[all]"`、AEDT 2024.2以降を対象とし、
   バージョン確認コマンド（`py -3 -c "import ansys.aedt.core; print(...)"`）を記載。
   フル商用ライセンス所有を前提とする旨を明記する（ライセンス制限の回避策等は記載しない）。
   AEDT-AI-Assistant の `knowledge/automation/pyaedt.md` にある接続・環境情報を参照して整合させる。
3. `docs/difficulty-criteria.md` を作成。冒頭に対象読者の前提（Pythonの基本文法習得済み、公式ドキュメント等を
   参照しながらコードを書ける人）を明記し、**難易度はPythonの難しさではなくAEDT/PyAEDTドメインの複雑さで
   決める**という方針を明文化する。その上で以下の基準を定義する（時間目安は多少の逸脱を許容する）:
   - easy（目安30分）: AEDTの基本操作を学ぶレベル。変数化、形状の作成・変更、物性の作成・変更などは
     代表的な例であり、これらに限定しない（AEDTの基本操作全般を対象としてよい）。
     「起動→何かする→保存→終了」という一連の流れを体験することが目的で、アプリケーション固有の
     知識は問わない。
     **モデリングパラダイムが近いアプリ同士で共通化し、`0.easy/common_3d`（hfss, maxwell_3d, icepak, q3d, mechanical）/
     `0.easy/common_2d`（maxwell_2d, 2D Extractor）/ `0.easy/common_schematic`（circuit, emit, twin_builder）
     の3つに分ける**（各アプリに2問以上揃える必要はない）。
     hfss_3d_layout と edb はレイヤー/ECAD操作でこの3区分になじまず、easyの対象から外しnormalから開始する。
   - normal（目安60分）: ここからアプリケーション別の課題を中心にする。連成解析（複数アプリにまたがる
     もの）は対象外。「モデル作成→Setup作成→解析実行」という自動化の基本を学ぶ。外部モジュール
     （例: CSVインポートから境界条件を割り当てる等）の利用も視野に入れる。ポスト処理はAEDT内で
     完結する簡単なものに留める。
   - hard（目安90分）: 高度なポスト処理を含める。複数アプリケーションにまたがる連成解析はこのレベルで
     扱ってもよいが必須ではない。
   - expert（目安90分以上）: 複数アプリケーションの利用よりも、matplotlib等を使ったデータ処理・後解析を
     含むことを重視する。
   各レベルの「含むもの/含まないもの」の判断基準も明記する。
4. `docs/exercise-template.md` を作成。`ex1_dipole` を範例として、README の必須セクション
   （タイトル/目安時間/題材/学習目標/課題（番号付き手順）/ヒント/評価基準/発展課題）、
   `starter.py` の TODO コメント規約、`solution.py` の命名・変数規約（`AEDT_VERSION` 変数など）を定義する。
5. `docs/review-checklist.md` を作成。共通評価基準（HFSS課題の「共通の評価基準」相当）をベースに、
   実行可否・境界条件の妥当性・レポート作成・`release_desktop()` によるクリーンアップ等の一般チェック項目を定義する。
6. `docs/roadmap/coverage.md` を作成。以下の一次ドラフトを反映した表を作る（アプリ×難易度×題材候補×ステータス）:

   | アプリ | easy | normal | hard | expert |
   |---|---|---|---|---|
   | common_3d（HFSS/Maxwell 3D/Icepak/Q3D Extractor/IcepakFEA共通） | 変数化/形状作成・変更/物性作成・変更（起動→保存→終了） | — | — | — |
   | common_2d（Maxwell 2D/2D Extractor共通） | 同上（2D断面形状） | — | — | — |
   | common_schematic（Circuit/EMIT/Twin Builder共通） | 回路要素の配置・接続（起動→保存→終了） | — | — | — |
   | HFSS（`hfss`） | （common_3dで代替可） | ダイポールアンテナ（Setup作成→解析→S11） | 導波管アイリスフィルタ＋高度後処理／MRI・電子レンジ電熱連成（任意の連成） | スパイラルインダクタ結果のPython後処理（matplotlib） |
   | Maxwell 3D（`maxwell_3d`） | （common_3dで代替可） | DC解析(質量中心)/チョーク setup+解析 | TEAM3浴槽板/TEAM7非対称導体＋高度後処理／Maxwell-Icepak連成（任意） | 磁石セグメンテーション結果のPython後処理 |
   | Icepak（`icepak`） | （common_3dで代替可） | グラフィックカード熱解析／CSVブロック定義（外部CSV→境界条件割当て） | 3DコンポーネントIDF/EDBインポート＋高度後処理／HFSS-Icepak連成（任意） | IDF/EDBインポート結果の温度データをPythonで可視化 |
   | Q3D Extractor（`q3d`） | （common_3dで代替可） | ブスバー解析 | ケーブルパラメータ抽出＋高度後処理／EDBからのPCB DCIR/AC連成（任意） | 抽出結果の周波数特性をPythonでプロット |
   | 2D Extractor（`2d_extractor`） | （common_2dで代替可） | CPWG・ストリップライン | 同上＋高度後処理 | 周波数特性をPythonでプロット |
   | HFSS 3D Layout（`hfss_3d_layout`） | （easy対象外） | パラメトリックPCB作成 | プリレイアウトSI(SMAコネクタ)＋高度後処理／パワーインテグリティ・DCIR連成（任意） | レイアウト解析結果のPythonカスタム可視化 |
   | Maxwell 2D（`maxwell_2d`） | （common_2dで代替可） | 抵抗計算/静電解析 setup+解析 | 2D軸対称アクチュエータ/PM同期モータ過渡＋高度後処理 | RMxprt→Maxwell2Dエクスポート結果等のPython後処理 |
   | Circuit（`circuit`） | （common_schematicで代替可） | 回路スキーマ作成+過渡解析 | サブサーキット管理/アイダイアグラム＋高度後処理 | PCIeバーチャルコンプライアンス/AMI結果のPythonカスタム解析 |
   | EMIT（`emit`） | （common_schematicで代替可） | アンテナ共存干渉基礎 | HFSS-EMIT連成（任意）＋高度後処理 | 干渉解析結果のPythonカスタムプロット |
   | Twin Builder（`twin_builder`） | （common_schematicで代替可） | RC回路解析/整流回路(コンデンサフィルタ) | Static ROM＋高度後処理 | Dynamic ROM/LTI ROM結果のPython比較プロット |
   | EDB（`edb`） | （easy対象外） | 設定ファイル(Configuration)基礎/IPC2581エクスポート | GDSインポートワークフロー＋高度後処理 | 設定ファイルワークフロー結果のPython集計・レポート |
   | misc（`misc`） | （easyはcommon分類になじまず、未定義） | Touchstoneファイル操作/Lumped Element Filter設計 | COM解析＋高度後処理 | Touchstone(skrf)/COM結果のPythonカスタム解析・プロット |
   | IcepakFEA（`mechanical`） | （common_3dで代替可） | Phase Bで検討 | Phase Bで検討 | Phase Bで検討 |

   各セルに「ステータス（未着手/下書き/レビュー中/完了）」列を追加し、最初は全て「未着手」とする。
   emit は公式サンプルが少ないため、各難易度1〜2問で可とする旨を注記する。
   icepak の Sherlock連携（別アプリ）は対象外とし、題材候補から除外する。
   hard/expertで挙げた「連成（任意）」系の題材は、hardでのみ許容し、expertでは扱わない
   （expertはPython後処理を重視するため）。連成課題を採用する場合は主導アプリ側のフォルダに1つだけ置き、
   関連アプリ側に重複配置しない。
   ※ IcepakFEA（PyAEDTクラス名は `Mechanical`）は公式サイトに単体カテゴリがなく、公開例の多くはHFSS-IcepakFEA連成
   （MRI解析等）。normal/hard/expertの具体的な題材はPhase Bでの検証結果を踏まえて決定する。
7. `docs/app-selection.md` を作成。`common_3d`/`common_2d`/`common_schematic` の easy 課題では学習者が使用するAEDTアプリケーションを
   自分で選べるようにするため、`ansys.aedt.core` のクラス名対応表（例: HFSS→`Hfss`, Icepak→`Icepak`,
   Maxwell 3D→`Maxwell3d`, Maxwell 2D→`Maxwell2d`, Q3D Extractor→`Q3d`, 2D Extractor→`Q2d`, HFSS 3D Layout→`Hfss3dLayout`,
   Circuit→`Circuit`, EMIT→`Emit`, Twin Builder→`TwinBuilder`, IcepakFEA→`Mechanical`（表示名とクラス名が異なる点に注意）、
   RMxprt→`Rmxprt`）と、`from ansys.aedt.core import Icepak` / `app = Icepak()` 形式の最小サンプルを載せる。
   EDBのみ `from pyedb import Edb` である点も注記する。

**Phase A の成果物は `docs/` 配下の6ファイル + ルート `README.md` のみ。コード実装は含まない。**

---

## Phase B: パイロット実装（HFSS、全難易度で型を検証）

*depends on Phase A*

1. `exercise/0.easy/common_3d/ex1_xxx/`（3Dモデラー系のアプリ非依存基本操作課題）、
   `exercise/1.normal/hfss/ex1_xxx/`, `exercise/2.hard/hfss/ex1_xxx/`,
   `exercise/3.expert/hfss/ex1_xxx/` を作成。coverage.md の該当セルを題材に、
   README/starter/solution の3点セットを作成する。
   - easy は `common_3d/` 配下で1アプリに限定せず、3Dモデラー系（Hfss/Maxwell3d/Icepak/Q3d）に共通する
     AEDT基本操作（変数化・形状作成/変更・物性作成/変更などは代表例で、これらに限定しない）とする。
     **使用するアプリケーションは学習者が自分で選べるようにし**、README または starter.py 冒頭に
     「アプリケーションの選び方」節を設けて `docs/app-selection.md` の対応表を参照させる
     （`from ansys.aedt.core import Icepak` → `app = Icepak()` のように、選んだクラスを1箇所の変数/importに
     差し込むだけで動く形にする）。common_2d・common_schematicはパイロット完了後にPhase Cで同様に作成する。
   - normal以降はHFSSを軸に、連成解析なし（normal）→ hardでは任意の連成 or 高度後処理 →
     expertではPython後処理（matplotlib等）を中心に据える。
   - 既存の `2026.PyAnsysTraning_inJapan/WorkShop/HFSS/ex1_dipole` 等は「参考にする既存資産」として
     位置づけるが、コピーはせず、`docs/exercise-template.md` の型に沿って PyAEDT-Learning-Hub 用に
     書き直す（対象読者・前提が異なるため）。
2. HFSS 4問が完成した時点で `docs/roadmap/coverage.md` の該当行のステータスを更新し、
   `docs/exercise-template.md` に運用上気づいた修正があれば反映する（型の妥当性検証)。
3. `exercise/README.md`（全体索引）を作成し、難易度別の学び方・前提知識・進め方を記載する
   （`WorkShop/HFSS/README.md` の「進め方」「共通の評価基準」セクションを参考に構成）。

**Phase B 完了時点でテンプレートが実運用に耐えるか確認し、必要なら Phase A のドキュメントに差分反映する。**

---

## Phase C: 段階的ロールアウト（残り12アプリ）

*depends on Phase B（型確定後）*

優先順位（ヒアリングで「主要8アプリ」を推奨と回答されたため、この順で実施）:

- **Tier 1**（優先度高、Phase Bで検証済みのHFSSに続く中核ソルバー）: maxwell_3d, icepak, q3d
- **Tier 2**: hfss_3d_layout, maxwell_2d, 2d_extractor, circuit, mechanical
- **Tier 3**（題材が少ない/ニッチ、最後に着手）: emit, twin_builder, edb, misc

各アプリごとに:
1. `docs/roadmap/coverage.md` の該当行を参照し、4難易度分（emit は1〜2問/難易度）の
   README/starter/solution を作成する。
2. 作成後、`docs/review-checklist.md` に沿って自己レビューし、coverage.md のステータスを更新する。
3. 1アプリ分の作業は独立して検証可能（そのアプリのフォルダのみで完結）なので、
   Tier内・Tier間は別セッションに分割して進めてよい。

---

## Relevant files
- `d:\+Projects\repos\PyAEDT-Learning-Hub\memo\` — 課題作成者向け内部メモ（本計画ファイル置き場）。課題実施者には非公開。
- `d:\+Projects\repos\PyAEDT-Learning-Hub\docs\` — 新規6ドキュメントの置き場所（現在空）
- `d:\+Projects\repos\PyAEDT-Learning-Hub\exercise\{0.easy,1.normal,2.hard,3.expert}\` — 既存の空スキャフォールド（活用）
- `d:\+Projects\repos\PyAEDT-Learning-Hub\exercise\HFSS\`, `exercise\HFSS_3DLayout\` — 削除対象（空フォルダ、方式変更のため不要）
- `2026.PyAnsysTraning_inJapan\WorkShop\HFSS\README.md` / `ex1_dipole\{README.md,starter.py,solution.py}` — フォーマットの参照テンプレート
- `AEDT-AI-Assistant\examples\README.md` および `examples\<app>\` — 動作確認済みAPIパターンの参照先（コードの丸写しはしないが、API呼び出しの正確性確認に使う）
- `AEDT-AI-Assistant\knowledge\automation\pyaedt.md` — 環境構築ガイド作成時の参照元
- `d:\+Projects\repos\pyaedt\src\ansys\aedt\core\` / `d:\+Projects\repos\pyedb\src\pyedb\` — PyAEDT/PyEDBのローカルソースリポジトリ。
  引数名・戻り値・内部実装が不明なAPIは推測せず、ここをgrep/参照するか `inspect.signature()` で実行時検証する
  （AEDT-AI-Assistant のコード生成ワークフローと同様の方針）。

## Verification
1. Phase A後: 6つのdocsファイルと ルートREADME.md が存在し、`docs/roadmap/coverage.md` の表が全13アプリフォルダ×4難易度を網羅していることを目視確認。
2. Phase B後: HFSSの4問について `starter.py`/`solution.py` を実際にAEDT環境で実行し、
   `docs/review-checklist.md` の各項目を満たすか確認（ライセンスが必要なため手動実行）。
   Python構文エラーがないことは `get_errors` で確認。
3. Phase C各アプリ完了時: 同様にreview-checklistで確認し、coverage.mdのステータスを更新。

## Decisions
- 公式サンプルは著作権配慮のため直接転用せず、独自課題として再構成する。
- 難易度先のフォルダ構造を採用し、既存のアプリ先フォルダ（HFSS, HFSS_3DLayout）は削除する。
- 全全13アプリフォルダを最終目標とするが、実装は優先順位（Tier1→2→3）に段階的ロールアウトし、
  `coverage.md` で進捗管理することで複数セッションにまたがる実行を可能にする。
- emitのように公式サンプルが少ないアプリは、2〜3問/難易度の原則を緩和する。
- フル商用ライセンス所有を前提とし、ライセンス制限への配慮は不要。
- `solution.py` は `starter.py` と同一フォルダに配置する。
- 難易度の基準軸はPythonの難しさではなくAEDT/PyAEDTドメインの複雑さとする
  （読者は「Pythonの基本文法習得済み・ドキュメント参照しながらコードを書ける人」を全難易度共通の前提とする）。

## 追加ヒアリング結果（確定事項）
- ライセンス: フル商用ライセンス所有を前提とする（学生版制限やHPCライセンス回避などは考慮不要）。
- `solution.py` は `starter.py` と同一フォルダに配置する（分離しない）。
- 対象読者の前提知識: 「Pythonの基本文法は習得済みで、サイト・公式ドキュメント等を参照しながら
  コードを書ける人」を全難易度共通のベースラインとする。
  → 難易度の軸は **Pythonの難易度ではなく、AEDT/PyAEDTのドメイン知識・ワークフローの複雑さ** で決める
  （例: 使う境界条件/解析タイプの数、パラメトリック設計の有無、マルチフィジックス連成の有無、
  高レベルAPI・設定ファイルの活用度）。`docs/difficulty-criteria.md` の冒頭にこの前提を明記する。

## 再ヒアリング結果（難易度基準の全面改訂）
- Sherlockインポートは別アプリの機能のため、icepakの題材候補から除外する。
- easy（目安30分）: AEDT基本操作全般（起動→保存→終了の流れ）。変数化・形状作成/変更・物性作成/変更は
  代表例であり、これらに限定しない。アプリケーションに依存しない課題でよく、`exercise/0.easy/common/`
  を新設して良い。各アプリに2問以上そろえる必要はない。
- normal（目安60分）: ここからアプリケーション別の課題を中心にする。連成解析は対象外。
  「モデル作成→Setup作成→解析実行」の自動化基本＋外部モジュール活用（例: CSVインポートから
  境界条件を割り当てる）＋AEDT内で完結する簡単なポスト処理。
  （旧基準の「easy」相当の内容の一部はnormalに繰り上げ）
- hard（目安90分）: 高度なポスト処理を含める。複数アプリにまたがる連成解析はこのレベルでのみ、
  任意（必須ではない）で扱ってよい。
- expert（目安90分以上）: 複数アプリの利用よりも、matplotlib等を使ったデータ処理・後解析を重視する。
- 上記の時間・内容基準は多少の逸脱を許容する（厳密なルールではなく目安）。
- `common/` の easy 課題は特定アプリに固定せず、学習者が `Hfss`/`Icepak`/`Maxwell3d` 等から自由に選べる
  ようにする。そのためのクラス名対応表を `docs/app-selection.md` として独立ファイル化し、各課題の
  README/starter.py から参照する（課題ごとに対応表を重複記載しない）。

## 追加ヒアリング結果（memoフォルダの位置づけ）
- `memo/` は課題作成者（このプロジェクトを保守する側）が、課題作成にあたっての確認事項・決め事・検討経緯を
  記録しておく内部フォルダとする。
- 課題実施者（学習者）には見せない前提とする。`docs/` や `exercise/` などの学習者向け成果物には
  `memo/` の内容を転記・参照させない（学習者向けに必要な情報は改めて `docs/` 側に清書する）。

## 注記（履歴セクションについて）
上記の「Decisions」「追加ヒアリング結果」「再ヒアリング結果」は、その時点のヒアリング内容をそのまま記録した
議事録であり、後から方針が変わっても自動更新されない。**最新の結論は冒頭の「背景・決定事項」および各Phaseの
本文を正とする**。特に以下は履歴セクションの記述が古いので注意:
- easyのフォルダは `common/` 単体ではなく `common_3d`/`common_2d`/`common_schematic` の3分割が最新
- hfss_3d_layout と edb は easy 対象外（normalから開始）
- 製品名表記は「Q3D」「Q2D」ではなく「Q3D Extractor」「2D Extractor」（フォルダ名は `q3d`/`2d_extractor`）
