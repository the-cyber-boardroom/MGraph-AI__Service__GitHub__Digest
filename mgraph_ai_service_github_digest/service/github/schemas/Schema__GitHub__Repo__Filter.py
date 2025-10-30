from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path     import Safe_Str__File__Path
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref import Schema__GitHub__Repo__Ref


class Schema__GitHub__Repo__Filter(Schema__GitHub__Repo__Ref):
    filter_starts_with: Safe_Str__File__Path = None
    filter_contains   : Safe_Str__File__Path = None
    filter_ends_with  : Safe_Str__File__Path = None
