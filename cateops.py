from PIL import Image
from imageops import lay
import math


def categraph(n: float) -> Image:
    return lay(
        [Image.open('./res/cate.png')] * math.ceil(n),
        mode='RGBA', color=(0x00, 0x00, 0x00, 0x00)
    ).crop((0, 0, int(50 * n), 50))
