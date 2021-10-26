import requests
import re
import pandas as pd
import sqlite3
import urllib.request
from bs4 import UnicodeDammit, BeautifulSoup

headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    }

def main():

    html = getHtml()
    p_t = parsePage(html)
    printList(p_t)
    dbpath = r'E:\数据采集实验\实验2\rank.db'
    saveData2DB(p_t, dbpath)

def ST(list):
    char='' ; list=str(list)  #将半角字符转为全角
    for li in list:
        char += CT(li)
    return char

def CT(i):
    CHAR=chr(ord(i) + 65248)
    return CHAR

def getHtml():
    url = "https://www.shanghairanking.cn/rankings/bcur/2021"
    response = urllib.request.Request(url=url, headers=headers)
    page_text=urllib.request.urlopen(response)
    page_text=page_text.read()
    dammit=UnicodeDammit(page_text,["utf-8","gbk"])
    page_text=dammit.unicode_markup
    return page_text


def parsePage(html):
    soup = BeautifulSoup(html, 'html.parser')
    lis = soup.find_all("tr")
    datas = []
    for j in range(1,len(lis)):
            tr=lis[j]
            td=tr.find_all("td")
            score = td[4].text.strip()
            name = td[1].find('a').text.strip()
            rank=td[0].find('div').text.strip()
            datas.append([rank,name,score])
    return datas

# 按格式打印得到的数据
def printList(list):
    tplt = "{0:^4}\t{1:^10}\t{2:^6}"
    print(tplt.format("排名","学校","总分",chr(12288)))

    for data in list:
        print(tplt.format(ST(data[0]),data[1],ST(data[2]),chr(12288)))


def saveData2DB(Dlist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in Dlist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
            sql = '''
                insert into rank(
                    id,name,score
                    )
                    values(%s)
            ''' % ",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    print("保存到数据库成功！")


def init_db(dbpath):
        sql = '''
            create table rank
            (
            id text,
            name text,
            score text
            );
        '''
        INIT = sqlite3.connect(dbpath)
        CUR = INIT.cursor()
        CUR = INIT.execute(sql)
        INIT.commit()
        INIT.close()


if  __name__ == "__main__":
    main()


