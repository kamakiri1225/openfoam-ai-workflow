# セッション001 - プロジェクト立ち上げ〜計算実行

**期間**: 2026-05-08 〜 2026-05-09  
**使用モデル**: Claude Sonnet 4.6 + OpenAI Codex  
**目的**: LLM001プロジェクトの作成・方針決定・gmshモデル作成・計算実行

---

## フェーズ1: プロジェクト立ち上げ（Claude）

### ユーザー指示
> ポンチ絵からOpenFOAMの解析設定を行い計算実行するところまでをLLMで自動化する。
> gmshでモデル・メッシュ・境界条件をすべて作成する。
> やり取りの履歴をスライド用に保存すること。

### 実施内容
- プロジェクトディレクトリ `LLM001/` を作成（`docs/`, `geometry/`, `mesh/`, `case/`, `logs/`）
- ツール選択: gmsh（推奨）を採用
- テンプレート参照先: `ana002_buoyantPimple_circleTempRoughMesh_001`（変更禁止）

---

## フェーズ2: ポンチ絵からgmshスクリプト作成（Claude）

### 解析仕様（20260508_ポンチ絵2.png より）

| 項目 | 値 |
|---|---|
| タンク | 600mm(X) × 1000mm(Y) × 160mm(Z) |
| ポンプA | 中心(150,800)mm, 外径Φ70mm/内径Φ60mm, **流出** 100L/min |
| ポンプB | 中心(450,500)mm, 外径Φ40mm/内径Φ30mm, **流入** 100L/min |
| 流体 | 水（ν=1e-6 m²/s） |
| ソルバー目標 | buoyantPimpleFoam（熱流れ・浮力流れ） |

### 幾何モデルの方針
- ポンプ = 内径・外径を持つ中空円柱（アニュラー形状）のCADソリッド
- 流体領域 = タンク（Box）− ポンプA（中空円柱）− ポンプB（中空円柱）
- OCC（OpenCASCADE）のブーリアン差演算で実現

### 主なデバッグ事例

**問題1: gmsh Python APIのインストール**
```bash
pip3 install --break-system-packages gmsh
sudo apt install python-is-python3
```

**問題2: ブーリアン演算の失敗（coincident face問題）**
- 症状: タンクからポンプが差し引かれず、タンクがそのまま残る
- 原因: ポンプ円柱の底面(z=0)とタンク底面(z=0)が完全に一致するとOCCが差演算を失敗する
- 解決: ポンプ円柱を z=-2mm から開始する（`eps=0.002` オフセット）

**問題3: ポンプモデルの概念的な誤り**
- 最初は「穴を開ける」アプローチ（内径だけ除去）を実装
- 正しくは「中空円柱ソリッド（外径円柱 − 内径円柱）」をタンクから引く
- ユーザー指摘: 「内径と外径を持ったポンプがあり、それはソリッドモデルです」

### 生成ファイル
- `geometry/LLM001_pumpA.py`: gmsh Python API スクリプト
- `geometry/run_gmsh.sh`: メッシュ生成 + gmshToFoam 一括スクリプト

---

## フェーズ3: OpenFOAMケース構築・計算実行（Codex）

### Codexが追加・実装した内容

**アーキテクチャ追加**
- `config/LLM001.yaml`: 解析パラメータを一元管理するYAML設定ファイル
- `tools/generate_openfoam_from_yaml.py`: YAMLからOpenFOAMファイルを自動生成するPythonスクリプト
- `case/Allrun`: gmshToFoam → changeDictionary → checkMesh → simpleFoam を一括実行

**メッシュ変換結果（`log.gmshToFoam`）**
```
Patch 0: pumpWall     (4920 faces)
Patch 1: pumpA_outlet ( 378 faces)
Patch 2: pumpB_inlet  ( 144 faces)
Patch 3: sideWall     ( 530 faces)
Patch 4: frontWall    ( 314 faces)
Patch 5: topWall      (3480 faces)
Patch 6: bottom       (2428 faces)
```
全7パッチ正常検出。

**メッシュ品質（`log.checkMesh`）**
```
Max aspect ratio:        4.46  ← OK
Max non-orthogonality:  51.5°  ← OK
Max skewness:            0.70  ← OK
Total volume:         0.0952 m³
Mesh OK.
```

**計算結果（`log.simpleFoam`）**
```
残差(U, p): ~1e-6  ← 収束
pumpA_outlet の流束: +0.000833 m³/s (= 50 L/min)
pumpB_inlet  の流束: -0.000833 m³/s (= 50 L/min)
実行時間: 228秒（1000ステップ）
```

### 仕様との差異（要対応）

| 項目 | 元の仕様 | Codexの実装 | 備考 |
|---|---|---|---|
| ソルバー | buoyantPimpleFoam | **simpleFoam** | 熱流れ未実装 |
| 流量 | 100 L/min | **50 L/min** | YAML修正が必要 |
| 温度場 | あり | **なし** | T フィールド未作成 |

---

## フェーズ4: AIエージェント化の議論

### ユーザーの問い
> AIエージェントを作ると今回の強みはどこかにでてきますか？

### 強みが出る3つの場面

**1. ポンチ絵→設定の変換**
手書きスケッチと自然言語仕様を、gmsh/OpenFOAMが要求する数十ファイルの設定に変換する「What→How翻訳」。スクリプトでは対応できない入力のゆれをAIが吸収できる。

**2. エラー自己修正ループ**
「ブーリアン演算が無言で失敗する」「メッシュが発散する」といった診断が難しい問題に対して、AIが原因を推定してパラメータを調整し再実行するループを自律的に回せる。今回のcoincident face問題のデバッグがその原型。

**3. パラメータスタディの自動化**
YAMLを書き換えた複数ケースをエージェントが並列生成・実行し、「どのポンプ配置が最も温度分布を均一にするか」を自律探索できる。

---

## 残作業・次のステップ

- [ ] 流量を 50 L/min → 100 L/min に修正（`config/LLM001.yaml` の `flow_L_min`）
- [ ] buoyantPimpleFoamへの切り替えと `T`, `p_rgh`, `alphat` フィールド追加
- [ ] 熱源条件の設定（`pumpWall` に熱流束または温度境界）
- [ ] ParaViewで流速・圧力分布の可視化
- [ ] スライド用スクリーンショット取得

---

## 学んだこと・次回に活かすこと

1. **OCCのcoincident face問題**: ブーリアン演算するソリッドの面が完全に重なると失敗する。`eps` オフセットで回避。
2. **gmshの物理グループとOpenFOAMパッチ**: `addPhysicalGroup(2, tags, name=...)` の名前がそのままパッチ名になる。
3. **changeDictionary の役割**: `gmshToFoam` が出力する `defaultFaces` を正しいパッチに振り分けるために使う。
4. **YAML駆動設計の価値**: 解析パラメータをYAMLに集約することで、AIエージェントが設定を読み書きしやすくなる。
