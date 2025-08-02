import requests
from osbot_utils.type_safe.Type_Safe import Type_Safe
from osbot_utils.utils.Http import url_join_safe

SERVER__API_GITHUB_COM = "https://api.github.com"

class GitHub__API(Type_Safe):

    def requests__get(self, path='/'):
        url      = url_join_safe(SERVER__API_GITHUB_COM, path)
        response = requests.get(url)
        return response.json()


    def rate_limit(self):
        return self.requests__get('/rate_limit')

