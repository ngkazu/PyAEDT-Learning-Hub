# 課題テンプレート・執筆スタイルガイド

各課題は `README.md` + `starter.py` + `solution.py` の3点セットで構成する。
フォルダは `exercise/<難易度>/<app_slug>/exNN_<slug>/` に配置する（`<app_slug>` は
`common_3d`/`common_2d`/`common_circuit` のいずれか、またはアプリ固有のslug）。

## シリーズ番号（exNN）の付け方

`1.normal/` → `2.hard/` → `3.expert/` の同じ `exNN` 番号は「同じモデルを段階的に拡張したシリーズ」を表す
（詳細は [difficulty-criteria.md](difficulty-criteria.md) の「難易度のシリーズ設計」を参照）。

- 同じ `exNN_<slug>` 番号は、アプリフォルダ内の3階層（normal/hard/expert）で揃える。
  ただし `<slug>` はhard/expertでポスト処理の内容を反映して変えてよい
  （例: `1.normal/hfss/ex01_dipole_antenna/` → `2.hard/hfss/ex01_dipole_farfield/` →
  `3.expert/hfss/ex01_dipole_s11_postprocessing/`）。
- 新しいシリーズを追加するときは、そのアプリフォルダで未使用の次の番号（`ex01`, `ex02`, ...。
  2桁ゼロ埋め）を3階層すべてに割り当てる。既存シリーズの番号を後から変えない（大きな手戻りになるため）。
- 各README.mdの冒頭に、同じシリーズの他階層へのリンクを示す注記（`> この演習は...シリーズの
  ○○レベル`）を入れる。

## 作成順序

新しいシリーズを追加するときは、次の順序で作成する（先に全体を設計してから作るのではなく、
normalを完成させてから段階的に広げる）。

1. **normal**を先に作る（モデル作成→Setup作成→解析実行）。実AEDTでの実行確認もここで済ませる。
2. normalのモデルに**hard**（AEDT内部ポスト処理）を追加する。
3. hardの内容に**expert**（PyVista可視化・CSV入出力）を追加する。
4. normalで使った基礎メソッド（形状作成・ブーリアン演算・`create_setup()`など、**Setup作成くらいまでの
   粒度**）のうち、easy課題としてまだ独立に練習できるものがなければ `0.easy/common_3d/`（等）に追加する。
   周波数スイープ・レポート作成・フィールドプロットなど、hard/expert固有の高度な操作はeasyには含めない。

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

## 「題材」セクションの参照ルール

**タイトル直下の「題材」行**には、着想元にした公式サンプル（あれば）へのリンクを書く（後述の「題材の作り方」参照）。
**normal/hard/expert の課題**では、これに加えて、この課題で使う個別の操作を
先に練習できる easy 課題（`0.easy/common_3d/` 等）があれば、`題材` の段落内または直後に参照を追記する
（例: 「`modeler.subtract()` の基本操作は `0.easy/common_3d/ex02_boolean_subtract/` で練習できる」）。
easy 側にも、対応する normal 課題への参照を発展課題などに書き、双方向にリンクさせる。

## starter.py の規約

- 冒頭に `AEDT_VERSION = "2026.1"` のような環境依存変数をまとめる。
- 実装が必要な箇所には `# TODO: ...` コメントで、何を実装すべきかを具体的に書く。
- `common_3d` 等の課題では、アプリケーションクラスの import 部分を学習者が書き換える前提のコメントを入れる
  （`docs/app-selection.md` の対応表を参照するよう促す）。
- `settings.release_on_exception = False` を設定する（`lecture/00_environment_setup.md` 参照）。

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

このテンプレートは、社内の PyAEDT トレーニング資料（`2026.PyAnsysTraning_inJapan/WorkShop/HFSS/ex01_dipole/`）の
書式を参考にしている。ただし、対象読者・前提が異なるため、コードや文章はコピーせず本プロジェクト用に書き直すこと。
