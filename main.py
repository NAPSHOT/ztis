import feedparser

if __name__ == '__main__':
    with open("rsslist", "r") as ins:
        rssArray = []
        for line in ins:
            rssArray.append(line)

    NewsFeed = feedparser.parse(rssArray[0])
    entry = NewsFeed.entries[1]

    print(entry.title)

