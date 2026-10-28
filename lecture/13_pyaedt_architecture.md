# PyAEDTの基本構造 深掘りノート（自己学習）

[12_pyaedt_self_study.md](12_pyaedt_self_study.md) の「2. PyAEDTの基本構造」で触れた内容を、
さらに掘り下げて説明するノートです。`hfss.modeler` や `hfss.post` のようなサブオブジェクトが
実際には何のクラスなのか、`hfss["x"] = "10mm"` が内部でどう扱われるのか、複数デザイン・
複数プロジェクトをどう扱うのか、といった「中身」の部分を扱います。

演習を進めるだけであれば02番までの内容で十分です。このノートは、「なぜこう書くのか」を
一歩深く理解したい人、あるいはAPIドキュメントやソースコードを自分で読み進める力をつけたい人向けです。
内容はすべて `pyaedt` パッケージ本体のソースコード（`ansys.aedt.core`）を確認したうえで書いています。

---

## 1. オブジェクト階層・接続モデル

### 1.1 AEDTのネイティブな階層構造

PyAEDTのアプリオブジェクト（`hfss = Hfss(...)`）は、AEDTの内部階層のうち
「1つのデザイン」を指し示すハンドルです。AEDTの内部階層は次のようになっています。

```
Desktop（AEDTプロセスそのもの。oDesktop）
└── Project（1つの .aedt ファイルに対応。oProject）
    └── Design（1つの解析対象。oDesign）
        └── Editor（3D Modeler、Schematic Editor等。oEditor）
```

1つのDesktop（AEDTプロセス）は、複数のProjectを同時に開いておけます。1つのProjectは、
複数のDesignを持てます（例えば同じプロジェクトの中に、形状だけ少し変えた複数のHFSSデザインを
並べて比較する、といった使い方ができます）。

PyAEDTのアプリオブジェクトは、この階層の各レベルに対応するネイティブオブジェクトを、
そのままプロパティとして公開しています。

| プロパティ | 対応する階層 |
|---|---|
| `hfss.odesktop` | Desktop（AEDTプロセス全体） |
| `hfss.oproject` | 現在のProject |
| `hfss.odesign` | 現在のDesign（アプリオブジェクトが指しているデザイン） |
| `hfss.oeditor` | 現在のDesignのEditor（3D Modelerなど） |

この対応関係があるからこそ、[11_pyaedt_lecture.md](11_pyaedt_lecture.md)/
[12_pyaedt_self_study.md](12_pyaedt_self_study.md) の第4節で説明した「橋渡し方式」
（`hfss.oeditor.CreateBox(...)`）が成立します。

### 1.2 複数デザインの扱い

1つのプロジェクトに複数のデザインがある場合、どのデザインが「現在のアプリオブジェクトの対象か」を
切り替える必要があります。

```python
# 現在のプロジェクトに存在するデザイン名の一覧
hfss.design_list

# 既存デザインに切り替える（design_list に含まれる名前を指定した場合）
hfss.design_name = "HFSSDesign2"

# 存在しない名前を指定した場合は、現在のデザインの名前を変更する（切り替えではなく改名）
hfss.design_name = "MyRenamedDesign"
```

`design_name` への代入は、「代入した名前が既存デザイン名と一致するかどうか」で、
**デザインの切り替え**と**現在のデザインの改名**のどちらが起こるかが変わる、という点を
覚えておくと挙動を予測しやすくなります。

### 1.3 接続モード（起動 vs 接続、gRPC）

アプリオブジェクトのコンストラクタに渡す引数は、実際には内部で `Desktop` クラス
（`ansys.aedt.core.desktop.Desktop`）に渡されます。主な引数は次の通りです。

| 引数 | 役割 |
|---|---|
| `version` | 使用するAEDTのバージョン |
| `non_graphical` | 画面を出さずに実行するか |
| `new_desktop` | `True`: 新しいAEDTプロセスを起動する。`False`: 既存のプロセスに接続する |
| `port` | 既存プロセスに接続する際、どのポートで待ち受けているプロセスに繋ぐかを指定する（`new_desktop=False` と併用） |
| `aedt_process_id` | 既存プロセスに接続する際、OSのプロセスIDで指定する方法（`port` の代替手段） |
| `student_version` | Student版のAEDTを対象にするかどうか |
| `machine` | リモートマシン上のAEDTに接続する場合のホスト名 |

