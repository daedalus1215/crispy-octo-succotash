import { BlogsA0Controller } from "./blogs/blogs.controller.ts";

(() => {
    const blogController = new BlogsA0Controller();

    console.log('=== Blog Controller with Audit Trail Demo ===\n');

    // Demo 1: update Hamilton's blog with audit trail
    console.log('1. Updating Hamilton\'s blog (ID: 1) with audit trail...');

    const updateResult = blogController.updateBlog(
        1, 
        { 
            title: 'Updated Federalist No. 1 - Revised Edition', 
            body: 'This is a revised version with additional commentary' 
        },
        2, // Hamilton's ID
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_5_7)', // User Agent
        '192.168.1.100' // IP Address
    )

    console.log('\nUpdated Result: ', updateResult)
})()