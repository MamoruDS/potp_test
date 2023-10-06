from dataclasses import dataclass
from enum import Flag
from typing import NoReturn, Type, TypeVar

from .types import Attribute as _Attribute

A = TypeVar("A", bound=Flag)


@dataclass
class Attribute(_Attribute[A]):
    flag_cls: Type[A]
    flag_none: A
    names_map: dict[str, A]

    def get_attribute(self, name: str) -> A | NoReturn:
        try:
            return self.names_map[name]
        except KeyError:
            for a in self.flag_cls:
                if a.name == name:
                    return a
            raise ValueError(f"{name} is not a valid attribute")
