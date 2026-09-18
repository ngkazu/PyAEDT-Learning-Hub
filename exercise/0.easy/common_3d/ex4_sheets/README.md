# 演習4: シート形状（矩形・円）を作る

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/hfss/ex3_microstrip_line/` で使う `create_rectangle()` の
基本操作だけを切り出した準備運動。

## アプリケーションの選び方

この演習はアプリケーションに依存しない（3Dモデラー系であれば同じ手順で進められる）。
[docs/app-selection.md](../../../docs/app-selection.md) の `common_3d` 分類（HFSS / Maxwell 3D / Icepak /
Q3D Extractor / IcepakFEA）から好きなアプリケーションを1つ選び、`starter.py` 冒頭の import とアプリ生成部分を
書き換えてから進めること。以降の説明では例として `Icepak` を使う。

## 学習目標

- `modeler.create_rectangle(orientation, origin, sizes, name)` で矩形シート（2Dオブジェクト）を作成する
- `modeler.create_circle(orientation, origin, radius, name)` で円形シートを作成する
- `orientation` にはどの平面（`Plane.XY`/`Plane.XZ`/`Plane.YZ`）に作成するかを指定する
- シート（2D）は3Dソリッドと異なり、`Material` プロパティを持たないことを知る

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../docs/app-selection.md) から使いたいアプリケーションを選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動する。
3. 設計変数 `rect_w = "10mm"`, `rect_h = "20mm"`, `circle_r = "5mm"` を定義する。
4. `modeler.create_rectangle(orientation=Plane.XY, origin=[0, 0, 0], sizes=["rect_w", "rect_h"],
   name="MyRectangle")` で矩形シートを作成する。
5. `modeler.create_circle(orientation=Plane.XY, origin=["rect_w+circle_r+5mm", 0, 0], radius="circle_r",
   name="MyCircle")` で、矩形と重ならない位置に円形シートを作成する。
6. プロジェクトを保存する。
7. `release_desktop()` でAEDTを終了する。

## ヒント

- `Plane`（`from ansys.aedt.core.generic.constants import Plane`）は `XY`/`XZ`/`YZ` の3種類の列挙値を持つ。
  文字列 `"XY"` や整数を直接渡すこともできるが、`Plane.XY` のように書くと読みやすい。
- `create_rectangle()` の `sizes` は `[幅, 高さ]` の2要素、`create_circle()` の `radius` は半径1つだけを
  指定する点に注意（`create_box()` の `sizes` は3要素）。
- シートに `assign_material()` を呼んでも実質何も起こらない（`Material` プロパティが無いため）。
  導体として扱いたい場合は `assign_finite_conductivity()` や `assign_perfect_e()` を使う
  （`1.normal/hfss/ex3_microstrip_line/` を参照）。

## 評価基準

- [ ] 選んだアプリケーションが起動し、設計変数が定義されている
- [ ] `MyRectangle` という名前の矩形シートが作成されている
- [ ] `MyCircle` という名前の円形シートが、矩形と重ならない位置に作成されている
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- `orientation` を `Plane.XZ` や `Plane.YZ` に変えて、別の平面上にシートを作成してみてください。
- `create_circle()` の `num_sides` を `6` などに変えて、正多角形（六角形）を作成してみてください。
