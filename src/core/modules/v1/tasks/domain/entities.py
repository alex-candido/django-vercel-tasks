# core/modules/v1/tasks/domain/entities.py

import datetime

from dataclasses import dataclass, field
from typing import Optional

from core.__seedwork.domain.entities import Entity

@dataclass(kw_only=True, frozen=True, slots=True)
class Task(Entity):
    
    title: str
    description: Optional[str] = None
    status: str = "active"
    completed: bool = False
    position: int = 0
    created_at: Optional[datetime.datetime] = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    updated_at: Optional[datetime.datetime] = field(
        default_factory=lambda: datetime.datetime.now(datetime.timezone.utc)
    )
    
    def __post_init__(self):
        if not self.created_at:
            self._set('created_at', datetime.datetime.now(datetime.timezone.utc))
        if not self.updated_at:
            self._set('updated_at', datetime.datetime.now(datetime.timezone.utc))
            
    def completed(self):
        self._set('completed', True)
        self.update_timestamp()

    def incomplete(self):
        self._set('completed', False)
        self.update_timestamp()

    def change_status(self, status: str):
        self._set('status', status)
        self.update_timestamp()
    
    def update(self, title: str, description: Optional[str], position: int):
        self._set('title', title)
        self._set('description', description)
        self._set('position', position)
        self.update_timestamp()
        
    def update_timestamp(self):
        self._set('updated_at', datetime.datetime.now(datetime.timezone.utc))
