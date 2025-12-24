"""
Environment Config - 環境設定データ構造

環境設定を統合的に管理するデータクラス
"""

import os
import logging
from dataclasses import dataclass
from typing import Dict
from .environment_manager import EnvironmentManager
from .configuration_provider import ConfigurationProvider
from .log_controller import LogController


@dataclass
class EnvironmentConfig:
    """環境設定データクラス"""
    environment: str
    service_name: str
    aws_region: str
    log_level: str
    resource_suffix: str
    
    @classmethod
    def create_for_service(cls, service_name: str) -> 'EnvironmentConfig':
        """サービス固有の環境設定を作成"""
        env = EnvironmentManager.get_environment()
        config_provider = ConfigurationProvider(service_name)
        
        return cls(
            environment=env,
            service_name=service_name,
            aws_region=config_provider.get_aws_region(),
            log_level=logging.getLevelName(LogController.LOG_LEVELS[env]),
            resource_suffix=config_provider.get_environment_suffix()
        )