PyAEDTは内部的に、AEDTとの通信方式として**gRPC**という仕組みを使っています（古いバージョンや
特殊な環境では、COM/.NET経由の通信方式が使われることもありますが、現在の推奨・既定はgRPCです）。
この通信方式の違いは、`Hfss(...)` を呼ぶ側のコードとしては意識する必要はほとんどありません
（`version` や `new_desktop` を正しく指定していれば、内部で自動的に適切な方式が選ばれます）。

実務上重要なのは、「新規に起動するか、既存のプロセスに接続するか」という選択です。
同じAEDTプロセスに対して複数のスクリプトやデバッグセッションから接続したい場合（例えば、
1つのスクリプトでモデルを作り、別のインタラクティブなコンソールから結果を確認したい場合）は、
`new_desktop=False` と `port`（または `aedt_process_id`）を使って同じプロセスに接続します。

---

## 2. 変数システムの詳細

### 2.1 設計変数とプロジェクト変数の違い

[12_pyaedt_self_study.md](12_pyaedt_self_study.md) で見た `hfss["box_size"] = "10mm"` という書き方には、
実は2種類の変数スコープがあります。

| 書き方 | スコープ | GUI上の呼び方 |
|---|---|---|
| `hfss["length"] = "10mm"` | **デザイン変数**（そのデザインだけで有効） | Design Properties |
| `hfss["$length"] = "10mm"`（名前の先頭に `$` を付ける） | **プロジェクト変数**（同じプロジェクト内の全デザインで共有） | Project Variables |

名前の先頭に `$` が付いているかどうかで、PyAEDTはデザイン変数とプロジェクト変数を区別します。
1つのプロジェクトの中に複数のデザインを作り、それらに共通の寸法を持たせたい場合は、
プロジェクト変数（`$`付き）を使うと、1箇所の変更が全デザインに反映されます。通常の演習のように
1プロジェクトに1デザインしかない場合は、デザイン変数（`$`なし）で十分です。

### 2.2 独立変数と従属変数

変数には、もう1つの軸として「独立変数」と「従属変数」という区別があります。

- **独立変数**: `"10mm"` のように、具体的な数値（単位付き）を直接持つ変数。
- **従属変数**: `"2*length"` のように、他の変数を参照する式を持つ変数。

```python
hfss["length"] = "10mm"        # 独立変数
hfss["double_length"] = "2*length"  # 従属変数（lengthを参照）
```

PyAEDTの `variable_manager`（`hfss.variable_manager` でアクセスできる）は、この2種類を
内部的に分けて管理しています（`independent_variables` / `independent_project_variables` /
`independent_design_variables` といったプロパティで一覧を取得できます）。この区別が実務上
重要になるのは、パラメトリックスタディ（複数の値を振って再解析する）のときです。
従属変数は他の変数の値から自動的に決まるため、それ自体をスイープの対象にはできません
（スイープできるのは独立変数だけです）。

### 2.3 `set_variable()` の詳細オプション

`hfss["x"] = "10mm"` という角括弧の書き方は、内部では
`hfss.variable_manager.set_variable(...)` が呼ばれているだけの簡略記法です。
直接 `set_variable()` を呼ぶと、角括弧だけでは指定できない細かいオプションを追加できます。

```python
hfss.variable_manager.set_variable(
    name="p2",
    expression="10mm",
    read_only=True,      # GUI上で値を変更できないようにする
    hidden=True,         # GUIの変数一覧に表示しない
    description="この変数の説明文（Propertiesパネルに表示される）",
)
```

角括弧の書き方で十分な場面がほとんどですが、「この変数はスクリプト内部の都合で作ったもので、
利用者が誤って変更してほしくない」というような場合に `read_only=True` が使えることを
覚えておくとよいでしょう。

---

## 3. 各サブオブジェクトの内部構造

[12_pyaedt_self_study.md](12_pyaedt_self_study.md) の2.3節で、「`modeler` / `materials` /
`boundaries` / `create_setup` / `post` という共通構造はどのアプリでもほぼ共通している」と
説明しました。ここでは、それぞれの裏側にある実際のクラスを見て、この「共通構造＋アプリ固有の拡張」が
具体的にどうクラス設計として実現されているかを確認します。

