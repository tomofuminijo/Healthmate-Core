# 要件文書

## 概要

Healthmate プロダクト全体（Healthmate-Core、Healthmate-HealthManager、Healthmate-CoachAI、Healthmate-Frontend）の本番リリースに向けて、開発環境（dev）、ステージング環境（stage）、本番環境（prod）を適切に分離し、環境に応じたログレベル制御を実装する横断的機能です。現在は開発環境での実行のみですが、本番運用に向けて全サービスでの環境の切り分けとログ管理の最適化が必要です。

この機能は以下のサービスに影響します：
- **Healthmate-Core**: 共通環境設定モジュールの提供、Cognito環境別設定
- **Healthmate-HealthManager**: DynamoDB環境別テーブル、Lambda環境設定
- **Healthmate-CoachAI**: AgentCore環境別デプロイ、MCP環境設定
- **Healthmate-Frontend**: 環境別エンドポイント設定、ビルド設定

## 用語集

- **Environment_Manager**: 環境変数HEALTHMATE_ENVに基づいて環境設定を管理するシステム
- **Log_Controller**: 環境に応じてログレベルを制御するシステム
- **Configuration_Provider**: 各サービスに環境固有の設定を提供するシステム
- **Healthmate_Service**: Healthmate-Core、Healthmate-HealthManager、Healthmate-CoachAI、Healthmate-Frontendの総称

## 要件

### 要件 1

**ユーザーストーリー:** DevOpsエンジニアとして、環境変数を通じてデプロイ環境を制御したい。同じコードベースを異なる環境に安全にデプロイできるようにするため。

#### 受け入れ基準

1. WHEN HEALTHMATE_ENV環境変数が"dev"、"stage"、"prod"に設定されている場合、THE Environment_Manager SHALL その特定の環境に対してすべてのサービスを設定する
2. WHEN HEALTHMATE_ENV環境変数が設定されていない場合、THE Environment_Manager SHALL デフォルトで"dev"環境に設定する
3. WHEN 無効な環境値が提供された場合、THE Environment_Manager SHALL エラーをログに記録し、デフォルトで"dev"環境に設定する
4. THE Environment_Manager SHALL 許可されたリスト["dev", "stage", "prod"]に対して環境値を検証する
5. WHEN 環境設定が読み込まれた場合、THE Environment_Manager SHALL 現在の環境をINFOレベルでログに記録する

### 要件 2

**ユーザーストーリー:** システム管理者として、環境ごとに異なるログレベルを設定したい。開発環境では詳細なデバッグ情報を、本番環境ではクリーンなログを出力するため。

#### 受け入れ基準

1. WHEN 環境が"dev"の場合、THE Log_Controller SHALL ログレベルをDEBUGに設定し、すべてのログメッセージを出力する
2. WHEN 環境が"stage"の場合、THE Log_Controller SHALL ログレベルをINFOに設定し、DEBUGメッセージを抑制する
3. WHEN 環境が"prod"の場合、THE Log_Controller SHALL ログレベルをWARNINGに設定し、DEBUGとINFOメッセージを抑制する
4. THE Log_Controller SHALL すべてのHealthmate_Serviceで一貫したログフォーマットを適用する
5. WHEN ログレベルが変更された場合、THE Log_Controller SHALL 新しいログレベルで変更をログに記録する

### 要件 3

**ユーザーストーリー:** 開発者として、AWSリソースの環境固有設定を使用したい。開発、ステージング、本番で異なるリソースを使用するため。

#### 受け入れ基準

1. WHEN 環境が"dev"の場合、THE Configuration_Provider SHALL "-dev"サフィックス付きの開発用AWSリソース名を使用する
2. WHEN 環境が"stage"の場合、THE Configuration_Provider SHALL "-stage"サフィックス付きのステージング用AWSリソース名を使用する
3. WHEN 環境が"prod"の場合、THE Configuration_Provider SHALL サフィックスなしの本番用AWSリソース名を使用する
4. THE Configuration_Provider SHALL すべてのHealthmate_Serviceに対して環境固有のDynamoDBテーブル名を提供する
5. THE Configuration_Provider SHALL 環境固有のCognito User Pool設定を提供する
6. THE Configuration_Provider SHALL 環境固有のAgentCore Gatewayエンドポイントを提供する

### 要件 4

**ユーザーストーリー:** 開発者として、すべてのHealthmateサービス間で一貫した環境設定を使用したい。すべてのサービスが同じ環境コンテキストで動作するようにするため。

#### 受け入れ基準

1. THE Environment_Manager SHALL すべてのHealthmate_Serviceでインポート可能な共有設定モジュールを提供する
2. WHEN 任意のHealthmate_Serviceが開始される場合、THE Environment_Manager SHALL 一貫した環境検出を保証する
3. THE Configuration_Provider SHALL Healthmate-Coreサービスの環境固有設定を維持する
4. THE Configuration_Provider SHALL Healthmate-HealthManagerサービスの環境固有設定を維持する
5. THE Configuration_Provider SHALL Healthmate-CoachAIサービスの環境固有設定を維持する
6. THE Configuration_Provider SHALL Healthmate-Frontendサービスの環境固有設定を維持する

