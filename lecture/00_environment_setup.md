# PyAEDT 環境構築ガイド（自己学習版）

PyAEDTを使い始める前に必要な環境構築を、実際の操作手順に沿って説明します。
[01_pyaedt_lecture.md](01_pyaedt_lecture.md) / [02_pyaedt_self_study.md](02_pyaedt_self_study.md) で
扱うコード例を実際に動かすための準備にあたる内容です。要点だけを簡潔にまとめたリファレンスは
[docs/setup.md](../docs/setup.md) を参照してください（このノートはその内容を、実際の手順を追いながら
詳しく解説したものです）。

## 1. 2つの選択肢

PyAEDTを動かすPython環境には、大きく分けて2つの選択肢があります。

| 選択肢 | 向いている場面 |
|---|---|
| **AEDTからインストール**（AEDT同梱のCPythonにPyAEDTを追加する） | すぐに試したい、AEDTのAutomationタブから使えるConsole/Jupyter/Run Scriptも併せて使いたい |
| **自分で仮想環境を作成**（`pip install pyaedt[all]`） | VS Codeなど通常のIDEで開発したい、最新版やオプション依存を含めて柔軟にバージョン管理したい |

このプロジェクト（`PyAEDT-Learning-Hub`）の演習は、どちらの環境からでも進められます。
両方の作り方を知っておくと、場面に応じて使い分けられます。

---

## 2. AEDTからインストールする

### 2.1 インストーラースクリプトを実行する

AEDTには、**AEDTに同梱されているCPythonインタープリタ**を使ってPyAEDTを自動インストールする
スクリプトが用意されています。手順は次の通りです。

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

> **AEDT 2026 R2 SP2以降の場合**: PyAEDTが最初からAEDTのインストールに同梱されるようになりました
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

## 3. 自分で仮想環境を作成する

VS Codeなど通常のIDEで開発したい場合は、AEDT同梱の環境に頼らず、自分で仮想環境を作るのが
確実です。このプロジェクト自体も、この方法で検証用の `.venv` を作成しています。

### 3.1 仮想環境の作成とアクティベート

```powershell
# プロジェクトフォルダ直下で仮想環境を作成する
python -m venv .venv

# PowerShellでアクティベートする
.venv\Scripts\Activate.ps1
```

実行ポリシーの制限でアクティベートできない場合は、次のように一時的に許可してから実行します。

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
.venv\Scripts\Activate.ps1
```

### 3.2 PyAEDTのインストール

```powershell
pip install "pyaedt[all]"
```

バージョンを確認するには次のようにします。

```powershell
py -3 -c "import ansys.aedt.core; print(ansys.aedt.core.__version__)"
```

### 3.3 推奨設定

スクリプトの冒頭に次の設定を入れておくと、実行時に例外が起きてもAEDTが自動終了せず、
原因調査がしやすくなります。

```python
from ansys.aedt.core.generic.settings import settings

settings.release_on_exception = False
```

### 3.4 新規起動と既存セッションへの接続の使い分け

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
  （この点は[01_pyaedt_lecture.md](01_pyaedt_lecture.md)の1章・4章で触れた
  「内蔵スクリプトとの違い」そのものです）。

### 4.3 開発時の注意点

- スクリプトを何度も実行・デバッグし直していると、`release_desktop()` を呼ばずに
  中断してしまい、AEDTプロセスが残り続けることがある。残ってしまった場合は、タスクマネージャーで
  AEDTのプロセスを確認するか、`pyaedt session` コマンド（前章参照）でセッション一覧を確認して
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
[01_pyaedt_lecture.md](01_pyaedt_lecture.md) 以降のコード例は、どちらの環境でも同じように動きます。
