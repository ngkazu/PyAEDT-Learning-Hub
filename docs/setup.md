# 環境構築ガイド

## 前提条件

- **Python**: 3.10 以上
- **AEDT**: 2024.2 以降（推奨: 最新版）
- **ライセンス**: フル商用ライセンスを所有していること（学生版の機能制限やHPCライセンスの回避策は考慮しない）

## インストール

```powershell
pip install "pyaedt[all]"
```

バージョンを確認する:

```powershell
py -3 -c "import ansys.aedt.core; print(ansys.aedt.core.__version__)"
```

インストール済みの AEDT バージョンは、AEDT を起動して「ヘルプ > バージョン情報」で確認できる
（例: `2026.1`）。各課題の `starter.py` / `solution.py` 冒頭にある `AEDT_VERSION` 変数を、
お使いの環境のバージョンに合わせて書き換えてから実行すること。

## 推奨設定

スクリプトの冒頭で以下を設定しておくと、実行時のエラー発生時にAEDTが自動終了してしまうのを防げる。

```python
from ansys.aedt.core.generic.settings import settings

settings.release_on_exception = False
```

## 起動方法の選び方

- **新規に起動する場合**: `new_desktop=True` を指定する。
- **既に開いている AEDT セッションに接続する場合**: `new_desktop=False` を指定する
  （`port` や `aedt_process_id` を指定して既存プロセスを明示することもできる）。

```python
from ansys.aedt.core import Hfss

# 新規起動
hfss = Hfss(version="2026.1", new_desktop=True, non_graphical=False)

# 終了（必ず呼ぶこと。呼ばないとAEDTプロセスが残り続ける）
hfss.release_desktop(close_projects=True, close_desktop=True)
```

## アプリケーションの選び方

演習で使用する AEDT アプリケーション（`Hfss` / `Icepak` / `Maxwell3d` など）のクラス名対応表は
[docs/app-selection.md](app-selection.md) を参照すること。

## 検証用の仮想環境（任意）

このリポジトリ自体の検証には `.venv`（プロジェクト直下、`.gitignore` 済み）を使っている。
学習者が独自に仮想環境を作る場合も、同様に AEDT バンドルの Python、または通常の Python 3.10+ を
使って `pip install "pyaedt[all]"` すればよい。

## 困ったときの調べ方

- 公式ドキュメント: https://aedt.docs.pyansys.com/
- 公式サンプル集（着想元。コードの丸写しは避ける）: https://examples.aedt.docs.pyansys.com/
- 実行時に `dir(obj)` / `help(obj.method)` でその場でAPIを確認する。