### 3.1 `modeler`: Modeler3D → Primitives3D → GeometryModeler

`hfss.modeler` の実体は `Modeler3D` というクラスのインスタンスです。このクラスは
`Primitives3D`（さらにその基底の `GeometryModeler`）を継承しています。つまり、
「2D/3D共通の基礎的なモデリング機能（`GeometryModeler`）」の上に、「3D形状のプリミティブ作成
機能（`Primitives3D`）」が乗り、さらにその上に「Modeler3Dとしての完成形」がある、という
階層的な作りになっています。

`create_box()` のような形状作成メソッドを呼ぶと、戻り値として `Object3d` という
クラスのインスタンスが返ってきます。これは単なる名前の文字列ではなく、作成した形状を表す
「ハンドル」オブジェクトです。

```python
box = hfss.modeler.create_box(origin=[0, 0, 0], sizes=[10, 10, 10], name="Box1", material="vacuum")

box.name           # "Box1"
box.faces          # この形状の面（Face）オブジェクトの一覧
box.material_name  # "vacuum"
box.color = (255, 0, 0)  # 色を変更する（GUIの表示色が変わる）
box.delete()        # この形状を削除する
```

`Object3d` が「名前の文字列」ではなく「ハンドルオブジェクト」であることを理解していると、
このプロジェクトの演習コードで頻出する `winding1[0].name`（TEAM7演習等）や
`plate.name`（コイル・コア演習等）のような書き方が、なぜ `.name` を付けないといけないのかが
分かりやすくなります。多くのAPI（`assign_current()` の `assignment` 引数など）は、
`Object3d` インスタンスをそのまま渡せる場合と、名前の文字列を渡す必要がある場合の両方があるため、
迷ったら実際のソース（引数の型ヒント・docstring）を確認するのが確実です。

### 3.2 `materials`: Material クラス

`hfss.materials.add_material("my_material")` は `Material` というクラス（`CommonMaterial` を
継承）のインスタンスを返します。このオブジェクトのプロパティに値を代入することで、
導電率・透磁率・誘電率などの物性を設定できます。

```python
mat = hfss.materials.add_material("core_steel")
mat.conductivity = 2000000
mat.permeability.value = 1000
```

このプロジェクトの演習（例えばMaxwell 3Dのコイル・コア電磁石シリーズ）で、材料作成のたびに
同じようなパターンのコードが出てくるのは、この `Material` オブジェクトのプロパティ代入という
統一されたインターフェースがあるためです。

### 3.3 `boundaries`: BoundaryObject クラス

`assign_current()` や `wave_port()`、Q3Dの `source()`/`sink()` のような境界条件・励振の
割り当てメソッドは、いずれも `BoundaryObject` というクラスのインスタンスを返します。
`hfss.boundaries` は、現在のデザインに割り当てられている `BoundaryObject` の一覧です。

```python
current_source = hfss.assign_current(assignment="Face1", amplitude="1A")
print(current_source.name)  # 割り当てられた境界条件の名前

for b in hfss.boundaries:
    print(b.name, b.type)
```

「ポート」「電流源」「完全導体境界」「コイルターミナル」など、物理的な意味はアプリ・解析対象ごとに
まったく違いますが、PyAEDT上での**扱い方の形**（戻り値が `BoundaryObject`、`.name` でアクセスできる、
`hfss.boundaries` で一覧できる）は共通しています。

#### アプリ別の代表的な境界条件

「境界条件を割り当てるメソッドの名前・引数はアプリごとにまったく異なる」という点を、
このプロジェクトの演習で実際に使っているものに絞って一覧にしておきます。いずれも戻り値は
`BoundaryObject`（または、Q3Dの縮退行列のように専用クラス）です。

