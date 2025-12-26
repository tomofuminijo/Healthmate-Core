# 要件文書

## はじめに

Healthmate App プロダクトの全サービスにおいて、現在実装されている「prod環境の場合はサフィックスを付けない」という判定ロジックを削除し、prod環境でも他の環境と同様にサフィックスを付与するように統一する。これにより、デプロイメントスクリプトの複雑性を削減し、保守性を向上させる。

## 用語集

- **Environment_Suffix**: 環境を識別するためのリソース名末尾の文字列（`-dev`, `-stage`, `-prod`）。AgentCore Runtimeのみ `_dev`, `_stage`, `_prod`
- **Prod_Logic**: 現在のデプロイスクリプトに存在する「prod環境の場合はサフィックスを付けない」という条件分岐処理
- **Deploy_Script**: 各サービスのデプロイメントを実行するスクリプト
- **Healthmate_Service**: Healthmate-Core、Healthmate-HealthManager、Healthmate-CoachAI、Healthmate-Frontend、Healthmate-Appの5つのサービス

## 要件

### 要件1: prod環境判定ロジックの削除

**ユーザーストーリー:** DevOpsエンジニアとして、デプロイスクリプトからprod環境の特別扱いを削除したい。そうすることで、全環境で一貫したリソース命名ができ、スクリプトがシンプルになる。

#### 受け入れ基準

1. THE Deploy_Script SHALL 「prod環境の場合はサフィックスを付けない」というProd_Logicを削除する
2. THE Deploy_Script SHALL 全ての環境（dev、stage、prod）で一貫してEnvironment_Suffixを付与する
3. THE Deploy_Script SHALL 環境パラメータに基づいて単純にサフィックスを決定する
4. THE Deploy_Script SHALL prod環境に関する条件分岐を削除する
5. THE Deploy_Script SHALL 環境判定の複雑性を排除し、統一されたロジックを使用する

### 要件2: Healthmate-Core サービスの更新

**ユーザーストーリー:** システム管理者として、Healthmate-CoreのデプロイスクリプトからProd_Logicを削除したい。そうすることで、認証基盤のデプロイが一貫性を持つようになる。

#### 受け入れ基準

1. THE Deploy_Script SHALL Healthmate-CoreのProd_Logicを削除する
2. THE Deploy_Script SHALL prod環境でも他の環境と同様にサフィックスを付与する
3. THE Deploy_Script SHALL 環境パラメータのみに基づいてリソース名を決定する
4. THE Deploy_Script SHALL CloudFormation exportにも環境サフィックスを含める
5. THE Deploy_Script SHALL CDK設定で環境判定の条件分岐を削除する

### 要件3: Healthmate-HealthManager サービスの更新

**ユーザーストーリー:** バックエンド開発者として、HealthManagerのデプロイスクリプトからProd_Logicを削除したい。そうすることで、MCPサーバーのデプロイが一貫性を持つようになる。

#### 受け入れ基準

1. THE Deploy_Script SHALL HealthManagerのProd_Logicを削除する
2. THE Deploy_Script SHALL prod環境でも他の環境と同様にサフィックスを付与する
3. THE Deploy_Script SHALL DynamoDBテーブル、Lambda関数、AgentCore Gatewayの命名で環境判定を削除する
4. THE Deploy_Script SHALL 環境パラメータのみに基づいてリソース名を決定する
5. THE Deploy_Script SHALL MCP Gateway設定で環境判定の条件分岐を削除する

### 要件4: Healthmate-CoachAI サービスの更新

**ユーザーストーリー:** AI開発者として、CoachAIのデプロイスクリプトからProd_Logicを削除したい。そうすることで、エージェントのデプロイが一貫性を持つようになる。

#### 受け入れ基準

1. THE Deploy_Script SHALL CoachAIのProd_Logicを削除する
2. THE Deploy_Script SHALL prod環境でも他の環境と同様にサフィックスを付与する
3. THE Deploy_Script SHALL AgentCore Runtime名でアンダースコア、その他でハイフンを使用する
4. THE Deploy_Script SHALL 環境パラメータのみに基づいてリソース名を決定する
5. THE Deploy_Script SHALL CloudFormation統合で環境判定の条件分岐を削除する

### 要件5: Healthmate-Frontend サービスの更新

**ユーザーストーリー:** フロントエンド開発者として、FrontendのデプロイスクリプトからProd_Logicを削除したい。そうすることで、Webアプリケーションのデプロイが一貫性を持つようになる。

#### 受け入れ基準

1. THE Deploy_Script SHALL FrontendのProd_Logicを削除する
2. THE Deploy_Script SHALL prod環境でも他の環境と同様にサフィックスを付与する
3. THE Deploy_Script SHALL 環境パラメータのみに基づいてリソース名を決定する
4. THE Deploy_Script SHALL S3バケット、CloudFrontディストリビューションの命名で環境判定を削除する
5. THE Deploy_Script SHALL 環境固有のAPIエンドポイント設定で条件分岐を削除する

### 要件6: Healthmate-App サービスの更新

**ユーザーストーリー:** DevOpsエンジニアとして、統合デプロイシステムからProd_Logicを削除したい。そうすることで、全サービスの一括デプロイが一貫性を持つようになる。

#### 受け入れ基準

1. THE Deploy_Script SHALL Healthmate-AppのProd_Logicを削除する
2. THE Deploy_Script SHALL 全てのHealthmate_Serviceに環境パラメータを一貫して渡す
3. THE Deploy_Script SHALL 統合テストで環境判定の条件分岐を削除する
4. THE Deploy_Script SHALL ログシステムで環境判定の条件分岐を削除する
5. THE Deploy_Script SHALL 環境固有の設定検証で条件分岐を削除する

### 要件7: デプロイスクリプトの簡素化

**ユーザーストーリー:** 開発者として、デプロイスクリプトが単純で理解しやすくなることを望む。そうすることで、保守性が向上し、新しい開発者でも容易に理解できるようになる。

#### 受け入れ基準

1. THE Deploy_Script SHALL 環境判定の複雑な条件分岐を削除する
2. THE Deploy_Script SHALL 環境パラメータベースの単純なロジックのみを使用する
3. THE Deploy_Script SHALL コードの可読性を向上させる
4. THE Deploy_Script SHALL 環境固有の設定を統一された方法で管理する
5. THE Deploy_Script SHALL デバッグとトラブルシューティングを簡素化する