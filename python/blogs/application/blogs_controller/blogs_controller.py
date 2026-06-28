from typing import Any, Optional

from blogs.domain.services.blogs_service.blogs_service import BlogsService
from blogs.infrastructure.blogs_repository import BlogsRepository
from blogs.domain.entities.blog_entity import Blog
from users.infrastructure.user_repository import UserRepository
from audits.infrastructure.audit_repository import AuditRepository

class BlogsController:
    def __init__(self, blog_service: BlogsService) -> None:
        # Wire up the dependency chain
        self._blog_service = blog_service

    def update_blog(
        self,
        blog_id: int,
        update_data: dict[str, str],  # { "title"?: str, "body"?: str }
        requesting_user_id: int,
        user_agent: Optional[str] = None,
        ip_address: Optional[str] = None,
    ) -> Blog:
        return self._blog_service.update_blog(
            blog_id=blog_id,
            author_id=requesting_user_id,
            dto=update_data,
            ip_address=ip_address,
            user_agent=user_agent
        )



