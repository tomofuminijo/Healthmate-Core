# Healthmate プロダクト - Agent Steering

## 概要

このディレクトリには、Healthmate プロダクト全体のAgent Steeringファイルが集約されています。Healthmate-Core サービスが認証基盤として中核的な位置づけにあるため、全サービスの情報をここに一元化しています。

## Steering Files

### 🏗️ プロダクト全体
- **[product-overview.md](./product-overview.md)**: プロダクト概要とサービス構成
- **[tech-stack.md](./tech-stack.md)**: 技術スタックと開発ツール
- **[project-structure.md](./project-structure.md)**: プロジェクト構造と命名規則

### 🔧 個別サービス
- **[healthmanager-service.md](./healthmanager-service.md)**: HealthManager MCPサーバー
- **[coachai-service.md](./coachai-service.md)**: CoachAI エージェント
- **[ui-service.md](./ui-service.md)**: UI フロントエンド

## 重要な変更点

### 🏠 中央集約化
- **以前**: 各ワークスペースに個別のsteering files
- **現在**: Healthmate-Core に全て集約
- **理由**: Healthmate-Core が認証基盤として中核的役割を担うため

### 🗣️ 言語設定
- **チャット**: 日本語での対話
- **開発**: 日本語でのコミュニケーション
- **ドキュメント**: 日本語優先、必要に応じて英語併記

### 🐍 Python環境
- **必須**: 全てのPythonコマンドは仮想環境内で実行
- **セットアップ**: `python3 -m venv .venv && source .venv/bin/activate`
- **依存関係**: `pip install -r requirements.txt`

## 使用方法

### 新規開発時
1. 該当するサービスのsteering fileを参照
2. プロダクト全体のcontext（product-overview.md）を確認
3. 技術スタック（tech-stack.md）に従って開発環境をセットアップ

### 既存機能修正時
1. project-structure.md でファイル配置を確認
2. 該当サービスのpatternとbest practicesを参照
3. 統合テストで他サービスへの影響を確認

### 新機能追加時
1. product-overview.md でサービス間の責任分界を確認
2. 適切なサービスに機能を配置
3. 必要に応じて他サービスとの連携パターンを実装

## サービス間連携

### 認証フロー
```
Healthmate-Core (Cognito) → 全サービス (JWT Token)
```

### データフロー
```
HealthmateUI → HealthCoachAI → HealthManager → DynamoDB
```

### デプロイ順序
```
1. Healthmate-Core (認証基盤)
2. Healthmate-HealthManager (データ基盤)  
3. Healthmate-CoachAI (AI エージェント)
4. HealthmateUI (フロントエンド)
```

## 開発ガイドライン

### Python仮想環境
```bash
# 各サービスで必須
cd {service-directory}
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### テスト実行
```bash
# 単体テスト
pytest tests/unit/ -v

# 統合テスト（サービス固有）
python test_integration.py
```

### コード品質
```bash
# フォーマット
black .

# 型チェック
mypy .

# リント
flake8 .
```

## 更新履歴

- **2024-12**: Healthmate-Core への中央集約化
- **2024-12**: 日本語対応とPython仮想環境の必須化
- **2024-12**: AgentCore Memory統合とセッション継続性の追加