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
        recs = self._load_top()
        for rec in recs:
            if self._is_mybookmark(rec["url"]):
                print(rec['url'])
                continue
            rank_urls.append(rec["url"])
        return rank_urls

    def _load_top(self, num=100):
        """Load top recommend url"""
        self.md.clear()
        my_bookmark = Table('my_bookmark', self.md, Column('url_id'))
        bookmark = Table('bookmark', self.md, Column('url_id'))
        feed = Table('feed', self.md, Column('id'))
        j1 = join(bookmark, feed, bookmark.c.url_id == feed.c.id)
        j2 = j1.join(my_bookmark, bookmark.c.url_id == my_bookmark.c.url_id, isouter=True)
        s = select(columns=['*']).select_from(j2).where(
                my_bookmark.c.url_id == None).group_by(
                        bookmark.c.url_id).having(count(bookmark.c.url_id))
        print(s)
        return s.execute()

    def _is_mybookmark(self, url):
        """Check the url is already registered as my bookmark."""
        self.md.clear()
        t = Table('my_bookmarks', self.md)
        w = "url = '{}'".format(url)
        s = select(columns=['url'], from_obj=t).where(w)
        return s.execute().scalar()

"""Sample SQL
select count(b.url_id), b.url_id, f.title, f.url
from bookmark b
inner join feed f
on f.id = b.url_id
left join my_bookmark m
on b.url_id = m.url_id
where m.url_id is null
group by b.url_id
having count(b.url_id) > 1
order by count(b.url_id) desc limit 10;
"""
