from unittest                                                                               import TestCase
from osbot_utils.testing.__                                                                 import __
from osbot_utils.type_safe.primitives.core.Safe_UInt                                        import Safe_UInt
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                       import Type_Safe__Dict
from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Id               import Safe_Str__Cache_Id
from mgraph_ai_service_github_digest.service.cache.schemas.Schema__Cache__Store__Response   import Schema__Cache__Store__Response


class test_Schema__Cache__Store__Response(TestCase):

    def test__init__(self):                                                         # Test response schema initialization
        with Schema__Cache__Store__Response() as _:
            assert type(_)          is Schema__Cache__Store__Response
            assert type(_.cache_id) is Safe_Str__Cache_Id
            assert type(_.hash)     is type(None)
            assert type(_.paths)    is Type_Safe__Dict
            assert type(_.size)     is Safe_UInt

            # Note: cache_id auto-generates, hash has empty default
            assert _.obj() == __(cache_id = _.cache_id   ,
                                 hash     = None         ,
                                 paths    = __()         ,
                                 size     = 0)