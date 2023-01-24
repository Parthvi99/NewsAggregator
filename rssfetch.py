import Stompconnector
import feedparser
import stomp
import time
from threading import *
import db


news_urls = []
dbconn = db.getConnection()
cursorObj = dbconn.cursor()
query = f'SELECT main_links FROM mainrss'
cursorObj.execute(query)
mainlinks =cursorObj.fetchall()
for m in mainlinks:
    for ml in m:
        news_urls.append(ml)
cursorObj.close()
#list of urls of newschannels
# news_urls = ["http://rss.cnn.com/rss/cnn_latest", "https://feeds.feedburner.com/ndtvnews-top-stories", "https://timesofindia.indiatimes.com/rssfeedstopstories.cms",
#              "https://www.indiatoday.in/rss/1206514"]
#entries in each url
entries = [1,2,3,4,5,6,7,8,9,10]
links = []

class Feeds:

    def feed(self):
        #print("2s job current time : {}".format(time.ctime()))
        for url in news_urls:              #
            print(f">>>>>>Now Parsing {url}")
            NewsFeed = feedparser.parse(url)
            for j in range(0, len(NewsFeed.entries)):
                entry1 = NewsFeed.entries[j]
                if 'link' in entry1:  # will check link in list entry1
                    print("------News Link--------")
                    print(entry1["link"])
                    links.append(entry1["link"])




if __name__ ==  "__main__":
    _config = {                               #all config for activemq
        'host': 'localhost',
        'port': 61613,
        'user': 'admin',
        'passwd': 'admin',
        'pool_size': 1,
        'id': 'ID:LAPTOP-P0H41LV1-49936-1584366150606-0:1',
        'source_queue': '/queue/newsagg',
        'threshold': 900
    }
    while True:
        Feeds()
        obj= Feeds()
        f1= Thread(target=obj.feed)       #using thread
        f1.start()          #start with the execution of the thread to process the message
        f1.join()             # Wait until the thread's execution is completed. Then shut it down
        time.sleep(0.2)
        dbconn = db.getConnection()
        final_links = db.check_record(dbconn, links)     #getting non repeated links from db1
        # print(final_links, len(final_links))
        db.insertRecord(dbconn, final_links)  #inserting same in db1
        #stomptry.links = final_links
        Stompconnector.connect_and_subscribe(_config)
        conn = Stompconnector.connect_and_subscribe(_config)
        #stomptry.connect_and_subscribe(_config,final_links)    #passing(pushing) same in activemq
        for link in final_links:
            conn.send(body=link,destination='/queue/newsagg', headers={'persistent':'true'})

        time.sleep(120)    #for running the whole program again after 2mins


