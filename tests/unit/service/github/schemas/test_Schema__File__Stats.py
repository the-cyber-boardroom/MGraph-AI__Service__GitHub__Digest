from unittest                                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                    import Safe_UInt
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Name       import Safe_Str__File__Name
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path       import Safe_Str__File__Path
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__List                   import Type_Safe__List
from osbot_utils.utils.Objects                                                          import base_classes
from mgraph_ai_service_github_digest.service.github.schemas.Schema__File__Stats         import Schema__File__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Folder__Stats       import Schema__Folder__Stats


class test_Schema__File__Stats(TestCase):

    def test__init__(self):
        with Schema__File__Stats() as _:
            assert type(_)            is Schema__File__Stats
            assert base_classes(_)    == [Type_Safe, object]
            assert type(_.path)       is Safe_Str__File__Path
            assert type(_.name)       is Safe_Str__File__Name
            assert type(_.extension)  is Safe_Str__File__Name
            assert type(_.size_bytes) is Safe_UInt
            assert type(_.folder)     is Safe_Str__File__Path

    def test__init__with_values(self):
        with Schema__File__Stats(path       = Safe_Str__File__Path('src/module/file.py'),
                                 name       = Safe_Str__File__Path('file.py'           ),
                                 extension  = Safe_Str__File__Path('.py'               ),
                                 size_bytes = Safe_UInt(1234)                           ,
                                 folder     = Safe_Str__File__Path('src/module'        )) as _:
            assert _.path       == 'src/module/file.py'
            assert _.name       == 'file.py'
            assert _.extension  == '.py'
            assert _.size_bytes == 1234
            assert _.folder     == 'src/module'

    def test_json_serialization(self):
        original = Schema__File__Stats(path       = Safe_Str__File__Path('test/file.py'),
                                        name       = Safe_Str__File__Path('file.py'     ),
                                        extension  = Safe_Str__File__Path('.py'         ),
                                        size_bytes = Safe_UInt(500)                      ,
                                        folder     = Safe_Str__File__Path('test'        ))

        json_data = original.json()
        restored  = Schema__File__Stats(**json_data)

        assert str(restored.path)       == str(original.path)
        assert str(restored.name)       == str(original.name)
        assert str(restored.extension)  == str(original.extension)
        assert restored.size_bytes      == original.size_bytes
        assert str(restored.folder)     == str(original.folder)


class test_Schema__Folder__Stats(TestCase):

    def test__init__(self):
        with Schema__Folder__Stats() as _:
            assert type(_)                  is Schema__Folder__Stats
            assert base_classes(_)          == [Type_Safe, object]
            assert type(_.path)             is Safe_Str__File__Path
            assert type(_.depth)            is Safe_UInt
            assert type(_.size_bytes)       is Safe_UInt
            assert type(_.file_count)       is Safe_UInt
            assert type(_.direct_file_count) is Safe_UInt
            assert type(_.subfolder_count)  is Safe_UInt
            assert type(_.extensions)       is Type_Safe__List

    def test__init__with_values(self):
        with Schema__Folder__Stats(path              = Safe_Str__File__Path('src/module'),
                                   depth             = Safe_UInt(1)                      ,
                                   size_bytes        = Safe_UInt(50000)                  ,
                                   file_count        = Safe_UInt(25)                     ,
                                   direct_file_count = Safe_UInt(10)                     ,
                                   subfolder_count   = Safe_UInt(3)                      ,
                                   extensions        = ['.py', '.md', '.txt']            ) as _:
            assert _.path              == 'src/module'
            assert _.depth             == 1
            assert _.size_bytes        == 50000
            assert _.file_count        == 25
            assert _.direct_file_count == 10
            assert _.subfolder_count   == 3
            assert _.extensions        == ['.py', '.md', '.txt']

    def test_json_serialization(self):
        original = Schema__Folder__Stats(path              = Safe_Str__File__Path('test'),
                                          depth             = Safe_UInt(0)               ,
                                          size_bytes        = Safe_UInt(10000)           ,
                                          file_count        = Safe_UInt(5)               ,
                                          direct_file_count = Safe_UInt(3)               ,
                                          subfolder_count   = Safe_UInt(2)               ,
                                          extensions        = ['.py']                    )

        json_data = original.json()
        restored  = Schema__Folder__Stats(**json_data)

        assert str(restored.path)          == str(original.path)
        assert restored.depth              == original.depth
        assert restored.size_bytes         == original.size_bytes
        assert restored.file_count         == original.file_count
        assert restored.direct_file_count  == original.direct_file_count
        assert restored.subfolder_count    == original.subfolder_count


