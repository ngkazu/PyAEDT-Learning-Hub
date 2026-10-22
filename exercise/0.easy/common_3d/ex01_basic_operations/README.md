# 演習1: AEDTの基本操作（起動 → 変数 → 形状 → 保存 → 終了）

**目安時間: 30分**

題材: 特定の公式サンプルはなし（`lecture/01_pyaedt_lecture.md` §3 のデモをもとに、自分の手で再現する）。

## アプリケーションの選び方

この演習はアプリケーションに依存しない（3Dモデラー系であれば同じ手順で進められる）。
[docs/app-selection.md](../../../docs/app-selection.md) の `common_3d` 分類（HFSS / Maxwell 3D / Icepak /
Q3D Extractor / IcepakFEA）から好きなアプリケーションを1つ選び、`starter.py` 冒頭の import とアプリ生成部分を
書き換えてから進めること。以降の説明では例として `Icepak` を使う。

## 学習目標

- PyAEDTでAEDTを起動し、正しく終了するまでの一連の流れを身につける
- 設計変数（GUIの変数欄に出てくるもの）を定義し、形状に反映する
- 形状の作成と、既存形状への材料割り当てを行う

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../docs/app-selection.md) から使いたいアプリケーションを選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動する。
3. 設計変数 `box_size = "10mm"` を定義する（`app["box_size"] = "10mm"` のように角括弧で代入する）。
4. 原点 `[0, 0, 0]`、一辺 `box_size` の立方体を、名前 `"MyBox"` で作成する。
5. `MyBox` の材料を `"aluminum"` に変更する。
6. `box_size` の値を `"20mm"` に変更する（形状を作り直す必要はない。変数の値を書き換えるだけでよい）。
7. プロジェクトを保存する。
8. `release_desktop()` でAEDTを終了する（プロジェクト・プロセスの両方を閉じる）。

## ヒント

- 設計変数の定義・変更はどちらも `app["変数名"] = "値"` という同じ書き方でできる。
- 立方体の作成は `app.modeler.create_box(origin=..., sizes=..., name=...)`。
  `sizes` には数値ではなく変数名の文字列（`["box_size", "box_size", "box_size"]`）を渡せる。
- 既存の形状に材料を割り当て直すには `app.assign_material(assignment="MyBox", material="aluminum")` を使う
  （`create_box` の `material` 引数で最初から指定することもできるが、今回は「後から変更する」練習をする）。

## 評価基準

- [ ] 選んだアプリケーションが起動し、設計変数 `box_size` が定義されている
- [ ] `MyBox` という名前の立方体が作成されている
- [ ] `MyBox` の材料が `aluminum` になっている（GUIのプロパティで確認）
- [ ] `box_size` の値が `20mm` に更新され、形状サイズに反映されている
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- 立方体をもう1つ追加し、位置をずらして2つの形状が重ならないようにしてみてください。
- `docs/app-selection.md` の別のアプリケーションでも同じ手順を試し、形状作成APIの引数がどこまで共通化されているか比較してみてください。
