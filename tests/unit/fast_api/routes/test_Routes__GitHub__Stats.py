from unittest                                                               import TestCase
from osbot_fast_api.api.routes.Fast_API__Routes                             import Fast_API__Routes
from osbot_utils.type_safe.Type_Safe                                        import Type_Safe
from osbot_utils.type_safe.type_safe_core.collections.Type_Safe__Dict import Type_Safe__Dict
from osbot_utils.utils.Objects                                              import base_classes
from starlette.responses                                                    import PlainTextResponse
from mgraph_ai_service_github_digest.fast_api.routes.Routes__GitHub__Stats  import Routes__GitHub__Stats


class test_Routes__GitHub__Stats(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.routes_github_stats = Routes__GitHub__Stats()

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

    # ==================== FILES TABLE VIEW TESTS ====================

    def test_files_by_size_view_table(self):                                                # Test table view
        with self.routes_github_stats as _:
            response = _.files_by_size_view_table(limit=10)

            assert type(response)      is PlainTextResponse
            assert response.media_type == 'text/plain'

            text = response.body.decode('utf-8')
            assert 'Files by Size'     in text
            assert 'Path'              in text
            assert 'Size (bytes)'      in text
            assert 'Extension'         in text
            assert '┌'                 in text                                              # Table border chars
            assert '└'                 in text

    def test_files_by_size_view_table__footer(self):                                        # Test footer in table
        with self.routes_github_stats as _:
            response = _.files_by_size_view_table(limit=5)
            text     = response.body.decode('utf-8')

            assert 'Total:'   in text
            assert 'files'    in text
            assert 'bytes'    in text

    # ==================== FOLDERS TESTS ====================

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

    # ==================== FOLDERS TABLE VIEW TESTS ====================

    def test_folders_by_size_view_table(self):                                              # Test table view
        with self.routes_github_stats as _:
            response = _.folders_by_size_view_table(depth=1, limit=10)

            assert type(response)      is PlainTextResponse
            assert response.media_type == 'text/plain'

            text = response.body.decode('utf-8')
            assert 'Folders by Size'   in text
            assert 'depth=1'           in text
            assert 'Path'              in text
            assert 'Files'             in text
            assert 'Subfolders'        in text
            assert '┌'                 in text
            assert '└'                 in text

    def test_folders_by_size_view_table__different_depths(self):                            # Test different depths
        with self.routes_github_stats as _:
            response_0 = _.folders_by_size_view_table(depth=0, limit=10)
            response_2 = _.folders_by_size_view_table(depth=2, limit=10)

            text_0 = response_0.body.decode('utf-8')
            text_2 = response_2.body.decode('utf-8')

            assert 'depth=0' in text_0
            assert 'depth=2' in text_2

    # ==================== FOLDERS TREE VIEW TESTS ====================

    def test_folders_by_size_view_tree(self):                                               # Test tree view
        with self.routes_github_stats as _:
            response = _.folders_by_size_view_tree(max_depth=2)

            assert type(response)      is PlainTextResponse
            assert response.media_type == 'text/plain'

            text = response.body.decode('utf-8')
            assert '📁'               in text                                               # Folder emoji
            assert 'Total:'           in text
            assert 'files'            in text

    def test_folders_by_size_view_tree__structure(self):                                    # Test tree structure chars
        with self.routes_github_stats as _:
            response = _.folders_by_size_view_tree(max_depth=3)
            text     = response.body.decode('utf-8')

            assert '├── ' in text or '└── ' in text                                         # Tree connectors

    def test_folders_by_size_view_tree__with_sizes(self):                                   # Test sizes in tree
        with self.routes_github_stats as _:
            response = _.folders_by_size_view_tree(max_depth=2, show_size=True)
            text     = response.body.decode('utf-8')

            # Should have size info (KB, MB, or B)
            assert 'KB' in text or 'MB' in text or ' B' in text
            assert 'files' in text

    def test_folders_by_size_view_tree__without_sizes(self):                                # Test tree without sizes
        with self.routes_github_stats as _:
            response = _.folders_by_size_view_tree(max_depth=2, show_size=False)
            text     = response.body.decode('utf-8')

            # Still has folder structure
            assert '📁' in text
            # But individual folder lines shouldn't have size info (except header)
            lines = text.split('\n')
            folder_lines = [l for l in lines if '├── 📁' in l or '└── 📁' in l]
            for line in folder_lines:
                assert 'KB' not in line                                                     # No size in folder lines

    # ==================== EXTENSION BREAKDOWN TESTS ====================

    def test_extension_breakdown(self):
        with self.routes_github_stats as _:
            result = _.extension_breakdown()

            assert type(result) is Type_Safe__Dict
            assert '.py' in result                                                          # Python files exist

            py_stats = result['.py']
            assert 'count'       in py_stats
            assert 'total_bytes' in py_stats
            assert py_stats['count'] > 0

    def test_extension_breakdown_view_table(self):                                          # Test table view
        with self.routes_github_stats as _:
            response = _.extension_breakdown_view_table()

            assert type(response)      is PlainTextResponse
            assert response.media_type == 'text/plain'

            text = response.body.decode('utf-8')
            assert 'Extension Breakdown' in text
            assert 'Extension'           in text
            assert 'Count'               in text
            assert 'Total Size'          in text
            assert 'Avg Size'            in text
            assert '.py'                 in text                                            # Python extension

    def test_extension_breakdown_view_table__order_by_count(self):                          # Test order by count
        with self.routes_github_stats as _:
            response = _.extension_breakdown_view_table(order='count')
            text     = response.body.decode('utf-8')

            assert 'Extension Breakdown' in text

    # ==================== FOLDER TREE TESTS ====================

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

            # But depth 3 should have more nested children
            def max_depth(node, current=0):
                max_d = current
                for child in node.get('children', {}).values():
                    max_d = max(max_d, max_depth(child, current + 1))
                return max_d

            assert max_depth(result_1) <= 2 # see if this should be 1
            assert max_depth(result_3) >= max_depth(result_1)

    def test_repo_stats__custom_repo(self):                                                 # Test with different repo
        with self.routes_github_stats as _:
            result = _.repo_stats(owner = 'the-cyber-boardroom'              ,
                                  name  = 'MGraph-AI__Service__GitHub__Digest',
                                  ref   = 'dev'                              )

            assert result['owner'] == 'the-cyber-boardroom'
            assert result['name']  == 'MGraph-AI__Service__GitHub__Digest'
            assert result['ref']   == 'dev'