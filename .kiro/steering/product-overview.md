# Healthmate App プロダクト概要

## Product Vision

Healthmate App は、AI駆動の包括的健康管理プラットフォームです。ユーザーが短期・中期・長期の様々な健康目標を達成できるよう、パーソナライズされたAI健康コーチがサポートします。

## Service Architecture

Healthmate App は5つの専門化されたサービスで構成されています：

### Healthmate-Core サービス（認証基盤）
- **役割**: 認証基盤とプロダクト全体の設定管理
- **技術**: Amazon Cognito User Pool + AWS CDK
- **責任**: ユーザー認証、認可、他サービス間の共通設定

### Healthmate-HealthManager サービス
- **役割**: 健康データ管理バックエンド
- **技術**: Model Context Protocol (MCP) サーバー
- **責任**: データ永続化、API提供、認証・認可

### Healthmate-CoachAI サービス  
- **役割**: AI健康コーチエージェント
- **技術**: Amazon Bedrock AgentCore Runtime
- **責任**: パーソナライズされた健康アドバイス、ユーザー対話

### Healthmate-Frontend サービス
- **役割**: Webフロントエンドインターフェース
- **技術**: React + TypeScript + Vite
- **責任**: ユーザーインターフェース、認証フロー、データ可視化

### Healthmate-App サービス（統合管理）
- **役割**: 統合デプロイメント管理とプロジェクト統括
- **技術**: Bash スクリプト + 統合テスト
- **責任**: 一括デプロイ・アンデプロイ、前提条件チェック、サービス間依存関係管理

## Terminology Standards

### 階層構造
- **プロダクト**: Healthmate App（完全なソリューション）
- **ワークスペース**: Healthmate ワークスペース（開発環境）
- **サービス**: 個別サービス（Healthmate-Core、Healthmate-HealthManager、Healthmate-CoachAI、Healthmate-Frontend、Healthmate-App）

### 命名規則
- **サービス名**: 必ず「サービス」を付けて呼ぶ
- **AWS リソース**: `healthmate-` プレフィックス統一
- **コード**: snake_case（関数）、PascalCase（クラス）
- **プロダクト名**: 「Healthmate App」（「Healthmate プロダクト」から変更）

## Integration Points

### データフロー
```
Healthmate-Frontend サービス
    ↓ (JWT Token + User Input)
Healthmate-CoachAI サービス  
    ↓ (MCP Protocol)
Healthmate-HealthManager サービス
    ↓ (DynamoDB Operations)
Health Data Storage
```

### 認証フロー
```
Healthmate-Core サービス (Cognito User Pool)
    ↓ (JWT Token)
All Other Services (認証情報共有)
```

### 通信プロトコル
- **Frontend ↔ AI**: HTTPS API calls（AgentCore Runtime経由）
- **AI ↔ Backend**: Model Context Protocol (MCP)
- **Frontend ↔ Backend**: RESTful API（直接データ操作時）
- **All ↔ Core**: Cognito JWT Token認証

## Deployment Order

### 必須デプロイ順序
```
1. Healthmate-Core サービス（認証基盤）
2. Healthmate-HealthManager サービス（データ基盤）
3. Healthmate-CoachAI サービス（AI エージェント）
4. Healthmate-Frontend サービス（フロントエンド）
```

### 統合管理
```
Healthmate-App サービス
├── 前提条件チェック（check_prerequisites.sh）
├── 一括デプロイ（deploy_all.sh）
├── 一括アンデプロイ（undeploy_all.sh）
└── 統合テスト（test_integration.sh）
```

## 言語設定

- **開発言語**: 日本語でのコミュニケーション
- **チャット機能**: 日本語での対話
- **ドキュメント**: 日本語優先、必要に応じて英語併記