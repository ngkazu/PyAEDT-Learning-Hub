---
name: pyaedt-learning-hub-exercise-authoring
description: "PyAEDT-Learning-Hub プロジェクトで課題（exercise）の README.md/starter.py/solution.py 3点セットを新規作成・修正する際に使う。easy/normal/hard/expert のシリーズ設計、PyEDB/HFSS 3D Layoutの実践的な落とし穴、AEDTライブ検証からの教材化ワークフロー、commit規約をカバーする。他のSynopsys製品向けの一般的なHFSS/AEDTスキルとは別に、このリポジトリ固有の規約・既知の落とし穴を優先する。"
topic: "PyAEDT-Learning-Hub"
sub_topic: "exercise-authoring"
---

## Instructions

このSkillは `D:\+Projects\repos\PyAEDT-Learning-Hub` 専用。リポジトリの `.github/copilot-instructions.md`
と `docs/` 配下（`exercise-template.md`, `difficulty-criteria.md`, `review-checklist.md`, `app-selection.md`）
が正式な方針ドキュメント。このSkillはそれらを**実行手順・コードパターン・既知の落とし穴**まで具体化したもの。
方針とこのSkillが矛盾する場合はリポジトリのドキュメントを優先し、矛盾があればユーザーに報告する。

### 0. 作業前チェック

1. `.github/copilot-instructions.md` と `docs/exercise-template.md` を確認（セッション内で未読なら読む）。
2. `docs/roadmap/coverage.md` で対象アプリ/シリーズの進捗ステータスを確認する。
3. 既存の類似課題（同じ難易度・近い題材）を1つ以上読み、見出し構成・トーン・コメントスタイルを把握する
   （例: HFSS 3D Layout/PyEDBなら `exercise/1.normal/hfss_3d_layout/ex01_diff_pair/`、
   Sパラメータ系の後処理パターンなら `exercise/2.hard/circuit/ex01_rlc_filter_sparams/` と
   `exercise/3.expert/circuit/ex01_rlc_filter_postprocessing/`）。

### 1. 3点セット作成の順序（`docs/exercise-template.md` 準拠）

1. **normalを先に作る**（モデル作成→Setup作成→解析実行、ポスト処理なし）。実AEDTで実行確認を済ませる。
2. normalのモデルに **hard**（AEDT内部ポスト処理: Report/Field Plot）を追加する。
3. hardの内容に **expert**（Python後処理: CSV・matplotlib・必要なら Touchstone/PyVista）を追加する。
4. 既存のeasy課題でカバーされていない基礎操作があれば `0.easy/common_3d|common_2d|common_circuit|pyedb/`
   に追加する（Setup作成くらいまでの粒度。周波数スイープ・レポート・フィールドプロット等の高度操作は含めない）。

シリーズ番号（`exNN`）は、同じアプリフォルダ内でnormal/hard/expertを揃える。既存シリーズの番号は変更しない。
各READMEの冒頭に、シリーズの他レベルへの相互参照リンクを入れる（easy↔normal↔hard↔expert、双方向）。

### 2. ライブ検証→教材化ワークフロー（MANDATORY）

**コードを教材に書く前に、必ずAEDT上で実際に動かして確認する。** 推測で書いたAPIコールは高確率で失敗する
（特にPyEDB/HFSS 3D Layout）。

1. AEDTセッションの状態を確認し（`check_aedt_status`）、未接続なら `launch_aedt`
   （`non_graphical=False`、MCPガードレールに従い `--non-graphical` は使わない）。
2. **一時フォルダ**（`tempfile.gettempdir()` 配下など、exerciseフォルダの外）でモデルを作り、
   `run_python_code` でAPIを1手順ずつ検証する。`new_desktop=False`（またはprojectパス指定のみ）で
   MCP所有のDesktopにアタッチする。`new_desktop=True`/`release_desktop()` は検証コードでは使わない
   （MCPガードレール: Desktop所有権はMCP側）。
3. ソルブを伴う場合は必ず `blocking=False` で起動し、起動前後で `is_solved`/`are_there_simulations_running`
   をスナップショットして「起動できたか」を確認する。完了は別ターンで確認する（結果読み取りは完了後）。
