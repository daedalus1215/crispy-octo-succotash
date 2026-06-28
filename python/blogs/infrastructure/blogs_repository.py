from __future__ import annotations

from blogs.domain.entities.blog_entity import Blog

BLOGS: list[dict] = [
    {
        "id": 1,
        "authorId": 2,
        "title": "Federalist No. 1 \u2014 General Introduction (Hamilton)",
        "body": "To the People of the State of New York: AFTER an unequivocal experience of the inefficiency of the subsisting federal government, you are called upon to deliberate on a new Constitution for the United States of America.",
    },
    {
        "id": 2,
        "authorId": 2,
        "title": "Federalist No. 11 \u2014 The Utility of the Union in Respect to Commercial Relations and a Navy (Hamilton)",
        "body": "To the People of the State of New York: THE importance of the Union, in a commercial light, is one of those points about which there is least room to entertain a difference of opinion, and which has, in fact, commanded the most general assent of men who have any acquaintance with the subject.",
    },
    {
        "id": 3,
        "authorId": 2,
        "title": "Federalist No. 12 \u2014 The Utility of the Union In Respect to Revenue (Hamilton)",
        "body": "To the People of the State of New York: THE effects of Union upon the commercial prosperity of the States have been sufficiently delineated. Its tendency to promote the interests of revenue will be the subject of our present inquiry.",
    },
    {
        "id": 4,
        "authorId": 2,
        "title": "Federalist No. 15 \u2014 The Insufficiency of the Present Confederation to Preserve the Union (Hamilton)",
        "body": "To the People of the State of New York: IN THE course of the preceding papers, I have endeavored, my fellow-citizens, to place before you, in a clear and convincing light, the importance of Union to your political safety and happiness.",
    },
    {
        "id": 5,
        "authorId": 2,
        "title": "Federalist No. 78 \u2014 The Judiciary Department (Hamilton)",
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
        "title": "Notes on the State of Virginia \u2014 Preface/Advertisement (Jefferson, 1787 ed.)",
        "body": "ADVERTISEMENT. THE following Notes were written in Virginia in the year 1781, and somewhat corrected and enlarged in the winter of 1782, in answer to Queries proposed to the Author, by a Foreigner of Distinction...",
    },
    {
        "id": 10,
        "authorId": 1,
        "title": "Virginia Statute for Religious Freedom (Jefferson, 1786)",
        "body": "Whereas Almighty God hath created the mind free; that all attempts to influence it by temporal punishments or burthens, or by civil incapacitations, tend only to beget habits of hypocrisy and meanness...",
    },
]


class BlogsRepository:
    def fetch_blog(self, blog_id: int, author_id: int) -> Blog | None:
        row = next((b for b in BLOGS if b["id"] == blog_id and b["authorId"] == author_id), None)
        if row is None:
            return None
        return Blog.from_dict(row)

    def save(self, blog: Blog) -> Blog:
        BLOGS[blog.id] = blog.to_dict()
        return blog
