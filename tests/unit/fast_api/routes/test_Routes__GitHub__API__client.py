from unittest                                import TestCase
from tests.unit.Service__Fast_API__Test_Objs import TEST_API_KEY__NAME, TEST_API_KEY__VALUE, setup__service_fast_api_test_objs


class test_Routes__GitHub__API__client(TestCase):
    @classmethod
    def setUpClass(cls):
        with setup__service_fast_api_test_objs() as _:
            cls.client                = _.fast_api__client
            cls.client.headers[TEST_API_KEY__NAME] = TEST_API_KEY__VALUE        # todo: move this to the setup__service_fast_api_test_objs

    def test__repository_files_names(self):
        result = self.client.get('github-api/repository-files-names')
        assert result.status_code == 200