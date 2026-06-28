from datetime import datetime, timezone
from typing import Any, Optional

USERS = [
    {
        "id": 1,
        "name": "Thomas Jefferson",
        "bio": "American Founding Father, principal author of the Declaration of Independence, and the third President of the United States. Advocate for agrarian democracy, states' rights, and individual liberty.",
        "born": "April 13, 1743",
        "died": "July 4, 1826",
        "notableWorks": [
            "Declaration of Independence",
            "Notes on the State of Virginia",
            "Virginia Statute for Religious Freedom",
            "First Inaugural Address",
        ],
    },
    {
        "id": 2,
        "name": "Alexander Hamilton",
        "bio": "American Founding Father, co-author of The Federalist Papers, and the first Secretary of the Treasury. Advocate for a strong central government, industrial economy, and national bank.",
        "born": "January 11, 1755 or 1757",
        "died": "July 12, 1804",
        "notableWorks": [
            "Federalist No. 1",
            "Federalist No. 11",
            "Federalist No. 12",
            "Federalist No. 15",
            "Federalist No. 78",
        ],
    },
]



# Audit trail for tracking blog updates
AUDIT_LOGS: list[dict[str, Any]] = []


class BlogsA0Controller:
    def __init__(self) -> None:
        pass

    def _log_audit_event(
        self,
        blog_id: int,
        user_id: int,
        action: str,  # 'title_updated' | 'body_updated' | 'both_updated'
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> None:
        audit_log = {
            "id": len(AUDIT_LOGS) + 1,
            "blogId": blog_id,
            "userId": user_id,
            "action": action,
            "oldValue": old_value,
            "newValue": new_value,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "userAgent": user_agent,
            "ipAddress": ip_address,
        }

        AUDIT_LOGS.append(audit_log)

    def update_blog(
        self,
        blog_id: int,
        update_data: dict[str, str],  # { "title"?: str, "body"?: str }
        requesting_user_id: int,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> dict[str, Any]:
        # Step 1: Find the blog to update
        blog = next((b for b in BLOGS if b["id"] == blog_id), None)
        if not blog:
            return {"success": False, "message": "Blog not found"}

        # Step 2: Authorization check - only the author can update their blog
        if blog["authorId"] != requesting_user_id:
            return {
                "success": False,
                "message": "Unauthorized: You can only update your own blogs",
            }

        # Step 3: Determine what was updated and log audit events
        original_title = blog["title"]
        original_body = blog["body"]
        audit_log_id: Optional[int] = None

        title = update_data.get("title")
        body = update_data.get("body")

        if title and body:
            # Both title and body updated
            blog["title"] = title
            blog["body"] = body
            self._log_audit_event(
                blog_id,
                requesting_user_id,
                "both_updated",
                f'Title: "{original_title}" | Body: "{original_body[:100]}..."',
                f'Title: "{title}" | Body: "{body[:100]}..."',
                user_agent,
                ip_address,
            )
            audit_log_id = len(AUDIT_LOGS)
        elif title:
            # Only title updated
            blog["title"] = title
            self._log_audit_event(
                blog_id,
                requesting_user_id,
                "title_updated",
                original_title,
                title,
                user_agent,
                ip_address,
            )
            audit_log_id = len(AUDIT_LOGS)
        elif body:
            # Only body updated
            blog["body"] = body
            self._log_audit_event(
                blog_id,
                requesting_user_id,
                "body_updated",
                original_body[:100] + "...",
                body[:100] + "...",
                user_agent,
                ip_address,
            )
            audit_log_id = len(AUDIT_LOGS)

        return {
            "success": True,
            "message": "Blog updated successfully",
            "blog": blog,
            "auditLogId": audit_log_id,
        }

    # Helper method to get all blogs (for testing)
    def get_all_blogs(self) -> list[dict[str, Any]]:
        return BLOGS

    # Helper method to get blogs by author
    def get_blogs_by_author(self, author_id: int) -> list[dict[str, Any]]:
        return [blog for blog in BLOGS if blog["authorId"] == author_id]

    # Audit trail methods
    def _enrich(self, log: dict[str, Any]) -> dict[str, Any]:
        user = next((u for u in USERS if u["id"] == log["userId"]), None)
        blog = next((b for b in BLOGS if b["id"] == log["blogId"]), None)
        return {
            **log,
            "user": user["name"] if user else "Unknown User",
            "blog": blog["title"] if blog else "Unknown Blog",
        }

    def get_all_audit_logs(self) -> list[dict[str, Any]]:
        return [self._enrich(log) for log in AUDIT_LOGS]

    def get_audit_logs_by_blog(self, blog_id: int) -> list[dict[str, Any]]:
        return [self._enrich(log) for log in AUDIT_LOGS if log["blogId"] == blog_id]

    def get_audit_logs_by_user(self, user_id: int) -> list[dict[str, Any]]:
        return [self._enrich(log) for log in AUDIT_LOGS if log["userId"] == user_id]

    def get_audit_log_by_id(self, audit_log_id: int) -> Optional[dict[str, Any]]:
        log = next((l for l in AUDIT_LOGS if l["id"] == audit_log_id), None)
        if not log:
            return None
        return self._enrich(log)

    def get_audit_logs_by_action(self, action: str) -> list[dict[str, Any]]:
        return [self._enrich(log) for log in AUDIT_LOGS if log["action"] == action]
