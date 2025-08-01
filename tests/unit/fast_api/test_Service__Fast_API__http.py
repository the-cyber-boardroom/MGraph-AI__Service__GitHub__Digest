from fastapi                                        import FastAPI
from unittest                                       import TestCase
from osbot_fast_api.utils.Fast_API_Server           import Fast_API_Server
from mgraph_ai_service_github_digest.utils.Version  import version__mgraph_ai_service_github_digest
from tests.unit.Service__Fast_API__Test_Objs        import setup__service_fast_api_test_objs, TEST_API_KEY__NAME, TEST_API_KEY__VALUE


class test_Service__Fast_API__http(TestCase):

    @classmethod
    def setUpClass(cls):
        with setup__service_fast_api_test_objs() as _:
            cls.app = _.fast_api__app
            cls.fast_api_server = Fast_API_Server(app=cls.app)

    def test__setUpClass(self):
        with self.fast_api_server as _:
            assert type(_    ) is Fast_API_Server
            assert type(_.app) is FastAPI
            assert _.app == self.app

    def test__info__config(self):
        headers = {TEST_API_KEY__NAME:TEST_API_KEY__VALUE}

        with self.fast_api_server as _:
            response__no_auth__root           = _.requests_get('/')
            response__with_auth__root         = _.requests_get('/'            , headers=headers)
            response__with_auth__docs         = _.requests_get('/docs'        , headers=headers)
            response__with_auth__info_version = _.requests_get('/info/version', headers=headers)
            assert response__no_auth__root.status_code           == 401
            assert response__no_auth__root.json()                == { 'data'   : None     ,
                                                                      'error'  : None     ,
                                                                      'message': 'Client API key is missing, you need to set it on a header or cookie',
                                                                      'status' : 'error'  }
            assert response__with_auth__root        .status_code == 404
            assert response__with_auth__docs        .status_code == 200
            assert response__with_auth__info_version.status_code == 200
            assert response__with_auth__info_version.json()      == { 'version': version__mgraph_ai_service_github_digest}
            assert _.url()                                       == f'http://127.0.0.1:{_.port}/'
