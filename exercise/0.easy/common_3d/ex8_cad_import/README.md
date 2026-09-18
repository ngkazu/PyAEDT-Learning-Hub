# 演習8: CADのインポート（エクスポート→インポートの往復）

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`modeler.import_3d_cad()` の基本操作だけを切り出した準備運動。
外部CADファイルを別途用意する代わりに、自分で作った形状をSTEPファイルとしてエクスポートしてから
インポートし直す「往復」構成にすることで、この課題単体で完結できるようにしている。

## アプリケーションの選び方

この演習はアプリケーションに依存しない（3Dモデラー系であれば同じ手順で進められる）。
[docs/app-selection.md](../../../docs/app-selection.md) の `common_3d` 分類（HFSS / Maxwell 3D / Icepak /
Q3D Extractor / IcepakFEA）から好きなアプリケーションを1つ選び、`starter.py` 冒頭の import とアプリ生成部分を
書き換えてから進めること。以降の説明では例として `Icepak` を使う。

## 学習目標

- `modeler.export_3d_model()` で、モデル内の形状をSTEP等のCADファイル形式にエクスポートする
- `modeler.import_3d_cad()` で、外部CADファイルをモデルにインポートする
- `modeler.delete()` で、既存の形状をモデルから削除する

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../docs/app-selection.md) から使いたいアプリケーションを選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動する。
3. 設計変数 `box_size = "10mm"` を定義する。
4. 原点に一辺 `box_size` の立方体を `"MyBox"` として作成する。
5. `modeler.export_3d_model(file_name="my_box", file_path=app.working_directory, file_format=".step",
   assignment_to_export=[box.name])` で、箱をSTEPファイルとしてエクスポートする。
6. `modeler.delete([box.name])` で、元の箱をモデルから削除する。
7. `modeler.import_3d_cad(input_file=f"{app.working_directory}/my_box.step")` で、
   手順5でエクスポートしたSTEPファイルを読み込み直す。
8. プロジェクトを保存する。
9. `release_desktop()` でAEDTを終了する。

## ヒント

- `app.working_directory` は、そのプロジェクトの作業用フォルダのパス（文字列）を返す。
  エクスポート・インポートのファイルパスをその場で計算する際に使うと、環境に依存しないコードになる。
- `export_3d_model()` の `assignment_to_export` を省略すると、モデル内のすべてのオブジェクトが
  エクスポートされる。特定の形状だけを書き出したい場合は、対象の名前をリストで指定する。
- `import_3d_cad()` はデフォルトで `create_group=True` になっており、インポートした形状は
  グループとしてモデルツリーに追加される。

## 評価基準

- [ ] 選んだアプリケーションが起動し、`MyBox` が作成されている
- [ ] `MyBox` がSTEPファイルとしてエクスポートされている（`working_directory` にファイルが生成される）
- [ ] エクスポート後、元の `MyBox` が削除されている
- [ ] STEPファイルからインポートし直した形状がモデルに存在する
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- `file_format` を `.stp`, `.iges`, `.sat`（Windowsのみ）など別の形式に変えてみて、
  インポートできるか確認してください。
- `import_3d_cad()` の `healing=True` を試し、形状の修復オプションがどう機能するか確認してください。
