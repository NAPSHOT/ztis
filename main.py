import feedparser
import sqlite3

conn = sqlite3.connect('ztis.db')
cur = conn.cursor()


class RSSSource:

    def __init__(self, name, url):
        self.name = name
        self.url = url

    def add_news_list(self, newsList):
        self.newsList = newsList;

    def __str__(self):
        return "RSSSource object:\n Source name is %s Source URL is %s" % (self.name, self.url)

if __name__ == '__main__':
    rssArray = []
    with open("rsslist", "r") as file:
        while True:
            name = file.readline()
            url = file.readline()
            if not url: break  # EOF
            rssArray.append(RSSSource(name, url))

    for a in rssArray:
        newsFeed = feedparser.parse(a.url)
        a.add_news_list(newsFeed)
        for item in newsFeed.entries:
            try:
                title2 = item['title']
            except KeyError:
                title2 = 'default'
            try:
                publication_date2 = item['published']
            except KeyError:
                publication_date2 = 'default'
            try:
                author2 = item['author']
            except KeyError:
                author2 = 'default'
            try:
                summary2 = item['summary']
            except KeyError:
                summary2 = 'default'


            cur.execute("INSERT INTO ztis VALUES (?, ?, ?, ?)", (title2, summary2, publication_date2, author2))
            conn.commit()
