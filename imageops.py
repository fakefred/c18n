from PIL import Image

WHITE = (255, 255, 255, 255)


def stack(images: list, mode='RGBA', color=WHITE):
    w = max([im.size[0] for im in images])  # width of widest image
    h = sum([im.size[1] for im in images])  # sum of images' height

    stacked = Image.new(mode, (w, h), color=color)

    y = 0
    for im in images:
        stacked.paste(im, box=(0, y))  # no transparency
        y += im.size[1]

    return stacked


def lay(images: list, mode='RGBA', color=WHITE, bias=0):
    w = sum([im.size[0] for im in images])
    h = max([im.size[1] for im in images])

    laid = Image.new(mode, (w, h), color=color)

    x = 0
    for im in images:
        laid.paste(im, box=(x, 0), mask=im if 'A' in mode else None)
        x += im.size[0] + bias

    return laid
