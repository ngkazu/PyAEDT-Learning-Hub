# PyAEDT 環境構築ガイド（自己学習版）

PyAEDTを使い始める前に必要な環境構築を、実際の操作手順に沿って説明します。
[11_pyaedt_lecture.md](11_pyaedt_lecture.md) / [12_pyaedt_basic.md](12_pyaedt_basic.md) で
扱うコード例を実際に動かすための準備にあたる内容です。このプロジェクトにおける環境構築の正式な
一次情報はこのノートです（`docs/`配下には環境構築専用のドキュメントは置いていません）。

## 1. 3つの選択肢

PyAEDTを動かすまでの経路は、大きく分けて次の3つから選べます。いずれも最終的には同じ
`ansys.aedt.core` パッケージに行き着きます。

| 選択肢 | 概要 | 向いている場面 | 本章の説明篇 |
|---|---|---|---|
| (a) AEDT公式インストーラー | `pyaedt_installer_from_aedt.py` が自動で専用仮想環境を作成し、AEDTのAutomationタブにConsole/Jupyter等のパネルを追加する | すぐに試したい、AEDTのGUIから離れずに作業したい | §2 |
| (b) AEDT同梱Pythonで自作 venv | AEDTに同梱されているCPythonをベースに、自分で手動で仮想環境を作る | VS Codeで開発したいが、別途Pythonは入れたくない | §3.1 |
| (c) 別途Pythonで自作 venv | 通常のPython 3.10以上を使って自分で仮想環境を作る | VS Codeで開発したい。最新版やオプション依存を柔軟に管理したい | §3.2 |

(a)は「AEDTが自動で作る仮想環境」であり、(b)/(c)は「自分で手動作る仮想環境」です。
このプロジェクト（`PyAEDT-Learning-Hub`）の演習は、どの経路でも進めますが、`starter.py`/`solution.py`を
VS Codeで編集・実行する前提なので (b) または (c) が適しています。

---

## 2. AEDT公式インストーラーでセットアップする（前述(a)）

### 2.1 インストーラースクリプトを実行する

AEDTには、PyAEDTを自動インストールするスクリプトが用意されています。手順は次の通りです
（**Tools → Run Script** で起動した直後はAEDT組み込みのIronPythonインタープリタ上で動きますが、
スクリプトはその中で自分自身を**AEDT同梱のCPythonインタープリタ**から再起動し、実際の仮想環境作成・
パッケージインストール処理はそのCPython側で行います）。

