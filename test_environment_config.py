#!/usr/bin/env python3
"""
環境設定テストスクリプト

環境設定モジュールの動作確認用スクリプト
"""

import os
from healthmate_core.environment import (
    EnvironmentManager,
    ConfigurationProvider,
    LogController,
    EnvironmentConfig,
    safe_logging_setup
)


def test_environment_config():
    """環境設定のテスト"""
    print("=== Healthmate Environment Configuration Test ===\n")
    
    # 現在の環境変数を表示
    current_env = os.environ.get("HEALTHMATE_ENV", "未設定")
    print(f"HEALTHMATE_ENV: {current_env}")
    print(f"AWS_REGION: {os.environ.get('AWS_REGION', '未設定')}\n")
    
    # Environment Manager のテスト
    print("--- Environment Manager ---")
    environment = EnvironmentManager.get_environment()
    print(f"検出された環境: {environment}")
    print(f"本番環境?: {EnvironmentManager.is_production()}")
    print(f"開発環境?: {EnvironmentManager.is_development()}")
    print(f"ステージング環境?: {EnvironmentManager.is_staging()}\n")
    
    # Configuration Provider のテスト
    print("--- Configuration Provider ---")
    config_provider = ConfigurationProvider("healthmate-core")
    print(f"サービス名: {config_provider.service_name}")
    print(f"環境: {config_provider.environment}")
    print(f"AWS リージョン: {config_provider.get_aws_region()}")
    print(f"環境サフィックス: '{config_provider.get_environment_suffix()}'")
    print(f"Stack名例: {config_provider.get_stack_name('Healthmate-CoreStack')}")
    print(f"Stack名例: {config_provider.get_stack_name('Healthmate-HealthManagerStack')}")
    print()
    
    # Log Controller のテスト
    print("--- Log Controller ---")
    log_controller = safe_logging_setup("healthmate-core")
    if log_controller:
        logger = log_controller.get_logger("test")
        print(f"ログレベル: {log_controller.LOG_LEVELS[environment]}")
        
        # 各レベルのログをテスト
        logger.debug("これはDEBUGログです")
        logger.info("これはINFOログです")
        logger.warning("これはWARNINGログです")
        logger.error("これはERRORログです")
    else:
        print("Log Controller の初期化に失敗しました")
    
    print()
    
    # Environment Config のテスト
    print("--- Environment Config ---")
    env_config = EnvironmentConfig.create_for_service("healthmate-core")
    print(f"環境: {env_config.environment}")
    print(f"サービス名: {env_config.service_name}")
    print(f"AWS リージョン: {env_config.aws_region}")
    print(f"ログレベル: {env_config.log_level}")
    print(f"リソースサフィックス: '{env_config.resource_suffix}'")
    
    print("\n=== テスト完了 ===")


if __name__ == "__main__":
    test_environment_config()