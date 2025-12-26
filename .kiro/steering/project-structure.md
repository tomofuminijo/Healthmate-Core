# Project Structure

## Multi-Workspace Organization

The Healthmate App ecosystem consists of five separate workspace folders:

```
Healthmate-Core/              # Authentication foundation
Healthmate-HealthManager/     # MCP server backend
Healthmate-CoachAI/          # AI agent
Healthmate-Frontend/         # React frontend
Healthmate-App/              # Unified deployment management
```

## Healthmate-Core Structure

```
Healthmate-Core/
├── healthmate_core/             # CDK infrastructure modules
│   ├── __init__.py
│   └── healthmate_core_stack.py # Cognito User Pool stack
├── app.py                       # CDK app entry point
├── cdk.json                     # CDK configuration
├── deploy.sh                    # Deployment script
├── destroy.sh                   # Cleanup script
├── requirements.txt             # Python dependencies
├── .kiro/                       # Kiro configuration
│   └── steering/               # Centralized steering files
│       ├── product-overview.md
│       ├── tech-stack.md
│       ├── project-structure.md
│       ├── healthmanager-service.md
│       ├── coachai-service.md
│       └── ui-service.md
└── README.md                    # Service documentation
```

## Healthmate-HealthManager Structure

```
Healthmate-HealthManager/
├── cdk/                           # AWS CDK infrastructure
│   ├── cdk/                      # CDK Python modules
│   ├── app.py                    # CDK app entry point
│   ├── requirements.txt          # CDK dependencies
│   └── cdk.json                  # CDK configuration
├── lambda/                       # Lambda function handlers
│   ├── user/handler.py          # User management Lambda
│   ├── health_goal/handler.py   # Health goal Lambda
│   ├── health_policy/handler.py # Health policy Lambda
│   └── activity/handler.py      # Activity management Lambda
├── tests/                       # Test suites
│   ├── unit/                    # Unit tests
│   └── integration/             # Integration tests
├── mcp-schema/                  # MCP tool schemas
│   ├── user-management-mcp-schema.json
│   ├── health-goal-management-mcp-schema.json
│   ├── health-policy-management-mcp-schema.json
│   └── activity-management-mcp-schema.json
├── test_mcp_client.py          # Integration test client
├── requirements.txt            # Python dependencies
└── pytest.ini                 # Test configuration
```

## Healthmate-CoachAI Structure

```
Healthmate-CoachAI/
├── healthmate_coach_ai/
│   ├── __init__.py
│   └── agent.py                 # Main agent implementation
├── .bedrock_agentcore.yaml     # AgentCore configuration
├── deploy_to_aws.sh            # Deployment script
├── destroy_from_aws.sh         # Cleanup script
├── create_custom_iam_role.py   # IAM role creation
├── manual_test_agent.py        # Interactive testing
├── manual_test_deployed_agent.py # Deployed agent testing
├── check_deployment_status.py  # Status checking
├── agentcore-trust-policy.json # IAM trust policy
├── bedrock-agentcore-runtime-policy.json # Runtime policy
└── requirements.txt            # Python dependencies
```

## Healthmate-Frontend Structure

```
Healthmate-Frontend/
├── src/                         # React application source
│   ├── components/             # React components
│   ├── pages/                  # Page components
│   ├── hooks/                  # Custom React hooks
│   ├── services/               # API service layers
│   ├── utils/                  # Utility functions
│   ├── types/                  # TypeScript type definitions
│   └── main.tsx               # Application entry point
├── public/                     # Static assets
├── dist/                       # Build output
├── node_modules/               # Node.js dependencies
├── package.json                # Node.js project configuration
├── package-lock.json           # Dependency lock file
├── tsconfig.json               # TypeScript configuration
├── vite.config.ts              # Vite build configuration
├── tailwind.config.js          # Tailwind CSS configuration
├── components.json             # shadcn/ui configuration
├── .env                        # Environment variables
├── .env.example                # Environment variables template
└── README.md                   # Service documentation
```

## Healthmate-App Structure

