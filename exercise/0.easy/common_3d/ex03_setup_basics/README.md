# 演習3: セットアップ（解析条件）を作ってみる

**目安時間: 30分**

題材: 特定の公式サンプルはなし。`1.normal/hfss/ex01_dipole_antenna/` や `1.normal/hfss/ex02_iris_filter/` で
使う `create_setup()` の基本操作だけを切り出した準備運動。

## アプリケーションの選び方

この演習はアプリケーションに依存しない（3Dモデラー系であれば同じ手順で進められる）。
[docs/app-selection.md](../../../docs/app-selection.md) の `common_3d` 分類（HFSS / Maxwell 3D / Icepak /
Q3D Extractor / IcepakFEA）から好きなアプリケーションを1つ選び、`starter.py` 冒頭の import とアプリ生成部分を
書き換えてから進めること。以降の説明では例として `Icepak` を使う。

## 学習目標

- `app.create_setup(name=...)` で、そのアプリの既定の解析条件（セットアップ）を作成する
- 作成したセットアップは `setup.props`（辞書のようなオブジェクト）でプロパティを参照・変更できることを知る
- セットアップのプロパティ名（`"MaximumPasses"` 等）はアプリ（ソルバー）ごとに異なることを知る
  （本演習ではまだ具体的な解析は実行しない。詳しいプロパティ指定は `1.normal/` で扱う）

## 課題

`starter.py` の `# TODO` を埋めて、次の仕様を満たすスクリプトを完成させてください。

1. [docs/app-selection.md](../../../docs/app-selection.md) から使いたいアプリケーションを選び、
   `starter.py` の import 文とアプリ生成部分を書き換える。
2. `new_desktop=True`, `non_graphical=False` でアプリケーションを起動する。
3. 設計変数 `box_size = "10mm"` を定義し、原点に一辺 `box_size` の立方体 `"MyBox"` を作成する
   （セットアップだけでは意味がないため、最低限のモデルを用意する）。
4. `app.create_setup(name="MySetup")` で、名前だけ指定してセットアップを作成する
   （プロパティはすべてアプリごとの既定値のままにする）。
5. `"MaximumPasses" in setup.props` が真であれば、`setup.props["MaximumPasses"] = 5` に変更し、
   `setup.update()` を呼んで反映する（存在しない場合は何もしない）。
6. プロジェクトを保存する。
7. `release_desktop()` でAEDTを終了する。

## ヒント

- `create_setup()` は `name` 以外の引数（`**kwargs`）を省略すると、そのアプリの既定のセットアップタイプ・
  既定のプロパティ値で作成される。まずは既定値がどうなっているか、GUIの「Analysis」ツリーから
  `MySetup` を右クリック→「Properties」で確認してみるとよい。
- `setup.props` は辞書のように `in` 演算子でキーの有無を確認できる。存在しないキーに代入すると
  エラーになるため、必ず確認してから変更する。
- プロパティを変更した後は `setup.update()` を呼ばないと、AEDT側に反映されないことがある。

## 評価基準

- [ ] 選んだアプリケーションが起動し、`MyBox` が作成されている
- [ ] `MySetup` という名前のセットアップが作成されている（GUIの「Analysis」ツリーで確認）
- [ ] `MaximumPasses` プロパティが存在するアプリを選んだ場合、値が `5` に変更されている
- [ ] プロジェクトが保存され、`release_desktop()` で正しく終了している

## 発展課題（任意）

- `setup.props` の内容をすべて確認し（辞書として反復できる）、そのアプリ特有のプロパティ名を
  いくつか調べてみてください。
- `1.normal/hfss/ex01_dipole_antenna/` の `create_setup()` 呼び出しと比較し、
  どのプロパティが引数として明示的に渡されているか確認してみてください。
