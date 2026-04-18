import os

import httpx

from app.utils import notion_block_rich_segments, notion_property_rich_text


class Notion:
    def __init__(self):
        self.api_key = os.getenv("NOTION_API_KEY", "").strip()
        self.database_id = os.getenv("NOTION_DATABASE_ID", "").strip()

    async def create_page(self, meeting_id, title, meeting_date, parsed: dict):
        if not self.api_key or not self.database_id:
            raise ValueError("Set NOTION_API_KEY and NOTION_DATABASE_ID")

        hdr = {
            "Authorization": f"Bearer {self.api_key}",
            "Notion-Version": "2022-06-28",
            "Content-Type": "application/json",
        }

        summary_lines = parsed.get("summary") or []
        action_lines = parsed.get("action_items") or []
        decision_lines = parsed.get("key_decisions") or []

        ds = (meeting_date or "").strip()
        date_prop = (
            {"date": {"start": ds[:10]}}
            if len(ds) >= 10 and ds[4] == "-" and ds[7] == "-"
            else {"date": None}
        )

        body = {
            "parent": {"database_id": self.database_id},
            "properties": {
                "Title": {"title": [{"type": "text", "text": {"content": title[:2000]}}]},
                "Meeting ID": notion_property_rich_text(meeting_id),
                "Date": date_prop,
            },
        }

        meta = f"Meeting ID: {meeting_id}" + (f" · {meeting_date}" if meeting_date else "")
        seg = notion_block_rich_segments

        kids = [
            {"object": "block", "type": "paragraph", "paragraph": {"rich_text": seg(meta)}},
            {"object": "block", "type": "heading_2", "heading_2": {"rich_text": seg("Summary")}},
        ]
        if summary_lines:
            for line in summary_lines:
                kids.append(
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {"rich_text": seg(str(line))},
                    }
                )
        else:
            kids.append(
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": seg("(none)")}}
            )

        kids.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": seg("Action items")}})
        if action_lines:
            for line in action_lines:
                kids.append(
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {"rich_text": seg(str(line))},
                    }
                )
        else:
            kids.append(
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": seg("(none)")}}
            )

        kids.append({"object": "block", "type": "heading_2", "heading_2": {"rich_text": seg("Key decisions")}})
        if decision_lines:
            for line in decision_lines:
                kids.append(
                    {
                        "object": "block",
                        "type": "bulleted_list_item",
                        "bulleted_list_item": {"rich_text": seg(str(line))},
                    }
                )
        else:
            kids.append(
                {"object": "block", "type": "paragraph", "paragraph": {"rich_text": seg("(none)")}}
            )

        async with httpx.AsyncClient() as client:
            r = await client.post(
                "https://api.notion.com/v1/pages",
                headers=hdr,
                json=body,
                timeout=60.0,
            )
            if not r.is_success:
                raise RuntimeError(f"Notion create page: {r.status_code} {r.text}")
            page_id = r.json()["id"]

            for i in range(0, len(kids), 100):
                ra = await client.patch(
                    f"https://api.notion.com/v1/blocks/{page_id}/children",
                    headers=hdr,
                    json={"children": kids[i : i + 100]},
                    timeout=60.0,
                )
                if not ra.is_success:
                    raise RuntimeError(f"Notion append blocks: {ra.status_code} {ra.text}")

            return page_id
