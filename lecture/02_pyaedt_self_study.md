# PyAEDT 導入講義 自己学習版

[01_pyaedt_lecture.md](01_pyaedt_lecture.md)（発表者用の講義台本）と同じ5節構成・同じ内容を、
**講義に参加できなかった人、あるいは講義の内容を後から自分のペースで読み返したい人**向けに
書き直したものです。発表者の語りかけや「ここで画面を見せる」といった進行上の指示は取り除き、
文章だけで完結するように説明を補っています。

手元でAEDTとPyAEDTが使える環境（[00_environment_setup.md](00_environment_setup.md)参照）があれば、
コード例は実際に実行しながら読み進めることをお勧めします。`demo/` フォルダに、
このノートに出てくるコード例がそのまま実行できる形で置いてあります。

より詳しい・口語的な説明が欲しい場合は、発表者向けの詳細版
[docs/lecture-script-detail.md](../docs/lecture-script-detail.md) も参考になります
（内容はこのノートとほぼ同じですが、具体例や補足がさらに多く書かれています）。

---

## 1. イントロダクション

### PyAEDTとは何か

PyAEDTは、`ansys.aedt.core` という名前でインストールされる、Ansysの公式Pythonライブラリです。
AEDT（Ansys Electronics Desktop）は単一のソフトウェアではなく、HFSS（高周波電磁界解析）、
Maxwell（低周波電磁界解析）、Icepak（熱流体解析）、Q3D Extractor（寄生成分抽出）、
Circuit（回路シミュレーション）など、物理現象ごとに異なる解析エンジン（ソルバー）をまとめた
プラットフォームです。PyAEDTは、これらすべてのソルバーに対して同じ流儀でアクセスできるようにする
統一的なAPIを提供します。

AEDTのGUIで「モデルを作る」「材料を設定する」「境界条件を割り当てる」「メッシュを切る」
「解析を実行する」「結果を見る」という一連の作業は、すべてPyAEDTのPythonオブジェクトの
メソッド呼び出しとして表現できます。GUIで手間のかかる試行錯誤も、一度スクリプトに落とし込んで
しまえば、何度でも短時間で再現できるようになります。

もう一つ知っておきたいのは、レイアウト・基板（ECAD）の世界を扱う **PyEDB**（`pyedb`）という
別パッケージの存在です。HFSS 3D LayoutやEDB（Electronics Database）を直接操作したい場合は
PyEDBを使います。PyAEDTとPyEDBは密接に連携しますが、パッケージとしては別物です。
このノートではPyAEDT本体を中心に扱い、PyEDBには深入りしません。

### なぜPyAEDTを使うのか

1つ目の理由は**再現性**です。GUIでの操作は、同じ手順を人間が再現しようとすると、クリックの順番や
入力値の打ち間違いなど、微妙なブレが生じがちです。スクリプトに書いてしまえば、同じコードは
何度実行しても同じ結果を生みます。チームで設計レビューをするときも、「このスクリプトを実行すれば
このモデルが再現できる」という状態は非常に強力です。

2つ目は**パラメトリックスタディ**のしやすさです。「アンテナの長さを1mm刻みで10パターン試して、
それぞれの共振周波数を比較したい」というようなタスクは、GUIで10回繰り返すよりも、Pythonのfor文で
回したほうが圧倒的に速く、ミスも減ります。

3つ目は、Pythonの**通常のエコシステム**と組み合わせられる点です。解析結果をnumpyの配列として
取得し、pandasでデータフレームに整形し、matplotlibでグラフにする、といった一般的なデータ処理の
技術がそのまま使えます（`exercise/` の `3.expert/` の課題で繰り返し使うことになります）。

4つ目は、AEDTに内蔵されているスクリプト機能（IronPython・VBScriptベース）との違いです。
内蔵スクリプトはAEDTのプロセス内でしか動かない特殊な実行環境ですが、PyAEDTは普通のCPython、
つまり普段使っているのと同じPythonインタープリタで動きます。そのため、VS Codeのような普通のIDE、
pdbやdebugpyによる通常のデバッガ、pytestのようなテストフレームワーク、仮想環境（venv）による
パッケージ管理など、通常のPython開発で当たり前に使う道具立てがそのまま使えます。
この違いは第4節で詳しく扱います。

---

## 2. PyAEDTの基本構造

