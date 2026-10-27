# 難易度基準

## 対象読者の前提

すべての難易度に共通する前提として、対象読者は
**「Python の基本文法は習得済みで、公式ドキュメント等を参照しながらコードを書ける人」**とする。

**難易度は Python の難しさではなく、AEDT/PyAEDT ドメインの複雑さで決める。**
具体的には、使う境界条件・解析タイプの数、パラメトリック設計の有無、マルチフィジックス連成の有無、
高レベルAPI・設定ファイルの活用度などが判断軸になる。

以下の時間・内容基準は目安であり、多少の逸脱を許容する（厳密なルールではない）。

## easy（目安30分）

- AEDT の基本操作全般を学ぶレベル。「起動 → 何かする → 保存 → 終了」という一連の流れを体験することが目的。
- 変数化、形状の作成・変更、物性の作成・変更などは代表的な例であり、これらに限定しない。
- アプリケーション固有の知識は問わない。モデリングパラダイムが近いアプリ同士で共通化し、
  `exercise/0.easy/common_3d/`（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）、
  `exercise/0.easy/common_2d/`（Maxwell 2D, 2D Extractor）、
  `exercise/0.easy/common_schematic/`（Circuit, EMIT, Twin Builder）の3グループに分ける。
- HFSS 3D Layout・EDB はレイヤー/ECAD操作でこの3区分になじまないため、easy の対象外（normal から開始）。
- **含む**: 変数定義、単純な形状/回路要素の作成・変更、物性の割り当て、保存・終了。
- **含まない**: Setup作成、解析実行、複雑な境界条件の使い分け、複数アプリの連成。

## easy の区分け: 共通easy とアプリ固有easy

easy は原則 `common_3d`/`common_2d`/`common_schematic` の3グループ（アプリ非依存）に収める。
ただし、**グループ内の共通APIだけでは練習できないアプリ固有の操作**がある場合は、
`exercise/0.easy/<app_slug>/` に専用のeasy課題を追加してよい（例:
`0.easy/circuit/ex01_pulse_port`、`0.easy/twin_builder/ex01_halfwave_diode`）。

判断基準:

- **共通easyに入れる**: 同じグループ内のどのアプリでも同じ呼び出し方（シグネチャ）で動く操作。
  例えば `common_schematic` の `create_resistor`/`create_wire`/`create_gnd` は、PyAEDTの実装上
  `TwinBuilderComponents` が `CircuitComponents` を継承しているため、Circuit でも Twin Builder でも
  **文字通り同じコード**が動く（README内の「アプリケーションの選び方」で学習者が好きな方を選べる）。
- **アプリ固有easyに分ける**: 片方のアプリにしか存在しない、または呼び出した際の挙動が大きく異なる操作。
  例えば Twin Builder の `create_voltage_source` は `source_type` で波形タイプ（ESINE/EPULSE/
  ETRIANG等）を切り替えられ、`create_diode` のような非線形素子も扱えるが、これらは Circuit の
  基底クラスには存在しない。逆に Circuit の `create_voltage_pulse` や `create_interface_port`
  （2ポート回路の入出力）も、Twin Builder側の通常のワークフローでは使わない。
  こうした「継承元に無い・一方のアプリ固有の」操作は、専用フォルダ（`0.easy/circuit/`,
  `0.easy/twin_builder/` 等）に分けて練習する。
- 固有easyは、対応する `1.normal/<app_slug>/` シリーズの**前段**として位置づける（その固有APIが
  normal以降のどの課題で実際に使われるかをREADME冒頭に明記し、共通easy・固有easy・normal間を
  双方向リンクで結ぶ）。
- common_3d・common_2dも同様の考え方が当てはまる（例えば特定ソルバーにしかない境界条件・
  特殊な形状作成APIがあれば、同様にアプリ固有easyを追加する余地がある）。判断に迷ったら、
  「そのAPIが基底クラス/共通インターフェースの一部か、個別アプリのサブクラスだけの独自メソッドか」
  をPyAEDTのソースで確認してから決める。

## 難易度のシリーズ設計（normal/hard/expertの進め方）

normal/hard/expert はできるだけ **同じモデル（題材）が難易度ごとに段階的に育つ「シリーズ」** として設計する（easyは
`common_3d`/`common_2d`/`common_schematic` でアプリ非依存が基本だが、上記の判断基準に従いアプリ固有easyを
追加してもよい）。例: HFSSの「ダイポールアンテナ」シリーズなら

- normal: モデル作成→Setup作成→解析実行まで（ポスト処理なし）
- hard: normalと同じモデルに、AEDT内部ポスト処理（Report/Field Plot等）を追加
- expert: hardと同じモデルに、PyVista可視化とCSV入出力（条件をCSVから読み込み、結果をCSV/画像で出力）を追加

というように、前の難易度で作ったものに1つずつ機能を足していく。各課題は自完結（solution.py単体で実行可能）にするため、
モデル作成コード自体は各難易度のファイル内に重複して書く（他の難易度のファイルをimport/依存しない）。
同じシリーズの課題は `exNN_<slug>` の `NN` をシリーズ内で統一する（例: ダイポールアンテナシリーズはnormal/hard/expertすべて `ex1`）。

## normal（目安60分）

- ここからアプリケーション別の課題を中心にする。
- 「モデル作成 → Setup作成 → 解析実行」という自動化の基本を学ぶ。**解析実行までで終了し、
  ポスト処理（レポート作成等）は行わない**（ポスト処理はhard以降で追加する）。
- モデル作成の一環として、外部モジュールの利用も視野に入れる（例: CSVインポートから境界条件を割り当てる）。
- **含む**: 単一アプリでのモデル作成・Setup作成・解析実行。
- **含まない**: レポート/フィールドプロット等のポスト処理、複数アプリにまたがる連成解析、Pythonでのカスタムデータ処理。

## hard（目安90分）

- **normalと同じモデル・Setup・解析に、AEDT内部ポスト処理を追加**する（Report・Field Plot等）。
- 複数アプリケーションにまたがる連成解析は、**このレベルでのみ**、任意（必須ではない）で扱ってもよい。
- **含む**: normalの内容 + AEDT内部ポスト処理（Report作成、Field Plot作成など）、任意の連成解析。
- **含まない**: PyVistaを使った可視化、CSV入出力（expertの領域）。

## expert（目安90分以上）

- **hardと同じモデル・Setup・解析・ポスト処理に、以下を追加**する:
  - **PyVistaを使った可視化**（`get_antenna_data().farfield_data.plot_3d()` など、CPython+PyVista環境でのみ動作するPyAEDTならではの機能）
  - **CSVファイルからの条件読み込み**（例: 解析するパラメータの一覧をCSVで与える）
  - **結果のCSV/画像ファイルへの出力**（matplotlib・PyVistaのレンダリング結果を画像保存、数値結果をCSV保存）
- 連成解析は扱わない（hardで任意採用済みのため、expertでは純粋なPython後処理にフォーカスする）。
- **含む**: hardの内容 + PyVista可視化 + CSV入出力。
- **含まない**: 新規の複数アプリ連成、AEDT操作そのものの複雑化。

## レベル間の判断に迷ったときの目安

| 観点 | easy | normal | hard | expert |
|---|---|---|---|---|
| アプリ固有知識 | 不要 | 必要 | 必要 | 必要 |
| Setup作成・解析実行 | なし | あり | あり（normalと同じモデル） | あり（hardと同じモデル） |
| 複数アプリ連成 | なし | なし | 任意 | なし |
| ポスト処理 | なし | なし | AEDT内部（Report/Field Plot） | +PyVista可視化・CSV入出力 |
