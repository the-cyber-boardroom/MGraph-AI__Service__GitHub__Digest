from typing                                                                                    import List, Dict
from osbot_utils.type_safe.Type_Safe                                                           import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                                           import Safe_UInt
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name  import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner import Safe_Str__GitHub__Repo_Owner
from osbot_utils.type_safe.primitives.domains.git.safe_str.Safe_Str__Git__Ref                  import Safe_Str__Git__Ref
from mgraph_ai_service_github_digest.service.github.schemas.Schema__File__Stats                import Schema__File__Stats
from mgraph_ai_service_github_digest.service.github.schemas.Schema__Folder__Stats              import Schema__Folder__Stats


class Schema__Repo__Stats(Type_Safe):
    owner                 : Safe_Str__GitHub__Repo_Owner                            # Repository owner
    name                  : Safe_Str__GitHub__Repo_Name                             # Repository name
    ref                   : Safe_Str__Git__Ref                                      # Git ref (branch/tag/commit)

    total_files           : Safe_UInt                                               # Total number of files
    total_size_bytes      : Safe_UInt                                               # Total size in bytes
    total_folders         : Safe_UInt                                               # Total number of folders

    files                 : List[Schema__File__Stats]                               # Individual file stats
    folders               : List[Schema__Folder__Stats]                             # Folder stats at requested depth
    extensions_summary    : Dict[str, Dict[str, int]]                               # Extension -> {count, total_bytes}

    max_depth             : Safe_UInt                                               # Maximum folder depth in repo
    requested_depth       : Safe_UInt                                               # Depth requested for folder stats