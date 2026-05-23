# session_010 - ParaView用post.foamの作成

**日時**: 2026-05-09  
**対象**: `LLM001/case/post.foam`, `LLM001/case/Allrun`, `LLM001/case/Allmesh`

---

## 要望

ParaViewでOpenFOAMケースを読むため、ケース直下に空の `post.foam` を作成する。

## 対応

`LLM001/case/post.foam` を作成した。

また、`Allrun` と `Allmesh` の最後に以下を追加した。

```bash
touch post.foam
echo "Created ParaView reader file: post.foam"
```

これにより、メッシュ作成後または解析後に ParaView 用ファイルが自動で用意される。
