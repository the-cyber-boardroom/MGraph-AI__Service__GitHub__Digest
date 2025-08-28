from unittest                                                     import TestCase
from osbot_fast_api.api.routes.Fast_API__Routes                   import Fast_API__Routes
from osbot_utils.type_safe.Type_Safe                              import Type_Safe
from osbot_utils.utils.Objects                                    import base_classes
from mgraph_ai_service_github_digest.fast_api.routes.Routes__Info import Routes__Info


class test_Routes__Info(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes_info = Routes__Info()

    def test_setUpClass(self):
        with self.routes_info as _:
            assert type(_)         == Routes__Info
            assert base_classes(_) == [Fast_API__Routes, Type_Safe, object]

    def test_ip_address(self):
        with self.routes_info as _:
            assert len(_.ip_address().get('ip_address').split('.')) == 4