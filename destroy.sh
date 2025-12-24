#!/bin/bash

# Healthmate-Core 削除スクリプト
# デプロイされた Cognito User Pool を削除します

set -e  # エラー時に停止

# 環境設定
ENVIRONMENT=${HEALTHMATE_ENV:-dev}
echo "🌍 環境: $ENVIRONMENT"

echo "🗑️  Healthmate-Core リソースの削除を開始します..."

# 仮想環境をアクティベート
echo "📦 仮想環境をアクティベート中..."
source .venv/bin/activate

# 環境設定の確認
echo "⚙️  環境設定を確認中..."
STACK_NAME=$(python -c "
from healthmate_core.environment import ConfigurationProvider
config = ConfigurationProvider('healthmate-core')
print(config.get_stack_name('Healthmate-CoreStack'))
")

USER_POOL_NAME=$(python -c "
from healthmate_core.environment import ConfigurationProvider
config = ConfigurationProvider('healthmate-core')
print(f'Healthmate-userpool{config.get_environment_suffix()}')
")

echo "削除対象スタック: $STACK_NAME"
echo "削除対象User Pool: $USER_POOL_NAME"

# 確認メッセージ
echo ""
echo "⚠️  警告: この操作により以下のリソースが削除されます:"
echo "   - CloudFormation Stack: $STACK_NAME"
echo "   - Cognito User Pool: $USER_POOL_NAME"
echo "   - User Pool Client"
echo "   - User Pool Domain"
echo "   - 関連するすべてのユーザーデータ"
echo "   - CloudFormation Exports ($ENVIRONMENT 環境)"
echo ""
read -p "本当に削除しますか？ (yes/no): " confirm

if [ "$confirm" != "yes" ]; then
    echo "❌ 削除がキャンセルされました"
    exit 0
fi

# CDK destroy 実行
echo "🗑️  AWS リソースを削除中..."
cdk destroy --force

echo ""
echo "✅ Healthmate-Core リソース ($ENVIRONMENT 環境) が正常に削除されました"
echo ""