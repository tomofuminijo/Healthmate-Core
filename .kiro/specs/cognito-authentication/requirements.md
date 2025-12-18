# 要件定義書

## はじめに

Healthmate-Core サービスは、Healthmate プロダクトの認証基盤を管理するサービスです。Amazon Cognito User Pool を使用してユーザー認証機能を提供し、他のHealthmate サービス（HealthManager、CoachAI、UI）が共通して利用できる認証インフラを構築します。

## 用語集

- **Healthmate-Core**: 認証基盤を管理するサービス
- **Cognito User Pool**: AWS のユーザー認証サービス
- **User Pool Client**: Cognito User Pool にアクセスするためのクライアント設定
- **CloudFormation Stack**: AWS リソースを管理するためのインフラストラクチャコード
- **CDK**: AWS Cloud Development Kit、インフラストラクチャをコードで定義するツール

## 要件

### 要件 1

**ユーザーストーリー:** 開発者として、Healthmate プロダクトの認証基盤を構築したいので、Cognito User Pool を CDK で管理できるようにしたい

#### 受け入れ基準

1. WHEN CDK デプロイを実行する THEN システムは Cognito User Pool を作成する
2. WHEN User Pool を作成する THEN システムは名前を "Healthmate-userpool" に設定する
3. WHEN User Pool を作成する THEN システムは適切なセキュリティ設定を適用する
4. WHEN User Pool Client を作成する THEN システムは Client Secret を無効にする
5. WHEN CloudFormation Stack をデプロイする THEN システムは Stack 名を "Healthmate-CoreStack" に設定する

### 要件 2

**ユーザーストーリー:** 他のサービスの開発者として、認証に必要な情報を取得したいので、CloudFormation Output から User Pool の情報を参照できるようにしたい

#### 受け入れ基準

1. WHEN CloudFormation Stack がデプロイされる THEN システムは UserPoolId を Output として出力する
2. WHEN CloudFormation Stack がデプロイされる THEN システムは UserPoolClientId を Output として出力する
3. WHEN Output 値を参照する THEN システムは他のサービスから参照可能な形式で提供する

### 要件 3

**ユーザーストーリー:** システム管理者として、認証設定を適切に管理したいので、セキュアな User Pool 設定を適用したい

#### 受け入れ基準

1. WHEN User Pool を設定する THEN システムは強力なパスワードポリシーを適用する
2. WHEN User Pool を設定する THEN システムは適切な属性設定を行う
3. WHEN User Pool Client を設定する THEN システムは適切な認証フローを有効にする
4. WHEN User Pool Client を設定する THEN システムは不要な権限を無効にする

### 要件 4

**ユーザーストーリー:** 開発者として、インフラストラクチャをコードで管理したいので、Python CDK を使用して Cognito リソースを定義したい

#### 受け入れ基準

1. WHEN CDK コードを作成する THEN システムは Python 言語を使用する
2. WHEN CDK Stack を定義する THEN システムは適切なコンストラクト構造を使用する
3. WHEN CDK リソースを定義する THEN システムは AWS ベストプラクティスに従う
4. WHEN CDK デプロイを実行する THEN システムは正常にリソースを作成する

### 要件 5

**ユーザーストーリー:** 開発者として、デプロイメントプロセスを自動化したいので、CDK を使用してワンコマンドでデプロイできるようにしたい

#### 受け入れ基準

1. WHEN CDK プロジェクトを初期化する THEN システムは必要な依存関係を設定する
2. WHEN デプロイコマンドを実行する THEN システムは承認なしでデプロイを完了する
3. WHEN デプロイが完了する THEN システムは Output 値を表示する
4. WHEN エラーが発生する THEN システムは適切なエラーメッセージを表示する