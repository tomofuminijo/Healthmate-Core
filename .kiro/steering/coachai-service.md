# Healthmate-CoachAI サービス

## Service Overview

Healthmate-CoachAI サービスは、Healthmate プロダクトのAI健康コーチを担当するエージェントです。Amazon Bedrock AgentCore Runtime上で動作し、ユーザーにパーソナライズされた健康アドバイスを提供します。

### Primary Responsibilities

- **AI Health Coaching**: ユーザーの健康データに基づくパーソナライズされたアドバイス
- **MCP Client**: HealthManagerMCP サービスからの健康データ取得
- **JWT Processing**: フロントエンドから渡されるJWTトークンの処理とユーザー識別
- **Time-Aware Responses**: 現在時刻を考慮した適切なタイミングでのアドバイス
- **Session Continuity**: AgentCore Memoryによる会話の継続性

### Service Architecture

- **Framework**: Strands Agent SDK
- **Runtime**: Amazon Bedrock AgentCore Runtime
- **Platform**: Linux/ARM64 containers
- **Deployment**: Container-based deployment with ECR
- **Configuration**: CloudFormation outputs for dynamic configuration
- **Memory**: AgentCore Memory for session management

### Key Technologies

#### Core Dependencies
- **strands-agents**: Agent framework for tool integration
- **bedrock-agentcore**: Runtime environment integration
- **mcp**: Model Context Protocol client
- **boto3**: AWS SDK for CloudFormation and Cognito integration
- **pytz**: Timezone handling for time-aware responses

#### Development Tools
- **pytest**: Unit and integration testing
- **black**: Code formatting
- **mypy**: Type checking

### Agent Patterns

#### JWT Token Handling
```python
def _decode_jwt_payload(jwt_token: str) -> dict:
    """JWTトークンのペイロードをデコード（署名検証なし）"""
    # Base64URL decoding with padding adjustment
```

#### MCP Integration
```python
async def _call_mcp_tool(tool_name: str, parameters: dict) -> dict:
    """HealthManagerMCP サービスのツールを呼び出し"""
    # HTTP client with proper authentication headers
```

#### Time-Aware Responses
```python
def _get_current_time_in_timezone(timezone_str: str = "Asia/Tokyo") -> datetime:
    """ユーザーのタイムゾーンでの現在時刻を取得"""
```

#### Session Management
```python
# AgentCore Memory統合
from strands_agents.memory import AgentCoreMemorySessionManager

class HealthCoachAgent:
    def __init__(self):
        self.memory_manager = AgentCoreMemorySessionManager(
            memory_id="healthmate_coach_ai_mem-yxqD6w75pO"
        )
```

### Configuration Management

#### Environment Variables
- `HEALTHMANAGER_GATEWAY_ID`: MCP Gateway endpoint
- `AWS_REGION`: AWS region (default: us-west-2)
- `HEALTH_STACK_NAME`: CloudFormation stack name for dynamic config

#### CloudFormation Integration
```python
def _get_config_from_cloudformation() -> dict:
    """CloudFormationスタックから設定を動的取得"""
    # Gateway ID, Cognito settings from stack outputs
```

### Deployment Patterns

#### One-Command Deployment
```bash
./deploy_to_aws.sh  # IAM role creation + AgentCore deployment
```

#### Custom IAM Role
- **Role Name**: `Healthmate-CoachAI-AgentCore-Runtime-Role`
- **Permissions**: AgentCore Runtime + CloudFormation read + Cognito read

#### Testing Strategy
- **Interactive Testing**: `manual_test_agent.py` for development
- **Deployed Testing**: `manual_test_deployed_agent.py` for production validation
- **Status Monitoring**: `check_deployment_status.py` for deployment verification

### API Specification

#### Payload Structure
HealthmateUI サービスから送信される最適化されたペイロード：

```json
{
  "prompt": "ユーザーからのメッセージ",
  "sessionState": {
    "sessionAttributes": {
      "session_id": "healthmate-chat-1234567890-abcdef",
      "jwt_token": "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9...",
      "timezone": "Asia/Tokyo",
      "language": "ja"
    }
  }
}
```

#### Payload Elements
| フィールド | 必須 | 説明 |
|-----------|------|------|
| `prompt` | ✅ | ユーザーからのメッセージ |
| `sessionState.sessionAttributes.session_id` | ✅ | セッション継続性のためのID（33文字以上） |
| `sessionState.sessionAttributes.jwt_token` | ✅ | Cognito JWT トークン（user_id抽出用） |
| `sessionState.sessionAttributes.timezone` | ⚪ | ユーザーのタイムゾーン（デフォルト: "Asia/Tokyo"） |
| `sessionState.sessionAttributes.language` | ⚪ | ユーザーの言語設定（デフォルト: "ja"） |

### Session Continuity Features

#### AgentCore Memory統合
- **セッション継続性**: 会話の文脈を記憶し、継続的な対話を実現
- **AgentCoreMemorySessionManager**: 自動的なセッション管理
- **フォールバック機能**: メモリ統合失敗時の安全な動作保証
- **セッションID管理**: 33文字以上の要件に対応した自動生成

#### Memory Configuration
```yaml
# .bedrock_agentcore.yaml
agents:
  healthmate_coach_ai:
    bedrock_agentcore:
      memory:
        memory_id: "healthmate_coach_ai_mem-yxqD6w75pO"
        enabled: true
```

### Integration Points

- **HealthManagerMCP サービス**: MCP protocol for health data access
- **HealthmateUI サービス**: JWT token passing for user identification
- **Healthmate-Core サービス**: Cognito authentication integration
- **External AI Platforms**: Potential integration with other AI services

### Development Commands

#### 仮想環境セットアップ
```bash
cd Healthmate-CoachAI
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

#### Deployment
```bash
# ワンコマンドデプロイ（IAMロール自動作成）
./deploy_to_aws.sh
```

#### Testing
```bash
# インタラクティブテストプログラム
python manual_test_agent.py

# デプロイ済みエージェントの手動テスト
python manual_test_deployed_agent.py

# デプロイ状態確認
python check_deployment_status.py
```

#### Cleanup
```bash
# 全てのAWSリソースを削除
./destroy_from_aws.sh
```

### Service-Specific Best Practices

- **Error Handling**: Graceful fallback when MCP services are unavailable
- **User Context**: Always extract user ID from JWT for personalized responses
- **Time Sensitivity**: Consider user's timezone and current time for advice
- **Security**: Never log or expose JWT tokens or sensitive user data
- **Session Management**: Utilize AgentCore Memory for conversation continuity
- **Language Support**: 日本語での対話を基本とする
- **Memory Testing**: セッション継続性の定期的な動作確認