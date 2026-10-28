# ポスト処理の全体像（自己学習）

`exercise/` のnormal→hard→expertで繰り返し登場する「解析結果をどう見る・どう使うか」という
ポスト処理のパターンを、概念として整理したノートです。個別の演習README（例えば
[2.hard/maxwell_3d/ex01_choke_lossreport/](../exercise/2.hard/maxwell_3d/ex01_choke_lossreport/)）を
読む前に、まずこのノートで全体像をつかんでおくと、どの演習のhard/expertに進んでも
「このコードは今どの段階の処理をしているのか」が把握しやすくなります。

内容はすべて `pyaedt` パッケージ本体のソースコード（`ansys.aedt.core.visualization.post`）を
確認したうえで書いています。

---

## 1. 全体像：2系統のポスト処理

PyAEDTでのポスト処理は、大きく2つの系統に分けられます。

| 系統 | 中身 | 使うAPI |
|---|---|---|
| **AEDT内部ポスト処理** | AEDTのGUI上に「レポート」や「フィールドプロット」として保存される、AEDT側の機能 | `hfss.post.create_report()`、`hfss.post.create_fieldplot_surface()` など |
| **Python側ポスト処理** | 解析結果の数値をPythonに取り出し、numpy/matplotlib/PyVistaなど通常のPythonエコシステムで処理する | `hfss.post.get_solution_data()`、`hfss.post.plot_field_from_fieldplot()` など |

このプロジェクトの難易度設計（`docs/difficulty-criteria.md`）は、この2系統の使用範囲にそのまま
対応しています。

| 難易度 | ポスト処理の範囲 |
|---|---|
| **normal** | ポスト処理なし（モデル作成→Setup作成→解析実行まで） |
| **hard** | AEDT内部ポスト処理（レポート作成・フィールドプロット作成） |
| **expert** | Python側ポスト処理（`get_solution_data()`でのデータ取得・CSV入出力・matplotlib・PyVista可視化） |

重要なのは、**expertで使うPyVista可視化は、hardでAEDT内部に作ったフィールドプロットを
「読みに行く」形になっている**という点です。つまり、hardで `create_fieldplot_surface()` を
呼んでおかないと、expertで `plot_field_from_fieldplot()` を呼んでも表示するものがありません。
この依存関係を知っておくと、「なぜexpertの演習はhardのモデルをベースにしていると書いてあるのか」が
腑に落ちます。

---

## 2. AEDT内部ポスト処理 (1): レポート（グラフ・データテーブル）

### 2.1 `create_report()` の基本

`post.create_report()` は、AEDTのGUI上の「Results」ツリーに現れるレポートを作成します。
2Dグラフ（周波数特性など）にも、単一の値を表示するデータテーブルにも使えます。

```python
hfss.post.create_report(
    expressions="dB(S(1,1))",
    plot_name="S11 Return Loss",
)
```

主な引数は次の通りです。

| 引数 | 役割 |
|---|---|
| `expressions` | プロットする式（1つの文字列、またはリスト）。例: `"dB(S(1,1))"`、`"SolidLoss"` |
| `setup_sweep_name` | どのSetup・スイープの結果を使うか。省略時は最初のSetupと最初のスイープ |
| `report_category` | レポートの種類（`"Modal Solution Data"`、`"Fields"`、`"Far Fields"` など）。省略時はAEDTの既定カテゴリ |
| `plot_type` | 表示形式。既定は `"Rectangular Plot"`（2Dグラフ）。単一の値を見たいときは `"Data Table"` を使う |
| `context` | Q3D/Q2Dの縮退行列名、遠方界の無限球面名など、レポートの文脈を指定する |
| `plot_name` | 作成するレポートの名前 |

### 2.2 `report_category` と `plot_type` の組み合わせ例

このプロジェクトの演習で実際に使っているパターンを整理すると、次のようになります。

| 目的 | `report_category` | `plot_type` | 使用例 |
|---|---|---|---|
| Sパラメータの周波数特性 | `"Modal Solution Data"` または省略 | `"Rectangular Plot"`（既定） | HFSSのS11・S21レポート |
| 損失・インダクタンスなど単一値の確認 | `"Fields"` | `"Data Table"` | Maxwell 3Dの巻線損失・コア損失、Q3Dの自己インダクタンス |
| ラインに沿った分布 | `"Fields"` | 既定（2Dグラフ） | TEAM7演習の$B_z$ライン分布 |
| 遠方界ゲインパターン | `"Far Fields"` | `"Radiation Pattern"` | ダイポールアンテナ・パッチアンテナの放射パターン |

「周波数のように連続的に変化する値は2Dグラフ、単一のスカラー値（ある瞬間の損失やインダクタンスの値）は
Data Table」という使い分けが基本方針です。

### 2.3 生のベクトル成分はそのまま式にできない

