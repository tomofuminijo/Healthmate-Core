"""
Healthmate Environment Configuration Module

環境設定とログ管理の統合モジュール
"""

from .environment_manager import (
    EnvironmentManager,
    EnvironmentError,
    InvalidEnvironmentError,
    ConfigurationError,
    handle_environment_error
)
from .configuration_provider import ConfigurationProvider
from .log_controller import LogController, JSONFormatter, LoggingError, safe_logging_setup
from .environment_config import EnvironmentConfig

__all__ = [
    'EnvironmentManager',
    'ConfigurationProvider', 
    'LogController',
    'EnvironmentConfig',
    'JSONFormatter',
    'EnvironmentError',
    'InvalidEnvironmentError',
    'ConfigurationError',
    'LoggingError',
    'handle_environment_error',
    'safe_logging_setup'
]

# バージョン情報
__version__ = '1.0.0'