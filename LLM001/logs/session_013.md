# session_013 - 0/Uの流量条件にL/minコメントを追加

**日時**: 2026-05-09  
**対象**: `LLM001/tools/generate_openfoam_from_yaml.py`, `LLM001/case/0/U`

---

## 要望

YAMLでは流量を `flow_L_min` として L/min で指定しているが、OpenFOAM の `0/U` では `m3/s` に変換される。

変換後の値だけだと元の指定値が分かりにくいため、`0/U` の `volumetricFlowRate` 行に L/min のコメントを残したい。

## 対応

`generate_openfoam_from_yaml.py` の `generate_u()` を修正し、`role: inlet` のポンプについて以下の形式で出力するようにした。

```foam
volumetricFlowRate  constant 0.0008333333333; // 50 L/min
```

現在の YAML では `pumpB_inlet` が `50 L/min` のため、既存の `case/0/U` も同じコメント付きに修正した。

## 注意

このCodex実行環境の Windows 側では `python.exe` が起動できないため、自動再生成は失敗した。OpenFOAM/WSL 側で `Allrun` または `Allmesh` を実行すると、修正後の生成スクリプトにより同じコメント付きで `0/U` が再生成される。