### 2.1 パッケージ全体像

```python
from ansys.aedt.core import Hfss, Icepak, Maxwell3d, Q3d, Circuit
```

`ansys.aedt.core` パッケージの直下に、AEDTの各アプリケーションに対応するクラスが1つずつ
用意されています。HFSSを使いたければ `Hfss` クラス、Maxwell 3Dを使いたければ `Maxwell3d` クラス、
という具合です。クラス名の綴りがアプリの表示名と微妙に違う場合がある点（例えば2D Extractorは
`Q2d`、IcepakFEAは `Mechanical`）には注意してください。対応アプリ全てのクラス名対応表は
[docs/app-selection.md](../docs/app-selection.md) に一覧化されているので、迷ったらそこを確認します。

### 2.2 「アプリオブジェクト」を起点にすべてが決まる

PyAEDTのコードは、ほぼ例外なく次のパターンで始まります。

```python
hfss = Hfss(version="2026.1", new_desktop=True, non_graphical=False)
```

この1行が実行されると、裏側ではAEDTのプロセスが起動（または既存プロセスへの接続）し、
新しいプロジェクト・デザインが作成されます。戻り値の `hfss`（「アプリオブジェクト」と呼びます）が、
以降のすべての操作の起点になります。

引数の意味は次の通りです。

- `version`: 使用するAEDTのバージョンを文字列で指定します。複数バージョンのAEDTが同じマシンに
  入っていることもあるので、明示しておくと安全です。手元の環境のバージョンは、AEDTを起動して
  「ヘルプ > バージョン情報」で確認できます（詳細は [00_environment_setup.md](00_environment_setup.md)）。
- `new_desktop`: `True` にすると、新しいAEDTプロセスを起動します。`False` にすると、
  既に起動しているAEDTセッションに接続しにいきます（`port` や `aedt_process_id` を併用して
  どのプロセスに繋ぐか指定することもできます）。何も考えずに `new_desktop=True` のスクリプトを
  繰り返し実行すると、AEDTプロセスがどんどん増えてしまう点に注意してください。
- `non_graphical`: `True` にすると画面を一切出さずバックグラウンドで動作します。CI
  （継続的インテグレーション）環境や、バッチ処理でたくさんのケースを流したいときに使います。
  最初のうちは、動作を目で確認できる `False` で進めるのがおすすめです。

この `hfss` という1つのオブジェクトが、これから説明するすべての機能の入り口になります。

### 2.3 主なサブオブジェクト

アプリオブジェクトは、役割ごとに整理されたサブオブジェクトをプロパティとして持っています。

| プロパティ | 役割 |
|---|---|
| `hfss.modeler` | 形状（ジオメトリ）の作成・変更。箱・円柱の作成、ブーリアン演算（結合・削除）など、3D/2Dモデリングはすべてここ |
| `hfss.materials` | 物性（材料）の作成・変更。既存材料を使うだけでなく、独自の導電率・透磁率を持つカスタム材料もここで作れる |
| `hfss.boundaries` | 境界条件・励振の一覧・追加。ポート、電流源、完全導体境界など物理的な境界条件の管理 |
| `hfss.mesh` | メッシュ設定。メッシュの細分化領域の指定など |
| `hfss.setups` / `hfss.create_setup(...)` | 解析Setup（周波数・収束条件など）の作成。GUIの「Analysis」ツリーに相当する |
| `hfss.post` | 結果のポスト処理。レポート作成、フィールドプロット、ソリューションデータの取得など、解析結果に関する操作はすべてここに集まる |
| `hfss.odesktop` / `hfss.oproject` / `hfss.odesign` / `hfss.oeditor` | AEDTのネイティブAPI（COMオブジェクト）への直接アクセス（第4節で詳しく扱う） |

重要なのは、「どのアプリクラス（`Hfss` / `Icepak` / `Maxwell3d` など）でも、この構造はほぼ共通している」
ということです。`modeler` で形を作り、`materials` で物性を決め、境界条件を割り当て、`create_setup` で
解析条件を作り、`post` で結果を見る。この5ステップの流れは、どのアプリでも変わりません。
アプリ固有の機能（例えばMaxwellの`assign_coil`やQ3Dの`insert_reduced_matrix`のような）は、
この共通構造の上に追加のメソッドとして乗っているだけです。この「共通構造＋アプリ固有の拡張」という
見方ができると、新しいアプリを触るときの心理的ハードルがかなり下がります。

