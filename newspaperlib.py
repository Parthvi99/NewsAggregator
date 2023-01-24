from newspaper import Article
import db
def upload_news(oururl):
    #oururl = "https://timesofindia.indiatimes.com/india/awantipora-encounter-top-hizbul-mujahideen-terrorist-riyaz-naikoo-killed-in-kashmir-encounter/articleshow/75572877.cms"
    article = Article(oururl)
    article.download()
    article.parse()
    data = []

    if article.title is not None:       #checks for article title in url and prints if present else NA
        print("----title----")
        print(article.title)
    else:
        article.title = "NA"
    if article.publish_date is not None:       #checks for article pbdate in url and prints if present else NA
        print("----publish_date----")
        print(article.publish_date)
    else:
        article.publish_date="NA"

    if article.text is not None:             #checks for article content in url and prints if present else NA
        print("----text----")
        print(article.text)
    else:
        article.text="NA"

    if article.authors is not None:           #checks for article authors in url and prints if present else NA
        print("----authors----")
        print(article.authors)
    else:        article.authors = "NA"

    if type(article.authors) is list:             #if more than one author is present in the list , it will create
        #for author in article.authors:            # separate entries for each author entry in mysql
        data.append((article.title, article.publish_date, article.text, ','.join(article.authors), oururl))
    else:
         data.append((article.title, article.publish_date, article.text, article.authors, oururl))         #for single entry #returned in tuple

    return data


if __name__ == '__main__':
    obj = upload_news()

    dbconn = db.getConnection()
    status = db.insertContent(dbconn, obj)




