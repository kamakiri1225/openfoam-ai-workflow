# session_004 - OpenFOAMメッシュ未作成への対応

**日時**: 2026-05-09  
**対象**: `LLM001/case/Allrun`, `LLM001/case/Allmesh`  

---

## 状況

ユーザーが `simpleFoam` を実行したところ、OpenFOAMケース内にメッシュがない状態だった。

確認したところ:

- `LLM001/mesh/LLM001_pumpAB.msh` は存在していた。
- `LLM001/case/constant/polyMesh` は存在していなかった。

つまり、gmsh形式の `.msh` はあるが、OpenFOAM形式の `constant/polyMesh` へ未変換だった。

## 対応

`LLM001/case/Allrun` を修正し、`simpleFoam` の前に以下を行うようにした。

- `constant/polyMesh/points` がなければ `../mesh/LLM001_pumpAB.msh` を `gmshToFoam` で変換する。
- 変換後に `checkMesh` を実行する。
- その後 `simpleFoam` を実行する。

また、メッシュ変換だけを行うための `LLM001/case/Allmesh` を追加した。

## 実行手順

OpenFOAM環境を source 済みのシェルで、以下を実行する。

```bash
cd LLM001/case
./Allmesh
```

解析まで一括実行する場合:

```bash
cd LLM001/case
./Allrun
```

手動で実行する場合:

```bash
cd LLM001/case
gmshToFoam ../mesh/LLM001_pumpAB.msh
checkMesh
simpleFoam
```

## 注意

`simpleFoam` は `constant/polyMesh` を読むだけで、`.msh` を自動変換しない。  
そのため、`simpleFoam` の前に必ず `gmshToFoam` が必要。
