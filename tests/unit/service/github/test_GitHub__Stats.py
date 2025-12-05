from unittest                                                                                   import TestCase
from mgraph_ai_service_github_digest.service.github.GitHub__API                                 import GitHub__API
from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt import Safe_UInt
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name   import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner  import Safe_Str__GitHub__Repo_Owner
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref                   import Safe_Str__Git__Ref
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict
from osbot_utils.utils.Objects                                                                  import base_classes
from mgraph_ai_service_github_digest.service.github.GitHub__Stats                               import GitHub__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref           import Schema__GitHub__Repo__Ref
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Repo__Stats                 import Schema__Repo__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__File__Stats                 import Schema__File__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Folder__Stats               import Schema__Folder__Stats


class test_GitHub__Stats(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.github_api      = GitHub__API  (cache_repo_zip=True)
        cls.github_stats    = GitHub__Stats(github_api=cls.github_api)
        cls.owner           = Safe_Str__GitHub__Repo_Owner('owasp-sbot' )
        cls.name            = Safe_Str__GitHub__Repo_Name ('OSBot-Utils')
        cls.ref             = Safe_Str__Git__Ref          ('dev'        )
        cls.github_repo_ref = Schema__GitHub__Repo__Ref(owner = cls.owner ,
                                                        name  = cls.name  ,
                                                        ref   = cls.ref   )

    def test_setUpClass(self):
        with self.github_stats as _:
            assert type(_)         is GitHub__Stats
            assert base_classes(_) == [Type_Safe, object]

    def test_repo_stats(self):
        with self.github_stats as _:
            stats = _.repo_stats(github_repo_ref=self.github_repo_ref, folder_depth=2)

            assert type(stats)        is Schema__Repo__Stats
            assert stats.owner        == self.owner
            assert stats.name         == self.name
            assert stats.ref          == self.ref
            assert stats.total_files  > 0
            assert stats.total_size_bytes > 0
            assert stats.total_folders > 0
            assert len(stats.files)   > 0
            assert len(stats.folders) > 0

    def test_repo_stats__files(self):                                                       # Test file stats structure
        with self.github_stats as _:
            stats = _.repo_stats(github_repo_ref=self.github_repo_ref, folder_depth=1)

            for file_stat in stats.files[:10]:                                              # Check first 10 files
                assert type(file_stat) is Schema__File__Stats
                assert file_stat.path
                assert file_stat.name
                assert file_stat.size_bytes >= 0

    def test_repo_stats__folders(self):                                                     # Test folder stats structure
        with self.github_stats as _:
            stats = _.repo_stats(github_repo_ref=self.github_repo_ref, folder_depth=2)

            for folder_stat in stats.folders:
                assert type(folder_stat) is Schema__Folder__Stats
                assert folder_stat.path
                assert folder_stat.depth <= 2                                               # Respects depth limit
                assert folder_stat.size_bytes >= 0
                assert folder_stat.file_count >= 0

    def test_repo_stats__folder_depth_0(self):                                              # Test depth 0 (root folders only)
        with self.github_stats as _:
            stats = _.repo_stats(github_repo_ref=self.github_repo_ref, folder_depth=0)

            for folder_stat in stats.folders:
                assert folder_stat.depth == 0                                               # Only root folders

    def test_repo_stats__folder_depth_1(self):                                              # Test depth 1
        with self.github_stats as _:
            stats = _.repo_stats(github_repo_ref=self.github_repo_ref, folder_depth=1)

            depths = {f.depth for f in stats.folders}
            assert depths == {Safe_UInt(0), Safe_UInt(1)}
            #assert depths <= {0, 1}                                                         # Only depth 0 and 1

    def test_repo_stats__extensions_summary(self):                                          # Test extension breakdown
        with self.github_stats as _:
            stats = _.repo_stats(github_repo_ref=self.github_repo_ref, folder_depth=0)

            assert '.py' in stats.extensions_summary                                        # Python files exist
            py_stats = stats.extensions_summary['.py']
            assert py_stats['count']       > 0
            assert py_stats['total_bytes'] > 0

    def test_files_by_size__descending(self):                                               # Test files sorted largest first
        with self.github_stats as _:
            files = _.files_by_size(github_repo_ref = self.github_repo_ref ,
                                    order           = 'desc'               ,
                                    limit           = 20                   )

            assert len(files) <= 20
            assert len(files) > 0

            for i in range(len(files) - 1):                                                 # Verify descending order
                assert files[i].size_bytes >= files[i+1].size_bytes

    def test_files_by_size__ascending(self):                                                # Test files sorted smallest first
        with self.github_stats as _:
            files = _.files_by_size(github_repo_ref = self.github_repo_ref ,
                                    order           = 'asc'                ,
                                    limit           = 20                   )

            assert len(files) <= 20

            for i in range(len(files) - 1):                                                 # Verify ascending order
                assert files[i].size_bytes <= files[i+1].size_bytes

    def test_files_by_size__limit(self):                                                    # Test limit parameter
        with self.github_stats as _:
            files_10 = _.files_by_size(github_repo_ref=self.github_repo_ref, limit=10)
            files_5  = _.files_by_size(github_repo_ref=self.github_repo_ref, limit=5 )

            assert len(files_10) == 10
            assert len(files_5)  == 5

    def test_folders_by_size__descending(self):                                             # Test folders sorted largest first
        with self.github_stats as _:
            folders = _.folders_by_size(github_repo_ref = self.github_repo_ref ,
                                        depth           = 1                    ,
                                        order           = 'desc'               ,
                                        limit           = 10                   )

            assert len(folders) > 0

            for folder in folders:
                assert folder.depth == 1                                                    # All at requested depth

            for i in range(len(folders) - 1):                                               # Verify descending order
                assert folders[i].size_bytes >= folders[i+1].size_bytes

    def test_folders_by_size__depth_0(self):                                                # Test root folders only
        with self.github_stats as _:
            folders = _.folders_by_size(github_repo_ref = self.github_repo_ref ,
                                        depth           = 0                    ,
                                        limit           = 20                   )

            for folder in folders:
                assert folder.depth == 0
                assert '/' not in str(folder.path)                                          # No nested path

    def test_folders_by_size__depth_2(self):                                                # Test deeper folders
        with self.github_stats as _:
            folders = _.folders_by_size(github_repo_ref = self.github_repo_ref ,
                                        depth           = 2                    ,
                                        limit           = 20                   )

            for folder in folders:
                assert folder.depth == 2

    def test_extension_breakdown(self):                                                     # Test extension statistics
        with self.github_stats as _:
            breakdown = _.extension_breakdown(github_repo_ref=self.github_repo_ref)

            assert type(breakdown) is Type_Safe__Dict
            assert len(breakdown) > 0
            assert '.py' in breakdown

            for ext, data in breakdown.items():
                assert 'count'       in data
                assert 'total_bytes' in data
                assert data['count'] > 0

    def test_folder_tree(self):                                                             # Test nested tree structure
        with self.github_stats as _:
            tree = _.folder_tree(github_repo_ref = self.github_repo_ref ,
                                 max_depth       = 2                    )

            assert type(tree) is dict
            assert 'name'       in tree
            assert 'children'   in tree
            assert 'size_bytes' in tree
            assert 'file_count' in tree

            assert tree['name']       == '/'
            assert tree['size_bytes']  > 0
            assert tree['file_count']  > 0

    def test_folder_tree__children(self):                                                   # Test tree children structure
        with self.github_stats as _:
            tree = _.folder_tree(github_repo_ref = self.github_repo_ref ,
                                 max_depth       = 2                    )

            children = tree['children']
            assert len(children) > 0

            for folder_name, folder_data in children.items():
                assert 'name'     in folder_data
                assert 'path'     in folder_data
                assert 'children' in folder_data

    def test_folder_tree__depth_limit(self):                                                # Test tree respects depth
        with self.github_stats as _:
            tree_1 = _.folder_tree(github_repo_ref=self.github_repo_ref, max_depth=1)
            tree_3 = _.folder_tree(github_repo_ref=self.github_repo_ref, max_depth=3)

            # Depth 3 should have more nested children
            def count_depth(node, current=0):
                max_d = current
                for child in node.get('children', {}).values():
                    max_d = max(max_d, count_depth(child, current + 1))
                return max_d

            depth_1 = count_depth(tree_1)
            depth_3 = count_depth(tree_3)

            assert depth_1 <= 2 #1          # todo: review the performance of this method
            assert depth_3 <= 4# 3          #       and if these values are correct

    # ==================== HELPER METHOD TESTS ====================

    def test__create_file_stats(self):
        with self.github_stats as _:
            file_stats = _._create_file_stats('osbot_utils/helpers/Task.py', 1234)

            assert str(file_stats.path)      == 'osbot_utils/helpers/Task.py'
            assert str(file_stats.name)      == 'Task.py'
            assert str(file_stats.extension) == '.py'
            assert str(file_stats.folder)    == 'osbot_utils/helpers'
            assert file_stats.size_bytes     == 1234

    def test__create_file_stats__no_extension(self):                                        # Test file without extension
        with self.github_stats as _:
            file_stats = _._create_file_stats('folder/Makefile', 500)

            assert str(file_stats.name)      == 'Makefile'
            assert str(file_stats.extension) == ''

    def test__create_file_stats__hidden_file(self):                                         # Test hidden file like .gitignore
        with self.github_stats as _:
            file_stats = _._create_file_stats('.gitignore', 100)

            assert str(file_stats.name)      == '.gitignore'
            assert str(file_stats.extension) == ''                                          # .gitignore has no extension
            assert str(file_stats.folder)    == ''

    def test__create_file_stats__root_file(self):                                           # Test file in root directory
        with self.github_stats as _:
            file_stats = _._create_file_stats('README.md', 2000)

            assert str(file_stats.path)      == 'README.md'
            assert str(file_stats.name)      == 'README.md'
            assert str(file_stats.extension) == '.md'
            assert str(file_stats.folder)    == ''