from unittest                                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                    import Safe_UInt
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict                   import Type_Safe__Dict
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                   import Type_Safe__List
from osbot_utils.utils.Objects                                                          import base_classes
from mgraph_ai_service_github_digest.service.github.schemas.Schema__File__Stats         import Schema__File__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Folder__Stats       import Schema__Folder__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Repo__Stats         import Schema__Repo__Stats


class test_Schema__Repo__Stats(TestCase):

    def test__init__(self):
        with Schema__Repo__Stats() as _:
            assert type(_)                    is Schema__Repo__Stats
            assert base_classes(_)            == [Type_Safe, object]
            assert type(_.total_files)        is Safe_UInt
            assert type(_.total_size_bytes)   is Safe_UInt
            assert type(_.total_folders)      is Safe_UInt
            assert type(_.files)              is Type_Safe__List
            assert type(_.folders)            is Type_Safe__List
            assert type(_.extensions_summary) is Type_Safe__Dict
            assert type(_.max_depth)          is Safe_UInt
            assert type(_.requested_depth)    is Safe_UInt

    def test__init__with_minimal_values(self):
        with Schema__Repo__Stats(owner            = 'test-owner' ,
                                  name             = 'test-repo'  ,
                                  ref              = 'main'       ,
                                  total_files      = 100          ,
                                  total_size_bytes = 50000        ) as _:
            assert _.owner            == 'test-owner'
            assert _.name             == 'test-repo'
            assert _.ref              == 'main'
            assert _.total_files      == 100
            assert _.total_size_bytes == 50000

    def test__init__with_nested_objects(self):
        file_stat   = Schema__File__Stats(path       = 'test.py'    ,
                                           name       = 'test.py'    ,
                                           extension  = '.py'        ,
                                           size_bytes = 100          ,
                                           folder     = ''           )
        folder_stat = Schema__Folder__Stats(path              = 'src' ,
                                             depth             = 0    ,
                                             size_bytes        = 1000 ,
                                             file_count        = 5    ,
                                             direct_file_count = 3    ,
                                             subfolder_count   = 1    )

        with Schema__Repo__Stats(owner              = 'test-owner'                      ,
                                  name               = 'test-repo'                       ,
                                  ref                = 'main'                            ,
                                  total_files        = 5                                 ,
                                  total_size_bytes   = 1000                              ,
                                  total_folders      = 1                                 ,
                                  files              = [file_stat]                       ,
                                  folders            = [folder_stat]                     ,
                                  extensions_summary = {'.py': {'count': 5, 'total_bytes': 1000}},
                                  max_depth          = 2                                 ,
                                  requested_depth    = 1                                 ) as _:
            assert len(_.files)   == 1
            assert len(_.folders) == 1
            assert '.py' in _.extensions_summary