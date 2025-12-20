# Technology Stack

## Architecture

**Serverless, cloud-native architecture** using AWS services with Model Context Protocol (MCP) for AI integration.

## Core Technologies

### Authentication (Healthmate-Core)
- **Runtime**: Python 3.12+
- **Infrastructure**: AWS CDK (Python)
- **Authentication**: Amazon Cognito User Pool
- **Exports**: CloudFormation Exports for other services

### Backend (Healthmate-HealthManager)
- **Runtime**: Python 3.12+
- **Infrastructure**: AWS CDK (Python)
- **Compute**: AWS Lambda functions
- **Database**: Amazon DynamoDB
- **Authentication**: Amazon Cognito (OAuth 2.0) - imported from Core
- **API Gateway**: Amazon Bedrock AgentCore Gateway
- **Protocol**: Model Context Protocol (MCP)

### AI Agent (Healthmate-CoachAI)
- **Framework**: Strands Agent SDK
- **Runtime**: Amazon Bedrock AgentCore Runtime
- **Platform**: Linux/ARM64 containers
- **Dependencies**: boto3, pytz, mcp
- **Memory**: AgentCore Memory for session continuity

### Frontend (HealthmateUI)
- **Framework**: FastAPI + htmx
- **Runtime**: AWS Lambda (Python 3.12)
- **Container**: Docker + Amazon ECR
- **Static Hosting**: Amazon S3 + CloudFront
- **Authentication**: Cognito OAuth 2.0 integration

## Development Tools

### Python Environment
- **仮想環境**: 全てのPythonコマンドは仮想環境内で実行
- **セットアップ**: `python3 -m venv .venv && source .venv/bin/activate`
- **依存関係**: `pip install -r requirements.txt`

### Testing
- **Framework**: pytest with hypothesis (property-based testing)
- **Coverage**: pytest-cov
- **Mocking**: moto for AWS services
- **Config**: pytest.ini with verbose output and short tracebacks

### Code Quality
- **Formatting**: black
- **Linting**: flake8
- **Type Checking**: mypy

## Common Commands

### Healthmate-Core

```bash
# Environment setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# CDK operations
cdk bootstrap
cdk deploy --require-approval never

# Testing
pytest tests/unit/ -v                    # Unit tests

# Cleanup
cdk destroy
```

### Healthmate-HealthManager

```bash
# Environment setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# CDK operations
cd cdk && npm install
cdk deploy --require-approval never

# Testing
pytest tests/unit/ -v                    # Unit tests
python test_mcp_client.py               # Integration tests

# Cleanup
cdk destroy
```

### Healthmate-CoachAI

```bash
# Setup and deploy
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
./deploy_to_aws.sh                      # One-command deploy

# Testing
python manual_test_agent.py             # Interactive testing
python manual_test_deployed_agent.py    # Test deployed agent
agentcore status                         # Check deployment status

# Development
agentcore invoke --dev "test message"   # Local development
```

### HealthmateUI

```bash
# Environment setup
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Development server
python run_dev.py                       # Auto-configuration

# Testing
pytest tests/unit/ -v                   # Unit tests
pytest tests/integration/ -v            # Integration tests
```

## Configuration Management

### Environment Variables
- **AWS_REGION**: Default us-west-2
- **HEALTH_STACK_NAME**: CloudFormation stack name
- **HEALTHMANAGER_GATEWAY_ID**: MCP Gateway identifier
- **LOG_LEVEL**: DEBUG for development

### CloudFormation Outputs
Required stack outputs for integration:
- `GatewayId`: MCP Gateway ID
- `UserPoolId`: Cognito User Pool ID
- `UserPoolClientId`: Cognito Client ID

## Security Patterns

- **JWT Authentication**: All API calls require Cognito JWT tokens
- **IAM Roles**: Least privilege access with custom roles
- **Environment-based Config**: No hardcoded credentials
- **Encryption**: Data encrypted in transit and at rest

## Deployment Patterns

- **Infrastructure as Code**: AWS CDK for all resources
- **Serverless**: Lambda functions with DynamoDB
- **Container Deployment**: AgentCore Runtime for AI agents
- **Gateway Integration**: MCP protocol for AI connectivity
- **Static Hosting**: S3 + CloudFront for frontend assets