> それぞれのサブオブジェクトが実際にはどのクラスなのか（`Object3d`, `Material`, `BoundaryObject`,
> `Setup`系, `PostProcessor`系）、複数デザイン・プロジェクト変数の扱いなど、もう一段深く知りたい場合は
> [03_pyaedt_architecture.md](03_pyaedt_architecture.md) を参照してください。

### 2.4 APIの調べ方（推測しない）

演習を進めていく中で、必ず「このメソッドの引数は何を渡せばいいんだろう」と迷う場面が出てきます。
そのときの調べ方を3段階で紹介します。

1. まず試してほしいのは、Python標準の `dir(obj)` と `help(obj.method)` です。`dir(hfss.modeler)` と
   打てば、`modeler` オブジェクトが持っているメソッド・プロパティの一覧がその場で見られます。
   `help(hfss.modeler.create_box)` と打てば、docstring（説明文）がその場で表示されます。
   対話的なPython環境（Pythonの対話シェル、Jupyter、VS Codeのデバッグコンソールなど）で
   そのまま使える方法です。
2. 次に、公式ドキュメント（https://aedt.docs.pyansys.com/）も参照できますが、情報が古かったり
   バージョン間の差異が反映しきれていなかったりすることもあります。
3. 一番確実なのは、PyAEDTパッケージ本体のソースコードを直接読むことです。`pip install` された
   場所をgrepすれば、引数名・デフォルト値・内部実装まですべて正確にわかります。

推測で書いたコードはだいたい動かないか、動いても意図と違う挙動をします。迷ったら調べる、
という姿勢を最初から持っておくと、このあとの演習がスムーズに進みます。

---

## 3. 基本操作デモ

ここでは「AEDTを起動する → 箱を1つ作る → 保存する → 終了する」という、考えうる限り最小の
一連の流れを見ていきます。地味に見えるかもしれませんが、この4ステップのパターンは、
このあとの演習、そして実務で書くどんなスクリプトでも必ず現れる「型」です。

`demo/demo1_basic_operations.py` と同じ内容です。手元の環境があれば、実際に実行してみてください。

```python
from ansys.aedt.core import Hfss

# 1. 起動（新規プロジェクトでHFSSを開く）
hfss = Hfss(version="2026.1", new_desktop=True, non_graphical=False)

# 2. 変数を定義する
hfss["box_size"] = "10mm"

# 3. 箱を作る（形状作成）
hfss.modeler.create_box(
    origin=[0, 0, 0],
    sizes=["box_size", "box_size", "box_size"],
    name="Box1",
    material="vacuum",
)

# 4. 保存する
hfss.save_project()

# 5. 終了する（AEDTプロセスとプロジェクトを閉じる）
hfss.release_desktop(close_projects=True, close_desktop=True)
```

### 各ステップの解説

**起動**（1行目〜）: 実行するとAEDTのウィンドウが開きます。ここで少し待ち時間が発生しますが、
AEDTというアプリケーション自体の起動に数秒〜数十秒かかるためで、PyAEDT固有の遅さではありません。

**変数定義**（`hfss["box_size"] = "10mm"`）: 角括弧を使ったこの書き方は、Pythonの辞書のように
見えますが、実際にはAEDTの**設計変数**（デザインプロパティ）として登録されます。GUIの
「Properties」パネルの変数一覧に、`box_size = 10mm` という項目が実際に追加されます。重要なのは、
この変数は単なるPython変数ではなく、AEDT側に実体を持つという点です。あとでGUIから値を変更すれば、
形状がリアルタイムに追従します。

**形状作成**（`create_box`）: `sizes` に `box_size` という文字列を渡している点に注目してください。
数値の `10` を直接渡すこともできますが、ここでは変数名の文字列を渡すことで、AEDT側の変数参照の
式（expression）として評価されます。これにより、あとで `box_size` の値を変えるだけで箱のサイズが
連動して変わる、パラメトリックなモデルになります。実行後、AEDTの3Dビューを確認すると箱が
生成されているのが見えるはずです。

**保存**（`save_project`）: このタイミングで `.aedt` ファイルがディスクに書き出されます。

