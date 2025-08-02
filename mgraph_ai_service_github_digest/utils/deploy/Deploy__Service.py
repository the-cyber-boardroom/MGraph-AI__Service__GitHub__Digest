from osbot_utils.utils.Env                                               import get_env
from osbot_fast_api_serverless.deploy.Deploy__Serverless__Fast_API       import Deploy__Serverless__Fast_API
from mgraph_ai_service_github_digest.config                              import SERVICE_NAME, LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS
from mgraph_ai_service_github_digest.fast_api.lambda_handler             import run
from mgraph_ai_service_github_digest.service.threat_intelligence.IP_Data import ENV_VAR__IP_DATA__API_KEY


class Deploy__Service(Deploy__Serverless__Fast_API):

    def deploy_lambda(self):
        with super().deploy_lambda() as _:
            ip_data__api_key = get_env(ENV_VAR__IP_DATA__API_KEY)            # todo add better way to add extra env vars during deployment
            if ip_data__api_key:
                _.set_env_variable(ENV_VAR__IP_DATA__API_KEY, ip_data__api_key)
            return _

    def handler(self):
        return run

    def lambda_dependencies(self):
        return LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS

    def lambda_name(self):
        return SERVICE_NAME
