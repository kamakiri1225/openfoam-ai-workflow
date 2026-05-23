# LLM001 ファイル構成と役割

このドキュメントでは、現在の `LLM001` プロジェクトのファイル構成、各ファイルの役割、YAML 仕様から gmsh メッシュ作成、OpenFOAM 解析実行までの流れを説明します。

## 全体像

現在の構成では、以下の YAML ファイルを仕様の中心にしています。

```text
config/LLM001.yaml
```

この YAML に、以下の情報をまとめています。

- タンク寸法
- ポンプ座標
- ポンプ外径・内径
- ポンプ下面位置
- 流入・流出の別
- 流量 L/min
- メッシュサイズ
- 水の物性
- OpenFOAM ソルバ設定

全体の流れは以下です。

```text
config/LLM001.yaml
    |
    +--> geometry/LLM001_pumpA.py
    |       -> mesh/LLM001_pumpAB.msh
    |
    +--> tools/generate_openfoam_from_yaml.py
            -> case/0/*
            -> case/constant/*
            -> case/system/*

mesh/LLM001_pumpAB.msh
    -> case/mesh/LLM001_pumpAB.msh
    -> gmshToFoam
    -> case/constant/polyMesh
    -> changeDictionary
    -> checkMesh
    -> simpleFoam
```

## トップレベルのファイル

### `Allmesh`

メッシュ作成と OpenFOAM 形式への変換を行うスクリプトです。

```bash
cd LLM001
./Allmesh
```

内部では以下を呼びます。

```text
geometry/run_gmsh.sh
```

`run_gmsh.sh` は gmsh メッシュを作成し、OpenFOAM コマンドが使える場合は `case/Allmesh` も呼びます。

### `Allrun`

YAML からメッシュ作成、OpenFOAM 変換、解析実行までを一括で行うスクリプトです。

```bash
cd LLM001
./Allrun
```

主な処理は以下です。

1. YAML から gmsh メッシュを作成する。
2. YAML から OpenFOAM 辞書ファイルを作成する。
3. `.msh` を `case/mesh/` にコピーする。
4. `gmshToFoam` で OpenFOAM メッシュに変換する。
5. `changeDictionary` で壁パッチを `wall` 型に変更する。
6. `checkMesh` を実行する。
7. `simpleFoam` を実行する。
8. ParaView 用の `post.foam` を作成する。

### `Allclean`

生成されたメッシュや計算結果を削除するスクリプトです。

```bash
cd LLM001
./Allclean
```

削除するもの:

- `mesh/LLM001_pumpAB.msh`
- `case/constant/polyMesh`
- `case/mesh`
- `100`, `200` などの時刻ディレクトリ
- `postProcessing`
- `log.*`
- `post.foam`

残すもの:

- `config/`
- `geometry/`
- `tools/`
- `case/0`
- `case/constant/transportProperties`
- `case/constant/turbulenceProperties`
- `case/system`

## `config/`

### `config/LLM001.yaml`

プロジェクトの中心となる仕様ファイルです。

タンク寸法:

```yaml
tank:
  size_m: [0.600, 1.000, 0.160]
```

ポンプ定義の例:

```yaml
pumps:
  - id: pumpB
    patch: pumpB_inlet
    role: inlet
    center_m: [0.450, 0.500]
    outer_diameter_m: 0.040
    inner_diameter_m: 0.030
    bottom_offset_m: 0.010
    top: tankTop
    flow_L_min: 50.0
```

各項目の意味:

- `id`: ポンプの識別名
- `patch`: gmsh と OpenFOAM で使う境界パッチ名
- `role`: `inlet` または `outlet`
- `center_m`: タンク平面上のポンプ中心座標
- `outer_diameter_m`: CAD 差分に使うポンプ外径
- `inner_diameter_m`: 設計情報として記録している内径
- `bottom_offset_m`: タンク底面からポンプ下面までの距離
- `top`: `tankTop` の場合、ポンプ上面はタンク上面まで届く
- `flow_L_min`: 流量 L/min

## `geometry/`

gmsh による形状作成とメッシュ作成を担当します。

### `geometry/LLM001_pumpA.py`

`config/LLM001.yaml` を読み込み、gmsh の CAD モデルを作成します。

主な役割:

- タンクソリッドを作成する。
- ポンプソリッドを作成する。
- タンクからポンプを CAD 差分で引く。
- 境界面を Physical Group に分類する。
- gmsh メッシュを生成する。
- `mesh/LLM001_pumpAB.msh` を出力する。

生成する Physical Group:

- YAML の `pumps[].patch` で指定したポンプ流入・流出パッチ
- `pumpWall`
- `topWall`
- `bottom`
- `sideWall`
- `frontWall`
- 体積グループ `fluid`

### `geometry/run_gmsh.sh`

gmsh メッシュ作成用の実行スクリプトです。

```bash
cd LLM001/geometry
./run_gmsh.sh
```

内部では以下を実行します。

```bash
python3 LLM001_pumpA.py --config ../config/LLM001.yaml
```

OpenFOAM の `gmshToFoam` が使える環境であれば、続けて以下も実行します。

```bash
cd ../case
./Allmesh
```