**終了**（`release_desktop`）: このメソッドを呼ばずにスクリプトを終了させてしまうと、AEDTのプロセスが
バックグラウンドに残り続けます。残り続けると何が困るかというと、(1) 次にスクリプトを実行したときに
意図せず既存プロセスに接続してしまったり、(2) AEDTのライセンスを掴んだままになって他の利用者や
自分自身の次回起動をブロックしてしまったり、といった問題が起こります。`close_projects=True,
close_desktop=True` を付けて、プロジェクトとデスクトップの両方をきちんと閉じる習慣をつけてください。

### つまずきやすいポイント

- スクリプトを途中で止めてしまった（例外が発生した、Ctrl+Cで止めた）場合、AEDTプロセスが
  残ることがあります。`settings.release_on_exception = False`（[00_environment_setup.md](00_environment_setup.md)参照）を
  設定しておくと、例外発生時にAEDTが自動終了してしまうのを防げるので、原因調査がしやすくなります。
- `non_graphical=False` で動かしている間は、AEDTのウィンドウが実際に操作可能な状態になっています。
  うっかり手動でクリックしてしまうと、スクリプトの実行と手動操作が競合することがあるので注意してください。

---

## 4. AEDT内蔵Script → PyAEDT変換

### なぜこの節が必要か

ここまでは最初からPyAEDTで書く前提で説明してきましたが、実務ではもう1つのパターンがよく出てきます。
「まずGUIで試行錯誤して形を作り、その後で自動化したい」というパターンです。AEDTにはGUI操作を
スクリプトとして記録する機能が内蔵されており、ここではその出力とPyAEDTのコードがどう対応するかを
説明します。

### AEDTのスクリプト記録機能

AEDTのメニューから、GUI操作をIronPython（Python 2系の文法に近い、.NET上で動くPython実装）または
VBScript形式のコードとして書き出す機能が使えます。記録されたコードは、`oDesktop` / `oProject` /
`oDesign` / `oEditor` という名前の特殊なオブジェクトに対して、AEDTのネイティブAPI（内部的には
COMベースのインターフェース）のメソッドを直接呼び出す形になっています。

実際に記録される内容を簡略化した例が次のコードです（`demo/demo2_before_native_script.py` と同じ）。

```python
# AEDT内蔵スクリプト記録が出力するコードのイメージ（簡略化）
oDesktop.RestoreWindow()
oProject = oDesktop.SetActiveProject("Project1")
oDesign = oProject.SetActiveDesign("HFSSDesign1")
oEditor = oDesign.SetActiveEditor("3D Modeler")
oEditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "0mm",
        "YPosition:=", "0mm",
        "ZPosition:=", "0mm",
        "XSize:=", "10mm",
        "YSize:=", "10mm",
        "ZSize:=", "10mm",
    ],
    [
        "NAME:Attributes",
        "Name:=", "Box1",
        "Flags:=", "",
        "Color:=", "(143 175 143)",
        "Transparency:=", 0,
        "PartCoordinateSystem:=", "Global",
        "UDMId:=", "",
        "MaterialValue:=", "\"vacuum\"",
        "SurfaceMaterialValue:=", "\"\"",
        "SolveInside:=", True,
    ],
)
```

このコードには2つの特徴があります。1つ目は、引数が `"NAME:BoxParameters", [...]` のような、
AEDTのネイティブAPI特有のキーと値を交互に並べたリスト形式になっている点です。これはPythonらしい
書き方ではなく、COM APIをそのままPythonの構文に当てはめたものです。2つ目は、このコードは
`oDesktop` 等の変数が最初から用意されている前提で書かれているため、**このコードだけを別のPython
環境にコピーしても動かない**という点です。AEDTのスクリプトコンソールの中でだけ完結するコードです。

### 変換方法（2つのアプローチ）

**(a) 橋渡し方式**: PyAEDTのアプリオブジェクトは、2.3節の表で触れた `.odesktop` / `.oproject` /
`.odesign` / `.oeditor` というプロパティを通じて、まったく同じネイティブAPIオブジェクトを
公開しています。つまり、記録されたコードの `oEditor.CreateBox(...)` の部分を
`hfss.oeditor.CreateBox(...)` に書き換えるだけで、そのままPythonスクリプトとして動かせます
（`demo/demo2_after_pyaedt_conversion.py` の前半部分がこの例）。

