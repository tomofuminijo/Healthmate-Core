#!/bin/bash

# Healthmate-Core デプロイスクリプト
# Cognito User Pool を AWS にデプロイします

set -e  # エラー時に停止

echo "🚀 Healthmate-Core デプロイを開始します..."

# 仮想環境をアクティベート
echo "📦 仮想環境をアクティベート中..."
source .venv/bin/activate

# 依存関係の確認
echo "🔍 依存関係を確認中..."
pip install -r requirements.txt --quiet

# CDK Bootstrap の確認（初回のみ必要）
echo "🔧 CDK Bootstrap を確認中..."
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

# Output 値を取得して表示
aws cloudformation describe-stacks \
    --stack-name Healthmate-CoreStack \
    --query 'Stacks[0].Outputs[*].[OutputKey,OutputValue,Description]' \
    --output table 2>/dev/null || echo "Output 値の取得に失敗しました。AWS CLI の設定を確認してください。"

echo ""
echo "🎉 Healthmate-Core の認証基盤が正常にデプロイされました！"
echo ""
echo "📝 次のステップ:"
echo "   - 他のサービス（HealthManager、CoachAI、UI）でこれらの値を参照できます"
echo "   - Export 名: Healthmate-Core-UserPoolId, Healthmate-Core-UserPoolClientId"
echo ""