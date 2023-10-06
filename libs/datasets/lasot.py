from enum import Flag, auto

from ..attribute import Attribute as _Attr
from ..dataset import Dataset
from ..types import Path
from ..video import Video


class LaSOTAttr(Flag):
    NONE = 0
    CM = auto()
    """Camera Motion: abrupt motion of the camera"""
    VC = auto()
    """View Change: viewpoint affects target appearance significantly"""
    ROT = auto()
    """Rotation: the target object rotates in the image"""
    SV = auto()
    """Scale Variation: the ratio of target bounding box is outside the range `[0.5, 2]`"""
    DEF = auto()
    """Deformation: the target object is deformable during tracking"""
    BC = auto()
    """Background Clutter: the background near the target object has the similar appearance as the target"""
    POC = auto()
    """Partial Occlusion: the target object is partially occluded in the sequence"""
    FOC = auto()
    """Full Occlusion: the target object is fully occluded in the sequence"""
    MB = auto()
    """Motion Blur: the target region is blurred due to the motion of target object or camera"""
    IV = auto()
    """Illumination Variation: the illumination in the target region changes"""
    ARC = auto()
    """Aspect Ratio Change: the ratio of bounding box aspect ratio is outside the rage `[0.5, 2]`"""
    OV = auto()
    """Out-of-View: the target object completely leaves the video frame"""
    LR = auto()
    """Low Resolution: the area of target box is smaller than 1000 pixels in at least one frame"""
    FM = auto()
    """Fast Motion: the motion of target object is larger than the size of its bounding box"""


_ATTR_NAMES_MAP = {
    "Camera Motion": LaSOTAttr.CM,
    "View Change": LaSOTAttr.VC,
    "Rotation": LaSOTAttr.ROT,
    "Scale Variation": LaSOTAttr.SV,
    "Deformation": LaSOTAttr.DEF,
    "Background Clutter": LaSOTAttr.BC,
    "Partial Occlusion": LaSOTAttr.POC,
    "Full Occlusion": LaSOTAttr.FOC,
    "Motion Blur": LaSOTAttr.MB,
    "Illumination Variation": LaSOTAttr.IV,
    "Aspect Ratio Change": LaSOTAttr.ARC,
    "Out-of-View": LaSOTAttr.OV,
    "Low Resolution": LaSOTAttr.LR,
    "Fast Motion": LaSOTAttr.FM,
}


class LaSOTVideo(Video["LaSOTDataset", LaSOTAttr]):
    ...


class LaSOTDataset(Dataset["LaSOTVideo", LaSOTAttr]):
    def __init__(self, h5fp: Path) -> None:
        super().__init__(
            "LaSOT",
            h5fp,
            LaSOTVideo,
            _Attr(LaSOTAttr, LaSOTAttr.NONE, _ATTR_NAMES_MAP),
        )