```python
# (a) 橋渡し方式: 記録スクリプトの oEditor.CreateBox(...) を app.oeditor.CreateBox(...) に置き換えるだけ
hfss.oeditor.CreateBox(
    [
        "NAME:BoxParameters",
        "XPosition:=", "0mm",
        "YPosition:=", "0mm",
        "ZPosition:=", "0mm",
        "XSize:=", "10mm",
        "YSize:=", "10mm",
        "ZSize:=", "10mm",
    ],
    [
        "NAME:Attributes",
        "Name:=", "Box1",
        "Flags:=", "",
        "Color:=", "(143 175 143)",
        "Transparency:=", 0,
        "PartCoordinateSystem:=", "Global",
        "UDMId:=", "",
        "MaterialValue:=", "\"vacuum\"",
        "SurfaceMaterialValue:=", "\"\"",
        "SolveInside:=", True,
    ],
)
```

このアプローチの良いところは、ほぼ機械的な置き換えだけで動く速さです。GUIで作った複雑な形状
（何十個もの引数を持つような複雑なフィーチャー）を、短時間で「とにかく動くPythonスクリプト」に
したいときに向いています。欠点は、コードの意図が読み取りにくい（`"XPosition:=", "0mm"` が何を
表しているか、慣れないと分かりにくい）ことと、引数リストの構造をAEDT側の仕様に合わせて
正確に保たなければならない点です。

**(b) 高レベルAPIへの書き直し（推奨）**: 第3節で見た `hfss.modeler.create_box(origin=...,
sizes=..., name=..., material=...)` のような、PyAEDTが提供する高レベルなAPIに書き直す方法です。

```python
# (b) 高レベルAPI方式（推奨）: 同じ箱を PyAEDT の modeler API で作成
hfss.modeler.create_box(
    origin=[20, 0, 0],
    sizes=[10, 10, 10],
    name="Box2",
    material="vacuum",
)
```

見比べると一目瞭然ですが、`create_box` のほうが、引数名（`origin`, `sizes`, `name`, `material`）から
何をしているのかが明確に読み取れます。こちらのアプローチの良いところは、**保守性・可読性**です。
半年後に自分や同僚がこのコードを読んだときに、意図がすぐ分かります。また、`modeler.create_box`
という書き方は、Hfssに限らずMaxwell3dでもIcepakでも（アプリ固有の違いはあれど）同じような流儀で
使えるため、**他のアプリへの応用が効く**という利点もあります。

### 使い分けの指針

新規にコードを書くときは基本的に(b)の高レベルAPIを使ってください。(a)の橋渡し方式は、GUIで
既に作り込んだ複雑な形状を「取り急ぎ移植したい」という限定的な場面で、一時的な手段として使うのが
実務的です。このプロジェクトの演習教材も、すべて(b)の高レベルAPIで書かれています。

---

## 5. まとめ・次のステップ

### このノートのポイント

1. PyAEDTのコードは、必ず「アプリオブジェクト」（`Hfss(...)` のようなコンストラクタ呼び出しの
   戻り値）を起点に、`modeler` / `materials` / `boundaries` / `create_setup` / `post` という
   共通の構造でできている。
2. 「起動 → 何かする → 保存 → 終了」という最小の流れを確認した。特に `release_desktop()` を
   必ず呼ぶ、という運用上の注意点を押さえておく。
3. AEDTのGUI操作記録と、PyAEDTの高レベルAPIの関係・変換方法を見た。新規に書くときは
   高レベルAPIを使う、という指針を確認した。

### 次に取り組むこと

次は `exercise/0.easy/` の課題で、ここで見た内容を実際に自分の手で書いて復習しましょう。
`common_3d` / `common_2d` / `common_circuit` の3つのフォルダから、自分が使いたいアプリケーションを
選んで進めてください。どのアプリを選べばいいか迷ったら、
[docs/app-selection.md](../docs/app-selection.md)の対応表を見てください。

### 詰まったときの道しるべ

1. 各課題の`README.md`内の「ヒント」セクション。
2. [docs/app-selection.md](../docs/app-selection.md)（アプリケーションの選び方・クラス名対応表）。
3. 公式ドキュメント（https://aedt.docs.pyansys.com/）。
4. `dir(obj)` / `help(obj.method)` によるその場での確認（2.4節で説明した方法）。
