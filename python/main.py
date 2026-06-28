from python.blogs.application.blogs_controller import BlogsA0Controller


def main() -> None:
    blog_controller = BlogsA0Controller()

    print("=== Blog Controller with Audit Trail Demo ===\n")

    # Demo 1: update Hamilton's blog with audit trail
    print("1. Updating Hamilton's blog (ID: 1) with audit trail...")

    update_result = blog_controller.update_blog(
        1,
        {
            "title": "Updated Federalist No. 1 - Revised Edition",
            "body": "This is a revised version with additional commentary",
        },
        2,  # Hamilton's ID
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_7)",  # User Agent
        "192.168.1.100",  # IP Address
    )

    print("\nUpdated Result: ", update_result)


if __name__ == "__main__":
    main()
