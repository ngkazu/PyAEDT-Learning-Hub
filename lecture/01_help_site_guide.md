# Help サイト・リポジトリの歩き方

このノートは `11_pyaedt_lecture.md`〜`14_post_processing.md`（PyAEDT本編）や
`31_pyedb_basic.md`（PyEDB基礎）で学ぶ**前に**、あるいは学びながら並行して読むためのノートです。
公式ドキュメントサイト（Help サイト）とGitHubリポジトリの「地図」を先に把握しておくと、
講義やノートで出てくるAPIを自分で調べられるようになります。

対象サイト・リポジトリ:

- PyAEDT Help サイト: https://aedt.docs.pyansys.com/version/stable/index.html
- PyEDB Help サイト: https://edb.docs.pyansys.com/version/stable/index.html
- PyAEDT GitHubリポジトリ: https://github.com/ansys/pyaedt
- PyEDB GitHubリポジトリ: https://github.com/ansys/pyedb

---

## 1. なぜ「サイトの地図」を先に知っておくべきか

`11_pyaedt_lecture.md` §2.4「APIの調べ方」で触れている通り、このプロジェクトの課題は
「推測で書かない、その場で確認する」ことを徹底しています。`dir()`/`help()` でも確認できますが、
**どのクラスのメソッドを見ればよいか見当がつかない**ときは、Help サイトのAPI referenceを
俯瞰できると探すスピードが大きく変わります。このノートでは、API referenceが実際にどういう
軸で分類されているかを先に押さえておきます。

---

## 2. PyAEDT Help サイトの構成

トップページ（https://aedt.docs.pyansys.com/version/stable/index.html ）には、
大きく次のセクションがあります。

- **Getting started** — インストール・最初の一歩
- **User guide** — ワークフロー単位の解説記事
- **API reference** — クラス・メソッドのリファレンス（このノートで中心的に扱う）
- **Examples** — 実行可能なサンプルスクリプト集

### 2.1 API referenceの2つの軸

`11_pyaedt_lecture.md` §2.1「パッケージ全体像」で見た

```python
from ansys.aedt.core import Hfss, Icepak, Maxwell3d, Q3d, Circuit
```

という構造は、Help サイトのAPI referenceにもそのまま現れます。ただし分け方は**1つではなく2つ**
あります。

**(A) アプリケーション別**

API reference の "Application and solvers" ページに、`ansys.aedt.core` 直下の
全アプリクラスが一覧で並びます。

```
ansys.aedt.core.hfss.Hfss
ansys.aedt.core.maxwell.Maxwell3d
ansys.aedt.core.maxwell.Maxwell2d
ansys.aedt.core.icepak.Icepak
ansys.aedt.core.q3d.Q3d
ansys.aedt.core.q3d.Q2d
ansys.aedt.core.hfss3dlayout.Hfss3dLayout
ansys.aedt.core.circuit.Circuit
ansys.aedt.core.twinbuilder.TwinBuilder
ansys.aedt.core.mechanical.Mechanical
ansys.aedt.core.rmxprt.Rmxprt
...
```

ここから各アプリクラスのページに飛ぶと、そのアプリ固有のメソッド一覧（例えば `Hfss` なら
`create_setup` の引数が何を受け付けるか等）が見られます。`docs/app-selection.md`
のクラス名対応表は、まさにこの一覧を元にしています。

**(B) 機能（モジュール）別**

API reference にはアプリ別ページとは**別に**、機能ごとのページが並びます。
§2.3「主なサブオブジェクト」の表と対応させると、次のようになります。

| §2.3のサブオブジェクト | 対応する機能ページ |
|---|---|
| `hfss.modeler`（モデル作成） | **Primitives3D** / Primitives2D / PrimitivesCircuit / Primitives3DLayout |
| `hfss.materials`（物性） | **MaterialManagement** |
| `hfss.boundaries`（境界条件・励振） | **Boundaries** |
| `hfss.mesh`（メッシュ） | **Mesh** |
| `hfss.setups` / `create_setup(...)`（セットアップ） | **Setup** / SetupTemplates（アプリ別の既定パラメータ） |
| `hfss.post`（ポスト処理） | **Visualization**（Reports / Post-processing / Graphics / Advanced Visualizationの4層） |

**なぜ2軸あるのか**: アプリクラス（`Hfss`, `Maxwell3d`, ...）は、§2.3で見た通り
`modeler` / `materials` / `boundaries` / `mesh` / `setups` / `post` という**共通の構造**を
持っています。そのため「このアプリで何ができるか」を知りたいときはアプリ別ページを、
「境界条件やセットアップそのものの詳しい引数・戻り値を知りたい」ときは機能別ページを見る、
という使い分けになります。例えば `Setup` ページには

```
* ``Setup`` for HFSS, Maxwell 2D, Maxwell 3D, Q2D Extractor, and Q3D Extractor
* ``Setup3DLayout`` for HFSS 3D Layout
* ``SetupCircuit`` for Circuit and Twin Builder
```

のように、同じ「セットアップ」という概念がアプリ系統ごとに別クラスで実装されていることが
明記されています。アプリ別ページだけを見ていると気づきにくい「このアプリ系統はこのSetupクラスを
使っている」という対応関係が、機能別ページを見ると分かります。

### 2.2 探し方の実践的な手順

1. まず `docs/app-selection.md` で自分が使うアプリのクラス名を確認する。
2. 「このアプリで何ができるか」を知りたい → API reference の **Application and solvers**
   からそのクラスのページへ。
