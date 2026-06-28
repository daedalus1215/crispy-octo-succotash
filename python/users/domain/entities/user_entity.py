from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class User:
    """Domain entity — represents a user in the system."""

    id: int
    name: str
    bio: str
    born: str
    died: str
    notable_works: list[str]

    @classmethod
    def from_dict(cls, data: dict) -> User:
        """Hydrate a User from a raw dictionary (e.g. a DB row or API payload)."""
        return cls(
            id=data["id"],
            name=data["name"],
            bio=data["bio"],
            born=data["born"],
            died=data["died"],
            notable_works=data["notableWorks"],
        )