### 要件 5

**ユーザーストーリー:** システム管理者として、環境コンテキストを含む構造化ログを使用したい。環境間で効果的に監視とトラブルシューティングを行うため。

#### 受け入れ基準

1. THE Log_Controller SHALL すべてのログメッセージに環境情報を含める
2. THE Log_Controller SHALL すべてのログメッセージにサービス名を含める
3. THE Log_Controller SHALL "stage"と"prod"環境で構造化ログにJSON形式を使用する
4. THE Log_Controller SHALL "dev"環境で人間が読みやすい形式のログを使用する
5. WHEN エラーが発生した場合、THE Log_Controller SHALL 環境に関係なく常にログに記録する
6. THE Log_Controller SHALL すべてのログエントリにタイムスタンプ、ログレベル、サービス名、環境を含める

### 要件 6

**ユーザーストーリー:** DevOpsエンジニアとして、デプロイ時の環境検証を行いたい。ユーザーに影響を与える前に設定エラーを防ぐため。

#### 受け入れ基準

1. WHEN CDKデプロイが開始される場合、THE Environment_Manager SHALL リソース作成前にHEALTHMATE_ENVを検証する
2. WHEN 環境固有リソースが作成される場合、THE Configuration_Provider SHALL リソース命名規則を検証する
3. WHEN 無効な環境設定が検出された場合、THE Environment_Manager SHALL 明確なエラーメッセージでデプロイを失敗させる
4. THE Environment_Manager SHALL 検証チェックを通じて間違った環境への偶発的なデプロイを防ぐ
5. WHEN デプロイが完了した場合、THE Environment_Manager SHALL 成功した環境設定をログに記録する

### 要件 7

**ユーザーストーリー:** 開発者として、移行期間中の後方互換性を維持したい。環境分離を実装している間、既存のデプロイメントが継続して動作するようにするため。

#### 受け入れ基準

1. WHEN 既存のデプロイメントでHEALTHMATE_ENVが設定されていない場合、THE Environment_Manager SHALL 現在の動作を維持する
2. THE Configuration_Provider SHALL 移行期間中にレガシーと新しい設定方法の両方をサポートする
3. WHEN レガシー設定が検出された場合、THE Environment_Manager SHALL 非推奨警告をログに記録する
4. THE Environment_Manager SHALL 現在の単一環境から複数環境セットアップへの移行パスを提供する
5. WHEN 新しい環境設定が適用された場合、THE Environment_Manager SHALL 既存のデータと設定を保持する

### 要件 8

**ユーザーストーリー:** 各サービスの開発者として、サービス固有の環境設定を適切に管理したい。各サービスの特性に応じた環境別設定を実現するため。

#### 受け入れ基準

1. WHEN Healthmate-Coreサービスがデプロイされる場合、THE Configuration_Provider SHALL 環境別のCognito User Pool名とCloudFormation Export名を設定する
2. WHEN Healthmate-HealthManagerサービスがデプロイされる場合、THE Configuration_Provider SHALL 環境別のDynamoDBテーブル名とLambda関数名を設定する
3. WHEN Healthmate-CoachAIサービスがデプロイされる場合、THE Configuration_Provider SHALL 環境別のAgentCore設定とIAMロール名を設定する
4. WHEN Healthmate-Frontendサービスがビルドされる場合、THE Configuration_Provider SHALL 環境別のAPI エンドポイントとCognito設定を提供する
5. THE Configuration_Provider SHALL 各サービスで環境変数ファイル（.env.dev、.env.stage、.env.prod）をサポートする

### 要件 9

**ユーザーストーリー:** DevOpsエンジニアとして、段階的な実装とテストを行いたい。各サービスの環境設定を確実に動作確認してから次のサービスに進むため。

#### 受け入れ基準

1. THE Environment_Manager SHALL Healthmate-Core → Healthmate-HealthManager → Healthmate-CoachAI → Healthmate-Frontendの順序で実装をサポートする
2. WHEN Healthmate-Coreサービスの環境設定が完了した場合、THE Environment_Manager SHALL 環境別Cognito設定の動作テストを可能にする
3. WHEN Healthmate-HealthManagerサービスの環境設定が完了した場合、THE Environment_Manager SHALL 環境別DynamoDB接続とMCP動作テストを可能にする
4. WHEN Healthmate-CoachAIサービスの環境設定が完了した場合、THE Environment_Manager SHALL 環境別AgentCore デプロイとMCP連携テストを可能にする
5. WHEN Healthmate-Frontendサービスの環境設定が完了した場合、THE Environment_Manager SHALL 全サービス統合での環境別動作テストを可能にする
6. THE Environment_Manager SHALL 各段階で前のサービスとの連携テストを実行可能にする