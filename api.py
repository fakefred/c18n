from mastodon import Mastodon, StreamListener
from caterank import caterank
from config import *
from os import remove
from datetime import datetime, timezone

masto = Mastodon(
    api_base_url=API_BASE_URL,
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    access_token=ACCESS_TOKEN
)


def time_string() -> str:
    # 2020-01-29 12:30:34|.957996+00:00
    # <--   splice    -->| HACK
    return str(datetime.now(timezone.utc))[:19]


def determine_visibility(vis: str) -> str:
    # only direct if incoming status is direct; else unlisted
    return 'direct' if vis == 'direct' else 'unlisted'


def handle_toot(status: dict, irtid: int, irtacct: str, vis: str):
    sid = status['id']
    path = str(sid) + '.jpg'
    # @handle[@domain]; uniqueness guaranteed
    acct = status['account']['acct']
    # only accept stati from @CateCounter@yeet.social
    if not acct == 'CateCounter@yeet.social':
        # return
        pass

    # BEGIN ATROCITIES
    # caterank: save to './caterank.jpg' if status is cate count
    if caterank(status['content']) is not None:
        media_id = masto.media_post(
            './caterank.png', mime_type='image/png')['id']
        # publish toot
        masto.status_post(
            f'@{irtacct} :cate: The top 10 most cursed people are:',
            in_reply_to_id=irtid,
            visibility=vis,
            media_ids=media_id
        )
        # log to console
        print(f'{time_string()}: Generated categraph for status id {sid} by {acct}')


class Listener(StreamListener):
    def on_notification(self, ntf):
        # All your notifications are belong to us!
        if ntf['type'] == 'mention':
            irtid = ntf['status']['in_reply_to_id']
            if irtid is not None:
                handle_toot(masto.status(irtid), ntf['status']['id'],
                            ntf['status']['account']['acct'],
                            determine_visibility(ntf['status']['visibility']))


def start_streaming():
    listener = Listener()
    masto.stream_user(listener)


if __name__ == '__main__':
    start_streaming()
