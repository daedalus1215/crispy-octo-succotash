from __future__ import annotations

from users.domain.entities.user_entity import User

USERS: list[dict] = [
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


class UserRepository:
    """Infrastructure layer — maps raw data into domain entities."""

    def fetch_user(self, user_id: int) -> User | None:
        """Find a user by ID. Returns None when the user does not exist."""
        row = next((u for u in USERS if u["id"] == user_id), None)
        if row is None:
            return None
        return User.from_dict(row)

    def list_users(self) -> list[User]:
        return [User.from_dict(row) for row in USERS]



