import feedparser
import sqlite3
rssArray = []

def create_table(cur):
    print("Creating new ztis table")
    try:
        cur.execute("""CREATE TABLE ztis (
    id               INTEGER    PRIMARY KEY
                                UNIQUE,
    source           TEXT (600),
    title            TEXT (200) UNIQUE,
    summary          TEXT (600),
    publication_date DATE,
    author           TEXT (100)
);
""")
    except:
        pass

def drop_table(cur):
    print("Dropping ztis table with all data")
    try:
        cur.execute("DROP TABLE ztis")
    except:
        pass

def delete_duplicates(conn, cur):
    print("Deleting duplicates form ztis table")
    try:
        cur.execute("DELETE FROM ztis WHERE rowid NOT IN (SELECT MIN(rowid) FROM ztis GROUP BY title)")
        conn.commit()
        print("Duplicates correctly removed")
    except:
        pass

def count_data(cur):
    try:
        cur.execute("SELECT COUNT(*) FROM ztis")
        count = cur.fetchone()
        print("There are %d rows in ztis table" % (count))
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
            cur.execute("INSERT OR IGNORE INTO ztis(source, title, summary, publication_date, author) VALUES (?,?,?,?,?)", (source, title, summary, publication_date, author))
            counter += 1
            conn.commit()
            #, (source, title, summary, publication_date, author)
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
    count_data(cur)
    read_rsslist()
    download_data()
#    drop_table(cur)
#    create_table(cur)
    save_data(conn, cur)
    delete_duplicates(conn, cur)
    count_data(cur)
    conn.close()