```
Healthmate-App/
├── deploy_all.sh              # Unified deployment script
├── undeploy_all.sh            # Unified undeployment script
├── check_prerequisites.sh     # Prerequisites validation
├── test_integration.sh        # Integration testing
├── lib/                       # Common libraries
│   ├── common.sh             # Common functions and logging
│   └── services.sh           # Service-specific operations
├── logs/                     # Execution logs
├── tests/                    # Test scripts
│   └── integration/          # Integration test suites
├── .gitignore                # Git ignore patterns
└── README.md                 # Comprehensive documentation
```

## Key File Patterns

### Lambda Handlers
- **Location**: `lambda/{service}/handler.py`
- **Pattern**: Each service has its own Lambda function
- **Naming**: `{service}Lambda` (e.g., UserLambda, ActivityLambda)
- **Structure**: Standard AWS Lambda handler with error handling and logging

### MCP Schemas
- **Location**: `mcp-schema/` directory
- **Pattern**: `{service}-management-mcp-schema.json`
- **Purpose**: Define MCP tool interfaces for each service
- **Services**: user, health-goal, health-policy, activity

### Test Organization
- **Unit Tests**: `tests/unit/` - Mock AWS services, test business logic
- **Integration Tests**: `tests/integration/` - Test with real AWS services
- **Manual Tests**: Root level Python scripts for interactive testing

### Configuration Files
- **CDK**: `cdk.json` - CDK-specific configuration
- **pytest**: `pytest.ini` - Test runner configuration
- **AgentCore**: `.bedrock_agentcore.yaml` - Agent deployment config
- **Requirements**: `requirements.txt` - Python dependencies per project

## Naming Conventions

### Services
- **Healthmate-Core**: Authentication foundation
- **Healthmate-HealthManager**: Backend MCP server
- **Healthmate-CoachAI**: AI agent
- **Healthmate-Frontend**: React frontend application
- **Healthmate-App**: Unified deployment management

### AWS Resources
- **Prefix**: `healthmate-` for all resources
- **Tables**: `healthmate-{entity}` (users, goals, policies, activities)
- **Functions**: `healthmate-{Service}Lambda`
- **Gateway**: `healthmate-gateway`
- **User Pool**: `Healthmate-userpool`

### Code Structure
- **Classes**: PascalCase
- **Functions**: snake_case
- **Constants**: UPPER_SNAKE_CASE
- **Files**: snake_case.py

## Development Workflow

### Local Development
1. Set up virtual environment in each project: `python3 -m venv .venv`
2. Activate virtual environment: `source .venv/bin/activate`
3. Install dependencies: `pip install -r requirements.txt`
4. Use project-specific test commands
5. Deploy infrastructure before testing integration

### Deployment Order
1. **Healthmate-Core**: Deploy authentication foundation first
2. **Healthmate-HealthManager**: Deploy MCP backend second
3. **Healthmate-CoachAI**: Deploy agent after MCP backend
4. **Healthmate-Frontend**: Deploy frontend last

### Unified Management
- **Healthmate-App**: Orchestrates deployment of all 4 services
- **Prerequisites Check**: Validates environment before deployment
- **Dependency Management**: Ensures correct deployment order
- **Error Handling**: Provides retry mechanisms and detailed logging

### Testing Strategy
- **Unit tests**: Fast, isolated, mocked dependencies
- **Integration tests**: Real AWS services, end-to-end flows
- **Manual tests**: Interactive scripts for development and debugging
- **Property-based tests**: Using hypothesis for comprehensive testing

## Python Environment Requirements

### 仮想環境の使用
- **必須**: 全てのPythonコマンドは仮想環境内で実行
- **作成**: `python3 -m venv .venv`
- **アクティベート**: `source .venv/bin/activate` (macOS/Linux)
- **依存関係インストール**: `pip install -r requirements.txt`

### 開発パターン
```bash
# 標準的な開発セットアップ
cd {service-directory}
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# テスト実行
pytest tests/unit/ -v

# コード品質チェック
black .
flake8 .
mypy .
```