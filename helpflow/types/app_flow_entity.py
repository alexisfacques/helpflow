from typing import Callable, Self

from .entity import Entity, EntityDefinition, FieldDefinition

class AppFlowEntity:
    __nested_entities: dict[str, Self] = {}
    __retrieve_handler: str | None = None
    __query_handler: str | None = None
    __write_handler: str | None = None

    def __init__(
        self,
        id: str,
        fields: tuple[FieldDefinition, ...],
        label: str | None = None,
        description: str | None = None
    ) -> None:
        self.__id = id
        self.__label = label
        self.__description = description
        self.__fields = fields

    @property
    def id(self) -> str:
        return self.__id

    @property
    def is_writable(self) -> bool:
        return self.__write_handler is not None
        # TODO: Ensure at least one field is actually writable

    @property
    def entity(self) -> Entity:
        return {
            'entityIdentifier': self.__id,
            'hasNestedEntities': len(self.__nested_entities) > 0,
            'isWritable': self.is_writable,
            'label': self.__label,
            'description': self.__description
        }

    @property
    def entity_definition(self) -> EntityDefinition:
        return {
            'entity': self.entity,
            'fields': list(self.__fields)
        }

    def Retrieve(self):
        def wrapper(fn):
            self.__retrieve_handler = fn
            return fn
        return wrapper

    def Query(self):
        def wrapper(fn):
            self.__query_handler = fn
            return fn
        return wrapper

    def Write(self):
        def wrapper(fn):
            self.__write_handler = fn
            return fn
        return wrapper
    
