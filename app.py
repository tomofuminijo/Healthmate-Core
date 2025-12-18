#!/usr/bin/env python3
"""
Healthmate-Core CDK Application

Cognito User Pool を管理する認証基盤サービスのエントリーポイント
"""

import aws_cdk as cdk
from healthmate_core.healthmate_core_stack import HealthmateCoreStack


def main():
    """CDK アプリケーションのメイン関数"""
    app = cdk.App()
    
    # Healthmate-CoreStack を作成
    HealthmateCoreStack(
        app, 
        "Healthmate-CoreStack",
        description="Healthmate プロダクトの認証基盤（Cognito User Pool）を管理するスタック",
        # 環境設定（必要に応じて設定）
        env=cdk.Environment(
            account=app.node.try_get_context("account"),
            region=app.node.try_get_context("region") or "us-west-2"
        )
    )
    
    app.synth()


if __name__ == "__main__":
    main()