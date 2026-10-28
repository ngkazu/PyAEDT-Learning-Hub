# 演習6: 形状の移動（Move）と回転（Rotate）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`modeler.move()`/`modeler.rotate()` の基本操作だけを切り出した準備運動。

## アプリケーションの選び方

この演習はアプリケーションに依存しない（3Dモデラー系であれば同じ手順で進められる）。
[docs/app-selection.md](../../../../docs/app-selection.md) の `common_3d` 分類（HFSS / Maxwell 3D / Icepak /
Q3D Extractor / IcepakFEA）から好きなアプリケーションを1つ選び、`starter.py` 冒頭の import とアプリ生成部分を
書き換えてから進めること。以降の説明では例として `Icepak` を使う。

## 学習目標

- `modeler.move(assignment, vector)` で、既存の形状を平行移動する
- `modeler.rotate(assignment, axis, angle, units)` で、既存の形状を軸周りに回転する
- 作成時の位置・向きを後から変更する（作り直さない）操作の流れを身につける

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../../docs/app-selection.md) から使いたいアプリケーションを選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動する。
3. 設計変数 `box_size = "10mm"` を定義する。
4. 原点に一辺 `box_size` の立方体を `"MyBox"` として作成する。
5. `modeler.move(assignment=box.name, vector=["box_size*2", 0, 0])` で、箱をX軸方向に
   `box_size*2` だけ移動する。
6. `modeler.rotate(assignment=box.name, axis="Z", angle=45, units="deg")` で、箱をZ軸周りに
   45度回転する。
7. プロジェクトを保存する。
8. `release_desktop()` でAEDTを終了する。

## ヒント

- `move()` の `vector` は移動量（相対的なオフセット）であり、絶対座標ではない。
- `rotate()` の `axis` は `"X"`/`"Y"`/`"Z"` のいずれか（グローバル座標系の軸）。
- `move()`・`rotate()` はどちらも形状を「作り直さず」その場で変換する。GUIの「モデルツリー」で
  座標値を見ても変わらないが、実際の3D表示上の位置・向きは変わっていることをGUIで確認するとよい。

## 評価基準

- [ ] 選んだアプリケーションが起動し、`MyBox` が作成されている
- [ ] `MyBox` がX軸方向に `box_size*2` だけ移動している（GUIで確認）
- [ ] `MyBox` がZ軸周りに45度回転している（GUIで確認）
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- `axis` を `"X"`/`"Y"` に変えて、回転軸による見た目の違いを確認してください。
- `move()` を複数回呼び出し、移動が累積（相対的に積み重なる）することを確認してください。
