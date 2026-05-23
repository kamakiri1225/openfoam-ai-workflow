# session_006 - wall function用パッチ型エラーへの対応

**日時**: 2026-05-09  
**対象**: `LLM001/case/system/changeDictionaryDict`, `LLM001/case/Allmesh`, `LLM001/case/Allrun`

---

## 発生したエラー

OpenFOAM 2512 で `simpleFoam` 実行時に以下のエラーが発生した。

```text
FOAM FATAL ERROR:
Invalid wall function specification
Patch type for patch pumpWall must be wall
Current patch type is patch
```

## 原因

`gmshToFoam` で変換された境界パッチが OpenFOAM の `patch` 型になっていた。

一方、初期条件ファイルでは以下の壁関数を使用している。

- `nutkWallFunction`
- `kqRWallFunction`
- `omegaWallFunction`

これらの壁関数は、対象パッチの型が `wall` である必要がある。  
そのため、`pumpWall` が `patch` 型のままだと実行時に停止する。

## 対応

`system/changeDictionaryDict` を追加し、`gmshToFoam` 後に壁パッチ型を修正するようにした。

壁にするパッチ:

- `pumpWall`
- `topWall`
- `bottom`
- `sideWall`
- `frontWall`

`patch` のままにするパッチ:

- `pumpB_inlet`
- `pumpA_outlet`

`Allmesh` と `Allrun` に `changeDictionary` 実行を追加した。

実行順:

```bash
gmshToFoam mesh/LLM001_pumpAB.msh
changeDictionary
checkMesh
simpleFoam
```

`Allrun` では、既に `constant/polyMesh` が存在する場合でも毎回 `changeDictionary` を実行する。

## 再実行

```bash
cd LLM001/case
sh Allrun
```

メッシュ変換とチェックだけの場合:

```bash
cd LLM001/case
sh Allmesh
```
