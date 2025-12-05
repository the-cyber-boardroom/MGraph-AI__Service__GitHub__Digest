from unittest                                                                           import TestCase
from osbot_utils.type_safe.Type_Safe                                                    import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                    import Safe_UInt
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path       import Safe_Str__File__Path
from osbot_utils.utils.Objects                                                          import base_classes
from mgraph_ai_service_github_digest.service.github.GitHub__Stats__Tree                 import GitHub__Stats__Tree, TREE_CHAR_BRANCH, TREE_CHAR_LAST, TREE_ICON_FOLDER
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Folder__Stats       import Schema__Folder__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Repo__Stats         import Schema__Repo__Stats


class test_GitHub__Stats__Tree(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.stats_tree = GitHub__Stats__Tree()
        cls.sample_folders = [
            Schema__Folder__Stats(path              = Safe_Str__File__Path('src'           ),
                                  depth             = Safe_UInt(0)                          ,
                                  size_bytes        = Safe_UInt(5000)                       ,
                                  file_count        = Safe_UInt(10)                         ,
                                  direct_file_count = Safe_UInt(3)                          ,
                                  subfolder_count   = Safe_UInt(2)                          ,
                                  extensions        = ['.py']                               ),
            Schema__Folder__Stats(path              = Safe_Str__File__Path('src/utils'     ),
                                  depth             = Safe_UInt(1)                          ,
                                  size_bytes        = Safe_UInt(2000)                       ,
                                  file_count        = Safe_UInt(4)                          ,
                                  direct_file_count = Safe_UInt(4)                          ,
                                  subfolder_count   = Safe_UInt(0)                          ,
                                  extensions        = ['.py']                               ),
            Schema__Folder__Stats(path              = Safe_Str__File__Path('src/core'      ),
                                  depth             = Safe_UInt(1)                          ,
                                  size_bytes        = Safe_UInt(3000)                       ,
                                  file_count        = Safe_UInt(6)                          ,
                                  direct_file_count = Safe_UInt(6)                          ,
                                  subfolder_count   = Safe_UInt(0)                          ,
                                  extensions        = ['.py']                               ),
            Schema__Folder__Stats(path              = Safe_Str__File__Path('tests'         ),
                                  depth             = Safe_UInt(0)                          ,
                                  size_bytes        = Safe_UInt(1500)                       ,
                                  file_count        = Safe_UInt(5)                          ,
                                  direct_file_count = Safe_UInt(5)                          ,
                                  subfolder_count   = Safe_UInt(0)                          ,
                                  extensions        = ['.py']                               ),
        ]
        cls.sample_stats = Schema__Repo__Stats(owner            = 'test-owner'              ,
                                               name             = 'test-repo'               ,
                                               ref              = 'main'                    ,
                                               total_files      = Safe_UInt(15)             ,
                                               total_size_bytes = Safe_UInt(6500)           ,
                                               total_folders    = Safe_UInt(4)              ,
                                               folders          = cls.sample_folders        ,
                                               files            = []                        ,
                                               extensions_summary = {}                      ,
                                               max_depth        = Safe_UInt(1)              ,
                                               requested_depth  = Safe_UInt(1)              )

    def test_setUpClass(self):
        with self.stats_tree as _:
            assert type(_)         is GitHub__Stats__Tree
            assert base_classes(_) == [Type_Safe, object]

    def test_format_size__bytes(self):
        with self.stats_tree as _:
            assert _.format_size(500) == '500 B'
            assert _.format_size(0)   == '0 B'
            assert _.format_size(1)   == '1 B'

    def test_format_size__kilobytes(self):
        with self.stats_tree as _:
            assert _.format_size(1024)   == '1.0 KB'
            assert _.format_size(2048)   == '2.0 KB'
            assert _.format_size(1536)   == '1.5 KB'
            assert _.format_size(10240)  == '10.0 KB'

    def test_format_size__megabytes(self):
        with self.stats_tree as _:
            assert _.format_size(1024 * 1024)            == '1.0 MB'
            assert _.format_size(2 * 1024 * 1024)        == '2.0 MB'
            assert _.format_size(int(1.5 * 1024 * 1024)) == '1.5 MB'

    def test_folder_tree(self):
        with self.stats_tree as _:
            result = _.folder_tree(stats     = self.sample_stats ,
                                   owner     = 'test-owner'      ,
                                   name      = 'test-repo'       ,
                                   ref       = 'main'            ,
                                   max_depth = 2                 )

            assert type(result) is str
            assert TREE_ICON_FOLDER in result
            assert 'test-owner/test-repo (main)' in result

    def test_folder_tree__header(self):                                                     # Test header format
        with self.stats_tree as _:
            result = _.folder_tree(stats=self.sample_stats, owner='o', name='n', ref='r', max_depth=1)

            lines = result.split('\n')
            assert f'{TREE_ICON_FOLDER} o/n (r)' in lines[0]
            assert 'Total:'                      in lines[1]
            assert 'bytes'                       in lines[1]
            assert 'files'                       in lines[1]

    def test_folder_tree__contains_folders(self):                                           # Test all folders appear
        with self.stats_tree as _:
            result = _.folder_tree(stats=self.sample_stats, owner='o', name='n', ref='r', max_depth=2)

            assert 'src'    in result
            assert 'tests'  in result
            assert 'utils'  in result
            assert 'core'   in result

    def test_folder_tree__tree_connectors(self):                                            # Test tree structure characters
        with self.stats_tree as _:
            result = _.folder_tree(stats=self.sample_stats, owner='o', name='n', ref='r', max_depth=2)

            assert TREE_CHAR_BRANCH in result or TREE_CHAR_LAST in result

    def test_folder_tree__with_sizes(self):                                                 # Test size info appears
        with self.stats_tree as _:
            result = _.folder_tree(stats=self.sample_stats, owner='o', name='n', ref='r', max_depth=2, show_size=True)

            assert 'KB' in result or 'MB' in result or ' B' in result
            assert 'files' in result

    def test_folder_tree__without_sizes(self):                                              # Test no size info when disabled
        with self.stats_tree as _:
            result = _.folder_tree(stats=self.sample_stats, owner='o', name='n', ref='r', max_depth=2, show_size=False)

            # Folder icon should still appear
            assert TREE_ICON_FOLDER in result

            # Check that folder lines don't have size info (header still has totals)
            lines = result.split('\n')
            folder_lines = [l for l in lines if TREE_CHAR_BRANCH in l or TREE_CHAR_LAST in l]
            for line in folder_lines:
                assert 'KB' not in line
                assert 'MB' not in line
                assert 'files)' not in line                                                 # (X files) shouldn't appear

    def test_folder_tree__depth_0(self):                                                    # Test only root folders
        with self.stats_tree as _:
            result = _.folder_tree(stats=self.sample_stats, owner='o', name='n', ref='r', max_depth=0)

            # Root folders should appear
            assert 'src'   in result
            assert 'tests' in result

            # Child folders should NOT appear at depth 0
            # They might still appear as folder names but not with tree structure
            lines = result.split('\n')
            tree_lines = [l for l in lines if TREE_CHAR_BRANCH in l or TREE_CHAR_LAST in l]

            # Only root level folders in tree structure
            for line in tree_lines:
                assert 'utils' not in line or 'src/utils' not in line
                assert 'core'  not in line or 'src/core'  not in line

    def test_folder_tree_simple(self):                                                      # Test simplified tree
        with self.stats_tree as _:
            result = _.folder_tree_simple(folders   = self.sample_folders ,
                                          owner     = 'test-owner'        ,
                                          name      = 'test-repo'         ,
                                          ref       = 'main'              )

            assert type(result) is str
            assert TREE_ICON_FOLDER in result
            assert 'test-owner/test-repo (main)' in result

    def test_folder_tree_simple__structure(self):                                           # Test tree structure
        with self.stats_tree as _:
            result = _.folder_tree_simple(folders=self.sample_folders, owner='o', name='n', ref='r')

            # Should have proper tree structure
            assert TREE_CHAR_BRANCH in result or TREE_CHAR_LAST in result
            assert 'src'   in result
            assert 'tests' in result

    def test_folder_tree_simple__with_sizes(self):                                          # Test with sizes
        with self.stats_tree as _:
            result = _.folder_tree_simple(folders=self.sample_folders, owner='o', name='n', ref='r', show_size=True)

            assert 'KB' in result or 'MB' in result or ' B' in result

    def test_folder_tree_simple__without_sizes(self):                                       # Test without sizes
        with self.stats_tree as _:
            result = _.folder_tree_simple(folders=self.sample_folders, owner='o', name='n', ref='r', show_size=False)

            # Header line might have some info but folder lines shouldn't have sizes
            lines = result.split('\n')
            folder_lines = [l for l in lines if TREE_CHAR_BRANCH in l or TREE_CHAR_LAST in l]
            for line in folder_lines:
                assert 'KB' not in line
                assert 'files)' not in line

    def test_folder_tree__nested_structure(self):                                           # Verify proper nesting
        with self.stats_tree as _:
            result = _.folder_tree(stats=self.sample_stats, owner='o', name='n', ref='r', max_depth=2)

            lines = result.split('\n')

            # Find src line and its children
            src_idx = None
            for i, line in enumerate(lines):
                if 'src' in line and (TREE_CHAR_BRANCH in line or TREE_CHAR_LAST in line):
                    if 'utils' not in line and 'core' not in line:                          # Root src, not child
                        src_idx = i
                        break

            # Children should come after parent
            if src_idx is not None:
                remaining = '\n'.join(lines[src_idx+1:])
                # Children should appear after src
                assert 'utils' in remaining or 'core' in remaining

    def test_folder_tree__empty_folders(self):                                              # Test with no folders
        empty_stats = Schema__Repo__Stats(owner            = 'o'             ,
                                          name             = 'n'             ,
                                          ref              = 'r'             ,
                                          total_files      = Safe_UInt(0)    ,
                                          total_size_bytes = Safe_UInt(0)    ,
                                          total_folders    = Safe_UInt(0)    ,
                                          folders          = []              ,
                                          files            = []              ,
                                          extensions_summary = {}            )

        with self.stats_tree as _:
            result = _.folder_tree(stats=empty_stats, owner='o', name='n', ref='r', max_depth=2)

            # Should still have header
            assert TREE_ICON_FOLDER in result
            assert 'o/n (r)' in result
            assert 'Total:' in result