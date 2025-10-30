from osbot_utils.type_safe.Type_Safe                                                            import Type_Safe
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Name   import Safe_Str__GitHub__Repo_Name
from osbot_utils.type_safe.primitives.domains.git.github.safe_str.Safe_Str__GitHub__Repo_Owner  import Safe_Str__GitHub__Repo_Owner


class Schema__GitHub__Repo(Type_Safe):
    owner : Safe_Str__GitHub__Repo_Owner    = None
    name  : Safe_Str__GitHub__Repo_Name     = None

