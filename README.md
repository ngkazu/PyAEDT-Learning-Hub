# PyAEDT-Learning-Hub

PyAEDT（`ansys.aedt.core` / `pyedb`）を使ってAEDT自動化を学ぶための**課題集**プロジェクトです。

## 構成

```
lecture/    課題に入る前に行う45分講義の資料（PyAEDTの基本構造・使い方）
docs/       課題作成の方針・テンプレート・進捗管理などのドキュメント
exercise/   難易度別の課題本体（このプロジェクトの主役）
memo/       課題作成者向けの内部メモ（学習者は見る必要なし）
```

## 進め方

1. **`lecture/`** の講義資料に目を通す（すでに講義を受講済みなら読み飛ばしてよい）。
2. **`docs/setup.md`** に沿って環境を準備する。
3. **`docs/app-selection.md`** で、演習に使いたいAEDTアプリケーションのクラス名を確認する。
4. **`exercise/0.easy/`** から順に、`1.normal/` → `2.hard/` → `3.expert/` と難易度を上げながら進める。
   各課題フォルダには `README.md`（課題文）・`starter.py`（穴埋め用）・`solution.py`（模範解答）がある。
   まず `README.md` を読み、`starter.py` をコピーして自分で実装し、詰まったら `solution.py` を確認する。

## 難易度の考え方

難易度は Python の難しさではなく、**AEDT/PyAEDT ドメインの複雑さ**で決まっています。
詳細は [docs/difficulty-criteria.md](docs/difficulty-criteria.md) を参照してください。

- **easy（目安30分）**: AEDTの基本操作（起動→何かする→保存→終了）。アプリ非依存の`common_3d`/`common_2d`/`common_circuit`から選べる。
- **normal（目安60分）**: アプリ別の自動化基本（モデル作成→Setup作成→解析実行まで。ポスト処理は行わない）。
- **hard（目安90分）**: normalと同じモデルにAEDT内部ポスト処理（Report/Field Plot）を追加。複数アプリの連成解析はここでのみ任意で扱う。
- **expert（目安90分以上）**: hardの内容にPyVista可視化・CSV入出力を追加。matplotlib等を使ったPythonデータ処理を重視。

## 前提知識

- Python の基本文法（変数・関数・辞書/リスト・for ループ・クラスの使い方）を習得済みであること。
- AEDT/PyAEDTの経験は不要（`lecture/` と easy 課題から学べる構成になっている）。

## ドキュメント一覧

| ファイル | 内容 |
|---|---|
| [docs/setup.md](docs/setup.md) | 環境構築ガイド |
| [docs/app-selection.md](docs/app-selection.md) | アプリケーション選択リファレンス |
| [docs/difficulty-criteria.md](docs/difficulty-criteria.md) | 難易度基準 |
| [docs/exercise-template.md](docs/exercise-template.md) | 課題の書式・執筆スタイルガイド |
| [docs/review-checklist.md](docs/review-checklist.md) | レビュー・品質チェックリスト |
| [docs/roadmap/coverage.md](docs/roadmap/coverage.md) | アプリ×難易度のカバレッジ表（進捗管理） |
| [docs/lecture-script-detail.md](docs/lecture-script-detail.md) | 導入講義（`lecture/`）の発表者読み上げ用詳細版スクリプト |

## 参考

- 各課題は [PyAEDT Examples](https://examples.aedt.docs.pyansys.com/) を着想元として、学習目的で独自に作成しています
  （公式サンプルの丸写しはしていません）。
- PyAEDT公式ドキュメント: https://aedt.docs.pyansys.com/