3. 「境界条件・セットアップ・ポスト処理そのものの詳細な引数」を知りたい → API reference の
   **Boundaries** / **Setup** / **Visualization** 等の機能別ページへ。
4. サイト右上または左サイドバーの検索（`Ctrl+F`相当）でメソッド名から探すのも有効。

---

## 3. PyEDB Help サイトの構成

PyEDBは `31_pyedb_basic.md` §1で説明した通り、HFSS 3D Layout/EDBのレイヤー構造
（ECAD）を扱う別パッケージです。Help サイトの構成はPyAEDTと少し異なります。

- **Getting started** — インストール・gRPC/DotNetバックエンドの違い
- **User guide** — ワークフロー単位の解説（stackup、configurationなど）
- **API reference** — `Edb` クラスを起点にした `database` サブパッケージのリファレンス
- **Examples** / **Workflows** — DRC、SI/PIなど用途別のサンプル

### 3.1 PyEDBのAPI referenceは「Edbクラス起点」の1階層

PyAEDTのように「アプリ別」「機能別」の2軸ではなく、PyEDBは `Edb` クラス（唯一のエントリポイント）
から辿れる `database` サブパッケージの中に、`31_pyedb_basic.md` で扱った概念がそれぞれ
サブフォルダとして対応しています。

| `31_pyedb_basic.md` で扱った概念 | `database` サブパッケージ内の対応箇所（目安） |
|---|---|
| スタックアップ（§2） | `layers` |
| ネット（§3） | `net` |
| トレース・プレーン（§4） | `primitive` / `geometry` |
| パッドスタック・ビア（§5） | `hierarchy`（パッドスタックインスタンス等） |
| ポート（§6） | `ports` / `terminal` |

`edb.stackup` / `edb.nets` / `edb.modeler` / `edb.padstacks` / `edb.source_excitation`
といった、普段コードで使っているプロパティ名は、Help サイトのサブパッケージ名と必ずしも
一致しないことがある点に注意してください（例えば `edb.padstacks` の実体は `hierarchy`
サブパッケージ内のクラス）。確実なのは `dir(edb.padstacks)` や `inspect.signature()`
でその場のオブジェクトから直接確認する方法です（`31_pyedb_basic.md` §7と同じ方針）。

---

## 4. GitHubリポジトリの使いどころ

Help サイトは「完成されたドキュメント」ですが、以下のような疑問はソースコードを直接見た方が
早いことがあります。

- このメソッドの引数は本当にこの型で合っているか（型ヒント・docstringを直接読む）
- このバージョンでこの機能はまだ無いのでは？（CHANGELOGやコミット履歴で確認する）
- サンプルコードが動かない、エラーメッセージの正確な原因は何か（実装を直接読む）

### 4.1 PyAEDT: https://github.com/ansys/pyaedt

- `src/ansys/aedt/core/` — パッケージ本体。`hfss.py`, `maxwell.py`, `icepak.py` のように
  アプリクラスがファイル単位で分かれている。`modules/` 配下に `boundary`, `solve_setup` 等、
  機能別の実装がある（§2.1の2軸構成は、実はソースコードのディレクトリ構成そのものに対応している）。
- `doc/source/API/` — Help サイトのAPI referenceページの元になっている `.rst` ファイル。
  ここを見ると、あるクラスがどのページに載っているか（逆引き）が分かる。
- `examples/` — Help サイトの「Examples」に載るサンプルスクリプトの元データ。

### 4.2 PyEDB: https://github.com/ansys/pyedb

- `src/pyedb/grpc/database/` — §3.1の表で挙げた `layers`, `net`, `primitive`, `hierarchy`,
  `ports`, `terminal` 等のサブパッケージの実体。
- `src/pyedb/grpc/edb.py`（またはそれに相当するファイル） — `Edb` クラス本体。

### 4.3 Issueやコミット履歴も有用

「このエラーメッセージで検索する」「このバージョンから挙動が変わっていないか確認する」際は、
GitHubのIssue検索・コミット履歴検索も参考になります（このプロジェクトの課題作成でも、
実際にAEDT上で動作検証しつつ、必要に応じてソースを直接読む方針を取っています。
詳しくは `31_pyedb_basic.md` §7「APIの調べ方」を参照）。

---

## 5. まとめ

- PyAEDTのAPI referenceは **アプリ別**（`Hfss`, `Maxwell3d`, ...）と **機能別**
  （Primitives3D, Boundaries, Setup, Visualization, ...）の2軸がある。アプリオブジェクトの
  サブオブジェクト構造（`11_pyaedt_lecture.md` §2.3）と対応させて探すと迷わない。
- PyEDBのAPI referenceは `Edb` クラス起点の `database` サブパッケージ1本で、
  `31_pyedb_basic.md` で扱った概念（スタックアップ・ネット・配線・ビア・ポート）と対応させられる。
- Help サイトで概要・引数を掴み、詳細や疑問点はGitHubリポジトリのソースコードで確認する、
  という往復がこのプロジェクト全体の基本方針（推測しない、その場で確認する）。

## 次に読むもの

- PyAEDT本体の基本構造に進む: [11_pyaedt_lecture.md](11_pyaedt_lecture.md)
- PyEDBの基礎に進む: [31_pyedb_basic.md](31_pyedb_basic.md)
- アプリ選びに迷ったら: [docs/app-selection.md](../docs/app-selection.md)
- 演習を始める場合は [exercise/README.md](../exercise/README.md) へ。
