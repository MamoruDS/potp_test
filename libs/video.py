from enum import Flag
from typing import Iterator, TypeVar

import cv2
import h5py
import numpy as np
import numpy.typing as npt

from .types import Attribute, Video as _Video, VideoItem, D

A = TypeVar("A", bound=Flag)


class Video(_Video[D, A]):
    # gt_bboxes: list[npt.NDArray[np.float32]]
    name: str
    attrs: A | None

    _dataset: D
    _node: h5py.Group
    _frames: h5py.Dataset
    _gt_bboxes: h5py.Dataset

    def load_attributes(self, attrmgr: h5py.AttributeManager) -> A | None:
        if self._dataset.attr is None:
            return None
        da: Attribute[A] = self._dataset.attr

        loaded = self._dataset.attr.flag_none
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

        gt_bboxes = node["gt_bboxes"]
        if isinstance(gt_bboxes, h5py.Dataset):
            video._gt_bboxes = gt_bboxes
        else:
            raise ValueError(f"{name} gt_bboxes is not a dataset")

        if video._frames.shape[0] != video._gt_bboxes.shape[0]:
            raise ValueError(
                f"{name} frames and gt_bboxes have different lengths"
            )

        video.name = name
        video.attrs = video.load_attributes(node.attrs)

        return video

    def _get_frame(self, idx: int) -> npt.NDArray[np.uint8]:
        # TODO: assume frames are jpeg compressed
        buf = np.frombuffer(self._frames[idx], dtype=np.uint8)
        return cv2.imdecode(buf, cv2.IMREAD_COLOR)

    def _get_gt_bbox(self, idx: int) -> npt.NDArray[np.float32]:
        return self._gt_bboxes[idx]

    @property
    def init_bbox(self) -> npt.NDArray[np.float32]:
        return self._get_gt_bbox(0)

    @property
    def width(self) -> int:
        return self._get_frame(0).shape[1]

    @property
    def height(self) -> int:
        return self._get_frame(0).shape[0]

    def __len__(self) -> int:
        return self._frames.shape[0]

    def __getitem__(self, idx: int) -> VideoItem:
        return self._get_frame(idx), self._get_gt_bbox(idx)

    def __iter__(self) -> Iterator[VideoItem]:
        for i in range(len(self)):
            yield self[i]
