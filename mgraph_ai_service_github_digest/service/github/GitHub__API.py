from osbot_utils.helpers.Safe_Id                                    import Safe_Id
from osbot_utils.type_safe.Type_Safe                                import Type_Safe
from osbot_utils.type_safe.decorators.type_safe                     import type_safe
from mgraph_ai_service_github_digest.service.shared.Http__Requests  import Http__Requests

SERVER__API_GITHUB_COM = "https://api.github.com"

class GitHub__API(Type_Safe):
    http_request : Http__Requests

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.http_request.base_url = SERVER__API_GITHUB_COM

    def apis_available(self):
        return self.http_request.get('/')

    def rate_limit(self):
        return self.http_request.get('/rate_limit')

    @type_safe
    def repository(self, owner: Safe_Id , repo: Safe_Id):
        path = f'/repos/{owner}/{repo}'
        return self.http_request.get(path)

