
const USERS = [
    {
      id: 1,
      name: "Thomas Jefferson",
      bio: "American Founding Father, principal author of the Declaration of Independence, and the third President of the United States. Advocate for agrarian democracy, states' rights, and individual liberty.",
      born: "April 13, 1743",
      died: "July 4, 1826",
      notableWorks: [
        "Declaration of Independence",
        "Notes on the State of Virginia",
        "Virginia Statute for Religious Freedom",
        "First Inaugural Address"
      ]
    },
    {
      id: 2,
      name: "Alexander Hamilton",
      bio: "American Founding Father, co-author of The Federalist Papers, and the first Secretary of the Treasury. Advocate for a strong central government, industrial economy, and national bank.",
      born: "January 11, 1755 or 1757",
      died: "July 12, 1804",
      notableWorks: [
        "Federalist No. 1",
        "Federalist No. 11",
        "Federalist No. 12",
        "Federalist No. 15",
        "Federalist No. 78"
      ]
    }
  ];
  
  const BLOGS = [
    {
      "id": 1,
      "authorId": 2,
      "title": "Federalist No. 1 — General Introduction (Hamilton)",
      "body": "To the People of the State of New York: AFTER an unequivocal experience of the inefficiency of the subsisting federal government, you are called upon to deliberate on a new Constitution for the United States of America."
    },
    {
      "id": 2,
      "authorId": 2,
      "title": "Federalist No. 11 — The Utility of the Union in Respect to Commercial Relations and a Navy (Hamilton)",
      "body": "To the People of the State of New York: THE importance of the Union, in a commercial light, is one of those points about which there is least room to entertain a difference of opinion, and which has, in fact, commanded the most general assent of men who have any acquaintance with the subject."
    },
    {
      "id": 3,
      "authorId": 2,
      "title": "Federalist No. 12 — The Utility of the Union In Respect to Revenue (Hamilton)",
      "body": "To the People of the State of New York: THE effects of Union upon the commercial prosperity of the States have been sufficiently delineated. Its tendency to promote the interests of revenue will be the subject of our present inquiry."
    },
    {
      "id": 4,
      "authorId": 2,
      "title": "Federalist No. 15 — The Insufficiency of the Present Confederation to Preserve the Union (Hamilton)",
      "body": "To the People of the State of New York: IN THE course of the preceding papers, I have endeavored, my fellow-citizens, to place before you, in a clear and convincing light, the importance of Union to your political safety and happiness."
    },
    {
      "id": 5,
      "authorId": 2,
      "title": "Federalist No. 78 — The Judiciary Department (Hamilton)",
      "body": "To the People of the State of New York: WE proceed now to an examination of the judiciary department of the proposed government."
    },
    {
      "id": 6,
      "authorId": 1,
      "title": "A Summary View of the Rights of British America (Jefferson, 1774)",
      "body": "Resolved, that it be an instruction to the said deputies, when assembled in general congress with the deputies from the other states of British America, to propose to the said congress that an humble and dutiful address be presented to his majesty..."
    },
    {
      "id": 7,
      "authorId": 1,
      "title": "Declaration of Independence (Jefferson, 1776)",
      "body": "When in the Course of human events, it becomes necessary for one people to dissolve the political bands which have connected them with another..."
    },
    {
      "id": 8,
      "authorId": 1,
      "title": "First Inaugural Address (Jefferson, March 4, 1801)",
      "body": "Friends and Fellow-Citizens: Called upon to undertake the duties of the first executive office of our country, I avail myself of the presence of that portion of my fellow-citizens which is here assembled..."
    },
    {
      "id": 9,
      "authorId": 1,
      "title": "Notes on the State of Virginia — Preface/Advertisement (Jefferson, 1787 ed.)",
      "body": "ADVERTISEMENT. THE following Notes were written in Virginia in the year 1781, and somewhat corrected and enlarged in the winter of 1782, in answer to Queries proposed to the Author, by a Foreigner of Distinction..."
    },
    {
      "id": 10,
      "authorId": 1,
      "title": "Virginia Statute for Religious Freedom (Jefferson, 1786)",
      "body": "Whereas Almighty God hath created the mind free; that all attempts to influence it by temporal punishments or burthens, or by civil incapacitations, tend only to beget habits of hypocrisy and meanness..."
    }
  ];

  // Audit trail for tracking blog updates
  const AUDIT_LOGS: Array<{
    id: number;
    blogId: number;
    userId: number;
    action: 'title_updated' | 'body_updated' | 'both_updated';
    oldValue?: string;
    newValue?: string;
    timestamp: string;
    userAgent?: string;
    ipAddress?: string;
  }> = [];
  
  export class BlogsA0Controller {
    constructor(){}

    private logAuditEvent(
      blogId: number, 
      userId: number, 
      action: 'title_updated' | 'body_updated' | 'both_updated',
      oldValue?: string,
      newValue?: string,
      userAgent?: string,
      ipAddress?: string
    ): void {
      const auditLog = {
        id: AUDIT_LOGS.length + 1,
        blogId,
        userId,
        action,
        oldValue,
        newValue,
        timestamp: new Date().toISOString(),
        userAgent,
        ipAddress
      };
      
      AUDIT_LOGS.push(auditLog);
    }
  
    public updateBlog(
      blogId: number, 
      updateData: { title?: string; body?: string }, 
      requestingUserId: number,
      userAgent?: string,
      ipAddress?: string
    ): { success: boolean; message: string; blog?: any; auditLogId?: number } {
      // Step 1: Find the blog to update
      const blog = BLOGS.find(b => b.id === blogId);
      if (!blog) {
        return { success: false, message: 'Blog not found' };
      }

      // Step 2: Authorization check - only the author can update their blog
      if (blog.authorId !== requestingUserId) {
        return { success: false, message: 'Unauthorized: You can only update your own blogs' };
      }

      // Step 3: Determine what was updated and log audit events
      const originalTitle = blog.title;
      const originalBody = blog.body;
      let auditLogId: number | undefined;

      if (updateData.title && updateData.body) {
        // Both title and body updated
        blog.title = updateData.title;
        blog.body = updateData.body;
        this.logAuditEvent(
          blogId, 
          requestingUserId, 
          'both_updated',
          `Title: "${originalTitle}" | Body: "${originalBody.substring(0, 100)}..."`,
          `Title: "${updateData.title}" | Body: "${updateData.body.substring(0, 100)}..."`,
          userAgent,
          ipAddress
        );
        auditLogId = AUDIT_LOGS.length;
      } else if (updateData.title) {
        // Only title updated
        blog.title = updateData.title;
        this.logAuditEvent(
          blogId, 
          requestingUserId, 
          'title_updated',
          originalTitle,
          updateData.title,
          userAgent,
          ipAddress
        );
        auditLogId = AUDIT_LOGS.length;
      } else if (updateData.body) {
        // Only body updated
        blog.body = updateData.body;
        this.logAuditEvent(
          blogId, 
          requestingUserId, 
          'body_updated',
          originalBody.substring(0, 100) + '...',
          updateData.body.substring(0, 100) + '...',
          userAgent,
          ipAddress
        );
        auditLogId = AUDIT_LOGS.length;
      }

      return { success: true, message: 'Blog updated successfully', blog, auditLogId };
    }

    // Helper method to get all blogs (for testing)
    public getAllBlogs(): any[] {
      return BLOGS;
    }

    // Helper method to get blogs by author
    public getBlogsByAuthor(authorId: number): any[] {
      return BLOGS.filter(blog => blog.authorId === authorId);
    }

    // Audit trail methods
    public getAllAuditLogs(): any[] {
      return AUDIT_LOGS.map(log => ({
        ...log,
        user: USERS.find(u => u.id === log.userId)?.name || 'Unknown User',
        blog: BLOGS.find(b => b.id === log.blogId)?.title || 'Unknown Blog'
      }));
    }

    public getAuditLogsByBlog(blogId: number): any[] {
      return AUDIT_LOGS
        .filter(log => log.blogId === blogId)
        .map(log => ({
          ...log,
          user: USERS.find(u => u.id === log.userId)?.name || 'Unknown User',
          blog: BLOGS.find(b => b.id === log.blogId)?.title || 'Unknown Blog'
        }));
    }

    public getAuditLogsByUser(userId: number): any[] {
      return AUDIT_LOGS
        .filter(log => log.userId === userId)
        .map(log => ({
          ...log,
          user: USERS.find(u => u.id === log.userId)?.name || 'Unknown User',
          blog: BLOGS.find(b => b.id === log.blogId)?.title || 'Unknown Blog'
        }));
    }

    public getAuditLogById(auditLogId: number): any | null {
      const log = AUDIT_LOGS.find(log => log.id === auditLogId);
      if (!log) return null;
      
      return {
        ...log,
        user: USERS.find(u => u.id === log.userId)?.name || 'Unknown User',
        blog: BLOGS.find(b => b.id === log.blogId)?.title || 'Unknown Blog'
      };
    }

    public getAuditLogsByAction(action: 'title_updated' | 'body_updated' | 'both_updated'): any[] {
      return AUDIT_LOGS
        .filter(log => log.action === action)
        .map(log => ({
          ...log,
          user: USERS.find(u => u.id === log.userId)?.name || 'Unknown User',
          blog: BLOGS.find(b => b.id === log.blogId)?.title || 'Unknown Blog'
        }));
    }
  }
  