| アプリ | 代表的な境界条件 | メソッド例 | 使用演習 |
|---|---|---|---|
| HFSS | Wave Port（導波管・伝送線路の入出力） | `hfss.wave_port(assignment=sheet.name, name="Port1")` | `1.normal/hfss/ex02_iris_filter/`、`ex03_microstrip_line/` |
| HFSS | 輻射境界（Airbox表面） | `hfss.assign_radiation_boundary_to_faces(assignment=face_ids)` / `assign_radiation_boundary_to_objects(regiｖon)` | `1.normal/hfss/ex01_dipole_antenna/` 他 |
| HFSS | 有限導電率（2Dシートを導体として扱う） | `hfss.assign_finite_conductivity(assignment=sheet.name, material="copper")` | `1.normal/hfss/ex03_microstrip_line/` |
| HFSS | プローブ給電ポート | `patch.create_probe_port(ground, rel_x_offset=0.485)` | `1.normal/hfss/ex04_patch_antenna/` |
| Maxwell 3D | 電流励振（ソリッド断面への通電） | `m3d.assign_current(assignment=face_name, amplitude="1000A")` | `1.normal/maxwell_3d/ex01_choke/`、`ex02_asymmetric_conductor/` |
| Maxwell 3D | コイル励振（巻線） | `assign_coil()` → `assign_winding()` → `add_winding_coils()` | `1.normal/maxwell_3d/ex03_coil_core/` |
| Maxwell 3D | 渦電流・変位電流の有無 | `m3d.eddy_effects_on(assignment=[...], enable_eddy_effects=False)` | `1.normal/maxwell_3d/ex02_asymmetric_conductor/` |
| Maxwell 3D | インダクタンス計算用の縮退（Matrix） | `assign_matrix()`（`MatrixMagnetostatic`/`SourceMagnetostatic` と併用） | `2.hard/maxwell_3d/ex03_coil_core_fieldplot/` |
| Icepak | 熱源（総発熱量） | `ipk.assign_source(assignment=face, thermal_condition="Total Power", assignment_value="20W")` | `1.normal/icepak/ex01_heatsink/` |
| Icepak | 圧力開口（流体の出入口） | `ipk.assign_pressure_free_opening(assignment=face_id, no_reverse_flow=True)` | `1.normal/icepak/ex01_heatsink/` |
| Icepak | 固定温度壁 | `ipk.assign_stationary_wall(geometry=face_ids, boundary_condition="Temperature", temperature="AmbientTemp")` | `1.normal/icepak/ex01_heatsink/` |
| Q3D Extractor | ソース／シンク（電流の入出力端子） | `q3d.source(assignment=obj, direction=q3d.axis_directions.XPos, name="Source1")` / `q3d.sink(...)` | `1.normal/q3d/ex01_busbar/` |
| Q3D Extractor | 縮退行列（複数導体の直列・並列結合） | `q3d.insert_reduced_matrix(operation_name="JoinSeries", assignment=[...])` | `2.hard/q3d/ex01_busbar_matrixreport/` |

この表からも分かる通り、**境界条件は物理分野ごとに全く別の概念**（電磁界の「ポート」、熱流体の
「開口」、Q3Dの「ソース/シンク」）ですが、PyAEDT上では「`assign_*()` または似た名前のメソッドを呼ぶ→
`BoundaryObject`（または類する専用オブジェクト）が返る→`hfss.boundaries` 的なプロパティで一覧できる」
という共通の「形」に収まっています。新しいアプリで知らない境界条件に出会ったときも、
「`assign_` や `insert_` で始まるメソッド名を `dir()` で探す」という調べ方（§2.4）がそのまま使えます。

### 3.4 `create_setup()`: Setupクラスの系統

`create_setup()` の戻り値は、ベースとなる `Setup`（`CommonSetup` を継承）クラスそのものではなく、
呼び出したアプリに応じた専用のサブクラスになります。例えば、HFSSなら `SetupHFSS`、
Q3D Extractorなら `SetupQ3D` が返ります。

この違いが実際に表れる例として、このプロジェクトのQ3D Extractorの演習
（`exercise/1.normal/q3d/ex01_busbar/`）で使った `create_linear_step_sweep()` は、
`SetupQ3D` だけが持つ専用メソッドです。HFSSの `SetupHFSS` には同じ役割のメソッドとして
`create_frequency_sweep()` や `create_linear_count_sweep()` が用意されています
（メソッド名が微妙に異なる点に注意）。「共通構造＋アプリ固有の拡張」という考え方は、
Setupオブジェクトのクラス階層にもそのまま表れています。

