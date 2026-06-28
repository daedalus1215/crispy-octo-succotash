from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Blog:
    id: int
    author_id: int
    title: str
    body: str

    @classmethod
    def from_dict(cls, data: dict) -> Blog:
        return cls(
            id=data["id"],
            author_id=data["authorId"],
            title=data["title"],
            body=data["body"],
        )

    def to_dict(self) -> dict:
        """Serialize back to the store format (camelCase keys)."""
        return {
            "id": self.id,
            "authorId": self.author_id,
            "title": self.title,
            "body": self.body,
        }
