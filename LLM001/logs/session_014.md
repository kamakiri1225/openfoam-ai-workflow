# session_014 - Allcleanスクリプト追加

**日時**: 2026-05-09  
**対象**: `LLM001/Allclean`, `LLM001/case/Allclean`

---

## 要望

トップレベルから実行できる `./Allclean` スクリプトが欲しい。

## 対応

`LLM001/Allclean` を追加した。

実行:

```bash
cd LLM001
./Allclean
```

トップレベルの `Allclean` は以下を行う。

- `case/Allclean` を実行する。
- `mesh/LLM001_pumpAB.msh` を削除する。

`LLM001/case/Allclean` も拡張した。

削除対象:

- 計算時刻ディレクトリ `[1-9]*`
- `processor*`
- `postProcessing`
- `log.*`
- `dynamicCode`
- `constant/polyMesh`
- `case/mesh`
- `post.foam`

`0/`, `constant/transportProperties`, `constant/turbulenceProperties`, `system/` の設定ファイルは残す。
