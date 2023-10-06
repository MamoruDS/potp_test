from enum import Flag
from os import PathLike
from typing import (
    Generic,
    Iterator,
    Optional,
    Protocol,
    Type,
    TypeVar,
    Union,
)
from typing_extensions import Self, NoReturn

import h5py
import numpy as np
import numpy.typing as npt

Path = Union[str, PathLike]
VideoItem = tuple[npt.NDArray[np.uint8], npt.NDArray[np.float32]]

A = TypeVar("A", bound=Flag)
V = TypeVar("V", bound="Video")
D = TypeVar("D", bound="Dataset")


class NoAttribute(Flag):
    NONE = 0


class Attribute(Protocol, Generic[A]):
    flag_cls: Type[A]
    flag_none: A
    names_map: dict[str, A]

    def get_attribute(self, name: str) -> A | NoReturn:
        ...


class Dataset(Protocol, Generic[V, A]):
    name: str
    video_vls: Type[V]
    attr: Attribute[A] | None
    _h5: h5py.File | None

    def __init__(
        self,
        name: str,
        h5fp: Path,
        video_cls: Type[V],
        attr: Type[A] | None = None,
    ) -> None:
        ...

    def _get_video(self, v_name: str) -> V:
        ...

    def __getitem__(self, idx: Union[int, str]) -> V:
        ...

    def __len__(self) -> int:
        ...

    def __iter__(self) -> Iterator[V]:
        ...


class Video(Protocol, Generic[D, A]):
    name: str
    attrs: A | None

    _dataset: D
    _node: h5py.Group
    _frames: h5py.Dataset
    _gt_bboxes: h5py.Dataset

    @classmethod
    def create(cls, dataset: D, node: h5py.Group, name: str) -> Self:
        ...

    def __len__(self) -> int:
        ...

    def __getitem__(self, idx: int) -> VideoItem:
        ...

    def __iter__(self) -> Iterator[VideoItem]:
        ...
