"""Notion-related text helpers."""

NOTION_TEXT_LIMIT = 2000


def notion_property_rich_text(text: str) -> dict:
    """Rich text shape for database properties (e.g. Meeting ID)."""
    return {
        "rich_text": [
            {"type": "text", "text": {"content": (text or "-")[:NOTION_TEXT_LIMIT]}}
        ]
    }


def notion_block_rich_segments(text: str) -> list:
    """Inner rich_text array for page blocks."""
    return [{"type": "text", "text": {"content": (text or "")[:NOTION_TEXT_LIMIT]}}]
