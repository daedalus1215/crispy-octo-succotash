from blogs.infrastructure.blogs_repository import BlogsRepository
from users.infrastructure.user_repository import UserRepository
from audits.infrastructure.audit_repository import AuditRepository
from blogs.domain.services.blogs_service.blogs_service import BlogsService

class BlogsServiceFactory:
    
    @classmethod
    def create(cls):
        blog_repo = BlogsRepository()
        user_repo = UserRepository()
        audit_repo = AuditRepository()
        return BlogsService(blog_repo, user_repo, audit_repo)