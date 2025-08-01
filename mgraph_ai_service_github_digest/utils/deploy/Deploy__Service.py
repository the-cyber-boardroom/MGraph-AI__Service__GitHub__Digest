from osbot_fast_api_serverless.deploy.Deploy__Serverless__Fast_API      import Deploy__Serverless__Fast_API
from mgraph_ai_service_github_digest.config                             import SERVICE_NAME, LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS
from mgraph_ai_service_github_digest.fast_api.lambda_handler            import run

class Deploy__Service(Deploy__Serverless__Fast_API):

    def handler(self):
        return run

    def lambda_dependencies(self):
        return LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS

    def lambda_name(self):
        return SERVICE_NAME
