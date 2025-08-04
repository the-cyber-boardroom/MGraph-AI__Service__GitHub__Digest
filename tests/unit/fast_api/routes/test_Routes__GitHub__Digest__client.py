from unittest                                import TestCase

from osbot_utils.utils.Dev import pprint

from tests.unit.Service__Fast_API__Test_Objs import setup__service_fast_api_test_objs, TEST_API_KEY__NAME, TEST_API_KEY__VALUE


class test_Routes__GitHub__Digest__client(TestCase):
    @classmethod
    def setUpClass(cls):
        with setup__service_fast_api_test_objs() as _:
            cls.client                = _.fast_api__client
            cls.client.headers[TEST_API_KEY__NAME] = TEST_API_KEY__VALUE        # todo: move this to the setup__service_fast_api_test_objs

    def test__github_digest__repo_files_in_markdown(self):
        response = self.client.get('/github-digest/repo-files-in-markdown')
        assert response.status_code == 200
        assert response.headers['content-type'] == 'text/markdown; charset=utf-8'
        assert '### osbot_utils/__init__.py' in response.text
