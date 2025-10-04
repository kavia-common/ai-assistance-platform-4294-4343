"""
Suggest service that returns a static list of suggestion strings.
"""

from __future__ import annotations

from typing import List


# PUBLIC_INTERFACE
def get_suggestions() -> List[str]:
    """
    Return a static list of helpful prompts a user can try.
    """
    return [
        "Summarize the following text...",
        "Draft an email requesting a project status update.",
        "Explain this code snippet in simple terms.",
        "Generate test cases for this function.",
        "Brainstorm 5 ideas to improve user onboarding.",
    ]
