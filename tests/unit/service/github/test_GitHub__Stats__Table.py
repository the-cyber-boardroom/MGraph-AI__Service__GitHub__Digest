from unittest                                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                    import Safe_UInt
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path       import Safe_Str__File__Path
from osbot_utils.utils.Objects                                                          import base_classes
from mgraph_ai_service_github_digest.service.github.GitHub__Stats__Table                import GitHub__Stats__Table
from mgraph_ai_service_github_digest.service.github.schemas.Schema__File__Stats         import Schema__File__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Folder__Stats       import Schema__Folder__Stats


class test_GitHub__Stats__Table(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.stats_table = GitHub__Stats__Table()
        cls.sample_files = [
            Schema__File__Stats(path       = Safe_Str__File__Path('src/main.py'    ),
                                name       = Safe_Str__File__Path('main.py'        ),
                                extension  = Safe_Str__File__Path('.py'            ),
                                size_bytes = Safe_UInt(1500)                        ,
                                folder     = Safe_Str__File__Path('src'            )),
            Schema__File__Stats(path       = Safe_Str__File__Path('src/utils.py'   ),
                                name       = Safe_Str__File__Path('utils.py'       ),
                                extension  = Safe_Str__File__Path('.py'            ),
                                size_bytes = Safe_UInt(800)                         ,
                                folder     = Safe_Str__File__Path('src'            )),
            Schema__File__Stats(path       = Safe_Str__File__Path('README.md'      ),
                                name       = Safe_Str__File__Path('README.md'      ),
                                extension  = Safe_Str__File__Path('.md'            ),
                                size_bytes = Safe_UInt(500)                         ,
                                folder     = Safe_Str__File__Path(''               )),
        ]
        cls.sample_folders = [
            Schema__Folder__Stats(path              = Safe_Str__File__Path('src'       ),
                                  depth             = Safe_UInt(0)                      ,
                                  size_bytes        = Safe_UInt(2300)                   ,
                                  file_count        = Safe_UInt(2)                      ,
                                  direct_file_count = Safe_UInt(2)                      ,
                                  subfolder_count   = Safe_UInt(0)                      ,
                                  extensions        = ['.py']                           ),
            Schema__Folder__Stats(path              = Safe_Str__File__Path('tests'     ),
                                  depth             = Safe_UInt(0)                      ,
                                  size_bytes        = Safe_UInt(1200)                   ,
                                  file_count        = Safe_UInt(3)                      ,
                                  direct_file_count = Safe_UInt(3)                      ,
                                  subfolder_count   = Safe_UInt(1)                      ,
                                  extensions        = ['.py']                           ),
        ]

    def test_setUpClass(self):
        with self.stats_table as _:
            assert type(_)         is GitHub__Stats__Table
            assert base_classes(_) == [Type_Safe, object]

    def test_files_table(self):
        with self.stats_table as _:
            result = _.files_table(files = self.sample_files ,
                                   owner = 'test-owner'      ,
                                   name  = 'test-repo'       ,
                                   ref   = 'main'            )

            assert type(result) is str
            assert 'Files by Size: test-owner/test-repo (main)' in result
            assert 'Path'           in result
            assert 'Size (bytes)'   in result
            assert 'Extension'      in result
            assert 'src/main.py'    in result
            assert '1500'           in result
            assert '.py'            in result

    def test_files_table__headers(self):                                                    # Test table has correct headers
        with self.stats_table as _:
            result = _.files_table(files=self.sample_files, owner='o', name='n', ref='r')

            assert '#'              in result
            assert 'Path'           in result
            assert 'Size (bytes)'   in result
            assert 'Size (KB)'      in result
            assert 'Extension'      in result

    def test_files_table__footer(self):                                                     # Test footer with totals
        with self.stats_table as _:
            result = _.files_table(files=self.sample_files, owner='o', name='n', ref='r')

            assert 'Total:'  in result
            assert '3 files' in result
            assert '2,800'   in result                                                      # 1500 + 800 + 500

    def test_files_table__borders(self):                                                    # Test table has borders
        with self.stats_table as _:
            result = _.files_table(files=self.sample_files, owner='o', name='n', ref='r')

            assert '┌' in result
            assert '┐' in result
            assert '└' in result
            assert '┘' in result
            assert '│' in result

    def test_files_table__empty_list(self):                                                 # Test with empty file list
        with self.stats_table as _:
            result = _.files_table(files=[], owner='o', name='n', ref='r')

            assert 'Files by Size' in result
            assert 'Total: 0 files' in result

    def test_folders_table(self):
        with self.stats_table as _:
            result = _.folders_table(folders = self.sample_folders ,
                                     owner   = 'test-owner'        ,
                                     name    = 'test-repo'         ,
                                     ref     = 'main'              ,
                                     depth   = 0                   )

            assert type(result) is str
            assert 'Folders by Size (depth=0)' in result
            assert 'test-owner/test-repo'      in result
            assert 'Path'                      in result
            assert 'Files'                     in result
            assert 'Subfolders'                in result
            assert 'src'                       in result
            assert 'tests'                     in result

    def test_folders_table__headers(self):                                                  # Test table has correct headers
        with self.stats_table as _:
            result = _.folders_table(folders=self.sample_folders, owner='o', name='n', ref='r', depth=1)

            assert '#'              in result
            assert 'Path'           in result
            assert 'Size (bytes)'   in result
            assert 'Size (KB)'      in result
            assert 'Files'          in result
            assert 'Direct Files'   in result
            assert 'Subfolders'     in result

    def test_folders_table__footer(self):                                                   # Test footer with totals
        with self.stats_table as _:
            result = _.folders_table(folders=self.sample_folders, owner='o', name='n', ref='r', depth=0)

            assert 'Total:'     in result
            assert '2 folders'  in result
            assert '5 files'    in result                                                   # 2 + 3

    def test_folders_table__depth_in_title(self):                                           # Test depth shows in title
        with self.stats_table as _:
            result_0 = _.folders_table(folders=self.sample_folders, owner='o', name='n', ref='r', depth=0)
            result_2 = _.folders_table(folders=self.sample_folders, owner='o', name='n', ref='r', depth=2)

            assert 'depth=0' in result_0
            assert 'depth=2' in result_2

    def test_extensions_table(self):
        breakdown = {'.py' : {'count': 10, 'total_bytes': 5000 },
                     '.md' : {'count': 3 , 'total_bytes': 1500 },
                     '.txt': {'count': 2 , 'total_bytes': 200  }}

        with self.stats_table as _:
            result = _.extensions_table(breakdown = breakdown    ,
                                        owner     = 'test-owner' ,
                                        name      = 'test-repo'  ,
                                        ref       = 'main'       )

            assert type(result) is str
            assert 'Extension Breakdown' in result
            assert '.py'                 in result
            assert '.md'                 in result
            assert '.txt'                in result

    def test_extensions_table__headers(self):                                               # Test table has correct headers
        breakdown = {'.py': {'count': 5, 'total_bytes': 2500}}

        with self.stats_table as _:
            result = _.extensions_table(breakdown=breakdown, owner='o', name='n', ref='r')

            assert 'Extension'          in result
            assert 'Count'              in result
            assert 'Total Size (bytes)' in result
            assert 'Total Size (KB)'    in result
            assert 'Avg Size (bytes)'   in result

    def test_extensions_table__order_by_size(self):                                         # Test ordering by size (default)
        breakdown = {'.small': {'count': 100, 'total_bytes': 100  },
                     '.large': {'count': 1  , 'total_bytes': 10000}}

        with self.stats_table as _:
            result = _.extensions_table(breakdown=breakdown, owner='o', name='n', ref='r', order='size')

            # .large should appear before .small in the table
            large_pos = result.find('.large')
            small_pos = result.find('.small')
            assert large_pos < small_pos

    def test_extensions_table__order_by_count(self):                                        # Test ordering by count
        breakdown = {'.few' : {'count': 2  , 'total_bytes': 10000},
                     '.many': {'count': 100, 'total_bytes': 100  }}

        with self.stats_table as _:
            result = _.extensions_table(breakdown=breakdown, owner='o', name='n', ref='r', order='count')

            # .many should appear before .few in the table
            many_pos = result.find('.many')
            few_pos  = result.find('.few')
            assert many_pos < few_pos

    def test_extensions_table__footer(self):                                                # Test footer with totals
        breakdown = {'.py': {'count': 10, 'total_bytes': 5000},
                     '.md': {'count': 5 , 'total_bytes': 2500}}

        with self.stats_table as _:
            result = _.extensions_table(breakdown=breakdown, owner='o', name='n', ref='r')

            assert 'Total:'         in result
            assert '2 extensions'   in result
            assert '15 files'       in result
            assert '7,500'          in result                                               # 5000 + 2500

    def test_extensions_table__avg_size(self):                                              # Test average size calculation
        breakdown = {'.py': {'count': 10, 'total_bytes': 5000}}                             # Avg = 500

        with self.stats_table as _:
            result = _.extensions_table(breakdown=breakdown, owner='o', name='n', ref='r')

            assert '500' in result                                                          # Average size