# session_007 - changeDictionary実行対象の修正

**日時**: 2026-05-09  
**対象**: `LLM001/case/Allrun`, `LLM001/case/Allmesh`

---

## 発生した警告

`changeDictionary` 実行時に以下の警告が出た。

```text
Requested field to change dictionaryReplacement does not exist in ".../LLM001/case/0"
```

## 原因

`changeDictionary` をオプションなしで実行していたため、OpenFOAM がデフォルトで `0/` 配下のフィールド辞書を変更対象として見に行っていた。

今回変更したいのは `constant/polyMesh/boundary` のパッチ型であり、`0/` のフィールドではない。

## 対応

`Allrun` と `Allmesh` の `changeDictionary` 実行を以下に変更した。

```bash
changeDictionary -constant
```

これにより、`system/changeDictionaryDict` の `boundary` 変更が `constant/polyMesh/boundary` に適用される。

## 修正後の実行順

```bash
gmshToFoam mesh/LLM001_pumpAB.msh
changeDictionary -constant
checkMesh
simpleFoam
```
