from osbot_utils.type_safe.Type_Safe                                                 import Type_Safe
from osbot_utils.type_safe.primitives.domains.identifiers.Safe_Id                    import Safe_Id
from mgraph_ai_service_github_digest.service.cache.schemas.Safe_Str__Cache_Namespace import Safe_Str__Cache_Namespace


class Schema__Cache__Store__Request(Type_Safe):                            # Request to store data in cache
    strategy  : Safe_Id                          = None                    # Storage strategy (temporal_latest, etc)
    namespace : Safe_Str__Cache_Namespace        = None                    # Namespace for isolation
    data      : bytes                                                      # Raw data to store
