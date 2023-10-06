from enum import Flag
from typing import Iterator, TypeVar

import cv2
import h5py
import numpy as np
import numpy.typing as npt

from .types import Attribute, Video as _Video, VideoItem, D

A = TypeVar("A", bound=Flag)


class Video(_Video[D, A]):
    name: str
    attrs: A | None

    _dataset: D
    _node: h5py.Group
    _frames: h5py.Dataset
    _gt: h5py.Dataset

    def load_attributes(self, attrmgr: h5py.AttributeManager) -> A | None:
        if self._dataset.attr is None:
            return None
        da: Attribute[A] = self._dataset.attr

        loaded = da.flag_none
        attrs = attrmgr.get("0")
        if attrs is not None:
            for a_name in attrs:
                loaded |= da.get_attribute(a_name)

        return loaded

    @classmethod
    def create(cls, dataset: D, node: h5py.Group, name: str):
        video = cls()
        video._dataset = dataset
        video._node = node

        frames = node["frames"]
        if isinstance(frames, h5py.Dataset):
            video._frames = frames
        else:
            raise ValueError(f"{name} frames is not a dataset")

        gt = node["gt_bboxes"]  # FIXME:
        if isinstance(gt, h5py.Dataset):
            video._gt = gt
        else:
            raise ValueError(f"{name} gt is not a h5py dataset")

        if video._frames.shape[0] != video._gt.shape[0]:
            raise ValueError(f"{name} frames and gt have different lengths")

        video.name = name
        video.attrs = video.load_attributes(node.attrs)

        return video

    def _get_frame(self, idx: int) -> npt.NDArray[np.uint8]:
        # TODO: assume frames are jpeg compressed
        buf = np.frombuffer(self._frames[idx], dtype=np.uint8)
        return cv2.imdecode(buf, cv2.IMREAD_COLOR)

    def _get_gt(self, idx: int) -> npt.NDArray[np.float32]:
        return self._gt[idx]

    @property
    def init_gt(self) -> npt.NDArray[np.float32]:
        return self._get_gt(0)

    @property
    def width(self) -> int:
        return self._get_frame(0).shape[1]

    @property
    def height(self) -> int:
        return self._get_frame(0).shape[0]

    def __len__(self) -> int:
        return self._frames.shape[0]

    def __getitem__(self, idx: int) -> VideoItem:
        return self._get_frame(idx), self._get_gt(idx)

    def __iter__(self) -> Iterator[VideoItem]:
        for i in range(len(self)):
            yield self[i]