4. 検証で確定したAPI呼び出し・引数名・戻り値の扱いを、教材の `solution.py` にそのまま使う
   （`new_desktop=True`, `release_desktop(close_projects=True, close_desktop=True)` は教材の
   スタンドアロン実行用としてはそのまま使ってよい。検証時だけMCP安全な形に読み替える）。
5. 検証が終わったら一時フォルダを削除し、AEDTは必要に応じて `disconnect_from_aedt(close_desktop=True,
   close_projects=True)` で閉じる。

### 3. PyEDB / HFSS 3D Layout の既知の落とし穴

これらは実際のデバッグで発見したもの。推測せず、ここに書いてある通りに実装する。

- **`create_differential_wave_port` / `create_wave_port` をストリップライン端の平面トレースに使わない。**
  wave port は内部でcoax(同軸)ポート扱いになり、ポート領域内にvia/bondwireを要求する。via のない
  平面トレース端に使うと `could not find suitable geometry to form the terminal of the coax port`
  でメッシュ生成が失敗する。
  → 正解: `edb.source_excitation.create_edge_port_vertical(prim_id=trace.id, point_on_edge=[x,y],
  port_name=..., reference_layer="GND_TOP", hfss_type="Gap")`（vertical gap port、via不要）。
- **ビア作成APIの正しい名前**: `edb.padstacks.create(...)`（✗ `create_padstack`は存在しない）、
  `edb.padstacks.place(position=..., definition_name=..., net_name=...)`（✗ `place_padstack`は存在しない）。
  定義（`create`）と配置（`place`）は別メソッド。
- **ネット作成**: `edb.nets.find_or_create_net(net_name=...)`（同名なら再利用、安全に何度でも呼べる）。
- **PyEDBの座標はメートル単位**（PyAEDTの3D Modelerのような `"10mm"` 文字列ではなく `0.010` のような数値）。
  層厚・ビア寸法など一部プロパティは `"35um"` のような単位付き文字列も使える。
- **差動Sパラメータは `context="Differential Pairs"` が必須**（`create_report()` にも
  `get_solution_data()` にも）。なしだと式の文法が正しくてもプロットが空/データ取得不能になる。
  - 差動ペア設定: `h3d.set_differential_pair(assignment=正側ポート名, reference=負側ポート名,
    differential_mode=..., common_mode=..., differential_reference=100, common_reference=25)`
  - 確認: `h3d.get_differential_pairs()`
  - 式: `S(出力側ペア名, 入力側ペア名)`（例 `S(Diff_Out,Diff_In)` = Sdd21、`S(Diff_In,Diff_In)` = Sdd11）
- **`setup.sweeps[0]` は再取得タイミングによって空リストになることがある。**
  `create_linear_count_sweep(...)` の**戻り値**を変数で受けて `.name` を使うこと
  （`sweep = h3d.create_linear_count_sweep(...)`; `setup_sweep = f"{setup.name} : {sweep.name}"`）。
  `export_touchstone(sweep=...)` にも同じ戻り値の `.name` を渡す。
- **`SolutionData` オブジェクトを `if data:` のように真偽値評価しない**（内部numpy配列の評価で
  `ValueError: The truth value of an array...` になる）。`data.get_expression_data("式そのまま")` で
  `(周波数配列, 値配列)` のタプルを直接取り出す。
- **staleな `.aedt.lock`**: 前セッションの異常終了などで `<project>.aedt.lock` が残ると
  「Project is locked」になる。`list_projects()` で本当に開かれていないことを確認し、他のAEDT
  セッションで開いていないかユーザーに確認してから削除する（`.aedb` フォルダ自体は消さない）。

### 4. README.md の必須セクションとスタイル

`docs/exercise-template.md` 8セクション（タイトル/目安時間/題材/学習目標/課題/ヒント/評価基準/発展課題）を
満たす。加えて:

