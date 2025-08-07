from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo                        import Schema__GitHub__Repo
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.git.Safe_Str__Git__Ref              import Safe_Str__Git__Ref

class Schema__GitHub__Repo__Ref(Schema__GitHub__Repo):
    ref   : Safe_Str__Git__Ref              = None

