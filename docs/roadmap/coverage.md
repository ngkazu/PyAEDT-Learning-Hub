# カバレッジ表（アプリ×難易度、進捗トラッキング）

ステータス: 未着手 / 下書き / レビュー中 / 完了

| アプリ | easy | normal | hard | expert |
|---|---|---|---|---|
| common_3d（HFSS/Maxwell 3D/Icepak/Q3D Extractor/IcepakFEA共通） | 変数化/形状作成・変更/物性作成・変更（起動→保存→終了）<br>**状態: 完了**（`ex01_basic_operations`。AEDTでの実行検証済み）／ブーリアン演算(Subtract)<br>**状態: 完了**（`ex02_boolean_subtract`。AEDTでの実行検証済み）／セットアップ作成基礎<br>**状態: 完了**（`ex03_setup_basics`。AEDTでの実行検証済み）／シート形状(矩形・円)<br>**状態: 完了**（`ex04_sheets`。AEDTでの実行検証済み）／ブーリアン演算(Unite)<br>**状態: 完了**（`ex05_unite`。AEDTでの実行検証済み）／形状の移動・回転<br>**状態: 完了**（`ex06_move_rotate`。AEDTでの実行検証済み）／Plane作成<br>**状態: 完了**（`ex07_plane`。AEDTでの実行検証済み）／CADインポート<br>**状態: 完了**（`ex08_cad_import`。AEDTでの実行検証済み）／プロジェクト変数・デザイン変数<br>**状態: 完了**（`ex09_variables`。AEDTでの実行検証済み）／チョークのジオメトリ作成<br>**状態: 完了**（`ex10_choke_geometry`。要実行検証）／面の取得<br>**状態: 完了**（`ex11_get_faces`。要実行検証）／デザイン設定のJSON入出力<br>**状態: 完了**（`ex12_export_import_config`。要実行検証）／カスタム材料の作成<br>**状態: 完了**（`ex13_custom_material`。要実行検証）／断面切断＆ターミナル作成<br>**状態: 完了**（`ex14_section_terminal`。要実行検証）／ポリラインの回転複製<br>**状態: 完了**（`ex15_polyline_duplicate`。要実行検証）／ローカル座標系の作成<br>**状態: 完了**（`ex16_local_coordinate_system`。要実行検証）／非モデル形状の作成<br>**状態: 完了**（`ex17_non_model`。要実行検証）／直線方向への複製<br>**状態: 完了**（`ex18_duplicate_along_line`。AEDTでの実行検証済み）／解析領域(Region)の作成<br>**状態: 完了**（`ex19_create_region`。AEDTでの実行検証済み） | — | — | — |
| common_2d（Maxwell 2D/2D Extractor共通） | 同上（2D断面形状）<br>**状態: 未着手** | — | — | — |
| common_circuit（Circuit/EMIT/Twin Builder共通） | 回路要素の配置・接続（起動→配置→配線→保存→終了）<br>**状態: 完了**（`ex01_circuit_basics`。Circuit/Twin Builder でAEDT実行検証済み） | — | — | — |
| HFSS（`hfss`） | （common_3dで代替可） | ダイポールアンテナ（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex01_dipole_antenna`。AEDTでの実行検証済み）／導波管インダクティブアイリスフィルタ（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex02_iris_filter`。AEDTでの実行検証済み）／マイクロストリップ線路（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex03_microstrip_line`。AEDTでの実行検証済み）／プローブ給電パッチアンテナ（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex04_patch_antenna`。AEDTでの実行検証済み） | ダイポールアンテナ＋S11・遠方界レポート<br>**状態: 完了**（`ex01_dipole_farfield`。AEDTでの実行検証済み）／導波管インダクティブアイリスフィルタ＋高度後処理<br>**状態: 完了**（`ex02_iris_filter`。AEDTでの実行検証済み）／マイクロストリップ線路＋S/フィールドプロット<br>**状態: 完了**（`ex03_microstrip_line_fieldplot`。AEDTでの実行検証済み）／プローブ給電パッチアンテナ＋S11・遠方界レポート<br>**状態: 完了**（`ex04_patch_antenna_farfield`。AEDTでの実行検証済み） | ダイポールアンテナS11・遠方界データのPython後処理（VSWR・帯域幅算出・PyVista・CSV入出力）<br>**状態: 完了**（`ex01_dipole_s11_postprocessing`。AEDTでの実行検証済み）／導波管インダクティブアイリスフィルタのS/フィールドデータ後処理（CSV入出力・PyVista可視化）<br>**状態: 完了**（`ex02_iris_filter_postprocessing`。AEDTでの実行検証済み）／マイクロストリップ線路のS/フィールドデータ後処理（CSV入出力・PyVista可視化）<br>**状態: 完了**（`ex03_microstrip_line_postprocessing`。AEDTでの実行検証済み）／パッチアンテナの設計計算Python後処理（伝送線路モデル・CSV入出力・PyVista可視化）<br>**状態: 完了**（`ex04_patch_antenna_design`。AEDTでの実行検証済み） |
| Maxwell 3D（`maxwell_3d`） | （common_3dで代替可） | コモンモードチョーク（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex01_choke`。AEDTでの実行検証済み）／TEAM7非対称導体（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex02_asymmetric_conductor`。AEDTでの実行検証済み）／コイル・コア電磁石（Magnetostatic・Setup作成→解析実行のみ）<br>**状態: 完了**（`ex03_coil_core`。AEDTでの実行検証済み） | チョーク＋巻線損失・B場フィールドプロット<br>**状態: 完了**（`ex01_choke_lossreport`。AEDTでの実行検証済み）／TEAM7非対称導体＋$B_z$ラインレポート<br>**状態: 完了**（`ex02_asymmetric_conductor_bzreport`。AEDTでの実行検証済み）／コア内部の磁束密度フィールドプロット<br>**状態: 完了**（`ex03_coil_core_fieldplot`。AEDTでの実行検証済み） | チョークのインダクタンス/損失のPython集計・CSV・PyVista<br>**状態: 完了**（`ex01_choke_postprocessing`。AEDTでの実行検証済み）／TEAM7の公開実測データとの比較・誤差算出<br>**状態: 完了**（`ex02_asymmetric_conductor_benchmark`。AEDTでの実行検証済み）／磁束密度データのPython集計・CSV入出力＋PyVista可視化<br>**状態: 完了**（`ex03_coil_core_postprocessing`。AEDTでの実行検証済み） |
| Icepak（`icepak`） | （common_3dで代替可） | ヒートシンク熱解析（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex01_heatsink`。要実行検証）／小型筐体のファン冷却解析（native Fanコンポーネント）<br>**状態: 完了**（`ex02_small_cabinet_fan`。AEDTでの実行検証済み）／PCB表面実装部品の熱解析（多層基板・HTC壁面）<br>**状態: 完了**（`ex03_smd_pcb_thermal`。AEDTでの実行検証済み） | ヒートシンク熱解析＋温度フィールドプロット・モニタ<br>**状態: 完了**（`ex01_heatsink_fieldplot`。AEDTでの実行検証済み）／小型筐体のファン冷却解析＋温度フィールドプロット・モニタ<br>**状態: 完了**（`ex02_small_cabinet_fan_fieldplot`。AEDTでの実行検証済み）／PCB表面実装部品の熱解析＋温度フィールドプロット・モニタ<br>**状態: 完了**（`ex03_smd_pcb_thermal_fieldplot`。AEDTでの実行検証済み） | ヒートシンク熱解析 温度データのPython集計・CSV入出力＋PyVista可視化<br>**状態: 完了**（`ex01_heatsink_postprocessing`。AEDTでの実行検証済み）／小型筐体のファン冷却解析 温度データのPython集計・CSV入出力＋PyVista可視化（Fan動作点取得含む）<br>**状態: 完了**（`ex02_small_cabinet_fan_postprocessing`。AEDTでの実行検証済み）／PCB表面実装部品の熱解析 温度データのPython集計・CSV入出力＋PyVista可視化<br>**状態: 完了**（`ex03_smd_pcb_thermal_postprocessing`。AEDTでの実行検証済み） |
| Q3D Extractor（`q3d`） | （common_3dで代替可） | ブスバー解析（Setup作成→解析実行のみ）<br>**状態: 完了**（`ex01_busbar`。要実行検証） | ブスバー＋縮退行列・キャパシタンス/インダクタンスレポート<br>**状態: 完了**（`ex01_busbar_matrixreport`。要実行検証） | ブスバー容量・インダクタンスの周波数特性をPythonでプロット（CSV入出力・PyVista可視化）<br>**状態: 完了**（`ex01_busbar_postprocessing`。要実行検証） |
| 2D Extractor（`2d_extractor`） | （common_2dで代替可） | CPWG・ストリップライン<br>**状態: 未着手** | 同上＋高度後処理<br>**状態: 未着手** | 周波数特性をPythonでプロット<br>**状態: 未着手** |
| HFSS 3D Layout（`hfss_3d_layout`） | （easy対象外） | パラメトリックPCB作成<br>**状態: 未着手** | プリレイアウトSI(SMAコネクタ)＋高度後処理／パワーインテグリティ・DCIR連成（任意）<br>**状態: 未着手** | レイアウト解析結果のPythonカスタム可視化<br>**状態: 未着手** |
| Maxwell 2D（`maxwell_2d`） | （common_2dで代替可） | 抵抗計算/静電解析 setup+解析<br>**状態: 未着手** | 2D軸対称アクチュエータ/PM同期モータ過渡＋高度後処理<br>**状態: 未着手** | RMxprt→Maxwell2Dエクスポート結果等のPython後処理<br>**状態: 未着手** |
| Circuit（`circuit`） | （common_circuitで代替可） | RLC直列回路の過渡解析<br>**状態: 完了**（`ex01_rlc_transient`。AEDTでの実行検証済み） | RLCローパスフィルタのSパラメータ解析（S21・S11レポート）<br>**状態: 完了**（`ex01_rlc_filter_sparams`。AEDTでの実行検証済み） | RLCローパスフィルタ SパラメータのPython後処理（カットオフ算出・CSV入出力・matplotlib・Touchstone出力）<br>**状態: 完了**（`ex01_rlc_filter_postprocessing`。AEDTでの実行検証済み） |
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
- HFSSの追加シリーズとして、マイクロストリップ線路・パッチアンテナが完了。RCS（モノスタティック
  レーダー断面積、SBR+ソルバー）は**保留（将来課題）**とする。他シリーズと物理・ワークフローが大きく異なり
  （ポートを使わない平面波入射・SBR+専用のセットアップ）、ワークスペース内に動作確認済みの参考実装が
  ないため、着手時期は未定。各シリーズはnormal/hard/expertの3ファイル×3階層で構成される。
  ※ 当初予定していたアンテナアレイ・チョークコイル・フレキシブルケーブル/CPWGは、マイクロストリップ線路・
  RCSに差し替え済み（アンテナアレイは実装済みだったが、ユーザー判断によりex3をマイクロストリップ線路に
  置き換えた）。

