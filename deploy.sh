#!/bin/bash

# Healthmate-Core デプロイスクリプト
# Cognito User Pool を AWS にデプロイします

set -e  # エラー時に停止

# 環境設定
ENVIRONMENT=${HEALTHMATE_ENV:-dev}
echo "🌍 環境: $ENVIRONMENT"

echo "🚀 Healthmate-Core デプロイを開始します..."

# 仮想環境をアクティベート
echo "� 仮存想環境をアクティベート中..."
source .venv/bin/activate

# 依存関係の確認
echo "� 依存関係を確o認中..."
pip install -r requirements.txt --quiet

# 環境設定の確認
echo "⚙️  環境設定を確認中..."
python -c "
from healthmate_core.environment import EnvironmentManager, ConfigurationProvider
env = EnvironmentManager.get_environment()
config = ConfigurationProvider('healthmate-core')
print(f'検出された環境: {env}')
print(f'スタック名: {config.get_stack_name(\"Healthmate-CoreStack\")}')
print(f'User Pool名: Healthmate-userpool{config.get_environment_suffix()}')
"

# CDK Bootstrap の確認（初回のみ必要）
echo "�  CDK Bootstrap を確認中..."
cdk bootstrap --require-approval never 2>/dev/null || echo "Bootstrap は既に完了しています"

# CDK 構文チェック
echo "✅ CDK 構文をチェック中..."
cdk synth > /dev/null

# デプロイ実行（承認なし）
echo "🚀 AWS にデプロイ中..."
cdk deploy --require-approval never

# デプロイ結果の表示
echo ""
echo "✨ デプロイが完了しました！"
echo ""
echo "📋 Output 値:"
echo "============================================"

# 環境別スタック名を取得
STACK_NAME=$(python -c "
from healthmate_core.environment import ConfigurationProvider
config = ConfigurationProvider('healthmate-core')
print(config.get_stack_name('Healthmate-CoreStack'))
")

# Output 値を取得して表示
aws cloudformation describe-stacks \
    --stack-name "$STACK_NAME" \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue,Description]' \
    --output table 2>/dev/null || echo "Output 値の取得に失敗しました。AWS CLI の設定を確認してください。"

echo ""
echo "🎉 Healthmate-Core の認証基盤が正常にデプロイされました！"
echo ""
echo "📝 次のステップ:"
echo "   - 他のサービス（HealthManager、CoachAI、UI）でこれらの値を参照できます"
echo "   - Export 名は環境別に設定されています ($ENVIRONMENT 環境)"
echo ""