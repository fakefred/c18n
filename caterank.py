from PIL import Image, ImageDraw
from html import unescape
from htmlops import TootParser
from imageops import stack
from textops import hackertext
from cateops import categraph
from re import match

COLORS = ((0x28, 0x2c, 0x37, 0xff), (0x38, 0x3c, 0x47, 0xff))


def uncurse(toot: str):  # currently unused
    # toots come in a cursed format (HTML)
    # tags like <p>, <a href=""> and <br /> may appear
    parser = TootParser()
    parser.feed(toot)
    blessed = parser.content

    # also parse HTML encoding
    return unescape(blessed)


def caterank(content: str) -> Image:
    '''
    CateCounter toot template:
    0 | @fakefred The top 10 most cursed people are: 
    --|----------------------------------------------
    1 | 1. bclindner@mastodon.technology - 3.4 cates 
    2 | 2. Dee@fedi.underscore.world - 3.0 cates 
    3 | 3. AstroBadger@splat.soy - 2.0 cates 
    4 | 4. CateCounter - 2.0 cates 
    5 | 5. mdszy@mastodon.technology - 1.7 cates 
    6 | 6. trickster@mastodon.technology - 1.5 cates 
    7 | 7. dublinux@mastodon.technology - 1.0 cates

    ['7.', 'dublinux@mastodon.technology', '-', '1.0', 'cates']
     0      1                               2    3      4
    '''
    lines = uncurse(content).splitlines()[1:]
    rank = []
    for l in lines:
        if match(
            '^\d\. \w+(@(\w+\.)+\w+)? - \d+\.\d+ cates$', l.strip()
        ) is not None:
            segs = l.split()
            rank.append((
                segs[1],  # acct
                float(segs[3])  # cateness
            ))

    if rank:
        rows = []
        for idx, entry in enumerate(rank):
            row = Image.new('RGBA', (600, 60), color=COLORS[idx % 2])
            handle = hackertext(entry[0].split('@')[0])
            row.paste(handle, box=(10, 18), mask=handle)
            cates = categraph(entry[1])
            row.paste(cates, box=(250, 5), mask=cates)
            rows.append(row)

        output = stack(rows)
        output.save('./caterank.png')
        return output

    return None


if __name__ == '__main__':
    caterank('''@fakefred The top 10 most cursed people are: 
1. bclindner@mastodon.technology - 3.4 cates 
2. Dee@fedi.underscore.world - 3.0 cates 
3. AstroBadger@splat.soy - 2.0 cates 
4. CateCounter - 2.0 cates 
5. mdszy@mastodon.technology - 1.7 cates 
6. trickster@mastodon.technology - 1.5 cates 
7. dublinux@mastodon.technology - 1.0 cates''').show()
