from aws_cdk import (
    Stack,
    CfnOutput,
    Duration,
    aws_cognito as cognito,
)
from constructs import Construct
from .environment import EnvironmentManager, ConfigurationProvider


class HealthmateCoreStack(Stack):
    """
    Healthmate-Core CDK Stack
    
    Cognito User Pool と User Pool Client を管理し、
    他のサービスが利用できる認証基盤を提供します。
    """

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # 環境設定の初期化
        self.config_provider = ConfigurationProvider("healthmate-core")
        self.current_environment = EnvironmentManager.get_environment()

        # User Pool の作成
        self.user_pool = self._create_user_pool()
        
        # User Pool Domain の作成（ホストされたUIのため）
        self.user_pool_domain = self._create_user_pool_domain(self.user_pool)
        
        # User Pool Client の作成
        self.user_pool_client = self._create_user_pool_client(self.user_pool)
        
        # CloudFormation Output の作成
        self._create_outputs(self.user_pool, self.user_pool_client, self.user_pool_domain)

    def _create_user_pool(self) -> cognito.UserPool:
        """
        Cognito User Pool を作成します。
        
        Returns:
            cognito.UserPool: 作成された User Pool
        """
        user_pool = cognito.UserPool(
            self,
            "HealthmateUserPool",
            user_pool_name=f"Healthmate-userpool{self.config_provider.get_environment_suffix()}",
            # サインイン設定
            sign_in_aliases=cognito.SignInAliases(
                email=False,
                username=True,
                phone=False
            ),
            # 標準属性設定
            standard_attributes=cognito.StandardAttributes(
                email=cognito.StandardAttribute(
                    required=True,
                    mutable=True
                ),
                given_name=cognito.StandardAttribute(
                    required=False,
                    mutable=True
                ),
                family_name=cognito.StandardAttribute(
                    required=False,
                    mutable=True
                )
            ),
            # パスワードポリシー
            password_policy=cognito.PasswordPolicy(
                min_length=8,
                require_lowercase=True,
                require_uppercase=True,
                require_digits=True,
                require_symbols=True
            ),
            # アカウント回復設定
            account_recovery=cognito.AccountRecovery.EMAIL_ONLY,
            # セルフサインアップ設定
            self_sign_up_enabled=True,
            # ユーザー検証設定
            user_verification=cognito.UserVerificationConfig(
                email_subject="Healthmate アカウント確認",
                email_body="Healthmate へようこそ！確認コード: {####}",
                email_style=cognito.VerificationEmailStyle.CODE
            ),
            # MFA設定（将来の拡張用）
            mfa=cognito.Mfa.OPTIONAL,
            mfa_second_factor=cognito.MfaSecondFactor(
                sms=False,
                otp=True
            )
        )
        
        return user_pool

    def _create_user_pool_domain(self, user_pool: cognito.UserPool) -> cognito.UserPoolDomain:
        """
        User Pool Domain を作成します（ホストされたUIのため）。
        
        Args:
            user_pool: 関連付ける User Pool
            
        Returns:
            cognito.UserPoolDomain: 作成された User Pool Domain
        """
        user_pool_domain = user_pool.add_domain(
            "UserPoolDomain",
            cognito_domain=cognito.CognitoDomainOptions(
                domain_prefix=f"healthmate{self.config_provider.get_environment_suffix()}",  # 環境別プレフィックス
            ),
        )
        
        return user_pool_domain

    def _create_user_pool_client(self, user_pool: cognito.UserPool) -> cognito.UserPoolClient:
        """
        User Pool Client を作成します。
        
        Args:
            user_pool: 関連付ける User Pool
            
        Returns:
            cognito.UserPoolClient: 作成された User Pool Client
        """
        user_pool_client = cognito.UserPoolClient(
            self,
            "HealthmateUserPoolClient",
            user_pool=user_pool,
            # Client Secret を無効化
            generate_secret=False,
            # 認証フロー設定
            auth_flows=cognito.AuthFlow(
                user_password=True,
                user_srp=True,
                custom=False,
                admin_user_password=False
            ),
            # トークン有効期限設定
            access_token_validity=Duration.hours(1),
            refresh_token_validity=Duration.days(30),
            id_token_validity=Duration.hours(1),
            # セキュリティ設定
            prevent_user_existence_errors=True,
            # OAuth設定（将来の拡張用）
            o_auth=cognito.OAuthSettings(
                flows=cognito.OAuthFlows(
                    authorization_code_grant=True,
                    implicit_code_grant=False
                ),
                scopes=[
                    cognito.OAuthScope.OPENID,
                    cognito.OAuthScope.PROFILE,
                    cognito.OAuthScope.EMAIL,
                    cognito.OAuthScope.PHONE,  # 電話番号スコープ
                ],
                # コールバックURL（HealthCoachAI、HealthmateUI、外部AIクライアント用）
                # 実際のURLは後で更新する必要があります
                callback_urls=[
                    "https://healthcoachai.example.com/oauth/callback",  # HealthCoachAI
                    "https://healthmateui.example.com/oauth/callback",   # HealthmateUI
                    "https://chatgpt.com/connector_platform_oauth_redirect",  # ChatGPT
                    "http://localhost:8000/auth/callback"
                ],
                logout_urls=[
                    "https://healthcoachai.example.com/oauth/logout",
                    "https://healthmateui.example.com/oauth/logout",
                    "https://chatgpt.com/connector_platform_oauth_redirect",
                    "http://localhost:8000/auth/logout"
                ],
            )
        )
        
        return user_pool_client

    def _create_outputs(self, user_pool: cognito.UserPool, client: cognito.UserPoolClient, domain: cognito.UserPoolDomain) -> None:
        """
        CloudFormation Output を作成します。
        
        Args:
            user_pool: User Pool
            client: User Pool Client
            domain: User Pool Domain
        """
        # User Pool ID の出力
        CfnOutput(
            self,
            "UserPoolId",
            value=user_pool.user_pool_id,
            description="Cognito User Pool ID",
            export_name=f"Healthmate-UserPoolId{self.config_provider.get_environment_suffix()}"
        )
        
        # User Pool Client ID の出力
        CfnOutput(
            self,
            "UserPoolClientId", 
            value=client.user_pool_client_id,
            description="Cognito User Pool Client ID",
            export_name=f"Healthmate-UserPoolClientId{self.config_provider.get_environment_suffix()}"
        )
        
        # User Pool ARN の出力（追加情報として）
        CfnOutput(
            self,
            "UserPoolArn",
            value=user_pool.user_pool_arn,
            description="Cognito User Pool ARN",
            export_name=f"Healthmate-UserPoolArn{self.config_provider.get_environment_suffix()}"
        )
        
        # User Pool Domain の出力
        CfnOutput(
            self,
            "UserPoolDomain",
            value=domain.domain_name,
            description="Cognito User Pool Domain",
            export_name=f"Healthmate-UserPoolDomain{self.config_provider.get_environment_suffix()}"
        )
        
        # ホストされたUIのベースURL
        CfnOutput(
            self,
            "HostedUIUrl",
            value=f"https://{domain.domain_name}.auth.{self.region}.amazoncognito.com",
            description="Cognito Hosted UI Base URL",
            export_name=f"Healthmate-HostedUIUrl{self.config_provider.get_environment_suffix()}"
        )