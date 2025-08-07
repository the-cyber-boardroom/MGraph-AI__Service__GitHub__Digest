from osbot_utils.helpers.safe_str.Safe_Str                                                        import Safe_Str
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.git.Safe_Str__Git__Branch     import Safe_Str__Git__Branch
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.hashes.Safe_Str__SHA1         import Safe_Str__SHA1
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.hashes.Safe_Str__SHA1__Short  import Safe_Str__SHA1__Short
from mgraph_ai_service_github_digest.utils.for_osbot_utils.safe_str.git.Safe_Str__Git__Tag        import Safe_Str__Git__Tag


class Safe_Str__Git__Ref(Safe_Str):
    """
    Safe string class for any GitHub repository reference (branch, tag, or commit SHA).

    This class accepts any valid ref and validates it using the appropriate specialized class.
    It tries to determine the ref type and validate accordingly.

    Used in GitHub API calls like:
    - /repos/{owner}/{repo}/zipball/{ref}
    - /repos/{owner}/{repo}/git/ref/{ref}
    - /repos/{owner}/{repo}/commits/{ref}
    """
    max_length                 = 255
    allow_empty                = False
    trim_whitespace            = True

    def __new__(cls, value=None):
        # First, do basic Safe_Str processing
        if value is None:
            if cls.allow_empty:
                value = ""
            else:
                raise ValueError(f"in {cls.__name__}, value cannot be None when allow_empty is False")

        if not isinstance(value, str):
            value = str(value)

        if cls.trim_whitespace:
            value = value.strip()

        if not cls.allow_empty and (value is None or value == ""):
            raise ValueError("Value cannot be empty when allow_empty is False")

        if len(value) > cls.max_length:
            raise ValueError(f"Value exceeds maximum length of {cls.max_length} characters (was {len(value)})")

        # Try to validate as different ref types
        validation_errors = []

        # Check if it's a full SHA (40 hex chars)
        if len(value) == 40 and all(c in '0123456789abcdefABCDEF' for c in value):
            try:
                Safe_Str__SHA1(value)
                return str.__new__(cls, value)
            except ValueError as e:
                validation_errors.append(f"SHA validation: {e}")

        # Check if it's a short SHA (7 hex chars)
        if len(value) == 7 and all(c in '0123456789abcdefABCDEF' for c in value):
            try:
                Safe_Str__SHA1__Short(value)
                return str.__new__(cls, value)
            except ValueError as e:
                validation_errors.append(f"Short SHA validation: {e}")

        # Try as a tag (tags often have version patterns)
        if cls._looks_like_tag(value):
            try:
                Safe_Str__Git__Tag(value)
                return str.__new__(cls, value)
            except ValueError as e:
                validation_errors.append(f"Tag validation: {e}")

        # Try as a branch (default for non-SHA refs)
        try:
            Safe_Str__Git__Branch(value)
            return str.__new__(cls, value)
        except ValueError as e:
            validation_errors.append(f"Branch validation: {e}")

        # If nothing worked, raise an error with all attempts
        raise ValueError(f"Invalid GitHub ref '{value}'. Validation errors: {'; '.join(validation_errors)}")

    @classmethod
    def _looks_like_tag(cls, value: str) -> bool:
        """Heuristic to determine if a ref looks like a tag."""
        # Common tag patterns
        return (
            (value.startswith('v') and len(value) > 1 and value[1].isdigit()) or
            value.startswith('release-') or
            value.startswith('release/') or
            (value.count('.') >= 2 and any(part.isdigit() for part in value.split('.'))) or
            value in ['stable', 'latest', 'beta', 'alpha']
        )

    @property
    def ref_type(self) -> str:
        """
        Determine the type of this ref.
        Returns: 'sha', 'sha_short', 'tag', or 'branch'
        """
        # Check for full SHA
        if len(self) == 40 and all(c in '0123456789abcdefABCDEF' for c in self):
            return 'sha'

        # Check for short SHA
        if len(self) == 7 and all(c in '0123456789abcdefABCDEF' for c in self):
            return 'sha_short'

        # Check if it looks like a tag
        if self._looks_like_tag(self):
            return 'tag'

        # Default to branch
        return 'branch'

    @property
    def is_sha(self) -> bool:
        """Check if this ref is any type of commit SHA."""
        return self.ref_type in ['sha', 'sha_short']

    @property
    def is_branch(self) -> bool:
        """Check if this ref is likely a branch."""
        return self.ref_type == 'branch'

    @property
    def is_tag(self) -> bool:
        """Check if this ref is likely a tag."""
        return self.ref_type == 'tag'