#!/usr/bin/env python3
"""
Healthmate-Core CDK Application

Cognito User Pool を管理する認証基盤サービスのエントリーポイント
"""

import aws_cdk as cdk
from healthmate_core.healthmate_core_stack import HealthmateCoreStack
from healthmate_core.environment import EnvironmentManager, ConfigurationProvider, safe_logging_setup


def main():
    """CDK アプリケーションのメイン関数"""
    # ログ設定の初期化
    log_controller = safe_logging_setup("healthmate-core")
    
    # 環境設定の初期化
    environment = EnvironmentManager.get_environment()
    config_provider = ConfigurationProvider("healthmate-core")
    
    app = cdk.App()
    
    # 環境別スタック名の生成
    stack_name = config_provider.get_stack_name("Healthmate-CoreStack")
    
    # Healthmate-CoreStack を作成
    HealthmateCoreStack(
        app, 
        stack_name,
        description=f"Healthmate プロダクトの認証基盤（Cognito User Pool）を管理するスタック - {environment} 環境",
        # 環境設定
        env=cdk.Environment(
            account=app.node.try_get_context("account"),
            region=config_provider.get_aws_region()
        )
    )
    
    app.synth()


if __name__ == "__main__":
    main()