# 演習5: ブーリアン演算（Unite）で2つの箱を結合する

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`modeler.unite()` の基本操作だけを切り出した準備運動
（`0.easy/common_3d/ex2_boolean_subtract/` の Subtract と対になる演習）。

## アプリケーションの選び方

この演習はアプリケーションに依存しない（3Dモデラー系であれば同じ手順で進められる）。
[docs/app-selection.md](../../../docs/app-selection.md) の `common_3d` 分類（HFSS / Maxwell 3D / Icepak /
Q3D Extractor / IcepakFEA）から好きなアプリケーションを1つ選び、`starter.py` 冒頭の import とアプリ生成部分を
書き換えてから進めること。以降の説明では例として `Icepak` を使う。

## 学習目標

- `modeler.unite(assignment)` で、複数の形状を1つのオブジェクトに結合するブーリアン演算（Unite）を
  身につける
- Unite後は結合された側のオブジェクトがモデルツリーから消えることを理解する
  （`ex2_boolean_subtract` の `keep_originals` とは異なり、Uniteに `keep_originals` はない）

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../docs/app-selection.md) から使いたいアプリケーションを選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動する。
3. 設計変数 `box_size = "10mm"` を定義する。
4. 原点に一辺 `box_size` の立方体を `"Box1"` として作成する。
5. `origin=["box_size/2", 0, 0]` の位置に、同じサイズの立方体を `"Box2"` として作成する
   （Box1と一部重なるように配置する）。
6. `modeler.unite([box1.name, box2.name])` で、2つの箱を1つのオブジェクトに結合する。
7. プロジェクトを保存する。
8. `release_desktop()` でAEDTを終了する。

## ヒント

- `unite()` の引数は結合したいオブジェクトの名前のリスト。戻り値は結合後に残る（最初の）オブジェクト名。
- Unite後、モデルツリーを見ると `Box2` が消え、`Box1` だけが残っている（形状はL字型のような
  結合形状になっている）。
- 結合する形状同士が重なっていなくても接触していれば結合できるが、完全に離れていると
  結合できない（1つのオブジェクトとして繋がらない）。

## 評価基準

- [ ] 選んだアプリケーションが起動し、設計変数が定義されている
- [ ] `Box1` と `Box2` が一部重なる位置に作成されている
- [ ] Unite後、モデルツリーに `Box1`（結合形状）のみが残り、`Box2` が消えている
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- 3つ以上の箱を作成し、まとめて `unite()` に渡してすべて結合してみてください。
- `0.easy/common_3d/ex2_boolean_subtract/` と見比べて、UniteとSubtractの違い
  （`keep_originals` の有無）を確認してみてください。
