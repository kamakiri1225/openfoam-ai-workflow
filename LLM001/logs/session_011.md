# session_011 - YAML仕様駆動への変更

**日時**: 2026-05-09  
**対象**: `LLM001/config/LLM001.yaml`, `LLM001/geometry/LLM001_pumpA.py`, `LLM001/tools/`, `LLM001/case/`

---

## 要望

次の段階として、ポンプの座標・形状・流量条件・流入/流出の別を YAML ファイルに書き、それを読み込んで gmsh メッシュ作成と OpenFOAM 解析設定まで行う仕様に変更する。

## 追加したYAML仕様

`LLM001/config/LLM001.yaml` を追加した。

主な項目:

- `tank.size_m`
- `mesh.global_size_m`
- `mesh.pump_size_m`
- `fluid.nu_m2_s`
- `simulation.solver`
- `simulation.turbulence_model`
- `pumps`

`pumps` には以下を定義する。

- `id`
- `patch`
- `role`: `inlet` または `outlet`
- `center_m`
- `outer_diameter_m`
- `inner_diameter_m`
- `bottom_offset_m`
- `top`
- `flow_L_min`

## gmsh側の変更

`LLM001/geometry/LLM001_pumpA.py` を YAML 駆動へ変更した。

- タンク寸法を YAML から読む。
- ポンプ数・座標・外径・底面オフセット・上面位置を YAML から読む。
- ポンプをソリッド円柱として作成する。
- タンクから全ポンプを CAD 差分する。
- ポンプの `patch` と `role` に応じて physical group を作成する。
- メッシュサイズや出力先も YAML から読む。

## OpenFOAM側の変更

`LLM001/tools/generate_openfoam_from_yaml.py` を追加した。

このスクリプトは YAML から以下を生成する。

- `case/0/U`
- `case/0/p`
- `case/0/k`
- `case/0/omega`
- `case/0/nut`
- `case/constant/transportProperties`
- `case/constant/turbulenceProperties`
- `case/system/controlDict`
- `case/system/changeDictionaryDict`

`role: inlet` のポンプは `flowRateInletVelocity` になる。  
`role: outlet` のポンプは `p fixedValue 0` の圧力出口になる。

## 実行導線

`LLM001/geometry/run_gmsh.sh` は `config/LLM001.yaml` を `LLM001_pumpA.py` に渡す。

`LLM001/case/Allrun` と `LLM001/case/Allmesh` は、実行前に `generate_openfoam_from_yaml.py` を呼び、YAMLから解析設定を再生成する。

トップレベルにも以下を追加した。

- `LLM001/Allmesh`: YAMLから gmsh メッシュ作成、OpenFOAM変換、checkMesh。
- `LLM001/Allrun`: YAMLから gmsh メッシュ作成、OpenFOAM変換、checkMesh、simpleFoam。

## 使い方

YAMLを編集する。

```bash
LLM001/config/LLM001.yaml
```

メッシュまで:

```bash
cd LLM001
sh Allmesh
```

解析まで:

```bash
cd LLM001
sh Allrun
```

既存のケース内で解析設定だけ再生成する場合:

```bash
cd LLM001/case
python3 ../tools/generate_openfoam_from_yaml.py ../config/LLM001.yaml
```
