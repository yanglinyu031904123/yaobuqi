import sqlite3
import re
import urllib.request
from bs4 import UnicodeDammit

headers={
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36"
    }

#用urllib.request方法访问服务器

def getHtml(page):
    url = "https://9.push2.eastmoney.com/api/qt/clist/get?cb=jQuery1124025500369212952667_1634094365855&pn="+page+"&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:6,m:0+t:80,m:1+t:2,m:1+t:23&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1634094365856"
    r = urllib.request.Request(url, headers=headers)
    html=urllib.request.urlopen(r)
    html=html.read()
    dammit=UnicodeDammit(html,["utf-8","gbk"])
    html=dammit.unicode_markup
    return html

#使用正则表达式获取股票数据
def anahtml(html):
    page_datas = []
    exID = re.compile('"f12":"(.*?)",')#股票序号
    num = re.findall(exID, html)

    exName = re.compile('"f14":"(.*?)",')#股票名称
    name = re.findall(exName, html)

    exPrice = re.compile('"f2":(.*?),')#成交价格
    price = re.findall(exPrice, html)

    exRate = re.compile('"f3":(.*?),')#涨跌幅度
    changeRate = re.findall(exRate, html)

    exChange = re.compile('"f4":(.*?),')# 涨跌额
    change = re.findall(exChange, html)

    exPrice = re.compile('"f6":(.*?),')# 成交额
    CPRICE = re.findall(exPrice, html)

    exMax = re.compile('"f15":(.*?),')# 最高价格
    MAX = re.findall(exMax, html)

    exMin = re.compile('"f16":(.*?),')# 最低格
    MIN = re.findall(exMin, html)

    for i in range(len(num)):
        page_datas.append([num[i],name[i],price[i],changeRate[i]+"%",change[i],CPRICE[i]+"元",MAX[i],MIN[i]])
    return page_datas

#数据库的保存操作
def data_save(datalist, dbpath):
    init_db(dbpath)
    conn = sqlite3.connect(dbpath)
    cur = conn.cursor()
    for data in datalist:
        for index in range(len(data)):
            data[index] = '"' + data[index] + '"'
            sql = '''
                insert into shares(
                    num,name,price,changeRate,change,currentPrice,max,min
                    )
                    values(%s)
            ''' % ",".join(data)
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()
    print("保存成功！")

def init_db(dbpath):
        sql = '''
            create table shares(
            num text,name text,price text,
            changeRate text, change text,currentPrice text,
            max text,min text
            );
        '''
        cet = sqlite3.connect(dbpath)
        cu = cet.cursor()
        cu.execute(sql)
        cet.commit()
        cet.close()

def printList(list):
	tply="{0:^4}\t{1:^8}\t{2:^8}\t{3:^5}\t{4:^6}\t{5:^5}\t{6:^9}\t{7:^5}\t{8:^5}"
	print(tply.format("序号","股票代码","股票名称","最新价","涨跌幅","涨跌额","成交额","最高","最低",chr(12288)))
	a=1
	for data in list:
		print(tply.format(a,data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],chr(12288)))
		a= a + 1

if __name__ =="__main__":
    html = getHtml("1")
    LI = anahtml(html)
    printList(LI)
    DBpath = r'E:/数据采集实验/实验2/shares.db'
    data_save(LI, DBpath)