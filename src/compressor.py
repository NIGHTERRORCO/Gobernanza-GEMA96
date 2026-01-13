import difflib

class SemanticCompressor:
    """
    Module A: Semantic Compressor (Delta)
    Calculates the difference between old and new context to save tokens.
    """

    def calculate_delta(self, old_context: str, new_context: str) -> str:
        """
        Returns the delta (changes) between old_context and new_context.
        If no relation, returns new_context.
        """
        if not old_context:
            return new_context

        # Optimization: If identical, return empty delta marker
        if old_context == new_context:
            return "<DELTA:NO_CHANGE>"

        # Simple delta logic: Subtract common prefix/suffix or use diff
        # For this protocol implementation, we strictly return the part that is NEW.

        # Check if new_context starts with old_context (simple append scenario)
        if new_context.startswith(old_context):
            return new_context[len(old_context):]

        # Fallback to standard diff generation for complex changes
        # (Simulating complex semantic compression)
        d = difflib.Differ()
        diff = list(d.compare(old_context.splitlines(), new_context.splitlines()))

        # Filter only added lines for "Forward Delta"
        added_lines = [line[2:] for line in diff if line.startswith('+ ')]

        if not added_lines:
             # If strictly removing content, we return the whole new context
             # because we can't 'subtract' tokens in a generation stream easily without advanced state management.
             return new_context

        return "\n".join(added_lines)
