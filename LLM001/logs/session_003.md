# session_003 - OpenFOAM解析設定の初期作成

**日時**: 2026-05-09  
**対象**: `LLM001/case/`  

---

## ユーザー要望

- ポンチ絵・解析仕様の確定と gmsh ジオメトリ作成までは完了した認識。
- 次に OpenFOAM での解析設定へ進む。
- タンク内流体は水を想定する。

## 解析モデル方針

- 水の非圧縮・等温流れとして扱う。
- まずは定常解析 `simpleFoam` 用ケースを作成する。
- ポンプBを流量入口、ポンプAを圧力出口とする。
- ポンプ流量は 100 L/min = `0.0016666667 m3/s`。
- 水の動粘度は 20 degC 程度の代表値として `nu = 1.0e-06 m2/s`。
- ポンプB外径 40 mm、100 L/min の代表速度は約 `1.33 m/s`。
- レイノルズ数はおよそ `5e4` なので、初期設定は乱流 `kOmegaSST` とする。

## 追加したファイル

### 初期条件

- `LLM001/case/0/U`
- `LLM001/case/0/p`
- `LLM001/case/0/k`
- `LLM001/case/0/omega`
- `LLM001/case/0/nut`

### 物性・乱流モデル

- `LLM001/case/constant/transportProperties`
- `LLM001/case/constant/turbulenceProperties`

### 数値設定

- `LLM001/case/system/controlDict`
- `LLM001/case/system/fvSchemes`
- `LLM001/case/system/fvSolution`
- `LLM001/case/system/decomposeParDict`

### 実行補助

- `LLM001/case/Allrun`
- `LLM001/case/Allclean`

## 境界条件

### `pumpB_inlet`

- `U`: `flowRateInletVelocity`
- `volumetricFlowRate`: `0.0016666667 m3/s`
- `p`: `zeroGradient`
- `k`: `fixedValue 0.0066`
- `omega`: `fixedValue 53`

### `pumpA_outlet`

- `U`: `pressureInletOutletVelocity`
- `p`: `fixedValue 0`
- `k`, `omega`: `inletOutlet`

### 壁面

対象:

- `pumpWall`
- `topWall`
- `bottom`
- `sideWall`
- `frontWall`

設定:

- `U`: `noSlip`
- `p`: `zeroGradient`
- `k`: `kqRWallFunction`
- `omega`: `omegaWallFunction`
- `nut`: `nutkWallFunction`

## 未検証事項

- この環境では `simpleFoam` が見つからなかったため、OpenFOAM実行確認は未実施。
- gmshから変換した `constant/polyMesh` がある状態で、OpenFOAM環境を source して以下を実行する。

```bash
cd LLM001/case
checkMesh
simpleFoam
```

または:

```bash
cd LLM001/case
./Allrun
```

## 次に確認すること

- `gmshToFoam` 後の `constant/polyMesh/boundary` に、以下のパッチが存在すること。
  - `pumpB_inlet`
  - `pumpA_outlet`
  - `pumpWall`
  - `topWall`
  - `bottom`
  - `sideWall`
  - `frontWall`
- `checkMesh` で negative volume や重大な non-orthogonality がないこと。
- `simpleFoam` の流量モニタで、入口・出口流量が概ね釣り合うこと。
