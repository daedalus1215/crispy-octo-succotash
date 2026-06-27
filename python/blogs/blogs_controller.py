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

BLOGS = [
    {
        "id": 1,
        "authorId": 2,
        "title": "Federalist No. 1 — General Introduction (Hamilton)",
        "body": "To the People of the State of New York: AFTER an unequivocal experience of the inefficiency of the subsisting federal government, you are called upon to deliberate on a new Constitution for the United States of America.",
    },
    {
        "id": 2,
        "authorId": 2,
        "title": "Federalist No. 11 — The Utility of the Union in Respect to Commercial Relations and a Navy (Hamilton)",
        "body": "To the People of the State of New York: THE importance of the Union, in a commercial light, is one of those points about which there is least room to entertain a difference of opinion, and which has, in fact, commanded the most general assent of men who have any acquaintance with the subject.",
    },
    {
        "id": 3,
        "authorId": 2,
        "title": "Federalist No. 12 — The Utility of the Union In Respect to Revenue (Hamilton)",
        "body": "To the People of the State of New York: THE effects of Union upon the commercial prosperity of the States have been sufficiently delineated. Its tendency to promote the interests of revenue will be the subject of our present inquiry.",
    },
    {
        "id": 4,
        "authorId": 2,
        "title": "Federalist No. 15 — The Insufficiency of the Present Confederation to Preserve the Union (Hamilton)",
        "body": "To the People of the State of New York: IN THE course of the preceding papers, I have endeavored, my fellow-citizens, to place before you, in a clear and convincing light, the importance of Union to your political safety and happiness.",
    },
    {
        "id": 5,
        "authorId": 2,
        "title": "Federalist No. 78 — The Judiciary Department (Hamilton)",
        "body": "To the People of the State of New York: WE proceed now to an examination of the judiciary department of the proposed government.",
    },
    {
        "id": 6,
        "authorId": 1,
        "title": "A Summary View of the Rights of British America (Jefferson, 1774)",
        "body": "Resolved, that it be an instruction to the said deputies, when assembled in general congress with the deputies from the other states of British America, to propose to the said congress that an humble and dutiful address be presented to his majesty...",
    },
    {
        "id": 7,
        "authorId": 1,
        "title": "Declaration of Independence (Jefferson, 1776)",
        "body": "When in the Course of human events, it becomes necessary for one people to dissolve the political bands which have connected them with another...",
    },
    {
        "id": 8,
        "authorId": 1,
        "title": "First Inaugural Address (Jefferson, March 4, 1801)",
        "body": "Friends and Fellow-Citizens: Called upon to undertake the duties of the first executive office of our country, I avail myself of the presence of that portion of my fellow-citizens which is here assembled...",
    },
    {
        "id": 9,
        "authorId": 1,
        "title": "Notes on the State of Virginia — Preface/Advertisement (Jefferson, 1787 ed.)",
        "body": "ADVERTISEMENT. THE following Notes were written in Virginia in the year 1781, and somewhat corrected and enlarged in the winter of 1782, in answer to Queries proposed to the Author, by a Foreigner of Distinction...",
    },
    {
        "id": 10,
        "authorId": 1,
        "title": "Virginia Statute for Religious Freedom (Jefferson, 1786)",
        "body": "Whereas Almighty God hath created the mind free; that all attempts to influence it by temporal punishments or burthens, or by civil incapacitations, tend only to beget habits of hypocrisy and meanness...",
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
