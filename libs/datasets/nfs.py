from ..dataset import Dataset
from ..video import Video
from ..types import Path
from typing import TypeVar

ND = TypeVar("ND", bound="_NFSDataset")


class _NFSVideo(Video[ND]):
    ...


class NFS30Video(_NFSVideo["NFS30Dataset"]):
    ...


class NFS240Video(_NFSVideo["NFS240Dataset"]):
    ...


class _NFSDataset(Dataset[_NFSVideo]):
    def __init__(self, name: str, h5fp: Path) -> None:
        super().__init__(name, h5fp, _NFSVideo)


class NFS30Dataset(Dataset[NFS30Video]):
    def __init__(self, h5fp: Path) -> None:
        super().__init__("NFS30", h5fp, NFS30Dataset)


class NFS240Dataset(Dataset[NFS240Video]):
    def __init__(self, h5fp: Path) -> None:
        super().__init__("NFS240", h5fp, NFS240Dataset)
