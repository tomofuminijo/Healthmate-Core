# Healthmate プロダクト概要

## Product Vision

Healthmate プロダクトは、AI駆動の包括的健康管理プラットフォームです。ユーザーが長期的な健康目標（100歳まで健康に生きるなど）を達成できるよう支援します。

## Service Architecture

Healthmate プロダクトは4つの独立したサービスで構成されています：

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

## Terminology Standards

### 階層構造
- **プロダクト**: Healthmate プロダクト（完全なソリューション）
- **ワークスペース**: Healthmate ワークスペース（開発環境）
- **サービス**: 個別サービス（Healthmate-Core、Healthmate-HealthManager、Healthmate-CoachAI、Healthmate-Frontend）

### 命名規則
- **サービス名**: 必ず「サービス」を付けて呼ぶ
- **AWS リソース**: `healthmate-` プレフィックス統一
- **コード**: snake_case（関数）、PascalCase（クラス）

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

## 言語設定

- **開発言語**: 日本語でのコミュニケーション
- **チャット機能**: 日本語での対話
- **ドキュメント**: 日本語優先、必要に応じて英語併記