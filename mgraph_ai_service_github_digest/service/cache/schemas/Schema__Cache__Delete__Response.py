from osbot_utils.type_safe.Type_Safe                                          import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                          import Safe_UInt
from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Id import Safe_Str__Cache_Id


class Schema__Cache__Delete__Response(Type_Safe):                          # Response from delete operation
    deleted      : bool                                                    # Was deletion successful
    cache_id     : Safe_Str__Cache_Id                                      # ID that was deleted
    files_deleted: Safe_UInt                                               # Number of files deleted
