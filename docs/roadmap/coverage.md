# カバレッジ表（アプリ×難易度、進捗トラッキング）

ステータス: 未着手 / 下書き / レビュー中 / 完了

| アプリ | easy | normal | hard | expert |
|---|---|---|---|---|
| common_3d（HFSS/Maxwell 3D/Icepak/Q3D Extractor/IcepakFEA共通） | 変数化/形状作成・変更/物性作成・変更（起動→保存→終了）<br>**状態: 完了**（`ex1_basic_operations`。AEDTでの実行検証済み）／ブーリアン演算(Subtract)<br>**状態: 完了**（`ex2_boolean_subtract`。要実行検証）／セットアップ作成基礎<br>**状態: 完了**（`ex3_setup_basics`。要実行検証） | — | — | — |
| common_2d（Maxwell 2D/2D Extractor共通） | 同上（2D断面形状）<br>**状態: 未着手** | — | — | — |
| common_circuit（Circuit/EMIT/Twin Builder共通） | 回路要素の配置・接続（起動→保存→終了）<br>**状態: 未着手** | — | — | — |
| HFSS（`hfss`） | （common_3dで代替可） | ダイポールアンテナ（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex1_dipole_antenna`。AEDTでの実行検証済み）／導波管インダクティブアイリスフィルタ（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex2_iris_filter`。AEDTでの実行検証済み）／ダイポールアレイアンテナ（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex3_antenna_array`。AEDTでの実行検証済み） | ダイポールアンテナ＋S11・遠方界レポート<br>**状態: 完了**（`ex1_dipole_farfield`。要実行検証）／導波管インダクティブアイリスフィルタ＋高度後処理<br>**状態: 完了**（`ex2_iris_filter`。AEDTでの実行検証済み）／ダイポールアレイアンテナ＋S/遠方界レポート<br>**状態: 完了**（`ex3_antenna_array_farfield`。AEDTでの実行検証済み） | ダイポールアンテナS11・遠方界データのPython後処理（VSWR・帯域幅算出・PyVista・CSV入出力）<br>**状態: 完了**（`ex1_dipole_s11_postprocessing`。要実行検証：CSV入出力・PyVista部分は追加検証が必要）／導波管インダクティブアイリスフィルタのS/フィールドデータ後処理（CSV入出力・PyVista可視化）<br>**状態: 完了**（`ex2_iris_filter_postprocessing`。要実行検証）／ダイポールアレイアンテナのビームステアリングPython後処理（`edit_sources`・理論アレイファクタ・PyVista可視化）<br>**状態: 完了**（`ex3_antenna_array_beamsteering`。AEDTでの実行検証済み） |
| Maxwell 3D（`maxwell_3d`） | （common_3dで代替可） | DC解析(質量中心)/チョーク setup+解析<br>**状態: 未着手** | TEAM3浴槽板/TEAM7非対称導体＋高度後処理／Maxwell-Icepak連成（任意）<br>**状態: 未着手** | 磁石セグメンテーション結果のPython後処理<br>**状態: 未着手** |
| Icepak（`icepak`） | （common_3dで代替可） | グラフィックカード熱解析／CSVブロック定義（外部CSV→境界条件割当て）<br>**状態: 未着手** | 3DコンポーネントIDF/EDBインポート＋高度後処理／HFSS-Icepak連成（任意）<br>**状態: 未着手** | IDF/EDBインポート結果の温度データをPythonで可視化<br>**状態: 未着手** |
| Q3D Extractor（`q3d`） | （common_3dで代替可） | ブスバー解析<br>**状態: 未着手** | ケーブルパラメータ抽出＋高度後処理／EDBからのPCB DCIR/AC連成（任意）<br>**状態: 未着手** | 抽出結果の周波数特性をPythonでプロット<br>**状態: 未着手** |
| 2D Extractor（`2d_extractor`） | （common_2dで代替可） | CPWG・ストリップライン<br>**状態: 未着手** | 同上＋高度後処理<br>**状態: 未着手** | 周波数特性をPythonでプロット<br>**状態: 未着手** |
| HFSS 3D Layout（`hfss_3d_layout`） | （easy対象外） | パラメトリックPCB作成<br>**状態: 未着手** | プリレイアウトSI(SMAコネクタ)＋高度後処理／パワーインテグリティ・DCIR連成（任意）<br>**状態: 未着手** | レイアウト解析結果のPythonカスタム可視化<br>**状態: 未着手** |
| Maxwell 2D（`maxwell_2d`） | （common_2dで代替可） | 抵抗計算/静電解析 setup+解析<br>**状態: 未着手** | 2D軸対称アクチュエータ/PM同期モータ過渡＋高度後処理<br>**状態: 未着手** | RMxprt→Maxwell2Dエクスポート結果等のPython後処理<br>**状態: 未着手** |
| Circuit（`circuit`） | （common_circuitで代替可） | 回路スキーマ作成+過渡解析<br>**状態: 未着手** | サブサーキット管理/アイダイアグラム＋高度後処理<br>**状態: 未着手** | PCIeバーチャルコンプライアンス/AMI結果のPythonカスタム解析<br>**状態: 未着手** |
| EMIT（`emit`） | （common_circuitで代替可） | アンテナ共存干渉基礎<br>**状態: 未着手**（公式サンプルが少ないため1〜2問可） | HFSS-EMIT連成（任意）＋高度後処理<br>**状態: 未着手** | 干渉解析結果のPythonカスタムプロット<br>**状態: 未着手** |
| Twin Builder（`twin_builder`） | （common_circuitで代替可） | RC回路解析/整流回路(コンデンサフィルタ)<br>**状態: 未着手** | Static ROM＋高度後処理<br>**状態: 未着手** | Dynamic ROM/LTI ROM結果のPython比較プロット<br>**状態: 未着手** |
| EDB（`edb`） | （easy対象外） | 設定ファイル(Configuration)基礎/IPC2581エクスポート<br>**状態: 未着手** | GDSインポートワークフロー＋高度後処理<br>**状態: 未着手** | 設定ファイルワークフロー結果のPython集計・レポート<br>**状態: 未着手** |
| misc（`misc`） | （easyはcommon分類になじまず、未定義） | Touchstoneファイル操作/Lumped Element Filter設計<br>**状態: 未着手** | COM解析＋高度後処理<br>**状態: 未着手** | Touchstone(skrf)/COM結果のPythonカスタム解析・プロット<br>**状態: 未着手** |
| IcepakFEA（`mechanical`） | （common_3dで代替可） | Phase Bで検討<br>**状態: 未着手** | Phase Bで検討<br>**状態: 未着手** | Phase Bで検討<br>**状態: 未着手** |

## 優先順位（Phase C ロールアウト順）

- **Tier 1**（HFSSパイロットに続く中核ソルバー）: `maxwell_3d`, `icepak`, `q3d`
- **Tier 2**: `hfss_3d_layout`, `maxwell_2d`, `2d_extractor`, `circuit`, `mechanical`
- **Tier 3**（題材が少ない/ニッチ）: `emit`, `twin_builder`, `edb`, `misc`

## 注記

- `icepak` の Sherlock連携（別アプリの機能）は題材候補から除外済み。
- hard/expertで挙げた「連成（任意）」系の題材は hard でのみ許容し、expert では扱わない
  （expert は Python 後処理を重視するため）。連成課題を採用する場合は主導アプリ側のフォルダに1つだけ置き、
  関連アプリ側に重複配置しない。
- IcepakFEA（`mechanical`）の normal/hard/expert の具体的な題材は Phase B での検証結果を踏まえて決定する。
- normal/hard/expert は「シリーズ」構成（同じ `exNN_*` のモデルを段階的に拡張する）。詳細は
  [difficulty-criteria.md](../difficulty-criteria.md) の「難易度のシリーズ設計」を参照。
- HFSSの追加シリーズとして、アンテナアレイ（完了）に続き、パッチアンテナ（Stackup3D）・チョークコイル（EMC）・
  フレキシブルケーブル/CPWGの3トピックを予定（Phase B内で段階的に追加）。各シリーズはnormal/hard/expertの
  3ファイル×3階層で構成される。

