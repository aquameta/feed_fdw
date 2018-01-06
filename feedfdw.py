"""
    CREATE SERVER feed_srv foreign data wrapper multicorn options (
        wrapper 'multicorn.feedfdw.FeedFdw'
    );

    CREATE FOREIGN TABLE example_rss (
        "pubDate" timestamp,
        description character varying,
        title character varying,
        link character varying
    ) server feed_srv options (
        url     'http://example.org/rss/'
    );
"""

from . import ForeignDataWrapper
from datetime import datetime, timedelta
from logging import ERROR, WARNING
from multicorn.utils import log_to_postgres
import json
import feedparser




class FeedFdw(ForeignDataWrapper):
    """An rss foreign data wrapper.

    The following options are accepted:

    url --  The rss feed urls.

    The columns named are parsed, and are used as xpath expression on
    each item xml node. Exemple: a column named "pubDate" would return the
    pubDate element of an rss item.

    """

    def __init__(self, options, columns):
        super(FeedFdw, self).__init__(options, columns)
        self.url = options.get('url', None)
        if self.url is None:
            log_to_postgres("You MUST set an url when creating the table!",
                            ERROR)

    def execute(self, quals, columns):
        """Quals are ignored."""
        try:
            entries = []

            d = feedparser.parse(self.url)

            for e in d.entries:
                entry = []
                """
                entry.append(["id",          e.id])
                entry.append(["link",        e.link])
                entry.append(["title",       e.title])
                entry.append(["published",   e.published])
                entry.append(["updated",     e.updated])
                entry.append(["summary",     e.summary])
                entry.append(["content",     e.content])
                """

                entry.append(e.id)
                entry.append(e.link)
                entry.append(e.title)
                entry.append(e.published)
                entry.append(e.updated)
                entry.append(e.summary)
                entry.append(e.content[0].value)

                entries.append(entry)
                
            return entries
        except IOError:
            log_to_postgres("Cannot retrieve '%s'" % self.url, WARNING)
