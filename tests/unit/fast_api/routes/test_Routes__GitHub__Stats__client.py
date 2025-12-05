from unittest                                import TestCase
from tests.unit.Service__Fast_API__Test_Objs import setup__service_fast_api_test_objs, TEST_API_KEY__NAME, TEST_API_KEY__VALUE


class test_Routes__GitHub__Stats__client(TestCase):

    @classmethod
    def setUpClass(cls):
        with setup__service_fast_api_test_objs() as _:
            cls.client                         = _.fast_api__client
            cls.client.headers[TEST_API_KEY__NAME] = TEST_API_KEY__VALUE

    def test__repo_stats(self):
        response = self.client.get('/github-stats/repo-stats')

        assert response.status_code == 200
        data = response.json()
        assert 'total_files'        in data
        assert 'total_size_bytes'   in data
        assert 'files'              in data
        assert 'folders'            in data
        assert 'extensions_summary' in data

    def test__repo_stats__with_params(self):                                                # Test with query params
        response = self.client.get('/github-stats/repo-stats',
                                   params={'owner'       : 'owasp-sbot'  ,
                                           'name'        : 'OSBot-Utils' ,
                                           'ref'         : 'dev'         ,
                                           'folder_depth': 3             })

        assert response.status_code == 200
        data = response.json()
        assert data['owner'] == 'owasp-sbot'
        assert data['name']  == 'OSBot-Utils'
        assert data['ref']   == 'dev'

    def test__files_by_size(self):
        response = self.client.get('/github-stats/files-by-size')

        assert response.status_code == 200
        data = response.json()
        assert type(data) is list
        assert len(data) > 0

        for file in data:
            assert 'path'       in file
            assert 'size_bytes' in file

    def test__files_by_size__order_desc(self):                                              # Test descending order
        response = self.client.get('/github-stats/files-by-size',
                                   params={'order': 'desc', 'limit': 20})

        assert response.status_code == 200
        data = response.json()

        for i in range(len(data) - 1):
            assert data[i]['size_bytes'] >= data[i+1]['size_bytes']

    def test__files_by_size__order_asc(self):                                               # Test ascending order
        response = self.client.get('/github-stats/files-by-size',
                                   params={'order': 'asc', 'limit': 20})

        assert response.status_code == 200
        data = response.json()

        for i in range(len(data) - 1):
            assert data[i]['size_bytes'] <= data[i+1]['size_bytes']

    def test__files_by_size__limit(self):                                                   # Test limit parameter
        response = self.client.get('/github-stats/files-by-size',
                                   params={'limit': 10})

        assert response.status_code == 200
        data = response.json()
        assert len(data) == 10

    def test__folders_by_size(self):
        response = self.client.get('/github-stats/folders-by-size')

        assert response.status_code == 200
        data = response.json()
        assert type(data) is list
        assert len(data) > 0

        for folder in data:
            assert 'path'       in folder
            assert 'depth'      in folder
            assert 'size_bytes' in folder
            assert 'file_count' in folder

    def test__folders_by_size__depth(self):                                                 # Test depth parameter
        response = self.client.get('/github-stats/folders-by-size',
                                   params={'depth': 0})

        assert response.status_code == 200
        data = response.json()

        for folder in data:
            assert folder['depth'] == 0

    def test__folders_by_size__depth_2(self):                                               # Test deeper folders
        response = self.client.get('/github-stats/folders-by-size',
                                   params={'depth': 2, 'limit': 10})

        assert response.status_code == 200
        data = response.json()

        for folder in data:
            assert folder['depth'] == 2

    def test__folders_by_size__order(self):                                                 # Test ordering
        response = self.client.get('/github-stats/folders-by-size',
                                   params={'order': 'desc', 'limit': 10})

        assert response.status_code == 200
        data = response.json()

        for i in range(len(data) - 1):
            assert data[i]['size_bytes'] >= data[i+1]['size_bytes']

    def test__extension_breakdown(self):
        response = self.client.get('/github-stats/extension-breakdown')

        assert response.status_code == 200
        data = response.json()
        assert type(data) is dict
        assert '.py' in data

        py_stats = data['.py']
        assert 'count'       in py_stats
        assert 'total_bytes' in py_stats

    def test__folder_tree(self):
        response = self.client.get('/github-stats/folder-tree')

        assert response.status_code == 200
        data = response.json()
        assert 'name'       in data
        assert 'children'   in data
        assert 'size_bytes' in data
        assert 'file_count' in data
        assert data['name'] == '/'

    def test__folder_tree__max_depth(self):                                                 # Test max_depth parameter
        response = self.client.get('/github-stats/folder-tree',
                                   params={'max_depth': 2})

        assert response.status_code == 200
        data = response.json()

        def count_depth(node, current=0):
            max_d = current
            for child in node.get('children', {}).values():
                max_d = max(max_d, count_depth(child, current + 1))
            return max_d

        assert count_depth(data) <= 3 # todo: see if this shouldn't be 2