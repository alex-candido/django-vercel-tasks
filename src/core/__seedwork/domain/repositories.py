# core/__seedwork/domain/repositories.py

import abc
from abc import ABC
from typing import Any, Dict, Generic, List, Optional, TypeVar

from core.__seedwork.domain.entities import Entity, UniqueEntityId

ET = TypeVar('ET', bound=Entity)

# find_one, find_all, create_one, create_many, update_one, update_many, remove_one, remove_many, search, filter, find_by_id, find_by_ids, exists_by_id, exists_by_ids

class RepositoryInterface(Generic[ET], ABC):

    @abc.abstractmethod
    def find_one(self, key: str, value: Any) -> Optional[ET]:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_all(self) -> List[ET]:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_one(self, entity: ET) -> ET:
        raise NotImplementedError()

    @abc.abstractmethod
    def create_many(self, entities: List[ET]) -> List[ET]:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_one(self, entity_id: UniqueEntityId, data: Dict[str, Any]) -> ET:
        raise NotImplementedError()

    @abc.abstractmethod
    def update_many(self, data_list: List[Dict[str, Any]]) -> List[ET]:
        raise NotImplementedError()

    @abc.abstractmethod
    def remove_one(self, entity_id: UniqueEntityId) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def remove_many(self, entity_ids: List[UniqueEntityId]) -> None:
        raise NotImplementedError()

    @abc.abstractmethod
    def search(self, key: str, value: Any) -> List[ET]:
        raise NotImplementedError()

    @abc.abstractmethod
    def filter(self, **kwargs: Any) -> List[ET]:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_id(self, entity_id: UniqueEntityId) -> ET:
        raise NotImplementedError()

    @abc.abstractmethod
    def find_by_ids(self, entity_ids: List[UniqueEntityId]) -> List[ET]:
        raise NotImplementedError()

    @abc.abstractmethod
    def exists_by_id(self, entity_id: UniqueEntityId) -> bool:
        raise NotImplementedError()

    @abc.abstractmethod
    def exists_by_ids(self, entity_ids: List[UniqueEntityId]) -> bool:
        raise NotImplementedError()
