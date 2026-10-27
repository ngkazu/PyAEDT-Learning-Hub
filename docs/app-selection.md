# アプリケーション選択リファレンス

`exercise/0.easy/common_3d/` `common_2d/` `common_schematic/` の課題では、使用する AEDT アプリケーションを
学習者が自分で選ぶ。ここに載せているクラス名対応表を参照し、`starter.py` 冒頭の import とアプリ生成部分を
書き換えるだけで、同じ課題を好きなアプリケーションで進められる。

## クラス名対応表

| 表示名 | フォルダ(slug) | `ansys.aedt.core` クラス名 | 分類 |
|---|---|---|---|
| HFSS | `hfss` | `Hfss` | common_3d |
| Maxwell 3D | `maxwell_3d` | `Maxwell3d` | common_3d |
| Icepak | `icepak` | `Icepak` | common_3d |
| Q3D Extractor | `q3d` | `Q3d` | common_3d |
| IcepakFEA | `mechanical` | `Mechanical`（※表示名と異なる） | common_3d |
| Maxwell 2D | `maxwell_2d` | `Maxwell2d` | common_2d |
| 2D Extractor | `2d_extractor` | `Q2d` | common_2d |
| Circuit | `circuit` | `Circuit` | common_schematic |
| EMIT | `emit` | `Emit` | common_schematic |
| Twin Builder | `twin_builder` | `TwinBuilder` | common_schematic |
| HFSS 3D Layout | `hfss_3d_layout` | `Hfss3dLayout` | （easy対象外） |
| RMxprt | `rmxprt` | `Rmxprt` | （参考。今回のフォルダ対象外） |

※ IcepakFEA（`mechanical`）は表示名とPyAEDTクラス名が一致しない唯一の例。`from ansys.aedt.core import Mechanical`
で読み込む点に注意する。

EDB（`edb`）のみ `ansys.aedt.core` ではなく **PyEDB** パッケージを使う:

```python
from pyedb import Edb
```

## 最小サンプル（common_3d の例）

```python
from ansys.aedt.core import Icepak

AEDT_VERSION = "2026.1"

app = Icepak(version=AEDT_VERSION, new_desktop=True, non_graphical=False)
# ここから先はどのアプリでも共通のコードで進められる
app.release_desktop(close_projects=True, close_desktop=True)
```

`Icepak` の部分を上表のクラス名に差し替えるだけで、他のアプリケーションでも同じ課題を進められる。
