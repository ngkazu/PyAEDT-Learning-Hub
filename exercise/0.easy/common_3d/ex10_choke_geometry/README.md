# 演習10: チョークのジオメトリを作る（check_choke_values→create_choke）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/maxwell_3d/ex01_choke/` で使う `modeler.create_choke()` の
基本操作（設定辞書・JSON経由での呼び出し・戻り値の構造）だけを切り出して練習する演習。

## アプリケーションの選び方

このフォルダの課題は、3Dモデラー系アプリ（HFSS, Maxwell 3D, Icepak, Q3D Extractor, IcepakFEA）に共通する
基本操作を学ぶ。使いたいアプリケーションのクラス名は [docs/app-selection.md](../../../../docs/app-selection.md)
を参照し、`starter.py` 冒頭の import とアプリ生成部分を書き換える。

## 学習目標

- `modeler.create_choke()` 用のジオメトリパラメータ辞書（コア・巻線の形状定義）をJSON経由で渡す使い方を理解する
- `modeler.check_choke_values()` で辞書の整合性を事前チェックする
- `create_choke()` の戻り値の構造（`[success, core, [winding_obj, 座標リスト]]`）を理解する
- 励振やSetup作成を伴わない、ジオメトリ作成だけの最小構成で`create_choke()`に慣れる

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすジオメトリ作成を完成させてください。

1. 好きな3Dモデラー系アプリケーションを起動し、`modeler.model_units = "mm"` を設定する。
2. チョークのジオメトリパラメータを表す `choke_descriptor` 辞書を定義する。値は下表の通りでよい
   （`modeler.check_choke_values()` のdocstringに載っているデフォルト例そのまま）。

   | キー | 値 |
   |---|---|
   | `"Number of Windings"` | `{"1": True, "2": False, "3": False, "4": False}`（巻線1本） |
   | `"Layer"` | `{"Simple": True, "Double": False, "Triple": False}`（単層） |
   | `"Layer Type"` | `{"Separate": True, "Linked": False}`（**単層の場合は必ず`Separate`**。下記の注意を参照） |
   | `"Similar Layer"` | `{"Similar": True, "Different": False}` |
   | `"Mode"` | `{"Differential": True, "Common": False}` |
   | `"Wire Section"` | `{"None": False, "Hexagon": False, "Octagon": True, "Circle": False}` |
   | `"Core"` | `{"Name": "Core", "Material": "ferrite", "Inner Radius": 11, "Outer Radius": 17, "Height": 7, "Chamfer": 0.8}` |
   | `"Outer Winding"` | `{"Name": "Winding", "Material": "copper", "Inner Radius": 12, "Outer Radius": 16, "Height": 8, "Wire Diameter": 1, "Turns": 10, "Coil Pit(deg)": 9, "Occupation(%)": 0}` |
   | `"Mid Winding"` | `{"Turns": 8, "Coil Pit(deg)": 0.1, "Occupation(%)": 0}`（単層では未使用だがキーは必須） |
   | `"Inner Winding"` | `{"Turns": 12, "Coil Pit(deg)": 0.1, "Occupation(%)": 0}`（単層では未使用だがキーは必須） |

   > **注意（はまりやすい点）**: `"Layer"` が `"Simple"`（単層）のとき、`"Layer Type"` を
   > `"Linked": True` にすると、内部で巻線オブジェクトではなく座標リストだけが返り、
   > 後続の処理が失敗する。単層では必ず `"Separate": True` にすること。

3. 辞書を一時JSONファイルに書き出し（`json.dump()`）、`modeler.check_choke_values(input_dir=choke_fn,
   create_another_file=False)` で整合性を確認したうえで、`modeler.create_choke(input_file=choke_fn)` で
   チョークのジオメトリを作成する。戻り値のリストから `core = list_object[1]`、
   `winding = list_object[2]` を取り出す（励振の割り当てやSetup作成は行わない）。
4. プロジェクトを保存し、アプリケーションを終了する。

## ヒント

- `create_choke()` はJSONファイルのパスを引数に取る仕様のため、辞書を直接渡すことはできない。
- `modeler.create_choke()` は `Primitives3D` クラスのメソッドなので、HFSS/Maxwell 3D/Icepak/Q3D Extractor/
  IcepakFEAのどのアプリでも同じように使える。
- このジオメトリ作成・戻り値の構造に慣れておくと、`1.normal/maxwell_3d/ex01_choke/`
  （励振・Setup・解析実行を追加した発展形）がスムーズに進められる。

## 評価基準

- [ ] アプリケーションが起動し、チョーク（コア＋巻線）のジオメトリが作成されている
- [ ] `check_choke_values()` と `create_choke()` の呼び出し順序が正しい
- [ ] プロジェクト（`.aedt`）が保存されている

## 発展課題（任意）

- `"Number of Windings"` を `"2"` に変更し、巻線数を増やすとモデルがどう変わるか確認してください。
- 励振を割り当てて実際に解析まで行いたい場合は、
  [1.normal/maxwell_3d/ex01_choke/](../../../1.normal/maxwell_3d/ex01_choke/) に進んでみてください。
