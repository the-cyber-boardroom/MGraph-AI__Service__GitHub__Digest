from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.git.Safe_Str__Git__Ref_Base import Safe_Str__Git__Ref_Base

class Safe_Str__Git__Tag(Safe_Str__Git__Ref_Base):
    """
    Safe string class for GitHub tag names.

    Follows git-check-ref-format rules for tags.
    Tags have the same rules as general Git references.

    Examples:
    - "v1.0.0", "v2.3.4"
    - "release-1.0.0"
    - "2024.01.15"
    - "stable", "latest"
    """
    pass

