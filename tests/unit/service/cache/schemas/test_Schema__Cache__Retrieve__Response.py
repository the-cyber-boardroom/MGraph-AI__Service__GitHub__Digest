from unittest                                                                                import TestCase
from osbot_utils.type_safe.primitives.core.Safe_Str                                          import Safe_Str
from mgraph_ai_service_github_digest.service.cache.schemas.Schema__Cache__Retrieve__Response import Schema__Cache__Retrieve__Response


class test_Schema__Cache__Retrieve__Response(TestCase):

    def test__init__(self):                                                         # Test retrieve response initialization
        with Schema__Cache__Retrieve__Response() as _:
            assert type(_)             is Schema__Cache__Retrieve__Response
            assert type(_.data)        is bytes
            assert type(_.metadata)    is dict
            assert type(_.data_type)   is Safe_Str
            assert type(_.cache_hit)   is bool

            # Test defaults
            assert _.cache_hit == True
            assert _.cached_at is None
            assert _.cache_id  is None