#### `props`: Setupの詳細設定を辞書として扱う

`Setup`（および各サブクラス）は、`.props` という辞書的なプロパティを持っています。これは
AEDTのネイティブなSetupプロパティ（GUIの「Edit Setup」ダイアログで設定する項目）を、
そのままPython側の辞書のキーとして読み書きできるようにしたものです。

```python
setup = m3d.create_setup(name="MySetup")
setup.props["MaximumPasses"] = 6
setup.props["MinimumPasses"] = 2
setup.props["PercentError"] = 1
setup.update()  # 辞書への代入をAEDT側に反映する
```

`.props[キー] = 値` で代入した内容は、必ず `.update()` を呼ぶまでAEDT側に反映されません
（代入自体はPythonオブジェクト内部の辞書を書き換えるだけで、AEDTとの通信は `update()` が担当する）。

アプリによって、Setup作成時にこの `props` 辞書をどう扱うかに違いがあります。

| アプリ | 代表的なパターン | 例 | 使用演習 |
|---|---|---|---|
| Maxwell 3D | `create_setup()` で素のSetupを作り、`.props[...]` に事後代入してから `.update()` | `setup = m3d.create_setup(name="MySetup")`<br>`setup.props["Frequency"] = "150kHz"` | `1.normal/maxwell_3d/ex01_choke/` |
| Icepak | 同上。GUIのプロパティ名（`"Flow Regime"` など）をそのままキーにする | `setup.props["Flow Regime"] = "Laminar"`<br>`setup.props["Include Temperature"] = True` | `1.normal/icepak/ex01_heatsink/` |
| Q3D Extractor | `create_setup()` の `props` **引数**に辞書をまとめて渡す（事後代入ではなく作成時に一括指定） | `q3d.create_setup(name="MySetup", props={"AdaptiveFreq": "1000MHz"})` | `1.normal/q3d/ex01_busbar/` |
| HFSS | `create_setup()` の `**kwargs` にプロパティ名をそのままキーワード引数として渡す（`props`辞書は経由しない） | `hfss.create_setup(name="Setup1", Frequency="10GHz", MaxDeltaS=0.02, MaximumPasses=6)` | `1.normal/hfss/ex03_microstrip_line/` |

HFSSだけ毛色が違って見えますが、これは設計方針の違いというより、**このプロジェクトでの実際の
動作検証の結果**です。当初はHFSSでも「`create_setup()` で空のSetupを作ってから `.props[...]` に
事後代入する」パターンを使っていましたが、AEDTでの実行検証で挙動が不安定になることが分かったため、
「`create_setup()` の引数としてプロパティ名をキーワード引数でまとめて渡す」方式に修正した経緯があります
（`memo/work-log.md` のPhase B検証記録を参照）。Maxwell 3D・Icepak・Q3Dの演習では事後代入パターンで
問題が起きていないため、そのまま使っています。「APIの挙動は推測せず、実際にAEDTで動かして確認する」
という、このプロジェクト全体の方針（§2.4）がSetup周りでも実例として表れている形です。

#### Sweep: 周波数スイープの追加方法もアプリ別にばらばら

Setupを作成したあと、「どの周波数点を解くか」を追加指定するのが周波数スイープです。
`props` 以上にアプリ間の差が大きく、**同じHFSSの中でさえ3通りのやり方**があります。

| アプリ | 呼び出し方 | 代表例 | 使用演習 |
|---|---|---|---|
| HFSS (1) | `setup`オブジェクトのメソッド | `setup.add_sweep(name="Sweep1", sweep_type="Interpolating", RangeStart="1GHz", RangeEnd="2GHz")` | `1.normal/hfss/ex01_dipole_antenna/` |
| HFSS (2) | `setup`オブジェクトの別メソッド（引数名が(1)と異なる） | `setup.create_frequency_sweep(unit="GHz", name="Sweep1", start_frequency=8, stop_frequency=12, sweep_type="Interpolating")` | `2.hard/hfss/ex04_patch_antenna_farfield/` |
| HFSS (3) | `hfss`（アプリオブジェクト）側のメソッド（`setup`引数で対象を名前指定） | `hfss.create_linear_count_sweep(setup="Setup1", unit="GHz", start_frequency=0.1, stop_frequency=10, num_of_freq_points=201, sweep_type="Interpolating")` | `1.normal/hfss/ex03_microstrip_line/` |
| Maxwell 3D | `setup`オブジェクトの専用メソッド。通常の周波数掃引ではなく、EddyCurrentソルバーに**追加の単一周波数の解析点**を加える用途 | `setup.add_eddy_current_sweep(sweep_type="SinglePoints", start_frequency=50, units="Hz", clear=True)` | `2.hard/maxwell_3d/ex02_asymmetric_conductor_bzreport/` |
| Q3D Extractor | `setup`オブジェクトの専用メソッド。開始・終了・ステップ幅を直接指定する | `setup.create_linear_step_sweep(name="my_sweep", unit="GHz", start_frequency=0, stop_frequency=10, step_size=1, sweep_type="Discrete", save_fields=True)` | `1.normal/q3d/ex01_busbar/` |

