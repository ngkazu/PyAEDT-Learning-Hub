# 演習15: ポリラインの回転複製で環状形状を作る（create_polyline→duplicate_around_axis→unite）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/maxwell_3d/ex02_asymmetric_conductor/` のTEAM7コイルで使う
「4分の1形状を描いて回転複製し結合することで環状の立体を作る」モデリング手法だけを切り出して練習する演習。

## アプリケーションの選び方

このフォルダの課題は、3Dモデラー系アプリ（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）に共通する
基本操作を学ぶ。使いたいアプリケーションのクラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照し、`starter.py` 冒頭の import とアプリ生成部分を書き換える。

## 学習目標

- `modeler.create_polyline()` で、直線（`"Line"`）と円弧（`"Arc"`）を組み合わせたポリラインを描く
- `set_crosssection_properties()` で、ポリラインに断面形状を与えて棒状のソリッドにする
- `modeler.duplicate_around_axis()` で、軸まわりに複数複製する
- `modeler.unite()` で、複製した複数のオブジェクトを1つの環状形状に結合する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください
（4分の1形状のポイント定義は固定値なので変更不要です）。

1. 好きな3Dモデラー系アプリケーションを起動し、`modeler.model_units = "mm"` を設定する。
2. `create_polyline(points=[P1, P2, P3, P4], segment_type=["Line", "Arc"], name="Quarter")` で、
   直線1区間（P1→P2）＋円弧1区間（P2→P3→P4）からなる4分の1形状を描画する。
3. `set_crosssection_properties(section="Rectangle", width=5, height=10)` で、断面形状（矩形）を
   設定し、1本の棒状ソリッドにする。
4. `modeler.duplicate_around_axis(assignment="Quarter", axis="Z", angle=90, clones=4,
   create_new_objects=True, is_3d_comp=False)` で、Z軸まわりに90度ずつ回転複製する（4つ作る）。
5. `modeler.unite(["Quarter", "Quarter_1", "Quarter_2", "Quarter_3"])` で、複製した4つを結合し、
   1つの環状形状にする。
6. プロジェクトを保存し、アプリケーションを終了する。

## ヒント

- `segment_type=["Line", "Arc"]` の `"Arc"` セグメントは、直前の点を始点、次の点を経由点、
  その次の点を終点とする円弧を作る（`points`リストの点を順番に消費していく）。
- `duplicate_around_axis()` で `clones=4` を指定すると、元のオブジェクトに加えて3つの複製
  （`_1`, `_2`, `_3`という名前）が作られる。4分割（90度ずつ）なら、元の1つ＋複製3つ＝合計4つで
  1周（360度）になる。
- `unite()` には結合したいオブジェクト名のリストをまとめて渡せる（2回に分けて結合する必要はない）。

## 評価基準

- [ ] アプリケーションが起動し、直線＋円弧からなる4分の1形状が作成されている
- [ ] 断面形状が設定され、棒状のソリッドになっている
- [ ] Z軸まわりに90度ずつ4つ複製されている
- [ ] 4つが結合され、1つの環状形状になっている
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `clones`の数や`angle`を変えて、複製の間隔や個数がどう変わるか確認してください。
- 実際にコイルとして使ってみたい場合は、
  [1.normal/maxwell_3d/ex02_asymmetric_conductor/](../../../1.normal/maxwell_3d/ex02_asymmetric_conductor/)
  に進んでみてください。
