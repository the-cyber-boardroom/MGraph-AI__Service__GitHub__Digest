from osbot_utils.type_safe.primitives.safe_str.git.Safe_Str__Git__Ref               import Safe_Str__Git__Ref
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo    import Schema__GitHub__Repo

class Schema__GitHub__Repo__Ref(Schema__GitHub__Repo):
    ref   : Safe_Str__Git__Ref              = None

