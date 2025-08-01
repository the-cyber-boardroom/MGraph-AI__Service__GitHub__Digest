from unittest                                import TestCase
from tests.unit.Service__Fast_API__Test_Objs import setup__service_fast_api_test_objs, TEST_API_KEY__NAME, TEST_API_KEY__VALUE


class test_Routes__GitHub__Digest(TestCase):
    @classmethod
    def setUpClass(cls):
        with setup__service_fast_api_test_objs() as _:
            cls.client                = _.fast_api__client
            cls.client.headers[TEST_API_KEY__NAME] = TEST_API_KEY__VALUE        # todo: move this to the setup__service_fast_api_test_objs

    def test__ping(self):
        response = self.client.get('/github-digest/ping')
        assert response.status_code == 200
        assert response.json()      == "pong"