- タイトル直下に `> この演習は「○○シリーズ」の△△レベル。` という注記を入れ、同シリーズの他レベルへの
  相対リンクを張る（easy↔normal↔hard↔expert 双方向。片方向だけだと手戻りになる）。
- 「課題」セクションは番号付きリストで、`starter.py` の TODO と1対1対応させる。
- 「ヒント」セクションには、§3の落とし穴のうち該当するものを必ず含める。
- common_3d/common_2d/common_circuit/pyedb の課題は「アプリケーションの選び方」節を設け、
  `docs/app-selection.md` を参照する（対応表を重複記載しない）。
- 製品名表記は `.github/copilot-instructions.md` の対応表に従う（例: 「Q3D」ではなく「Q3D Extractor」）。

### 5. starter.py / solution.py の規約

- 冒頭に `AEDT_VERSION = "2026.1"` をまとめ、`settings.release_on_exception = False` を設定する。
- `starter.py` は `# TODO: ...` コメントで何を実装すべきか具体的に書く（README「課題」と対応させる）。
- `solution.py` は `starter.py` と同一フォルダ・同じ全体構成、TODO部分だけ実装済みにする。
- 最後に必ず `release_desktop(close_projects=True, close_desktop=True)`（EDBのみの場合は `edb.close()`）
  を呼ぶ。
- hard/expertは「各課題は自己完結させる」方針（normalのモデル作成コードをhard/expertにも重複して書く。
  importして使い回さない）。既存のRLC/差動ペアシリーズがこの方針の実例。

### 6. 日本語ドキュメント規約

`docs/`, `exercise/`, `lecture/` 配下のドキュメント・コメントはすべて日本語（コード・API名・引数名・
識別子・ファイルパスは英語のまま）。`memo/` は課題作成者向け内部メモで学習者には見せない
（`docs/`/`exercise/`からは参照・転記しない）。

### 7. コミット規約

- メッセージ形式: `<type>(<scope>): <日本語の要約1行>`（例: `feat(hfss_3d_layout): ...`,
  `docs(lecture): ...`, `refactor(pyedb): ...`）。
- 本文に、根本原因や設計判断があれば日本語で簡潔に記録する（後から読む人が「なぜこうしたか」を
  追えるように）。
- `__pycache__` 等の副生成物はコミット前に削除する。構文チェック（`py -3 -m py_compile ...`。
  このマシンでは素の `python` コマンドの挙動が不安定なことがあるため `py -3` を使う）を済ませる。
- コミット前に `git status --short` で意図しないファイルが混ざっていないか確認する。
- 実際にコミットするかはユーザーの明示的な指示を待つ（連続作業中で指示が明確な場合を除く）。

### 8. 進捗管理

課題を1つ完成させたら `docs/roadmap/coverage.md` の該当セルのステータスを更新する
（未着手 → 下書き → レビュー中 → 完了）。

## Examples

### Example 1: 新しいnormal課題を作る（HFSS 3D Layout / PyEDB）

1. §0: 既存の `exercise/1.normal/hfss_3d_layout/ex01_diff_pair/` を読んでスタイル把握。
2. §2: 一時フォルダでPyEDBのAPI（スタックアップ・ネット・トレース・ポート）を1つずつ検証。
   ポートは§3の「wave portを使わない」ルールに従い vertical gap port を使う。
3. 検証で確定したコードで `solution.py` を書く → `starter.py`（TODO化） → `README.md`（§4のセクション）。
4. `exercise/README.md` の演習一覧テーブルに1行追加し、相互参照リンクを張る。
5. 構文チェック → `__pycache__` 削除 → commitメッセージ案を提示 → ユーザー承認後にcommit/push。

### Example 2: 既存normalにhard/expertを追加する

1. §1「作成順序」に従い、まずhardのAEDTポスト処理（Report/Field Plot）を検証・作成。
2. hardのモデル作成コードをexpertにも複製し、Python後処理（CSV/matplotlib/Touchstone等）を追加。
   §3の「差動Sパラメータはcontext必須」等、該当する落とし穴をヒントに明記する。
3. normal側READMEの「発展課題」/冒頭注記をhard/expertへの実リンクに更新する（双方向リンク）。

