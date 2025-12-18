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

### 自動デプロイ（推奨）

```bash
# ワンコマンドデプロイ
./deploy.sh
```

### 手動デプロイ

```bash
# 仮想環境をアクティベート
source .venv/bin/activate

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

# CDK で参照する例
user_pool_id = Fn.import_value("Healthmate-Core-UserPoolId")
client_id = Fn.import_value("Healthmate-Core-UserPoolClientId")
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