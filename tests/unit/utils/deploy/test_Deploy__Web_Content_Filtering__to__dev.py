from unittest                                                                   import TestCase
from osbot_aws.testing.skip_tests                                               import skip__if_not__in_github_actions
from osbot_fast_api_serverless.deploy.Deploy__Serverless__Fast_API              import DEFAULT__ERROR_MESSAGE__WHEN_FAST_API_IS_OK
from mgraph_ai_service_github_digest.config                                     import LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS
from mgraph_ai_service_github_digest.utils.Version                              import version__mgraph_ai_service_github_digest
from Service__Fast_API__Test_Objs                                               import setup_local_stack
from osbot_utils.utils.Misc                                                     import list_set

from mgraph_ai_service_github_digest.utils.deploy.Deploy__Service import Deploy__Service


class test_Deploy__Web_Content_Filtering__to__dev(TestCase):

    @classmethod
    def setUpClass(cls):
        skip__if_not__in_github_actions()
        setup_local_stack()

        cls.deploy_fast_api__dev  = Deploy__Service(stage = 'dev')

    def test_1__check_stages(self):
        assert self.deploy_fast_api__dev .stage == 'dev'

    def test_2__upload_dependencies(self):
        upload_results = self.deploy_fast_api__dev.upload_lambda_dependencies_to_s3()
        assert list_set(upload_results) == LAMBDA_DEPENDENCIES__FAST_API_SERVERLESS

    def test_3__create(self):
        assert self.deploy_fast_api__dev .create() is True
        #self.test_4__invoke()

    def test_4__invoke(self):
        #pprint(self.deploy_fast_api__dev .invoke())
        assert self.deploy_fast_api__dev .invoke().get('errorMessage') == DEFAULT__ERROR_MESSAGE__WHEN_FAST_API_IS_OK

    def test_5__invoke__function_url(self):
        version = {'version': version__mgraph_ai_service_github_digest }
        assert self.deploy_fast_api__dev .invoke__function_url('/info/version') == version

    def test_6__delete(self):
        assert self.deploy_fast_api__dev .delete() is True
