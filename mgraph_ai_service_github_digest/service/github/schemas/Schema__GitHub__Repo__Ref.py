from mgraph_ai_service_github_digest.config                                         import GIT_HUB__API__DEFAULT__REF
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref       import Safe_Str__Git__Ref
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo    import Schema__GitHub__Repo


class Schema__GitHub__Repo__Ref(Schema__GitHub__Repo):
    ref   : Safe_Str__Git__Ref              = GIT_HUB__API__DEFAULT__REF

