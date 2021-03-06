"""Recommend url handle class."""
from sqlalchemy import MetaData
from sqlalchemy import Table, Column, join
from sqlalchemy.sql import select
from sqlalchemy.sql.functions import count

class Recommend(object):

    def __init__(self, engine):
        self.engine = engine
        self.md = MetaData(self.engine)

    def select(self):
        rank_urls = []
        for rec in self._load_top():
            rank_urls.append((rec["title"], rec["url"], rec["id"]))
        return rank_urls

    def _load_top(self, num=5):
        """Load top recommend url"""
        self.md.clear()
        my_bookmark = Table('my_bookmark', self.md, Column('url_id'))
        bookmark = Table('bookmark', self.md, Column('url_id'))
        feed = Table('feed', self.md, Column('id'), Column('title'), Column('url'))
        notification = Table('notification', self.md, Column('url_id'))

        j1 = join(bookmark, feed, bookmark.c.url_id == feed.c.id)
        j2 = j1.join(my_bookmark, bookmark.c.url_id == my_bookmark.c.url_id, isouter=True)
        j3 = j2.join(notification, notification.c.url_id == bookmark.c.url_id, isouter=True)

        s = select(columns=[feed.c.id, feed.c.url, feed.c.title]).\
                select_from(j3).where(my_bookmark.c.url_id == None).\
                where(notification.c.url_id == None).\
                group_by(bookmark.c.url_id).\
                having(count(bookmark.c.url_id)).\
                order_by(count(bookmark.c.url_id).desc()).\
                limit(num)
        #print(s) ### For debug
        return s.execute()
