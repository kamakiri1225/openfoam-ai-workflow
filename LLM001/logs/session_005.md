# session_005 - gmshメッシュのコピーとOpenFOAM変換手順の明示

**日時**: 2026-05-09  
**対象**: `LLM001/case/Allmesh`, `LLM001/case/Allrun`, `LLM001/case/mesh/`

---

## ユーザー要望

- 先ほど gmsh で作成したメッシュをコピーして使う。
- OpenFOAM 用への変換も必要。
- スケールに注意する。

## 対応

`LLM001/mesh/LLM001_pumpAB.msh` を `LLM001/case/mesh/LLM001_pumpAB.msh` にコピーした。

`Allmesh` と `Allrun` を修正し、以下の流れにした。

1. `../mesh/LLM001_pumpAB.msh` の存在を確認する。
2. `case/mesh/LLM001_pumpAB.msh` へコピーする。
3. コピーした `.msh` を `gmshToFoam` で `constant/polyMesh` に変換する。
4. `checkMesh` を実行する。
5. `Allrun` の場合は続けて `simpleFoam` を実行する。

`Allrun` は、既に `constant/polyMesh` がある場合でも、`case/mesh/LLM001_pumpAB.msh` が `constant/polyMesh/points` より新しければ再変換するようにした。

## スケール

`LLM001_pumpA.py` のジオメトリは以下のようにSI単位[m]で作成されている。

- タンクX: `0.600`
- タンクY: `1.000`
- タンクZ: `0.160`

したがって、OpenFOAM変換時に mm から m への `0.001` スケール変換は不要。  
今回の設定では `MESH_SCALE=1` と明示し、`.msh` 座標をそのままOpenFOAMへ渡す。

## 実行

メッシュ変換のみ:

```bash
cd LLM001/case
sh Allmesh
```

メッシュ変換から解析まで:

```bash
cd LLM001/case
sh Allrun
```

手動で行う場合:

```bash
cd LLM001/case
mkdir -p mesh
cp ../mesh/LLM001_pumpAB.msh mesh/LLM001_pumpAB.msh
gmshToFoam mesh/LLM001_pumpAB.msh
checkMesh
simpleFoam
```
