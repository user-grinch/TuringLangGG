class Util():
    @staticmethod
    def is_quoted(s: str) -> bool:
        """Check if a string is enclosed in quotes."""
        return s.startswith(('"', "'")) and s.endswith(('"', "'"))