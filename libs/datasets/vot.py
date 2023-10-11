from enum import Flag, auto

import h5py
import numpy as np
import numpy.typing as npt

from ..attribute import Attribute as _Attr
from ..dataset import Dataset
from ..types import Path
from ..video import Video


class FrameAttrs:
    camera_motion: npt.NDArray[np.bool_]
    illum_change: npt.NDArray[np.bool_]
    motion_change: npt.NDArray[np.bool_]
    occlusion: npt.NDArray[np.bool_]
    size_change: npt.NDArray[np.bool_]


class VOTAttr(Flag):
    NONE = 0
    CAMERA_MOTION = auto()
    ILLUM_CHANGE = auto()
    MOTION_CHANGE = auto()
    OCCLUSION = auto()
    SIZE_CHANGE = auto()


_ATTR_NAMES_MAP = {
    # "Camera Motion": Attribute.CAMERA_MOTION,
    # "Illumination Change": Attribute.ILLUM_CHANGE,
    # "Motion Change": Attribute.MOTION_CHANGE,
    # "Occlusion": Attribute.OCCLUSION,
    # "Size Change": Attribute.SIZE_CHANGE,
}


class VotVideo(Video["VotDataset", VOTAttr]):
    """Legacy VOT ST Video"""

    def get_tagged(self, tag: VOTAttr) -> npt.NDArray[np.uint8]:
        attrmgr: h5py.AttributeManager = self._node.attrs
        tags = None
        if tag == VOTAttr.CAMERA_MOTION:
            tags = attrmgr.get("camera_motion")
        elif tag == VOTAttr.ILLUM_CHANGE:
            tags = attrmgr.get("illum_change")
        elif tag == VOTAttr.MOTION_CHANGE:
            tags = attrmgr.get("motion_change")
        elif tag == VOTAttr.OCCLUSION:
            tags = attrmgr.get("occlusion")
        elif tag == VOTAttr.SIZE_CHANGE:
            tags = attrmgr.get("size_change")
        else:
            raise KeyError

        if tags is None:
            raise ValueError
        return tags

    def load_attributes(self, attrmgr: h5py.AttributeManager) -> VOTAttr:
        # TODO:
        attrs = VOTAttr.NONE

        camera_motion = attrmgr.get("camera_motion")
        if camera_motion is not None:
            if np.any(camera_motion):
                attrs |= VOTAttr.CAMERA_MOTION
        illum_change = attrmgr.get("illum_change")
        if illum_change is not None:
            if np.any(illum_change):
                attrs |= VOTAttr.ILLUM_CHANGE
        motion_change = attrmgr.get("motion_change")
        if motion_change is not None:
            if np.any(motion_change):
                attrs |= VOTAttr.MOTION_CHANGE
        occlusion = attrmgr.get("occlusion")
        if occlusion is not None:
            if np.any(occlusion):
                attrs |= VOTAttr.OCCLUSION
        size_change = attrmgr.get("size_change")
        if size_change is not None:
            if np.any(size_change):
                attrs |= VOTAttr.SIZE_CHANGE

        loaded = super().load_attributes(attrmgr)
        if loaded is not None:
            attrs |= loaded
        return attrs


class VotDataset(Dataset["VotVideo", VOTAttr]):
    def __init__(self, h5fp: Path) -> None:
        super().__init__(
            "VOT2019",
            h5fp,
            VotVideo,
            _Attr(VOTAttr, VOTAttr.NONE, _ATTR_NAMES_MAP),
        )
