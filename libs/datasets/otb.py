from enum import Flag, auto

from ..attribute import Attribute as _Attr
from ..dataset import Dataset
from ..types import Path
from ..video import Video


class Attribute(Flag):
    IV = auto()
    """Illumination Variation: the illumination in the target region is significantly changed"""
    SV = auto()
    """Scale Variation: the ratio of the bounding boxes of the first frame and the current frame is out of the range $[1/t_s, t_s],t_s>1(t_s=2)$"""
    OCC = auto()
    """Occlusion: the target is partially or fully occluded"""
    DEF = auto()
    """Deformation: non-rigid object deformation"""
    MB = auto()
    """Motion Blur: the target region is blurred due to the motion of target or camera"""
    FM = auto()
    """Fast Motion: the motion of the ground truth is larger than $t_m$ pixles ($t_m=20$)"""
    IPR = auto()
    """In-Plane Rotation: the target rotates in the image plane"""
    OPR = auto()
    """Out-of-Plane Rotation: the target rotates out of the image plane"""
    OV = auto()
    """Out-of-View: some portion of the target leaves the view"""
    BC = auto()
    """Background Clutters: the background near the target has the similar color or texture as the target"""
    LR = auto()
    """Low Resolution: the number of pixels inside the ground-truth bounding box is less than $t_r$ ($t_r=400$)"""


_ATTR_NAMES_MAP = {
    "Illumination Variation": Attribute.IV,
    "Scale Variation": Attribute.SV,
    "Occlusion": Attribute.OCC,
    "Deformation": Attribute.DEF,
    "Motion Blur": Attribute.MB,
    "Fast Motion": Attribute.FM,
    "In-Plane Rotation": Attribute.IPR,
    "Out-of-Plane Rotation": Attribute.OPR,
    "Out-of-View": Attribute.OV,
    "Background Clutters": Attribute.BC,
    "Low Resolution": Attribute.LR,
}


class OTB100Video(Video["OTB100Dataset", Attribute]):
    ...


class OTB100Dataset(Dataset["OTB100Video", Attribute]):
    def __init__(self, h5fp: Path) -> None:
        super().__init__(
            "OTB100", h5fp, OTB100Video, _Attr(Attribute, _ATTR_NAMES_MAP)
        )
