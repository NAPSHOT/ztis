import feedparser
import sqlite3
rssArray = []

def create_table(cur):
    print("Creating new ztis table")
    try:
        cur.execute("""CREATE TABLE ztis
                 (source, title, summary, publication_date, author)""")
    except:
        pass

def drop_table(cur):
    print("Dropping ztis table with all data")
    try:
        cur.execute("DROP TABLE ztis")
    except:
        pass

def read_rsslist():
    with open("rsslist", "r") as file:
        while True:
            name = file.readline()
            url = file.readline()
            if not url: break  # EOF
            rssArray.append(RSSSource(name, url))
    print("Read %d sources" % (len(rssArray)))

def download_data():
    for a in rssArray:
        print("Downloading feed from " + a.name)
        newsFeed = feedparser.parse(a.url)
        a.add_news_list(newsFeed)

def save_data(conn, cur):
    print("Saving data to ztis table...")
    counter = 0
    for a in rssArray:
        for item in a.newsList.entries:
            source = a.name
            try:
                title = item['title']
            except KeyError:
                title = 'default'
            try:
                publication_date = item['published']
            except KeyError:
                publication_date = 'default'
            try:
                author = item['author']
            except KeyError:
                author = 'default'
            try:
                summary = item['summary']
            except KeyError:
                summary = 'default'
            cur.execute("INSERT INTO ztis VALUES (?, ?, ?, ?, ?)", (source, title, summary, publication_date, author))
            counter += 1
            conn.commit()
    print("Correctly save %d feeds" % (counter))

class RSSSource:
    def __init__(self, name, url):
        self.name = name
        self.url = url

    def add_news_list(self, newsList):
        self.newsList = newsList

    def __str__(self):
        return "RSSSource object:\n Source name is %s Source URL is %s" % (self.name, self.url)

if __name__ == '__main__':
    conn = sqlite3.connect('ztis.db')
    cur = conn.cursor()
    read_rsslist()
    download_data()
#    drop_table(cur)
#    create_table(cur)
    save_data(conn, cur)
    conn.close()