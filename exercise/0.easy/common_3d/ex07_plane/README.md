# 演習7: Planeを作る

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`2.hard/hfss/ex02_iris_filter/` や `2.hard/hfss/ex04_patch_antenna_farfield/`
などで使う `modeler.create_plane()` の基本操作だけを切り出した準備運動。

## アプリケーションの選び方

この演習はアプリケーションに依存しない（3Dモデラー系であれば同じ手順で進められる）。
[docs/app-selection.md](../../../docs/app-selection.md) の `common_3d` 分類（HFSS / Maxwell 3D / Icepak /
Q3D Extractor / IcepakFEA）から好きなアプリケーションを1つ選び、`starter.py` 冒頭の import とアプリ生成部分を
書き換えてから進めること。以降の説明では例として `Icepak` を使う。

## 学習目標

- `modeler.create_plane(name, plane_base_x/y/z, plane_normal_x/y/z)` で、座標系上の平面（Plane）を
  作成する
- Planeが、シート（`create_rectangle` 等）やCADオブジェクトとは異なる「基準点＋法線ベクトル」だけで
  定義される特殊なジオメトリであることを理解する
- Planeが使われる典型的な場面（フィールドプロットのカットプレーン指定など）を知る

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../docs/app-selection.md) から使いたいアプリケーションを選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動する。
3. 設計変数 `box_size = "10mm"` を定義する。
4. 原点に一辺 `box_size` の立方体を `"MyBox"` として作成する（Planeが何を切るのか分かりやすくするための
   土台）。
5. `modeler.create_plane(name="MyPlane", plane_base_x="0mm", plane_base_y="box_size/2",
   plane_base_z="0mm", plane_normal_x="0mm", plane_normal_y="1mm", plane_normal_z="0mm")` で、
   箱の中心（y = box_size/2）を通り、Y軸方向を法線とするXZ平面を作成する。
6. プロジェクトを保存する。
7. `release_desktop()` でAEDTを終了する。

## ヒント

- Planeは「面」ではあるが、`create_rectangle()` で作るような実体のあるシートオブジェクトではない。
  GUIのモデルツリーでは「Planes」という別カテゴリに表示される。
- `plane_base_x/y/z` は平面上の基準点の座標、`plane_normal_x/y/z` は平面の法線ベクトルの方向を表す。
  法線が `(0, 1, 0)`（Y軸方向）の場合、その平面はXZ平面と平行になる。
- Planeは、`post.create_fieldplot_cutplane()`（電界などのカットプレーン表示）のように、
  「座標平面そのもの」を引数として要求するAPIで使われる。シートオブジェクトを渡すと動作しない場面がある
  （`2.hard/hfss/ex02_iris_filter/` 参照）。

## 評価基準

- [ ] 選んだアプリケーションが起動し、`MyBox` が作成されている
- [ ] `MyPlane` という名前のPlaneが、箱の中心を通るXZ平面として作成されている（GUIの「Planes」ツリーで確認）
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- `plane_normal_x/y/z` を `(1, 0, 0)` に変えて、YZ平面を作成してみてください。
- `2.hard/hfss/ex02_iris_filter/` のフィールドプロット作成コードを見て、`create_plane()` が
  どのように使われているか確認してみてください。
