# PyAEDT 導入講義

課題（`exercise/`）に入る前に行う、45分程度の講義用資料です。対象読者は「Pythonの基本文法は
習得済みだが、PyAEDT/AEDTの自動化操作は未経験、またはほぼ触ったことがない人」です。

## 目的

- PyAEDT（`ansys.aedt.core` / `pyedb`）が何をするためのライブラリかを理解する
- 主なクラス・関数の位置づけ（アプリオブジェクト → Modeler / Materials / Boundaries / Setup / Post の構造）を掴む
- 「起動 → 何かする → 保存 → 終了」という一連の基本操作を実際に見る
- AEDT内蔵のスクリプト記録機能で得られるコードと、PyAEDTのコードの関係・変換方法を理解する

この講義の内容は、直後に取り組む `exercise/0.easy/` の課題と一部重複します。これは意図的なもので、
講義で見た内容を課題でもう一度手を動かして復習する構成です（課題側は講義内容を前提にしていないので、
講義を聞いていなくても課題単体で進められます）。

## 時間配分（45分想定）

| # | セクション | 目安時間 | 資料 |
|---|---|---|---|
| 1 | イントロダクション（PyAEDTとは・なぜ使うか） | 5分 | `11_pyaedt_lecture.md` §1 |
| 2 | PyAEDTの基本構造（主なクラス・関数の紹介） | 15分 | `11_pyaedt_lecture.md` §2 |
| 3 | 基本操作デモ（開く・箱を作る・保存・閉じる） | 15分 | `11_pyaedt_lecture.md` §3, `demo/demo1_basic_operations.py` |
| 4 | AEDT内蔵Script → PyAEDT変換 | 8分 | `11_pyaedt_lecture.md` §4, `demo/demo2_*.py` |
| 5 | まとめ・次のステップ（課題への導線） | 2分 | `11_pyaedt_lecture.md` §5 |

時間配分は目安であり、質疑応答等で多少の逸脱は許容します。

## 構成物

```
lecture/
  README.md                このファイル
  00_environment_setup.md 環境構築ガイド（AEDTからのインストール・自分で仮想環境作成・VS Codeでの開発手順）
  11_pyaedt_lecture.md    発表者用の講義ノート（台本風、スライドではない）
  12_pyaedt_self_study.md 自己学習用ノート（11と同内容を読み物として整形。講義不参加者・復習用）
  13_pyaedt_architecture.md 「PyAEDTの基本構造」深掘りノート（オブジェクト階層・接続モデル、変数システム、
                            各サブオブジェクト（modeler/materials/boundaries/setup/post）の内部クラス構造、
                            アプリ別の代表的な境界条件、Setup/Sweepの`.props`辞書、`analyze()`の
                            呼び出し方。任意）
  14_post_processing.md    ポスト処理の全体像（Report/Field Plot/PyVista/CSV・matplotlibの使い分け。
                            どの演習のhard/expertにも共通する概念整理。任意）
  31_pyedb_basic.md        PyEDB（pyedb）の基礎ノート（スタックアップ・ネット・配線・ビア・ポート。
                            HFSS 3D Layout / EDB を使う人向けの別トラック。任意）
  demo/
    demo1_basic_operations.py         起動→箱作成→保存→終了の最小デモ
    demo2_before_native_script.py     AEDT内蔵スクリプト記録の出力イメージ（変換前）
    demo2_after_pyaedt_conversion.py  同内容をPyAEDTの高レベルAPIで書き直した例（変換後）
```

環境構築がまだの人は先に [00_environment_setup.md](00_environment_setup.md) を読むこと。

`11_pyaedt_lecture.md` は発表中に「見ながら話す」ための簡潔な台本。その場でそのまま読み上げられるレベルまで詳細化した版は
[docs/lecture-script-detail.md](../docs/lecture-script-detail.md) にある（同じ節構成・同じ時間配分）。
講義に参加できなかった人、後から自分のペースで読み返したい人向けの自己学習版は
[12_pyaedt_self_study.md](12_pyaedt_self_study.md) にある（発表者の進行指示を除き、文章だけで完結するように書き直してある）。

## 進め方（発表者向け）

1. `11_pyaedt_lecture.md` を上から読み進めながら、該当箇所で `demo/` のスクリプトを実際に実行して見せる。
2. デモはAEDTが起動している画面を投影しながら進めると効果的（`non_graphical=False` で実行する）。
3. 講義終了後、学習者は `exercise/0.easy/` の課題（`common_3d` / `common_2d` / `common_schematic`）に進む。

## 前提環境

`00_environment_setup.md` と同じ（Python 3.10+、`pip install "pyaedt[all]"`、AEDT 2024.2以降、フル商用ライセンス）。
