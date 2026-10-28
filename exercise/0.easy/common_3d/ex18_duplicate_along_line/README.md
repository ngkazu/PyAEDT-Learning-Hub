# 演習18: 直線方向への複製（duplicate_along_line）でフィン列を作る

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/icepak/ex01_heatsink/` や `1.normal/icepak/
ex02_small_cabinet_fan/` で、ヒートシンクのフィンを並べるために使う `modeler.duplicate_along_line()`
の基本操作だけを切り出して練習する演習。

## アプリケーションの選び方

このフォルダの課題は、3Dモデラー系アプリ（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）に共通する
基本操作を学ぶ。使いたいアプリケーションのクラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照し、`starter.py` 冒頭の import とアプリ生成部分を書き換える。

## 学習目標

- `modeler.duplicate_along_line(assignment, vector, clones)` で、指定したベクトル方向に
  等間隔で複製する方法を学ぶ
- `vector`がベクトルの**向き**と**ピッチ（間隔）**の両方を表すことを理解する
- `clones=N`は「合計N個（元の1個＋複製(N-1)個）」を意味することを理解する
- 戻り値 `(成功フラグ, 複製されたオブジェクト名のリスト)` を受け取り、元の名前と結合して
  全オブジェクト名のリストを作る方法を学ぶ

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../../docs/app-selection.md) から使いたいアプリケーションを選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動し、
   `modeler.model_units = "mm"` を設定する。
3. フィン1枚目（`"Fin"`）を `origin=[0, 0, 0]`, `sizes=[40, 2, 20]`,
   `material="Al-Extruded"` で作成する。
4. `_ok, clone_names = modeler.duplicate_along_line(assignment="Fin", vector=[0, 5, 0],
   clones=6)` で、Y方向にピッチ5mmで合計6枚に複製する。
5. `all_fin_names = ["Fin"] + clone_names` で、全フィン名のリストを作る
   （戻り値の`clone_names`には元のオブジェクト名`"Fin"`は含まれない）。
6. プロジェクトを保存する。
7. `release_desktop()` でアプリケーションを終了する。

## ヒント

- `vector=[0, 5, 0]`は「Y方向に5mmずつ」複製することを意味する。X成分・Z成分を0以外にすると、
  斜め方向への複製もできる。
- `clones=6`を指定すると、元の`"Fin"`に加えて5つの複製（`"Fin_1"`〜`"Fin_5"`という名前）が
  作られ、合計6枚になる。
- `duplicate_along_line()`の戻り値は`(成功フラグ, 複製されたオブジェクト名のリスト)`の
  タプル。複製されたオブジェクトをまとめて後続処理（境界条件の割り当てやフィールドプロット）に
  使いたいときは、元の名前と結合したリストを作っておくと扱いやすい。

## 評価基準

- [ ] 選んだアプリケーションが起動し、`modeler.model_units = "mm"` が設定されている
- [ ] `"Fin"`という名前のBoxが作成されている
- [ ] Y方向にピッチ5mmで、合計6枚のフィン（`"Fin"`, `"Fin_1"`〜`"Fin_5"`）が作成されている
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- `vector`を`[0, 5, 2]`のように斜め方向に変えて、複製の向きがどう変わるか確認してみてください。
- `clones`の数を変えて、生成されるオブジェクト名がどう変化するか確認してみてください。
