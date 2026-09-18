# PyAEDT 導入講義ノート（発表者用台本）

対象時間: 45分。`README.md` の時間配分に沿って進める。各節の冒頭に目安時間を記載する。

---

## 1. イントロダクション（5分）

### PyAEDTとは何か

- **PyAEDT**（`ansys.aedt.core`）は、Ansys Electronics Desktop（AEDT）を Python から自動操作するための
  公式ライブラリ。HFSS・Maxwell・Icepak・Q3D Extractor・Circuit など、AEDTに含まれるほぼ全てのアプリケーションを
  同じ流儀（Pythonのクラス・メソッド呼び出し）で操作できる。
- レイアウト・ECAD領域は **PyEDB**（`pyedb`）という別パッケージが担当する（HFSS 3D Layout・EDBで利用）。
  今回はPyAEDTを中心に扱う。

### なぜPyAEDTを使うか

- GUIでの手作業を自動化し、**再現性**（同じ手順を何度でも同じ結果で実行できる）を確保する。
- 変数を使ったパラメトリックスタディ（形状・材料・境界条件を変えて繰り返し解析）が容易になる。
- Pythonの通常のエコシステム（numpy, pandas, matplotlib など）と組み合わせて後処理ができる。
- AEDT内蔵のスクリプト機能（IronPython/VBScriptベース）と違い、**素のPython**（CPython）で書けるため、
  外部ライブラリ・IDE・デバッガなど通常のPython開発環境がそのまま使える。

---

## 2. PyAEDTの基本構造（15分）

### 2.1 パッケージ全体像

```python
from ansys.aedt.core import Hfss, Icepak, Maxwell3d, Q3d, Circuit
```

`ansys.aedt.core` 直下に、AEDTの各アプリケーションに対応するクラスが1つずつ用意されている。
今回の課題で扱うアプリと対応クラスの一覧は `docs/app-selection.md` にまとめてある。

### 2.2 「アプリオブジェクト」を起点にすべてが決まる

いずれのクラスも、インスタンス化した時点で AEDT を起動し、指定したプロジェクト/デザインに接続する。

```python
hfss = Hfss(version="2026.1", new_desktop=True, non_graphical=False)
```

- `version`: 使用する AEDT のバージョン文字列（例: `"2026.1"`）。
- `new_desktop`: `True` にすると新しいAEDTプロセスを起動する。既存セッションに繋ぐ場合は `False` にして
  `port` や `aedt_process_id` を指定する方法もある（詳しくは `docs/setup.md` を参照）。
- `non_graphical`: `True` にすると画面を出さずバックグラウンドで動く（CI向け）。講義では `False` で画面を見せる。

以後の操作はすべて、この `hfss`（アプリオブジェクト）のプロパティ・メソッドとして提供される。

### 2.3 主なサブオブジェクト

| プロパティ | 役割 |
|---|---|
| `hfss.modeler` | 形状（ジオメトリ）の作成・変更 |
| `hfss.materials` | 物性（材料）の作成・変更 |
| `hfss.boundaries` | 境界条件・励振の一覧・追加 |
| `hfss.mesh` | メッシュ設定 |
| `hfss.setups` / `hfss.create_setup(...)` | 解析Setup（周波数・収束条件など）の作成 |
| `hfss.post` | 結果のポスト処理（レポート作成、フィールドプロットなど） |
| `hfss.odesktop` / `hfss.oproject` / `hfss.odesign` / `hfss.oeditor` | AEDTのネイティブAPI（COMオブジェクト）への直接アクセス（§4で使う） |

どのアプリクラス（Hfss / Icepak / Maxwell3d など）でも、この構造はほぼ共通している
（アプリ固有の機能は個別のメソッドとして追加されている）。

### 2.4 APIの調べ方（推測しない）

- Python標準の `dir(obj)` や `help(obj.method)` でその場で確認できる。
- 公式ドキュメント: https://aedt.docs.pyansys.com/
- 引数名・戻り値まで正確に知りたい場合は、ローカルのソース（`ansys.aedt.core` パッケージ本体）を
  直接読むのが最も確実（このプロジェクトの課題作成でも同じ方針を採っている）。

---

## 3. 基本操作デモ（15分）

「起動 → 何かする（箱を作る）→ 保存 → 終了」という一連の流れを、実際に動かしながら見せる。
`demo/demo1_basic_operations.py` を実行する。

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

ポイント:

- `hfss["box_size"] = "10mm"` のように角括弧で代入すると、AEDTの**設計変数**（GUIの変数欄に出てくるもの）
  として登録される。値の変更が形状に反映される。
- `create_box` の `sizes` に変数名の文字列を渡せる（数値だけでなく式・変数参照も可）。
- `release_desktop()` を必ず呼ぶ。呼ばないと AEDT プロセスが残り続け、後続のスクリプトが繋がらなくなったり
  ライセンスを掴んだままになったりする。

---

## 4. AEDT内蔵Script → PyAEDT変換（8分）

### 4.1 AEDTのスクリプト記録機能

AEDTのGUI操作は、内蔵のスクリプト記録機能でIronPython/VBScript形式のコードとして書き出せる
（Tools メニューのスクリプト関連機能）。書き出されるコードは、`oDesktop` / `oProject` / `oDesign` / `oEditor`
という名前のオブジェクトに対して、AEDTのネイティブAPI（COMベース）のメソッドを直接呼び出す形になっている。

`demo/demo2_before_native_script.py` はそのイメージを示したもの（実際に記録されるコードを簡略化した例）:

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

このコードはAEDT内でしか動かない（`oDesktop` 等が最初から用意されている前提のコード）。

### 4.2 変換方法（2つのアプローチ）

**(a) 橋渡し方式**: PyAEDTのアプリオブジェクトは `.odesktop` / `.oproject` / `.odesign` / `.oeditor` として
同じネイティブAPIオブジェクトを公開している。そのため、記録されたコードの `oEditor.CreateBox(...)` の部分を
`hfss.oeditor.CreateBox(...)` に書き換えるだけで、そのまま動かせる（`demo/demo2_after_pyaedt_conversion.py` の
前半を参照）。手早く移植したいときに有効。

**(b) 高レベルAPIへの書き直し（推奨）**: 保守性・可読性を重視するなら、§3で見た
`hfss.modeler.create_box(origin=..., sizes=..., name=..., material=...)` のようなPyAEDTの高レベルAPIに
書き直す。パラメータの意味が明確になり、他のアプリでも似た書き方が使い回せる。

新規にコードを書くときは基本的に (b) を使い、GUIで作った複雑な形状を素早く移植したいときだけ (a) を
一時的に使う、という使い分けが実務的。

---

## 5. まとめ・次のステップ（2分）

- 今日はPyAEDTの「型」（アプリオブジェクト起点の構造、基本操作の流れ、ネイティブAPIとの橋渡し）を見た。
- 次は `exercise/0.easy/` の課題で、実際に手を動かして復習する
  （`common_3d` / `common_2d` / `common_circuit` から、使いたいアプリケーションを選んで進める。
  選び方は `docs/app-selection.md` を参照）。
- 詰まったときの調べ方: `docs/app-selection.md`、公式ドキュメント（aedt.docs.pyansys.com）、
  `dir()`/`help()` によるその場での確認。
