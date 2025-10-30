from unittest                                                                            import TestCase
from osbot_utils.testing.__                                                              import __
from osbot_utils.type_safe.Type_Safe                                                     import Type_Safe
from osbot_utils.utils.Objects                                                           import base_classes
from mgraph_ai_service_github_digest.service.cache.schemas.Schema__Cache__Store__Request import Schema__Cache__Store__Request


class test_Schema__Cache__Store__Request(TestCase):

    def test__init__(self):                                                         # Test schema initialization
        with Schema__Cache__Store__Request() as _:
            assert type(_)           is Schema__Cache__Store__Request
            assert base_classes(_)   == [Type_Safe, object]

            # Verify types
            assert type(_.strategy)  is type(None)
            assert type(_.namespace) is type(None)
            assert type(_.data)      is bytes

            # Verify defaults using .obj()
            assert _.obj() == __(strategy  = None   ,
                                 namespace = None   ,
                                 data      = b''    )

    def test__with_values(self):                                                    # Test with actual values
        test_data = b"test data"
        with Schema__Cache__Store__Request(strategy  = "temporal_latest"           ,
                                          namespace = "test-ns"                    ,
                                          data      = test_data                    ) as _:
            assert _.strategy  == "temporal_latest"
            assert _.namespace == "test-ns"
            assert _.data      == test_data



