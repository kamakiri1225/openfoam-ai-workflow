# session_009 - surfaceFieldValueのwriteFields必須エラー対応

**日時**: 2026-05-09  
**対象**: `LLM001/case/system/controlDict`

---

## 発生したエラー

`simpleFoam` 実行時に以下のエラーが発生した。

```text
FOAM FATAL IO ERROR:
Entry 'writeFields' not found in dictionary
system/controlDict/functions/inletFlowRate
```

## 原因

OpenFOAM 2512 の `surfaceFieldValue` function object で `writeFields` の明示が必要だった。

## 対応

`controlDict` の以下2つの function object に `writeFields false;` を追加した。

- `inletFlowRate`
- `outletFlowRate`

修正例:

```foam
inletFlowRate
{
    type            surfaceFieldValue;
    libs            ("libfieldFunctionObjects.so");
    writeControl    timeStep;
    writeInterval   10;
    log             true;
    writeFields     false;
    regionType      patch;
    name            pumpB_inlet;
    operation       sum;
    fields          (phi);
}
```
