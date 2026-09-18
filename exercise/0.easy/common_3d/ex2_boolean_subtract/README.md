# 演習2: ブーリアン演算（Subtract）で中空の箱を作る

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/hfss/ex2_iris_filter/` や `2.hard/hfss/ex2_iris_filter/` で使う
`modeler.subtract()` の基本操作だけを切り出した準備運動。

## アプリケーションの選び方

この演習はアプリケーションに依存しない（3Dモデラー系であれば同じ手順で進められる）。
[docs/app-selection.md](../../../docs/app-selection.md) の `common_3d` 分類（HFSS / Maxwell 3D / Icepak /
Q3D Extractor / IcepakFEA）から好きなアプリケーションを1つ選び、`starter.py` 冒頭の import とアプリ生成部分を
書き換えてから進めること。以降の説明では例として `Icepak` を使う。

## 学習目標

- `modeler.subtract(blank_list, tool_list, keep_originals=...)` で、ある形状から別の形状をくり抜く
  ブーリアン演算（Subtract）の基本を身につける
- `keep_originals` の意味（`False` なら `tool` 側の形状は削除される）を理解する
- 変数式（`"(outer_size-inner_size)/2"` のような数式）を座標指定に使う

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../docs/app-selection.md) から使いたいアプリケーションを選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動する。
3. 設計変数 `outer_size = "20mm"`, `inner_size = "10mm"`,
   `wall_gap = "(outer_size-inner_size)/2"` を定義する。
4. 原点 `[0, 0, 0]`、一辺 `outer_size` の立方体を `"OuterBox"`（材料 `"aluminum"`）として作成する。
5. 原点から `[wall_gap, wall_gap, wall_gap]` だけずらした位置に、一辺 `inner_size` の立方体を
   `"InnerBox"` として作成する（`OuterBox` の内部中央に収まる位置になる）。
6. `modeler.subtract(blank_list=outer_box, tool_list=inner_box, keep_originals=False)` で、`OuterBox` から
   `InnerBox` をくり抜く。
7. プロジェクトを保存する。
8. `release_desktop()` でAEDTを終了する。

## ヒント

- `subtract()` の `blank_list` は「くり抴かれる側」、`tool_list` は「くり抜く形状（型）」。
  引数名に `_list` が付くが、単一のオブジェクト（`Object3d`）や名前文字列をそのまま渡してもよい。
- `keep_originals` の既定値は `True`（`tool` 側も残す）。今回は明示的に `False` を渡して
  `tool` 側（`InnerBox`）を削除する。
- `True` にすると、くり抜いた後も `tool` 側の形状が残る（複数の形状から同じ穴をくり抜きたいときに使う。
  `2.hard/hfss/ex2_iris_filter/` の空気領域作成で使われている）。
- 変数式は文字列のまま `origin`/`sizes` に渡せる（`"wall_gap"` のように、定義した変数名をそのまま使う）。

## 評価基準

- [ ] 選んだアプリケーションが起動し、設計変数が定義されている
- [ ] `OuterBox` の内部中央に穴が空き、中空の箱になっている（GUIで断面を確認する）
- [ ] `InnerBox` はモデルツリーから削除されている（`keep_originals=False` の効果）
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- `keep_originals=True` に変えて実行し、`InnerBox` がモデルツリーに残ることを確認してください。
- `1.normal/hfss/ex2_iris_filter/` のアイリス作成コード（`create_iris()` 関数）を見て、
  同じ `subtract()` がどう応用されているか確認してみてください。
