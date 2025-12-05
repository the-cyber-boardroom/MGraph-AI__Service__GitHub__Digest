from unittest                                                               import TestCase
from osbot_fast_api.api.routes.Fast_API__Routes                             import Fast_API__Routes
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict
from osbot_utils.utils.Objects                                              import base_classes
from mgraph_ai_service_github_digest.fast_api.routes.Routes__GitHub__Stats  import Routes__GitHub__Stats


class test_Routes__GitHub__Stats(TestCase):

    @classmethod
    def setUpClass(cls):
        with Routes__GitHub__Stats() as _:
            cls.routes_github_stats = _
            _.github_stats.github_api.cache_repo_zip = True

    def test_setUpClass(self):
        with self.routes_github_stats as _:
            assert type(_)         is Routes__GitHub__Stats
            assert base_classes(_) == [Fast_API__Routes, Type_Safe, object]

    def test_repo_stats(self):
        with self.routes_github_stats as _:
            result = _.repo_stats()

            assert type(result) is dict
            assert 'owner'              in result
            assert 'name'               in result
            assert 'ref'                in result
            assert 'total_files'        in result
            assert 'total_size_bytes'   in result
            assert 'files'              in result
            assert 'folders'            in result
            assert 'extensions_summary' in result

    def test_repo_stats__with_depth(self):                                                  # Test folder_depth parameter
        with self.routes_github_stats as _:
            result_0 = _.repo_stats(folder_depth=0)
            result_2 = _.repo_stats(folder_depth=2)

            # Depth 0 should have fewer folders
            folders_0 = [f for f in result_0['folders'] if f['depth'] == 0]
            folders_2 = result_2['folders']

            assert len(folders_0) <= len(folders_2)

    def test_files_by_size(self):
        with self.routes_github_stats as _:
            result = _.files_by_size()

            assert type(result) is list
            assert len(result) > 0
            assert len(result) <= 50                                                        # Default limit

            for file in result:
                assert 'path'       in file
                assert 'name'       in file
                assert 'size_bytes' in file
                assert 'extension'  in file

    def test_files_by_size__order_desc(self):                                               # Test descending order
        with self.routes_github_stats as _:
            result = _.files_by_size(order='desc', limit=20)

            for i in range(len(result) - 1):
                assert result[i]['size_bytes'] >= result[i+1]['size_bytes']

    def test_files_by_size__order_asc(self):                                                # Test ascending order
        with self.routes_github_stats as _:
            result = _.files_by_size(order='asc', limit=20)

            for i in range(len(result) - 1):
                assert result[i]['size_bytes'] <= result[i+1]['size_bytes']

    def test_files_by_size__limit(self):                                                    # Test limit parameter
        with self.routes_github_stats as _:
            result_10 = _.files_by_size(limit=10)
            result_5  = _.files_by_size(limit=5)

            assert len(result_10) == 10
            assert len(result_5)  == 5

    def test_folders_by_size(self):
        with self.routes_github_stats as _:
            result = _.folders_by_size()

            assert type(result) is list
            assert len(result) > 0

            for folder in result:
                assert 'path'       in folder
                assert 'depth'      in folder
                assert 'size_bytes' in folder
                assert 'file_count' in folder

    def test_folders_by_size__depth(self):                                                  # Test depth parameter
        with self.routes_github_stats as _:
            result_0 = _.folders_by_size(depth=0)
            result_1 = _.folders_by_size(depth=1)

            for folder in result_0:
                assert folder['depth'] == 0

            for folder in result_1:
                assert folder['depth'] == 1

    def test_folders_by_size__order(self):                                                  # Test ordering
        with self.routes_github_stats as _:
            result_desc = _.folders_by_size(order='desc', limit=10)
            result_asc  = _.folders_by_size(order='asc' , limit=10)

            for i in range(len(result_desc) - 1):
                assert result_desc[i]['size_bytes'] >= result_desc[i+1]['size_bytes']

            for i in range(len(result_asc) - 1):
                assert result_asc[i]['size_bytes'] <= result_asc[i+1]['size_bytes']

    def test_extension_breakdown(self):
        with self.routes_github_stats as _:
            result = _.extension_breakdown()

            assert type(result) is Type_Safe__Dict
            assert '.py' in result                                                          # Python files exist

            py_stats = result['.py']
            assert 'count'       in py_stats
            assert 'total_bytes' in py_stats
            assert py_stats['count'] > 0

    def test_folder_tree(self):
        with self.routes_github_stats as _:
            result = _.folder_tree()

            assert type(result) is dict
            assert 'name'       in result
            assert 'children'   in result
            assert 'size_bytes' in result
            assert 'file_count' in result
            assert result['name'] == '/'

    def test_folder_tree__max_depth(self):                                                  # Test max_depth parameter
        with self.routes_github_stats as _:
            result_1 = _.folder_tree(max_depth=1)
            result_3 = _.folder_tree(max_depth=3)

            # Both should have the same root structure
            assert result_1['name'] == result_3['name'] == '/'

            # But depth 3 should have deeper nesting
            def max_depth(node, current=0):
                max_d = current
                for child in node.get('children', {}).values():
                    max_d = max(max_d, max_depth(child, current + 1))
                return max_d

            assert max_depth(result_1) <= 2     # see if this should not be 1
            assert max_depth(result_3) >= max_depth(result_1)

    def test_repo_stats__custom_repo(self):                                                 # Test with different repo
        with self.routes_github_stats as _:
            result = _.repo_stats(owner = 'the-cyber-boardroom'              ,
                                  name  = 'MGraph-AI__Service__GitHub__Digest',
                                  ref   = 'dev'                              )

            assert result['owner'] == 'the-cyber-boardroom'
            assert result['name']  == 'MGraph-AI__Service__GitHub__Digest'
            assert result['ref']   == 'dev'