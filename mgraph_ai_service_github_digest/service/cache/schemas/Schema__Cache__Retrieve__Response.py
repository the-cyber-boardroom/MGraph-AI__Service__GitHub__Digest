from typing                                                                   import Dict
from osbot_utils.type_safe.Type_Safe                                          import Type_Safe
from osbot_utils.type_safe.primitives.core.Safe_Str                           import Safe_Str
from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Id import Safe_Str__Cache_Id


class Schema__Cache__Retrieve__Response(Type_Safe):                        # Response from retrieve operation
    data         : bytes                                                   # Retrieved data
    metadata     : Dict                                                    # Cache metadata
    data_type    : Safe_Str                                                # Type of data (binary, json, string)
    cache_hit    : bool                      = True                        # Was this from cache
    cached_at    : Safe_Str                  = None                        # When was it cached
    cache_id     : Safe_Str__Cache_Id        = None                        # Cache entry ID