`"Bz"`（磁束密度のZ成分）のような、ベクトル量の特定の成分を直接 `expressions` に渡すことは
**できません**。PyAEDTの標準でサポートされているのは `"Mag_B"`（大きさ）のような量だけで、
特定成分を取り出したい場合は、`post.fields_calculator` を使ってAEDTのFields Calculator上で
式を明示的に定義する必要があります
（詳細は [2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/](../exercise/2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/)
のREADMEを参照）。この制約は、pyaedtのテスト・サンプル全体を検索しても大きさ系の量
（`Mag_B`/`Mag_E` など）以外の直接指定の前例が見つからないことから確認された事実です
（推測ではありません）。

---

## 3. AEDT内部ポスト処理 (2): フィールドプロット（コンター図）

### 3.1 `create_fieldplot_surface()` の基本

フィールドプロットは、形状の表面やカットプレーン上に、物理量（電界・磁界・電流密度など）を
色分けしたコンター図として表示する機能です。

```python
hfss.post.create_fieldplot_surface(
    assignment="Core",              # プロット対象（オブジェクト名・面など）
    quantity="Mag_B",               # プロットする量
    setup="MySetup : LastAdaptive", # "SetupName : SetupSweep" の形式
    intrinsics={"Freq": "150kHz", "Phase": "0deg"},
    plot_name="CoreMagB",
)
```

引数の中で特に注意が必要なのが `setup` と `intrinsics` です。

- `setup`: `"SetupName : SetupSweep"` という決まった形式の文字列で指定します。周波数スイープを
  追加していない場合は `"LastAdaptive"` を使います（アダプティブメッシュの解を使うという意味）。
  Interpolatingスイープの各周波数点は、既定ではフィールドデータが保存されない（後述）ため、
  スイープ名を指定してもデータが見つからずプロットが作成されないことがあります。
- `intrinsics`: 周波数・時間・位相など、解析タイプに応じて必要な「どの瞬間の値を見るか」を
  指定する辞書です。Setupで設定した値と一致させる必要があります（例えばEddyCurrentソルバーで
  `150kHz` で解析したなら、`intrinsics={"Freq": "150kHz", ...}` のように合わせる）。

このプロジェクトでは、対象の種類に応じて使うメソッドを使い分けています。

| 対象 | メソッド |
|---|---|
| オブジェクトの表面 | `create_fieldplot_surface()` |
| 平面で切った断面（カットプレーン） | `create_fieldplot_cutplane()`（シート形状ではなく `modeler.create_plane()` で作ったPlaneオブジェクトを渡す） |
| ライン（折れ線）に沿った分布 | `create_fieldplot_line()` |

### 3.2 「Save Fields」とスイープタイプの関係（落とし穴）

フィールドプロットを作ろうとして「データが見つからない」となる典型的な原因が、
**周波数スイープの種類とフィールド保存の関係**です。

- `sweep_type="Interpolating"` のスイープは、各周波数点を個別に解かずに補間で済ませるため、
  PyAEDTの実装上、`SaveFields` が常に `False` に強制されます。
- フィールドデータ（や、周波数ごとに取得したいマトリクス値など）を後から使いたい場合は、
  `sweep_type="Discrete"` と `save_fields=True` を明示的に指定する必要があります。

この問題は、Q3D Extractorのブスバー演習（`exercise/2.hard/q3d/ex01_busbar_matrixreport/`）を
実際にAEDTで実行した際に見つかった、実例に基づく注意点です。

---

## 4. Python側ポスト処理 (1): `SolutionData` でデータを取得する

### 4.1 `get_solution_data()` の基本

AEDT内部のレポートと違い、解析結果の数値そのものをPython側（numpy配列）として取得したい場合は
`post.get_solution_data()` を使います。戻り値は `SolutionData` というクラスのインスタンスです。

```python
solution = hfss.post.get_solution_data(
    expressions="dB(S(1,1))",
    setup_sweep_name=hfss.nominal_sweep,
    report_category="Modal Solution Data",
)
freq, s11_db = solution.get_expression_data(expression="dB(S(1,1))", formula="real")
```

主な引数は `create_report()` とほぼ共通しています（`expressions`、`setup_sweep_name`、
`report_category`、`context` など）。レポートを画面に作らずに、裏側で同じ種類のデータを
Pythonに持ってくる、というイメージです。

### 4.2 `get_expression_data()` の `formula` オプション

取得したデータから、実数部・虚数部・大きさ・dB値などを取り出すには `formula` 引数を使います。

| `formula` の値 | 意味 |
|---|---|
| `"real"`（既定） | 実部 |
| `"imag"` | 虚部 |
| `"mag"` / `"magnitude"` | 大きさ（絶対値） |
| `"db10"` | $10\log_{10}$ でdB変換 |
| `"db20"` | $20\log_{10}$ でdB変換（Sパラメータなど比率量向け） |
| `"phase"` / `"phaserad"` | 位相（度／ラジアン） |

