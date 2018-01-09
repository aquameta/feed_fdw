# feed_fdw

RSS and Atom Foreign Data Wrapper for PostgreSQL, via [Multicorn](http://multicorn.org/).

Uses the [feedparser](https://pypi.python.org/pypi/feedparser) library, which supports many different [feed formats](https://pythonhosted.org/feedparser/introduction.html).


## Installation

1. Install [multicorn](http://multicorn.org/)

2. Install feedparser:
```sh
sudo pip install feedparser
```
3. Copy feedfdw.py to the multicorn plugin directory:
```sh
cp ./feedfdw.py /usr/local/lib/python2.7/dist-packages/multicorn-1.3.4-py2.7-linux-x86_64.egg/multicorn
```

## Usage
```sql
create server feed_srv foreign data wrapper multicorn options (
    wrapper 'multicorn.feedfdw.FeedFdw'
);

create foreign table example_feed (
    id text,
    link text,
    title text,
    published text,
    updated text,
    summary text,
    content text
) server feed_srv options (
    url 'http://example.org/rss/'
);
```
