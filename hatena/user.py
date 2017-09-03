"""Bookmark user class"""

import urllib
import time
from datetime import date
from sqlalchemy import MetaData
from sqlalchemy import Table
from sqlalchemy.sql import select,update,insert
import requests

HATENA_ENTRY_URL = "http://b.hatena.ne.jp/entry/jsonlite/?url={url}"
ACCESS_INTERVAL = 0.5

class User:

    def __init__(self, engine, urls):
        # call twice, so in vain
        self.engine = engine 
        self.urls = urls
        self.interval = ACCESS_INTERVAL
        self.md = MetaData(self.engine)

    def extract(self):
        print "BookmarkUser extract"
        users = []
        for feedurl in self.urls:
            print "target url: %s" % (feedurl)
            url = self._make_entry_api_url(feedurl)
            f = self._request(url)
            # Don't examine patterns not "bookamark" keys
            print(f)
            if "bookmarks" not in f:
                continue
            for bookmark in f["bookmarks"]:
                #users.append([url[0], bookmark["user"]])
                if "user" not in bookmark:
                    continue
                users.append(bookmark["user"])
            #time.sleep(self.interval)
            time.sleep(1)
            ### TEST
            break
        return users

    def _make_entry_api_url(self, url):
        """Create hatena bookmark entry api url."""
        e_url = urllib.quote(url, safe='')
        return HATENA_ENTRY_URL.format(url=e_url)

    def _request(self, url):
        """Request api.
        
        Request argument url and return result data as dict.
        """
        return requests.get(url).json()

    def save(self, users):
        for user in users:
            is_register = self._is_register(user)
            print('{} -- {}'.format(user, str(is_register)))
            if is_register:
                self._update_recommend_time(user)
                continue
            self._append_user(user)

    def _is_register(self, user):
        """Check the user is already registered or not."""
        t = Table('users', self.md)
        w = "user_name = '{}'".format(user)
        s = select(columns=['user_name'], from_obj=t).where(w)
        return s.execute().scalar()

    def _update_recommend_time(self, user):
        """Update recommended user count."""
        self.md.clear()
        t = Table('users', self.md, autoload=True)
        w = "user_name = '{}'".format(user)
        u = update(t).where(w).values(recomend_times=t.c.recomend_times+1)
        u.execute()

    def _append_user(self, user):
        """Add new recommend user."""
        self.md.clear()
        t = Table('users', self.md, autoload=True)
        i = insert(t).values(user_name=user,
                             register_datetime=date.today())
        i.execute()

    def load_user_no(self, user):
        """Load user_no."""
        self.md.clear()
        t = Table('users', self.md, auto_load=True)
        w = "user_name = '{}'".format(user)
        s = select(columns=['user_no'], from_obj=t).where(w)
        return s.execute().fetchone()['user_no']
