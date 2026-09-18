# 課題テンプレート・執筆スタイルガイド

各課題は `README.md` + `starter.py` + `solution.py` の3点セットで構成する。
フォルダは `exercise/<難易度>/<app_slug>/exNN_<slug>/` に配置する（`<app_slug>` は
`common_3d`/`common_2d`/`common_circuit` のいずれか、またはアプリ固有のslug）。

## README.md の必須セクション

1. **タイトル**（`# 演習N: <課題名>`）
2. **目安時間**（`docs/difficulty-criteria.md` に沿った時間）
3. **題材**（着想元にした公式サンプルへの参照。あれば）
4. **学習目標**（この課題で身につくこと。箇条書き3〜6項目程度）
5. **課題**（`starter.py` の `# TODO` を埋めるための、番号付きの具体的な手順・仕様）
6. **ヒント**（詰まりやすいポイント、使うAPIの調べ方）
7. **評価基準**（`docs/review-checklist.md` をベースに、この課題固有のチェック項目）
8. **発展課題**（任意。時間があれば取り組む追加課題）

`common_3d` / `common_2d` / `common_circuit` の課題では、上記に加えて「アプリケーションの選び方」の
節を設け、`docs/app-selection.md` を参照させる（対応表を重複記載しない）。

## starter.py の規約

- 冒頭に `AEDT_VERSION = "2026.1"` のような環境依存変数をまとめる。
- 実装が必要な箇所には `# TODO: ...` コメントで、何を実装すべきかを具体的に書く。
- `common_3d` 等の課題では、アプリケーションクラスの import 部分を学習者が書き換える前提のコメントを入れる
  （`docs/app-selection.md` の対応表を参照するよう促す）。
- `settings.release_on_exception = False` を設定する（`docs/setup.md` 参照）。

## solution.py の規約

- `starter.py` と同一フォルダに配置する（分離しない）。
- `starter.py` と同じ `AEDT_VERSION` 変数・全体構成を維持し、`# TODO` 部分だけを実装した状態にする。
- 変数名・アプリオブジェクト名は `docs/app-selection.md` の最小サンプルに揃える
  （例: `app = Icepak(...)`、または課題によっては `hfss = Hfss(...)` のようにアプリ名をそのまま使う）。
- 最後に必ず `release_desktop()` を呼ぶ。

## 題材の作り方

- 公式サンプル（https://examples.aedt.docs.pyansys.com/）は**着想元として参照するのみ**。
  コードの丸写しはせず、学習目的で独自に作り直す。
- 引数名・戻り値・内部実装が不明なAPIは推測しない。ローカルの `pyaedt`/`pyedb` ソースを grep するか、
  `inspect.signature()` 等で実行時に検証する。

## 参考にしたフォーマット

このテンプレートは、社内の PyAEDT トレーニング資料（`2026.PyAnsysTraning_inJapan/WorkShop/HFSS/ex1_dipole/`）の
書式を参考にしている。ただし、対象読者・前提が異なるため、コードや文章はコピーせず本プロジェクト用に書き直すこと。
