from time import time
from typing import Optional, List, Any

from hit_analysis.io.io_utils import store_png
from hit_analysis.commons.utils import print_log


class Config:
    def __init__(self, out_dir: str = None, log: bool = True) -> None:
        self.out_dir = out_dir
        self.log = log

    def print_log(self, s: str, t: Optional[float] = None):
        if self.log:
            return print_log(s, t)
        return time()

    def store_png(self, path: List[str], name: Any, frame_decoded: bytes) -> None:
        if self.out_dir:
            store_png(self.out_dir, path, name, frame_decoded)
