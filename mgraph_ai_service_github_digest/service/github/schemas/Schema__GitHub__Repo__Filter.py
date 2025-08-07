from osbot_utils.helpers.Safe_Id                        import Safe_Id
from osbot_utils.helpers.safe_str.Safe_Str__File__Path  import Safe_Str__File__Path
from osbot_utils.type_safe.Type_Safe                    import Type_Safe

class Schema__GitHub__Repo(Type_Safe):
    owner : Safe_Str__GitHub__Repo_Owner
    name  :  Safe_Str__GitHub__Repo_Name
    ref   :  Safe_Str__GitHub__Repo_Ref
class Schema__GitHub__Repo__Filter(Type_Safe):
    owner             : Safe_Id              = None
    repo              : Safe_Id              = None
    ref               : Safe_Id              = None
    filter_starts_with: Safe_Str__File__Path = None
    filter_contains   : Safe_Str__File__Path = None
    filter_ends_with  : Safe_Str__File__Path = None
