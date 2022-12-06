from dataclasses import dataclass


@dataclass
class Role:
    id: str
    name: str
    perms: list
