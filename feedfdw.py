from . import ForeignDataWrapper
from datetime import datetime, timedelta
from logging import ERROR, WARNING
from multicorn.utils import log_to_postgres
import json
import feedparser


class FeedFdw(ForeignDataWrapper):
    def __init__(self, options, columns):
        super(FeedFdw, self).__init__(options, columns)
        self.url = options.get('url', None)
        if self.url is None:
            log_to_postgres("You musT set an url when creating the table.", ERROR)

    def execute(self, quals, columns):
        try:
            entries = []

            d = feedparser.parse(self.url)

            for e in d.entries:
                entry = []
                """
                prob should switch these to named entries?

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
                if e.content:
                    entry.append(e.content[0].value)
                else:
                    entry.append('')
#                if e.description:
#                    entry.append(e.description[0].value)
#                else:
#                    entry.append(e.description[0].value)
#
                entries.append(entry)
                
            return entries
        except IOError:
            log_to_postgres("Cannot retrieve '%s'" % self.url, WARNING)
