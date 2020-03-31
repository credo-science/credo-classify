from base64 import decodebytes
from io import BytesIO
from pathlib import Path
from typing import List, Any

from PIL import Image


def decode_base64(frame_content: str) -> bytes:
    return decodebytes(str.encode(frame_content))


def store_png(root: str, path: List[str], name: Any, frame_decoded: bytes) -> None:
    dirs = '/'.join(path)
    p = "%s/%s" % (root, dirs)
    fn = '%s/%s.png' % (p, str(name))
    Path(p).mkdir(parents=True, exist_ok=True)
    with open(fn, 'wb') as f:
        f.write(frame_decoded)
