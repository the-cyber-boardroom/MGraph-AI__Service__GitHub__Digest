from typing                                                                           import List, Optional
from mgraph_ai_service_github_digest.config                                           import GIT_HUB__API__DEFAULT__FILTER_STARTS_WITH, GIT_HUB__API__DEFAULT__FILTER_ENDS_WITH, GIT_HUB__API__DEFAULT__FILTER_CONTAINS
from osbot_utils.type_safe.primitives.domains.files.safe_str.Safe_Str__File__Path     import Safe_Str__File__Path
from mgraph_ai_service_github_digest.service.github.schemas.Schema__GitHub__Repo__Ref import Schema__GitHub__Repo__Ref


class Schema__GitHub__Repo__Filter(Schema__GitHub__Repo__Ref):
    # Existing include filters (AND logic between these)
    filter_starts_with     : Safe_Str__File__Path        = GIT_HUB__API__DEFAULT__FILTER_STARTS_WITH
    filter_contains        : Safe_Str__File__Path        = GIT_HUB__API__DEFAULT__FILTER_CONTAINS
    filter_ends_with       : Safe_Str__File__Path        = GIT_HUB__API__DEFAULT__FILTER_ENDS_WITH

    # Multiple include paths (OR logic) - if set, file must start with ANY of these
    filter_starts_with_any : List[str]

    # Exclusion filters (take priority over includes)
    filter_exclude_paths   : List[str]                     # Exclude if path contains any of these
    filter_exclude_prefixes: List[str]                     # Exclude if starts with any of these
    filter_exclude_suffixes: List[str]                     # Exclude if ends with any of these

    # Size controls
    max_file_size_bytes    : int                           # Skip files larger than this
    max_content_length     : int                           # Truncate content to this length
    truncate_patterns      : List[str]                     # Only truncate files matching these patterns (contains)