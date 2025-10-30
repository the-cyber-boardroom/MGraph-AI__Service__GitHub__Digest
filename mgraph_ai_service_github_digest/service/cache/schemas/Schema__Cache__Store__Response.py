from typing                                                                     import Dict
from osbot_utils.type_safe.Type_Safe                                            import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_UInt                            import Safe_UInt
from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Hash import Safe_Str__Cache_Hash
from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Id   import Safe_Str__Cache_Id


class Schema__Cache__Store__Response(Type_Safe):                           # Response from store operation
    cache_id  : Safe_Str__Cache_Id                                         # Unique ID for this cache entry
    hash      : Safe_Str__Cache_Hash                = None                 # Content hash
    paths     : Dict[str, list]                                            # Storage paths by category
    size      : Safe_UInt                                                  # Size in bytes
