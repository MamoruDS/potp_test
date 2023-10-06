from enum import Flag, auto

from ..attribute import Attribute as _Attr
from ..dataset import Dataset
from ..video import Video
from ..types import NoAttribute, Path


class UAVAttr(Flag):
    NONE = 0
    ARC = auto()
    """Aspect Ratio Change: the fraction of ground truth aspect ratio in the first frame and at least one subsequent frame is outside the range `[0.5, 2]`"""
    BC = auto()
    """Background Clutter: the background near the target has similar appearance as the target"""
    CM = auto()
    """Camera Motion: abrupt motion of the camera"""
    FM = auto()
    """Fast Motion: motion of the ground truth bounding box is larger than 20 pixels between two consecutive frames"""
    FOC = auto()
    """Full Occlusion: the target is fully occluded"""
    IV = auto()
    """Illumination Variation: the illumination of the target changes significantly"""
    LR = auto()
    """Low Resolution: at least one ground truth bounding box has less than 400 pixels"""
    OV = auto()
    """Out-of-View: some portion of the target leaves the view"""
    POC = auto()
    """Partial Occlusion: the target is partially occluded"""
    SOB = auto()
    """Similar Object: there are objects of similar shape or same type near the target"""
    SV = auto()
    """Scale Variation: the ratio of initial and at least one subsequent bounding box is outside the range `[0.5, 2]`"""
    VC = auto()
    """Viewpoint Change: viewpoint affects target appearance significantly"""


_ATTR_NAMES_MAP = {
    "Aspect Ratio Change": UAVAttr.ARC,
    "Background Clutter": UAVAttr.BC,
    "Camera Motion": UAVAttr.CM,
    "Fast Motion": UAVAttr.FM,
    "Full Occlusion": UAVAttr.FOC,
    "Illumination Variation": UAVAttr.IV,
    "Low Resolution": UAVAttr.LR,
    "Out-of-View": UAVAttr.OV,
    "Partial Occlusion": UAVAttr.POC,
    "Similar Object": UAVAttr.SOB,
    "Scale Variation": UAVAttr.SV,
    "Viewpoint Change": UAVAttr.VC,
}


class UAVVideo(Video["UAVDataset", UAVAttr]):
    ...


class UAVDataset(Dataset["UAVVideo", UAVAttr]):
    def __init__(self, h5fp: Path) -> None:
        super().__init__(
            "UAV123",
            h5fp,
            UAVVideo,
            _Attr(UAVAttr, UAVAttr.NONE, _ATTR_NAMES_MAP),
        )