HFSSに3通りもあるのは、PyAEDTの歴史的な経緯でAPIが複数追加されてきたためで、どれも最終的には
同じAEDTのスイープ機能を呼び出しています。実務上は「`setup.add_sweep()` を基本形として覚えておき、
演習や公式サンプルで別の書き方（`create_frequency_sweep()`・`create_linear_count_sweep()`）に
出会ったら、そういうものだと割り切って読む」くらいの付き合い方で十分です。

Maxwell 3DとQ3Dで名前は似ていても中身が違う点にも注意してください。Maxwell 3Dの
`add_eddy_current_sweep()` は「Sパラメータのような連続した周波数特性を得る」ものではなく、
「もともと1点の周波数で解いているEddyCurrentソルバーに、もう1点だけ追加で解かせる」ための
メソッドです（[14_post_processing.md](14_post_processing.md) で触れたTEAM7演習の50Hz追加が実例）。
一方Q3Dの `create_linear_step_sweep()` は、HFSSの周波数スイープと同じ「連続した周波数範囲を
解く」ためのものです。ただしQ3Dでは `sweep_type="Interpolating"` を指定すると内部的に
`SaveFields` が常に`False`に強制される、という実装上の制約があり（
[14_post_processing.md](14_post_processing.md) §3.2 参照）、hard/expertでマトリクスデータを
周波数ごとに取得したい場合は `sweep_type="Discrete"` を使う必要があります。

#### Sweepオブジェクトも `.props` 辞書を持つ

ここまで見た `add_sweep()` / `create_frequency_sweep()` / `create_linear_step_sweep()` などの
戻り値（`SweepHFSS`、`SweepMatrix`（Q3D用）など）は、実は内部で**Setupと同じ `.props` 辞書**を
持っています。つまり、Sweep作成時の引数で指定した `RangeStart`・`RangeEnd`・`SaveFields` などの
設定項目は、作成後も `.props[キー]` で直接読み書きできます。

```python
sweep = setup.add_sweep(name="Sweep1", sweep_type="Interpolating", RangeStart="1GHz", RangeEnd="2GHz")

sweep.props["RangeEnd"]       # "2GHz"（今設定されている値を読む）
sweep.props["RangeEnd"] = "3GHz"  # 値を書き換える
sweep.update()                 # Setupの.propsと同様、update()を呼ぶまでAEDT側には反映されない
```

挙動はSetupの `.props` とまったく同じ考え方です。コンストラクタ（`add_sweep()` 等）の引数は
「作成時にまとめて指定するための入り口」にすぎず、実体は中の `.props` 辞書であり、
作成後に読み直したり書き換えたりできる、という点を知っておくと、「作成時に渡し忘れた設定を
あとから追加したい」という場面で `add_sweep()` をもう一度呼び直す必要がないことが分かります
（`sweep.props[...]` に追記して `sweep.update()` すればよい）。

### 3.5 解析実行: `analyze()` の呼び出し方

モデルとSetupを作ったあとは、解析を実行します。こちらはこのプロジェクトの全演習で一貫して
使っている `setup.analyze()`（Setupオブジェクト経由の呼び出し）を指しますが、実はアプリオブジェクト自身にも
同じ役割のメソッドがあり、呼び出し方が2通りあります。