## `tools/`

YAML の読み込みや OpenFOAM 辞書ファイル生成を担当する補助スクリプト置き場です。

### `tools/config_io.py`

YAML 設定ファイルを読み込むためのモジュールです。

まず PyYAML を使おうとします。PyYAML がない場合は、現在の `LLM001.yaml` の構造を読める簡易パーサを使います。

### `tools/generate_openfoam_from_yaml.py`

`config/LLM001.yaml` から OpenFOAM の辞書ファイルを生成するスクリプトです。

生成するファイル:

- `case/0/U`
- `case/0/p`
- `case/0/k`
- `case/0/omega`
- `case/0/nut`
- `case/constant/transportProperties`
- `case/constant/turbulenceProperties`
- `case/system/controlDict`
- `case/system/changeDictionaryDict`

YAML の流量指定:

```yaml
flow_L_min: 50.0
```

OpenFOAM では `m3/s` に変換されます。

```foam
volumetricFlowRate  constant 0.0008333333333; // 50 L/min
```

OpenFOAM の値は `m3/s` ですが、元の L/min 値をコメントで残しています。

## `mesh/`

gmsh で作成されたメッシュを置くディレクトリです。

### `mesh/LLM001_pumpAB.msh`

gmsh 2.2 形式のメッシュファイルです。`gmshToFoam` で OpenFOAM メッシュへ変換します。

これは生成物なので、以下で削除できます。

```bash
./Allclean
```

## `case/`

OpenFOAM のケースディレクトリです。

### `case/Allmesh`

OpenFOAM 側のメッシュ変換とチェックを行います。

主な処理:

1. YAML から OpenFOAM 辞書を生成する。
2. `../mesh/LLM001_pumpAB.msh` を `case/mesh/LLM001_pumpAB.msh` にコピーする。
3. `gmshToFoam` を実行する。
4. `changeDictionary -constant -noZero` を実行する。
5. `checkMesh` を実行する。
6. `post.foam` を作成する。

### `case/Allrun`

OpenFOAM 解析を実行します。

主な処理:

1. YAML から OpenFOAM 辞書を生成する。
2. 必要に応じてメッシュをコピーする。
3. 必要に応じて `gmshToFoam` を実行する。
4. `changeDictionary -constant -noZero` を実行する。
5. `checkMesh` を実行する。
6. `simpleFoam` を実行する。
7. `post.foam` を作成する。

### `case/Allclean`

OpenFOAM の計算結果と変換済みメッシュを削除します。

### `case/0/`

初期条件と境界条件を置くディレクトリです。

以下のコマンドで YAML から再生成されます。

```bash
python3 ../tools/generate_openfoam_from_yaml.py ../config/LLM001.yaml
```

主なファイル:

- `U`: 速度境界条件
- `p`: 圧力境界条件
- `k`: 乱流エネルギー
- `omega`: 比散逸率
- `nut`: 乱流粘性

### `case/constant/`

物性値と OpenFOAM メッシュを置きます。

主なファイル・ディレクトリ:

- `transportProperties`: 水の動粘度
- `turbulenceProperties`: 乱流モデル設定
- `polyMesh/`: `gmshToFoam` で生成される OpenFOAM メッシュ

### `case/system/`

OpenFOAM の数値設定と実行設定を置きます。

主なファイル:

- `controlDict`: ソルバ、時間設定、function object
- `fvSchemes`: 離散化スキーム
- `fvSolution`: 線形ソルバと SIMPLE 設定
- `decomposeParDict`: 並列計算用設定
- `changeDictionaryDict`: `gmshToFoam` 後のパッチ型変換

`changeDictionaryDict` は、`gmshToFoam` 後に `patch` 型になっている壁面を `wall` 型に変更します。壁関数を使うには OpenFOAM のパッチ型が `wall` である必要があります。

## `img/`

ポンチ絵や目標形状の画像を置いています。

用途:

- 元のポンチ絵の確認
- 目標形状との比較
- 現在のメッシュ結果との比較

## `logs/`

会話と作業履歴を保存しています。

```text
session_001.md
session_002.md
...
```

各ログには以下を記録します。

- 要望
- 発生したエラー
- 原因
- 修正内容
- 未検証事項
- 次に確認すること

## 推奨実行手順

### YAML から解析まで一括実行

```bash
source /usr/lib/openfoam/openfoam2512/etc/bashrc
cd LLM001
./Allrun
```

### メッシュ作成とチェックのみ

```bash
source /usr/lib/openfoam/openfoam2512/etc/bashrc
cd LLM001
./Allmesh
```

### OpenFOAM 辞書だけ再生成

```bash
cd LLM001/case
python3 ../tools/generate_openfoam_from_yaml.py ../config/LLM001.yaml
```

### 生成物を削除

```bash
cd LLM001
./Allclean
```

## 注意点

- gmsh の形状は SI 単位、つまり m 単位で作成しています。
- `gmshToFoam` 時に `0.001` 倍する必要はありません。
- YAML の `flow_L_min` は OpenFOAM では `m3/s` に変換されます。
- `case/0/U` には元の L/min 値をコメントとして残します。
- ParaView で読むために `case/post.foam` を作成します。
