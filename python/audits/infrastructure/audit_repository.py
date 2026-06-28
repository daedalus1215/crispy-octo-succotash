from typing import Any, Optional
from datetime import datetime, timezone

# Audit trail for tracking blog updates
AUDIT_LOGS: list[dict[str, Any]] = []

class AuditRepository:
    def __init__(self) -> None:
        pass

    def log_event(
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

        # Audit trail methods
    def get_all_audit_logs(self) -> list[dict[str, Any]]:
        return list(AUDIT_LOGS)

    def get_audit_logs_by_blog(self, blog_id: int) -> list[dict[str, Any]]:
        return [log for log in AUDIT_LOGS if log["blogId"] == blog_id]

    def get_audit_logs_by_user(self, user_id: int) -> list[dict[str, Any]]:
        return [log for log in AUDIT_LOGS if log["userId"] == user_id]

    def get_audit_log_by_id(self, audit_log_id: int) -> Optional[dict[str, Any]]:
        return next((log for log in AUDIT_LOGS if log["id"] == audit_log_id), None)

    def get_audit_logs_by_action(self, action: str) -> list[dict[str, Any]]:
        return [log for log in AUDIT_LOGS if log["action"] == action]
