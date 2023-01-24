import mysql.connector as db


def getConnection():          #make connection with db
    con = db.connect(
        host="localhost",
        user="root",
        password="",
        database="newsagg"
    )

    if con.is_connected():      #checks if connection is made
        return con
    else:
        return False


def insertRecord(con, urls):
#inserting records in db1 called newsagg
    query = f"INSERT INTO news_links(url) VALUES(%s)"
    args = []

    for url in urls:
        args.append((url,))  #converting into tuple and appending in a list

    cursorObj = con.cursor()
    cursorObj.executemany(query, args)
    con.commit()

    if cursorObj.rowcount:    #checks the last row count
        status = True
    else:
        status = False

    cursorObj.close()

    return status


# Checking if the record exists and returning a list of non-existing records
def check_record(con, data):
    links = []
    cursor = con.cursor()

    for link in data:
        query = f"SELECT url FROM news_links WHERE url = '{link}' LIMIT 1"

        cursor.execute(query)
        result = cursor.fetchone()

        if result is None:
            links.append(link)

    cursor.close()

    return links

def insertContent(con, newsdata):
#insert records in table  called allcontent

    query = f"INSERT INTO allcontent(title,pbdate,text,author,url) VALUES(%s,%s,%s,%s,%s)"

    cursorObj = con.cursor()

    if type(newsdata) is list:                      #if condition for checking author part of newspaperlib
        cursorObj.executemany(query,newsdata)      #if the type of entry is a list,it will create a separate entry for each element
        con.commit()
        if cursorObj.rowcount:
            status = True
        else:
            status = False
    else:
        cursorObj.execute(query, newsdata)  # for single entry
        con.commit()

        if cursorObj.lastrowid:  # newaddition add new links change here
            status = True
        else:
            status = False

    cursorObj.close()

    return status



def closeconnection(con):     #disconnection
    return con.close()



