# core/__seedwork/domain/repositories.py

import abc
import math

from abc import ABC
from dataclasses import dataclass, field
from typing import Any, Generic, List, Optional, TypeVar

from core.__seedwork.domain.entities import Entity


ET = TypeVar('ET', bound=Entity)

class RepositoryInterface(Generic[ET]):
    
    @abc.abstractmethod
    def create_one(self, entity: ET) -> None:
        raise NotImplementedError()