1. PyAEDTインストーラーのPythonファイル（`pyaedt_installer_from_aedt.py`）を入手する
   （PyAEDT公式ドキュメントの [Installation](https://aedt.docs.pyansys.com/version/stable/Getting_started/Installation.html)
   ページからダウンロードできる）。
2. Electronics Desktop（AEDT）を起動し、メニューの **Tools → Run Script** からこのファイルを実行する。
3. 社内ネットワークなどでインターネット接続が制限されている場合は、**wheelhouse**
   （必要なパッケージを1つのzipにまとめたもの、[PyAEDTのGitHub Releases](https://github.com/ansys/pyaedt/releases)
   から入手可能）をダウンロードし、そのzipのフルパスを引数にして同じスクリプトを実行すれば
   オフラインインストールできる。

このインストーラーを実行すると、AEDT同梱のCPython用に**専用の仮想環境**が自動的に作られ、
そこにPyAEDTとその依存パッケージがインストールされます。加えて、AEDTのGUIの
**Automationタブ**に、PyAEDTの各種パネル（後述）が追加されます。

> **AEDT 2026 R1 SP2以降の場合**: PyAEDTが最初からAEDTのインストールに同梱されるようになりました
> （ランタイムの依存パッケージのみを含む軽量版）。この場合はインストーラースクリプトを実行しなくても
> すぐにPyAEDTが使える状態になっています。最新版への更新やオプション依存の追加が必要な場合は、
> 上記のインストーラースクリプト、または次章の「自分で仮想環境を作成する」方法を使います。

### 2.2 インストールすると使えるようになるもの（Automationタブ）

インストールが終わると、AEDTのリボンに **Automation** タブが追加され、その中に次のパネルが
並びます。それぞれ、裏側では「AEDT同梱のCPython環境」が使われています。

| パネル | 役割 |
|---|---|
| **Console** | 現在開いているAEDTセッションに最初から接続された、インタラクティブなPythonコンソールを開く。Pythonコマンドを1行ずつ対話的に実行しながら、現在のデザインを操作・確認できる。PyAEDTのコードスニペットを試したり、自動化ワークフローをデバッグしたりするのに向いている |
| **CLI** | `pyaedt` コマンドラインインターフェースに、別途ターミナルを開かなくてもAEDT内から直接アクセスできる。AEDTプロセスの管理やテスト設定の確認などができる |
| **Jupyter** | 現在のAEDTセッションに接続された状態の **Jupyter Notebookサーバー**を起動する。結果をノートブック内にインラインで可視化したり、Markdownで作業記録を残しながら解析を進めたり、できあがったノートブックをチームで共有したりするのに向いている |
| **Run script** | `.py` ファイルをAEDTのGUIから直接選んで実行できる。AEDTを離れずに自動化ワークフローやバッチ処理を走らせたいときに使う |
| **Extension Manager** | PyAEDTが提供するプリインストール済みの拡張機能や、自作のカスタム拡張機能を一覧・起動・管理する |

「ConsoleやJupyterを開くと、自分で `Hfss(...)` のようにアプリオブジェクトを作らなくても、
最初から現在のAEDTセッション・デザインに接続された状態でPythonコードが書き始められる」
という点が、このインストール方法ならではの利点です（1章のレクチャーノートで説明した
`hfss = Hfss(...)` の起動処理を省略できるイメージです）。

### 2.3 CLI（コマンドプロンプト）からの操作

AEDTのAutomationタブに入っているCLIパネルと同じ機能は、`pyaedt` コマンドとして
通常のコマンドプロンプト（PowerShellやターミナル）からも使えます。

```powershell
# インストール済みのPyAEDTバージョンを確認する
pyaedt version

# マシンにインストールされているAEDTのバージョン一覧を確認する
pyaedt aedt-versions

# --help で利用可能なサブコマンド一覧を確認する
pyaedt --help
```

主なサブコマンドは次の通りです。

| サブコマンド | 役割 |
|---|---|
| `version` | インストール済みPyAEDTのバージョン表示 |
| `aedt-versions` | マシンにインストールされているAEDTバージョンの一覧表示 |
| `session` | AEDTセッションの起動・一覧・停止・接続 |
| `project` | プロジェクトの一覧・オープン・作成・保存・クローズ |
| `script` | AEDT内でPythonスクリプトを実行する |
| `export` | スクリーンショットやデザイン設定のエクスポート |
| `panels` | AEDTへのPyAEDTパネルのインストール |
| `doc` | PyAEDTドキュメント関連リソースを開く |

---

## 3. 自分で仮想環境を作成する（前述(b)/(c)）

VS Codeなど通常のIDEで開発したい場合は、自分で仮想環境を作るのが確実です。
仮想環境のベースにするPythonは、**AEDT同梱のCPython**と、**別途インストールしたPython**の
2通りから選べます。どちらでもできあがる `ansys.aedt.core` 自体は同じものです。

### 3.1 (b) AEDT同梱のPythonを使う場合

AEDTには専用のCPythonインタープリタが同梱されており、別途Pythonをインストールしなくても
仮想環境を作成できます。インストール先のバージョンフォルダ名（`v261` など）は、AEDTの
バージョンに対応します（例: `v261` = AEDT 2026 R1）。2026 R1の場合のパスは次の通りです。

```powershell
# AEDT 2026 R1 (v261) 同梱のPythonで仮想環境を作成する
& "C:\Program Files\ANSYS Inc\v261\AnsysEM\commonfiles\CPython\3_10\winx64\Release\python\python.exe" -m venv .venv

# アクティベートしてインストールする
.venv\Scripts\Activate.ps1
pip install "pyaedt[all]"
```

他のAEDTバージョンを使う場合は、パス中の `v261` の部分をそのバージョンに対応する番号
（`v251`=2025 R1、`v252`=2025 R2 など）に置き換えます。`3_10`（Python 3.10）の部分は、
 AEDT 2023 R2〜2026 R2では共通です（AEDT 2027 R1以降はPython 3.13に変わる予定）。

この方法は、§2で見た「(a) AEDT公式インストーラー」とは別物です。インストーラーが
**自動的に**専用の仮想環境を作ってAEDTのAutomationタブにパネルを追加するのに対し、
こちらは**手動で**VS Code用の仮想環境を作る方法です。

### 3.2 (c) 別途インストールしたPythonを使う場合

通常のPython 3.10以上が入っていれば、それを使って仮想環境を作成することもできます。
このプロジェクト自体も、この方法で検証用の `.venv` を作成しています。

```powershell
# プロジェクトフォルダ直下で仮想環境を作成する
python -m venv .venv

# PowerShellでアクティベートする
.venv\Scripts\Activate.ps1
pip install "pyaedt[all]"
```

実行ポリシーの制限でアクティベートできない場合は、次のように一時的に許可してから実行します。

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1
```

### 3.3 `pip install` のオプション依存（extras）

`pip install "pyaedt[all]"` の `[all]` の部分は **extras**（オプション依存のグループ名）で、
必要なものだけを選んで切り替えられます。利用可能なextrasは
[pyproject.toml](https://github.com/ansys/pyaedt/blob/main/pyproject.toml) の
`[project.optional-dependencies]` に定義されています。主なものは次の通りです。

| extras | 追加される主なパッケージ | 用途 |
|---|---|---|
| `dotnet` | `ansys-pythonnet`, `pywin32`（Windows）, `cffi`（Linux） | .NET経由のレガシーAPI（EDBのDotNetバックエンドなど）を使う場合 |
| `graphics` | `pyvista`, `matplotlib`, `vtk`, `fpdf2`, `pillow` 等 | フィールドプロット・3D可視化・PDFレポート出力など、グラフィックス機能全般 |
| `jupyter` | `jupyterlab`, `ipython` | Jupyter Notebook環境で使う場合 |
| `examples` | `imageio`, `plotly`, `joblib`, `osmnx` 等 | 公式サンプル集（Examples）を動かす場合に必要な追加パッケージ |
| `all` | `graphics`一式 + `jupyter`一式 + `pandas`, `openpyxl`, `scikit-rf`, `typer`, `rpyc` 等 | グラフィックス・Jupyter込みの標準セット（**dotnetは含まない**） |
| `all-dotnet` | `all` の全部 + `dotnet` の全部 | `all` に加えて `.NET` 経由のAPIも使いたい場合 |

このプロジェクトでは `"pyaedt[all]"` を使っています（§3.1・§3.2のコマンド参照）。これは
グラフィックス機能（PyVista・matplotlib、hard/expertの課題で使う）とJupyter関連を含みますが、
`dotnet` extrasは含んでいません。複数のextrasを同時に指定したい場合はカンマ区切りで並べます。

```powershell
# 例: グラフィックスとJupyterだけ個別に指定する場合（[all]とほぼ同じ内容になる）
pip install "pyaedt[graphics,jupyter]"

# 例: .NET経由のAPIも使いたい場合
pip install "pyaedt[all-dotnet]"
```

> `dotnet` extrasは、PyEDBが内部で使う「DotNetバックエンド」（`31_pyedb_basic.md` 参照）や、
> 一部のレガシーAPIで必要になります。通常のPyAEDT学習・このプロジェクトの演習では必須では
> ありません（PyEDBはデフォルトでもgRPCバックエンドが使えます）。迷ったら `[all]` のままで
> 問題ありません。

### 3.4 バージョンの確認

どちらの方法でインストールした場合も、インストール済みの `pyaedt` バージョンは次のように
確認できます。

```powershell
py -3 -c "import ansys.aedt.core; print(ansys.aedt.core.__version__)"
```

### 3.5 推奨設定

スクリプトの冒頭に次の設定を入れておくと、実行時に例外が起きてもAEDTが自動終了せず、
原因調査がしやすくなります。

```python
from ansys.aedt.core.generic.settings import settings

settings.release_on_exception = False
```

### 3.6 新規起動と既存セッションへの接続の使い分け

```python
from ansys.aedt.core import Hfss

# 新規起動
hfss = Hfss(version="2026.1", new_desktop=True, non_graphical=False)

# 既存のAEDTセッションに接続する場合
hfss = Hfss(version="2026.1", new_desktop=False, non_graphical=False)

# 終了（必ず呼ぶこと）
hfss.release_desktop(close_projects=True, close_desktop=True)
```

---

## 4. VS Codeでの開発手順

自分で作った仮想環境（または前章のAEDT同梱の仮想環境）を使って、VS Codeで開発する手順です。

### 4.1 インタープリタの選択

1. VS Codeでプロジェクトフォルダを開く。
2. コマンドパレット（`Ctrl+Shift+P`）から **Python: Select Interpreter** を実行する。
3. 作成した `.venv` の中のPythonを選ぶ（通常は一覧に自動的に表示される。表示されない場合は
   「Enter interpreter path」から `.venv\Scripts\python.exe` を直接指定する）。

インタープリタを正しく選択すると、エディタ上で `ansys.aedt.core` のインポートに対する
補完・型ヒントが効くようになります。

### 4.2 スクリプトの実行・デバッグ

- 通常の実行: エディタ右上の実行ボタン、またはターミナルで
  `& .venv\Scripts\python.exe .\path\to\script.py` のようにPythonインタープリタのフルパスを
  指定して実行する。
- デバッグ実行: `F5`（または「実行とデバッグ」パネルから開始）。ブレークポイントを置いておけば、
  AEDTが起動した状態のまま、変数の中身（`hfss.modeler` の戻り値など）をその場で確認できる。
  PyAEDTは普通のCPythonで動くため、通常のPythonデバッガ（`debugpy`）がそのまま使える
  （この点は[11_pyaedt_lecture.md](11_pyaedt_lecture.md)の1章・4章で触れた
  「内蔵スクリプトとの違い」そのものです）。

### 4.3 開発時の注意点

- スクリプトを何度も実行・デバッグし直していると、`release_desktop()` を呼ばずに
  中断してしまい、AEDTプロセスが残り続けることがある。残ってしまった場合は、タスクマネージャーで
  AEDTのプロセスを確認するか、`pyaedt session` コマンド（§2.3参照）でセッション一覧を確認して
  手動で後始末する。
- 1つのワークスペースで複数のAEDT仮想環境（AEDT同梱のものと自分で作ったもの）を切り替えて
  使う場合は、VS Codeのインタープリタ選択を都度確認する（意図しない環境でパッケージを
  インストールしてしまう事故を防ぐため）。

---

## 5. まとめ：どちらを選ぶか

- **とにかくすぐに試したい・AEDTのGUIから離れずに作業したい**場合は、AEDTからのインストール
  （2章）で、Automationタブの Console / Jupyter をそのまま使うのが手早い。
- **VS Codeで腰を据えて開発したい・バージョン管理やチームでの共有を重視したい**場合は、
  自分で仮想環境を作成する（3章・4章）方法が向いている。このプロジェクトの演習
  （`exercise/`）は、後者の前提（`starter.py`/`solution.py` をVS Codeで編集・実行する）で
  作られている。

どちらの方法でインストールしても、できあがる `ansys.aedt.core` パッケージ自体は同じものです。
[11_pyaedt_lecture.md](11_pyaedt_lecture.md) 以降のコード例は、どちらの環境でも同じように動きます。
