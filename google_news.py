from bs4 import BeautifulSoup as soup
from urllib.request import urlopen
import time

#https://news.google.com/news/rss
news_url = "https://news.google.com/news/rss"
for url in news_url:
    Client = urlopen(url)
    xml_page = Client.read()
    Client.close()

    soup_page = soup(xml_page, "xml")
    news_list = soup_page.findAll("item")
    # Print news title, url and publish date
    for news in news_list:
        print(news.title.text)
        print(news.link.text)
        print(news.pubDate.text)
        print("-" * 60)






