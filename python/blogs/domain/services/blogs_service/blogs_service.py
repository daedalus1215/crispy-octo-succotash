from dataclasses import replace
from typing import Optional

from blogs.infrastructure.blogs_repository import BlogsRepository
from users.infrastructure.user_repository import UserRepository
from audits.infrastructure.audit_repository import AuditRepository

class BlogsService:
    def __init__(self, blog_repository: BlogsRepository, user_repository: UserRepository, audit_repository: AuditRepository) -> None:
        self._blog_repo = blog_repository
        self._user_repo = user_repository
        self._audit_repo = audit_repository

    def update_blog(self, 
                    blog_id: int, 
                    author_id: int, 
                    dto: dict[str, str], 
                    ip_address: Optional[str] = None, 
                    user_agent: Optional[str] = None) -> dict:
        user = self._user_repo.fetch_user(author_id)
        if not user:
            return {"success": False, "message": "Not a valid user"}

        blog = self._blog_repo.fetch_blog(blog_id, author_id)
        if not blog:
            return {"success": False, "message": "Not a valid blog"}

        # Build a dict of only the fields that changed
        changes: dict = {}
        audit: dict = {}
        if "title" in dto and dto["title"]:
            audit["title"] = blog.title
            changes["title"] = dto["title"]
        if "body" in dto and dto["body"]:
            audit["body"] = blog.body
            changes["body"] = dto["body"]

        # dataclasses.replace creates a new immutable instance with the changed fields
        updated_blog = replace(blog, **changes)

        self._audit_repo.log_event(blog_id, 
                            author_id,
                            old_value=audit,
                            action="Updated Blog",
                            new_value=changes,
                            user_agent= user_agent,
                            ip_address= ip_address)

        return {
            "success": True,
            "message": "Blog updated successfully",
            "blog": self._blog_repo.save(updated_blog),
        }

