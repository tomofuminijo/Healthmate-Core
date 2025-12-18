#!/bin/bash

# Healthmate-Core 削除スクリプト
# デプロイされた Cognito User Pool を削除します

set -e  # エラー時に停止

echo "🗑️  Healthmate-Core リソースの削除を開始します..."

# 仮想環境をアクティベート
echo "📦 仮想環境をアクティベート中..."
source .venv/bin/activate

# 確認メッセージ
echo ""
echo "⚠️  警告: この操作により以下のリソースが削除されます:"
echo "   - Cognito User Pool (Healthmate-userpool)"
echo "   - User Pool Client"
echo "   - 関連するすべてのユーザーデータ"
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
echo "✅ Healthmate-Core リソースが正常に削除されました"
echo ""