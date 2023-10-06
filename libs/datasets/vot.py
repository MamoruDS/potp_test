from typing import TypedDict

from ..dataset import Dataset
from ..types import Path
from ..video import Video


class VOTVideoAttrs(TypedDict):
    all: list[bool]
    camera_motion: list[bool]
    illumination_change: list[bool]
    motion_change: list[bool]
    size_change: list[bool]
    occlusion: list[bool]


class VotVideo(Video["VotDataset"]):
    """Legacy VOT ST Video"""

    ...


class VotDataset(Dataset[VotVideo]):
    def __init__(self, h5fp: Path) -> None:
        super().__init__("VOT2019", h5fp, VotVideo)
