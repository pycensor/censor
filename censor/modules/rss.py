# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,W0105,E0402,C0411


"rich site syndicte"


import html.parser
import re
import threading
import time
import urllib
import _thread


from urllib.error import HTTPError, URLError
from urllib.parse import quote_plus, urlencode
from urllib.request import Request, urlopen


from ..brokers import objs
from ..message import reply
from ..objects import Object, fmt, update
from ..storage import find, last, sync
from ..threads import Repeater, launch
from ..utility import fntime, laps


def __dir__():
    return (
            "Fetcher",
            "Parser",
            "Rss",
            "Seen",
            "dpl",
            "nme",
            "rem",
            "rss"
           )


DEBUG = False


def init():
    fetcher = Fetcher()
    fetcher.start()
    return fetcher


fetchlock = _thread.allocate_lock()


class Feed(Object):

    def len(self):
        return len(self.__dict__)

    def size(self):
        return len(self.__dict__)


class Rss(Object):

    def __init__(self):
        super().__init__()
        self.display_list = 'title,link,author'
        self.name = ''
        self.rss = ''

    def len(self):
        return len(self.__dict__)

    def size(self):
        return len(self.__dict__)


class Seen(Object):

    def __init__(self):
        super().__init__()
        self.urls = []

    def len(self):
        return len(self.__dict__)

    def size(self):
        return len(self.__dict__)


class Fetcher(Object):

    dosave = False
    seen = Seen()

    def __init__(self):
        super().__init__()
        self.connected = threading.Event()

    @staticmethod
    def display(obj):
        result = ''
        displaylist = []
        try:
            displaylist = obj.display_list or 'title,link'
        except AttributeError:
            displaylist = 'title,link,author'
        for key in displaylist.split(","):
            if not key:
                continue
            data = getattr(obj, key, None)
            if not data:
                continue
            data = data.replace('\n', ' ')
            data = striphtml(data.rstrip())
            data = unescape(data)
            result += data.rstrip()
            result += ' - '
        return result[:-2].rstrip()

    def fetch(self, feed):
        with fetchlock:
            counter = 0
            res = []
            for obj in reversed(list(getfeed(feed.rss, feed.display_list))):
                fed = Feed()
                update(fed, obj)
                update(fed, feed)
                if 'link' in fed:
                    url = urllib.parse.urlparse(fed.link)
                    if url.path and not url.path == '/':
                        uurl = f'{url.scheme}://{url.netloc}/{url.path}'
                    else:
                        uurl = fed.link
                    if uurl in Fetcher.seen.urls:
                        continue
                    Fetcher.seen.urls.append(uurl)
                counter += 1
                if self.dosave:
                    sync(fed)
                res.append(fed)
        if res:
            sync(Fetcher.seen)
        txt = ''
        feedname = getattr(feed, 'name', None)
        if feedname:
            txt = f'[{feedname}] '
        for obj in res:
            txt2 = txt + self.display(obj)
            for bot in objs:
                bot.announce(txt2.rstrip())
        return counter

    def run(self):
        thrs = []
        for feed in find('rss'):
            thrs.append(launch(self.fetch, feed, name=f"{feed.rss}"))
        return thrs

    def start(self, repeat=True):
        last(Fetcher.seen)
        if repeat:
            repeater = Repeater(300.0, self.run)
            repeater.start()


class Parser(Object):

    @staticmethod
    def getitem(line, item):
        lne = ''
        try:
            index1 = line.index(f'<{item}>') + len(item) + 2
            index2 = line.index(f'</{item}>')
            lne = line[index1:index2]
            if 'CDATA' in lne:
                lne = lne.replace('![CDATA[', '')
                lne = lne.replace(']]', '')
                lne = lne[1:-1]
        except ValueError:
            lne = None
        return lne

    @staticmethod
    def parse(txt, item='title,link'):
        res = []
        for line in txt.split('<item>'):
            line = line.strip()
            obj = Object()
            for itm in item.split(","):
                setattr(obj, itm, Parser.getitem(line, itm))
            res.append(obj)
        return res


def getfeed(url, item):
    if DEBUG:
        return [Object(), Object()]
    try:
        result = geturl(url)
    except (ValueError, HTTPError, URLError):
        return [Object(), Object()]
    if not result:
        return [Object(), Object()]
    return Parser.parse(str(result.data, 'utf-8'), item)


def gettinyurl(url):
    postarray = [
        ('submit', 'submit'),
        ('url', url),
    ]
    postdata = urlencode(postarray, quote_via=quote_plus)
    req = Request('http://tinyurl.com/create.php',
                  data=bytes(postdata, 'UTF-8'))
    req.add_header('User-agent', useragent(url))
    with urlopen(req) as htm:
        for txt in htm.readlines():
            line = txt.decode('UTF-8').strip()
            i = re.search('data-clipboard-text="(.*?)"', line, re.M)
            if i:
                return i.groups()
    return []


def geturl(url):
    url = urllib.parse.urlunparse(urllib.parse.urlparse(url))
    req = urllib.request.Request(url)
    req.add_header('User-agent', useragent("rss fetcher"))
    with urllib.request.urlopen(req) as response:
        response.data = response.read()
        return response


def striphtml(text):
    clean = re.compile('<.*?>')
    return re.sub(clean, '', text)


def unescape(text):
    txt = re.sub(r'\s+', ' ', text)
    return html.unescape(txt)


def useragent(txt):
    return 'Mozilla/5.0 (X11; Linux x86_64) ' + txt


"commands"


def dpl(event):
    if len(event.args) < 2:
        reply(event, 'dpl <stringinurl> <item1,item2>')
        return
    setter = {'display_list': event.args[1]}
    for feed in find('rss', {'rss': event.args[0]}):
        if feed:
            update(feed, setter)
            sync(feed)
    reply(event, 'ok')


def nme(event):
    if len(event.args) != 2:
        reply(event, 'name <stringinurl> <name>')
        return
    selector = {'rss': event.args[0]}
    for feed in find('rss', selector):
        if feed:
            feed.name = event.args[1]
            sync(feed)
    reply(event, 'ok')


def rem(event):
    if len(event.args) != 1:
        reply(event, 'rem <stringinurl>')
        return
    selector = {'rss': event.args[0]}
    for feed in find('rss', selector):
        if feed:
            feed.__deleted__ = True
            sync(feed)
    reply(event, 'ok')


def rss(event):
    if not event.rest:
        nrs = 0
        for feed in find('rss'):
            nrs += 1
            elp = laps(time.time()-fntime(feed.__fnm__))
            txt = fmt(feed)
            reply(event, f'{nrs} {txt} {elp}')
        if not nrs:
            reply(event, 'no rss feed found.')
        return
    url = event.args[0]
    if 'http' not in url:
        reply(event, 'i need an url')
        return
    for res in find('rss', {'rss': url}):
        if res:
            reply(event, f'already got {url}')
            return
    feed = Rss()
    feed.rss = event.args[0]
    sync(feed)
    reply(event, 'ok')
