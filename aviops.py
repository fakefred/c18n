from mastodon import Mastodon, MastodonNetworkError
from PIL import Image
from urllib import request
from os import listdir
from config import *

masto = Mastodon(
    api_base_url=API_BASE_URL2,
    client_id=CLIENT_ID2,
    client_secret=CLIENT_SECRET2,
    access_token=ACCESS_TOKEN2
)


def open_in_size(fp: str, size: int) -> Image:
    return Image.open(fp).resize((size, size))


def combine_filenames(name_from: str, ext_from: str) -> str:
    # combine name_from's name and ext_from's extension
    return name_from + '.' + ext_from.split('.')[-1]


def get_avi(acct: str, size: int) -> Image:
    if acct.find('@') == -1:
        acct += '@yeet.social'
    elif acct.endswith('@mastodon.technology'):
        acct = acct.replace('@mastodon.technology', '')

    path = './res/avis/'

    for file in listdir(path):
        if '.'.join(file.split('.')[:-1]) == acct:
            return open_in_size(path + file, size)

    # fetch url, then download avi image
    try:
        searched = masto.account_search(acct)
        avi_url = ''
        for ac in searched:
            if ac['acct'] == acct:
                avi_url = ac['avatar']

        if not avi_url:
            # nah, can't find one
            return Image.open('./res/err.png')

        # save to ./res/avis/{acct}.{extension from avi url}
        filename = path + combine_filenames(acct, avi_url)

        try:
            request.urlretrieve(avi_url, filename)
            return open_in_size(filename, size)
        except request.URLError:
            return Image.open('./res/err.png')

    except MastodonNetworkError:
        return Image.open('./res/err.png')
