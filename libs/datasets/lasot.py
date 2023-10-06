from ..dataset import Dataset
from ..types import Path
from ..video import Video


class LaSOTVideo(Video["LaSOTDataset"]):
    ...


class LaSOTDataset(Dataset["LaSOTVideo"]):
    def __init__(self, h5fp: Path) -> None:
        super().__init__("LaSOT", h5fp, LaSOTVideo)