使い分けの目安は、「Sパラメータのような比率量は `db20`」「損失・インダクタンス・容量のような
スカラー量は `real` または `mag`（複素数表現になり得る場合は `mag` の方が安全）」
「周波数応答そのものの実測値比較は `real`」です。

---

## 5. Python側ポスト処理 (2): PyVistaでの可視化

PyVistaを使った可視化には、目的が異なる2つの方法があります。混同しやすいので整理しておきます。

| メソッド | 何を描画するか |
|---|---|
| `app.plot()`（例: `hfss.plot()`、`q3d.plot()`） | **ジオメトリそのもの**（形状・色・配置）をPyVistaで描画する。解析結果は関係ない |
| `post.plot_field_from_fieldplot()` | AEDT内部に**既に作成済みのフィールドプロット**を、PyVistaで読み込んで画像化・インタラクティブ表示する |

```python
# (a) ジオメトリの確認用（解析前でも使える）
hfss.plot(show=False, output_file="model.png", plot_air_objects=False)

# (b) 解析結果（フィールドプロット）の可視化。事前に create_fieldplot_surface() 等で
#     plot_name="CoreMagB" のフィールドプロットを作成済みであることが前提
hfss.post.plot_field_from_fieldplot(
    plot_name="CoreMagB",
    project_path="results",
    image_format="png",
    view="isometric",
    show=False,
)
```

両方のメソッドに共通するパターンとして、**`show=False`＋`output_file`/`project_path`で画像保存、
`show=True`でインタラクティブウィンドウ表示**という2段階の呼び出しを使います。1回目で
非対話的に画像をファイルに残し、2回目でマウス操作可能なウィンドウを開く、という使い分けです
（このプロジェクトのすべてのexpert演習で、この2段階呼び出しパターンを採用しています）。

---

## 6. Python側ポスト処理 (3): CSV入出力とmatplotlib

expertの演習では、次のような一連の流れが繰り返し使われます。

1. **入力側**: `conditions.csv`（1行、複数列の条件）を `csv.DictReader` で読み込み、
   モデルのパラメータ（寸法・周波数など）に反映する。
2. **データ取得**: `get_solution_data()` → `get_expression_data()` で、必要な値をNumPy配列として取り出す。
3. **出力側**: 取得した値を `csv.writer` で `results_*.csv` に書き出す（`zip()` で複数の配列を
   まとめて1行ずつ書く、というパターンが共通）。
4. **可視化**: matplotlibで周波数特性やパラメータ依存性をグラフ化し、画像ファイルに保存する
   （`matplotlib.use("Agg")` を先に呼んでおくと、GUIバックエンドを使わず画像保存に専念できる）。

この「CSV読み込み→モデル反映→解析→データ取得→CSV書き出し→グラフ化」という流れそのものが、
expert演習に共通する型です。個別の演習ごとに違うのは、どんな物理量を対象にするかだけです。

---

## 7. まとめ：難易度別の実装チェックリスト

新しい演習（または自分のスクリプト）で「このポスト処理はどの段階まで実装すればよいか」を
判断するときのチェックリストです。

- **normal**: ここまでは何も実装しない（モデル作成・Setup作成・`analyze()`で終了）。
- **hard**: 次のどちらか（または両方）を実装する。
  - `post.create_report()` で、Sパラメータ・損失・インダクタンスなどのレポートを作る。
  - `post.create_fieldplot_surface()`（または`cutplane`/`line`）で、フィールドプロットを作る。
  - フィールドプロットを作る場合は、周波数スイープが `sweep_type="Discrete"`＋`save_fields=True`に
    なっているか確認する（§3.2）。
- **expert**: 次をすべて実装する。
  - `conditions.csv` からパラメータを読み込み、モデルに反映する。
  - `get_solution_data()`＋`get_expression_data()` で、Python側に数値を取得する。
  - 取得した数値を `results_*.csv` に出力する。
  - matplotlibでグラフ化し、画像保存する。
  - フィールドプロットを扱う演習では、`post.plot_field_from_fieldplot()` で画像出力＋インタラクティブ
    表示（`show=False`→`show=True`の2段階）を行う。フィールドプロットがない演習（Q3Dのブスバー等）では、
    `app.plot()` でモデル形状、またはフィールドプロット作成後に同様の2段階表示を行う。

---

## 次に読むもの

- 個別の演習に戻って、ここで整理した概念が実際のコードでどう現れるか確認してみてください
  （[exercise/README.md](../exercise/README.md)）。
- PyAEDTの基本構造（`modeler`/`materials`/`boundaries`/`post` の内部クラス階層）を
  振り返りたい場合は [13_pyaedt_architecture.md](13_pyaedt_architecture.md) を参照してください。
