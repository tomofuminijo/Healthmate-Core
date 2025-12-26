# Healthmate-Core

Healthmate プロダクトの認証基盤を管理するサービスです。Amazon Cognito User Pool を使用してユーザー認証機能を提供し、他の Healthmate サービス（HealthManager、CoachAI、UI）が共通して利用できる認証インフラを構築します。

## 概要

- **User Pool 名**: Healthmate-userpool
- **Stack 名**: Healthmate-CoreStack
- **Client Secret**: 無効（パブリッククライアント）
- **認証方式**: Email + Password

## 機能

### セキュリティ設定
- 強力なパスワードポリシー（8文字以上、大小英字・数字・記号必須）
- Email による本人確認
- MFA 対応（オプション）
- ユーザー存在エラーの防止

### 出力値
- `UserPoolId`: Cognito User Pool ID
- `UserPoolClientId`: User Pool Client ID  
- `UserPoolArn`: User Pool ARN

これらの値は CloudFormation Export として他のサービスから参照可能です。

## 環境設定

### 対応環境

Healthmate-Core は以下の3つの環境をサポートします：

- **dev**: 開発環境（デフォルト）
- **stage**: ステージング環境
- **prod**: 本番環境

### 環境変数

| 変数名 | 説明 | デフォルト値 | 例 |
|--------|------|-------------|-----|
| `HEALTHMATE_ENV` | デプロイ環境 | `dev` | `dev`, `stage`, `prod` |
| `AWS_REGION` | AWSリージョン | `us-west-2` | `us-west-2` |

### 環境別リソース命名

| 環境 | User Pool名 | Export名 | 例 |
|------|-------------|----------|-----|
| dev | `Healthmate-userpool-dev` | `Healthmate-Core-UserPoolId-dev` | 開発環境用 |
| stage | `Healthmate-userpool-stage` | `Healthmate-Core-UserPoolId-stage` | ステージング環境用 |
| prod | `Healthmate-userpool-prod` | `Healthmate-Core-UserPoolId-prod` | 本番環境用 |

## セットアップ

### 前提条件
- Python 3.12+
- AWS CLI 設定済み
- AWS CDK CLI インストール済み

### インストール

```bash
# リポジトリをクローン
git clone <repository-url>
cd Healthmate-Core

# 仮想環境を作成・アクティベート
python3 -m venv .venv
source .venv/bin/activate

# 依存関係をインストール
pip install -r requirements.txt
```

## デプロイ

### 環境別デプロイ

```bash
# 開発環境（デフォルト）
export HEALTHMATE_ENV=dev
./deploy.sh

# ステージング環境
export HEALTHMATE_ENV=stage
./deploy.sh

# 本番環境
export HEALTHMATE_ENV=prod
./deploy.sh
```

### 自動デプロイ（推奨）

```bash
# ワンコマンドデプロイ
./deploy.sh
```

### 手動デプロイ

```bash
# 仮想環境をアクティベート
source .venv/bin/activate

# 環境変数を設定（オプション）
export HEALTHMATE_ENV=dev  # dev, stage, prod

# CDK Bootstrap（初回のみ）
cdk bootstrap

# 構文チェック
cdk synth

# デプロイ
cdk deploy --require-approval never
```

## 削除

```bash
# リソースを削除
./destroy.sh
```

## 他サービスでの利用

### CloudFormation Import

```yaml
# 他のスタックで参照する例
Resources:
  MyResource:
    Type: AWS::SomeService::Resource
    Properties:
      UserPoolId: !ImportValue Healthmate-Core-UserPoolId
      ClientId: !ImportValue Healthmate-Core-UserPoolClientId
```

### CDK での参照

```python
from aws_cdk import Fn

# CDK で参照する例（環境別）
user_pool_id = Fn.import_value("Healthmate-Core-UserPoolId-dev")  # dev環境
client_id = Fn.import_value("Healthmate-Core-UserPoolClientId-dev")

# 本番環境の場合
user_pool_id = Fn.import_value("Healthmate-Core-UserPoolId-prod")  # prod環境
client_id = Fn.import_value("Healthmate-Core-UserPoolClientId-prod")
```

### 環境設定の確認

```bash
# 現在の環境設定を確認
python test_environment_config.py

# 環境別リソース名を確認
aws cloudformation describe-stacks --stack-name Healthmate-CoreStack-dev
aws cloudformation describe-stacks --stack-name Healthmate-CoreStack-stage  
aws cloudformation describe-stacks --stack-name Healthmate-CoreStack-prod
```

## 開発

### テスト実行

```bash
# 単体テスト
pytest tests/unit/ -v

# プロパティベーステスト
pytest tests/property/ -v

# 全テスト
pytest -v
```

### コード品質

```bash
# フォーマット
black .

# 型チェック
mypy .
```

## アーキテクチャ

```
┌─────────────────┐    ┌──────────────────┐
│   CDK Stack     │───▶│  CloudFormation  │
└─────────────────┘    └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  Cognito User    │
                       │      Pool        │
                       └──────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │  User Pool       │
                       │     Client       │
                       └──────────────────┘
```

## トラブルシューティング

### よくある問題

1. **Bootstrap エラー**
   ```bash
   cdk bootstrap
   ```

2. **権限エラー**
   - AWS CLI の設定を確認
   - IAM 権限を確認（Cognito 関連権限が必要）

3. **リージョン設定**
   - デフォルト: us-west-2
   - 変更する場合は `cdk.json` を編集

## ライセンス

MIT License