```python
# (a) Setupオブジェクト経由（このプロジェクトの全演習で使っている書き方）
setup = m3d.create_setup(name="MySetup")
setup.analyze()

# (b) アプリオブジェクト経由（setup引数で名前を指定。省略すると全Setupを解く）
m3d.analyze(setup="MySetup")
```

ソースを確認すると、`setup.analyze()` は内部で `self._app.analyze(setup=self.name, ...)` を呼んでいるだけ
（= 最終的には全て(b)に合流する）ことが分かります。さらに、歴史的な経緯で `analyze_setup(name=...)` という
ほぼ同じ引数構成の別メソッドもアプリオブジェクトに存在します（`app.analyze_setup(name="MySetup")`）。
どれを使っても結果は同じですが、このプロジェクトの演習では一貫して (a) の `setup.analyze()` を使っています
（「このSetupを解く」という意図がコード上に正確に表れるため）。

主な引数はどちらの呼び出し方でも共通です。

| 引数 | 役割 |
|---|---|
| `cores` / `tasks` / `gpus` | 解析に使う計算リソースの指定（HPC環境向け。指定しなければAEDTの既定設定を使う） |
| `blocking` | `True`（既定）なら、解析が完了するまでスクリプトの実行が止まる（このプロジェクトの演習はすべてこの方式）。
`False` にすると解析をバックグラウンドで走らせたまま次の行に進む（AEDT 2023 R2以降で有効） |
| `revert_to_initial_mesh` | 解析前に初期メッシュに戻すかどうか |

`setup.analyze()` の実際の実装（`modules/solve_setup.py`）を確認すると、`setup=None` を渡した
場合のアプリ側 `analyze()` は「全てのSetupを解く」動作になります。複数のSetupを作った後で、
特定のSetupだけを解きたい場合は、必ず `setup.analyze()`（または `app.analyze(setup="名前")`）のように
対象Setupを明示する必要があります。

### 3.6 `post`: PostProcessorクラスの系統

`hfss.post` は、HFSSなら `PostProcessorHFSS`、Maxwell 3Dなら `PostProcessorMaxwell`、
Icepakなら `PostProcessorIcepak` というクラスのインスタンスです。これらはすべて
共通の基底クラス `PostProcessor3D`（さらにその基底の `PostProcessorCommon`）を継承しています。

```
PostProcessorCommon（最も基礎的な共通機能）
└── PostProcessor3D（3Dソルバー共通の機能: create_fieldplot_surface() 等）
    ├── PostProcessorHFSS（HFSS固有の追加機能）
    ├── PostProcessorMaxwell（Maxwell固有の追加機能）
    └── PostProcessorIcepak（Icepak固有の追加機能）
```

このプロジェクトの演習で、HFSSでもMaxwell 3Dでも同じように `post.create_report()` や
`post.get_solution_data()` が使えるのは、これらが共通の基底クラス（`PostProcessorCommon`）に
定義されているためです。一方で、Maxwell 3D特有のフィールドプロット関連の機能（例えば
`post.create_fieldplot_line_traces()`）は `PostProcessorMaxwell` にしか存在しません。

`post.get_solution_data()` の戻り値は `SolutionData` というクラスのインスタンスです。
このプロジェクトの `3.expert/` の演習で繰り返し使っている `get_expression_data(expression=...,
formula=...)` は、この `SolutionData` クラスのメソッドです。

### 3.7 この節のまとめ

サブオブジェクトの呼び出し一つひとつが、実は「共通の基底クラス」と「アプリ固有のサブクラス」の
組み合わせでできている、ということを確認しました。新しいアプリ（例えばこれから触るIcepakや
Maxwell 2D）に取り組むときも、「基本的な使い方はこれまでと同じ基底クラスの機能だろう」
「見慣れないメソッドがあれば、それはそのアプリ固有のサブクラスの機能だろう」という当たりを
付けられるようになると、ドキュメントやソースコードを探す効率が上がります。

---

## 次に読むもの

- 演習を再開する場合は [exercise/README.md](../exercise/README.md) に戻ってください。
- ポスト処理の全体像（Report / Field Plot / PyVista / CSV・matplotlibの使い分け）を
  さらに深掘りしたい場合は、別のノートを参照してください（作成されていれば `lecture/` 配下に
  追加されます）。
