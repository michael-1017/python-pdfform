# -*- coding: utf-8 -*-

from io import BytesIO
from typing import Tuple, Union

from PIL import Image


def rotate_image(image_stream: bytes, rotation: Union[float, int]) -> bytes:
    buff = BytesIO()
    buff.write(image_stream)
    buff.seek(0)

    image = Image.open(buff)

    rotated_buff = BytesIO()
    image.rotate(rotation, expand=True).save(rotated_buff, format=image.format)
    rotated_buff.seek(0)

    result = rotated_buff.read()

    buff.close()
    rotated_buff.close()

    return result


def get_image_dimensions(image_stream: bytes) -> Tuple[float, float]:
    buff = BytesIO()
    buff.write(image_stream)
    buff.seek(0)

    image = Image.open(buff)

    return image.size
