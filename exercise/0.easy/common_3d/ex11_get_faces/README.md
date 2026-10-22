# 演習11: 面（Face）を取得する（get_object_faces→get_face_center/get_face_area）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/maxwell_3d/ex01_choke/` で使う
`modeler.get_object_faces()` の基本操作だけを切り出して練習する演習。

## アプリケーションの選び方

このフォルダの課題は、3Dモデラー系アプリ（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）に共通する
基本操作を学ぶ。使いたいアプリケーションのクラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照し、`starter.py` 冒頭の import とアプリ生成部分を書き換える。

## 学習目標

- `modeler.get_object_faces()` で、オブジェクト名から面IDのリストを取得する
- `modeler.get_face_center()` / `modeler.get_face_area()` で、面IDから中心座標・面積を取得する
- 境界条件や励振の割り当て（`assign_current()`など）に進む前段階として、面IDを扱う基本を身につける

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. 好きな3Dモデラー系アプリケーションを起動する。
2. `modeler.create_box(origin=[0, 0, 0], sizes=["10mm", "10mm", "10mm"], name="MyBox",
   material="aluminum")` で箱を作成する。
3. `modeler.get_object_faces(assignment=box.name)` で、箱の面IDのリストを取得する
   （直方体は6面あるため、リストの要素数は6になる）。
4. 取得したリストの最初の面ID（`face_ids[0]`）について、
   `modeler.get_face_center(assignment=face_ids[0])` で中心座標を、
   `modeler.get_face_area(assignment=face_ids[0])` で面積を取得する。
5. プロジェクトを保存し、アプリケーションを終了する。

## ヒント

- `get_object_faces()` はオブジェクト名（`str`）だけでなく、オブジェクトID（`int`）でも呼び出せる。
- `get_face_center()` は平面（planar）な面にのみ使える。曲面の場合は失敗することがある
  （今回の箱の面はすべて平面なので問題ない）。
- このあと `1.normal/maxwell_3d/ex01_choke/` で `get_object_faces()` を使って巻線の面を取得し、
  そこに電流励振を割り当てる流れに進む。

## 評価基準

- [ ] アプリケーションが起動し、箱が作成されている
- [ ] `get_object_faces()` で6個の面IDが取得できている
- [ ] 最初の面の中心座標・面積が取得できている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `face_ids` の全要素について `get_face_center()` を呼び出し、6面すべての中心座標を確認してください。
- 励振を割り当てて実際に解析まで行いたい場合は、
  [1.normal/maxwell_3d/ex01_choke/](../../../1.normal/maxwell_3d/ex01_choke/) に進んでみてください。
