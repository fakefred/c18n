from PIL import Image
from imageops import lay


def hackertext(text: str) -> Image:
    chars = []
    for char in text:
        if char.lower() in 'qwertyuiopasdfghjklzxcvbnm0123456789':
            key = char.lower()
        elif char == '.':
            key = 'dot'
        elif char == ',':
            key = 'comma'
        elif char == '-':
            key = 'dash'
        elif char == '_':
            key = 'underscore'
        else:
            key = ''

        if key:  # character valid
            chars.append(Image.open(f'./res/characters/hacker_{key}.png'))

    return lay(chars, mode='RGBA', color=(0x00, 0x00, 0x00, 0x00), bias=-5)
