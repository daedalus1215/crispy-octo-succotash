from blogs.domain.services.blogs_service.blogs_service_factory import BlogsServiceFactory
from blogs.application.blogs_controller.blogs_controller import BlogsController

class BlogsControllerFactory:
    
    @classmethod
    def create(cls):
        return BlogsController(BlogsServiceFactory.create())
        