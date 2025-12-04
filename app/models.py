from typing import List, Optional

from pydantic import BaseModel


class TeamMember(BaseModel):
    name: str
    role: Optional[str] = None
    skills: List[str] = []


class Task(BaseModel):
    id: int
    description: str
    assigned_to: Optional[str] = None
    deadline: Optional[str] = None
    priority: str = "Medium"        # Critical / High / Medium / Low
    dependencies: List[int] = []
    reason: Optional[str] = None
