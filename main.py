import feedparser

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
#    for rss in rssArray:
#        rss.add_news_list(feedparser.parse(rss.url)
#    for rss in rssArray:
#        print(rss)
#        print(rss.newsList.size)
#
#    print(entry.title)
    for a in rssArray:
        print(a)
        print(a.newsList)
        print("--------------------------------------------")