from base64 import decodebytes
from pathlib import Path
from typing import List

from PIL import Image


def decode_base64(frame_content: str) -> bytes:
    """
    Convert bytes encoded in base64 to array of bytes.
    :param frame_content: bytes encoded in base64
    :return: byte array
    """
    return decodebytes(str.encode(frame_content))


def store_png(root: str, path: List[str or int], name: str or int, image: bytes or Image) -> None:
    """
    Save image in PNG file.
    :param root: root directory for PNG files storage
    :param path: subdirectories, will be created when not exists
    :param name: file name without extensions
    :param image: instance of PIL.Image or array of bytes
    """
    dirs = '/'.join(map(lambda x: str(x), path))
    p = "%s/%s" % (root, dirs)
    fn = '%s/%s.png' % (p, str(name))
    Path(p).mkdir(parents=True, exist_ok=True)
    if isinstance(image, bytes):
        with open(fn, 'wb') as f:
            f.write(image)
    else:
        image.save(fn)
