import pytest
from unittest                                                           import TestCase
from osbot_utils.utils.Misc                                             import list_set
from osbot_fast_api_serverless.deploy.Deploy__Serverless__Fast_API      import DEFAULT__ERROR_MESSAGE__WHEN_FAST_API_IS_OK
from mgraph_ai_service_github_digest.config                             import LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS
from mgraph_ai_service_github_digest.utils.Version                      import version__mgraph_ai_service_github_digest
from mgraph_ai_service_github_digest.utils.deploy.Deploy__Service       import Deploy__Service


class test_Deploy__Service__to__prod(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.deploy_fast_api__prod  = Deploy__Service(stage = 'prod')

        with cls.deploy_fast_api__prod as _:
            if _.aws_config.aws_configured() is False:
                pytest.skip("this test needs valid AWS credentials")

    def test_1__check_stages(self):
        assert self.deploy_fast_api__prod .stage == 'prod'

    def test_2__upload_dependencies(self):
        upload_results = self.deploy_fast_api__prod.upload_lambda_dependencies_to_s3()
        assert list_set(upload_results) == LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS

    def test_3__create(self):
        assert self.deploy_fast_api__prod .create() is True

    def test_4__invoke(self):
        assert self.deploy_fast_api__prod .invoke().get('errorMessage') == DEFAULT__ERROR_MESSAGE__WHEN_FAST_API_IS_OK

    def test_4__invoke__function_url(self):
        version = {'version': version__mgraph_ai_service_github_digest}
        assert self.deploy_fast_api__prod .invoke__function_url('/info/version') == version

    # def test_4__delete(self):
    #     assert self.deploy_fast_api__prod .delete() is True