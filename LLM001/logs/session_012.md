# session_012 - Allrun/Allmeshの起動パス不具合修正

**日時**: 2026-05-09  
**対象**: `LLM001/Allrun`, `LLM001/Allmesh`, `LLM001/case/Allrun`, `LLM001/case/Allmesh`, `LLM001/geometry/run_gmsh.sh`

---

## 発生したエラー

`./Allrun` 実行時に以下のエラーが出た。

```text
Allmesh: 2: cd: can't cd to Allmesh
Allrun: 2: cd: can't cd to Allrun
```

## 原因

スクリプト冒頭で以下のようにしていた。

```bash
cd "${0%/*}" || exit 1
```

`sh Allrun` のように呼ばれると `$0` が `Allrun` になり、`${0%/*}` も `Allrun` のままになってしまい、`cd Allrun` を実行して失敗していた。

## 対応

各スクリプトの冒頭を以下に変更した。

```bash
cd "$(dirname "$0")" || exit 1
```

また、サブスクリプト呼び出しを `sh Allrun` ではなく `./Allrun` のようにした。

修正後:

```bash
cd LLM001
./Allrun
```

または:

```bash
cd LLM001
./Allmesh
```
