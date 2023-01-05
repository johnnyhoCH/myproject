# -*- coding: utf-8 -*-
"""
Created on Sat Nov 19 15:51:25 2022

@author: user
"""

import requests
from bs4 import BeautifulSoup

import db

from datetime import datetime as dt #抓日期函式庫

today = dt.today()
todayS = today.strftime('%Y-%m-%d')  #將設定好的日期格式轉換成字串使用


url = "https://shopee.tw/search?keyword=%E4%B8%AD%E8%8F%AF%E8%81%B7%E6%A3%92"


keyword = "中華職棒"

headers = {
    'user-agent': 'Googlebot',
      }     
data = requests.get(url,headers=headers,allow_redirects=True).text

soup = BeautifulSoup(data,'html.parser')

goods = soup.find_all("div",class_="row shopee-search-item-result__items")

allgoods = soup.find_all("div",class_="col-xs-2-4 shopee-search-item-result__item")

cursor = db.conn.cursor()

for items in allgoods:
    name = items.find("div",class_="dpiR4u").text
    price = items.find("span",class_="ZEgDH9").text
    photo = items.find("div",class_="yvbeD6 KUUypF")
    photo = photo.find("img").get("src")
    
    
    
   

  
    sql = "select * from product where name='{}' COLLATE utf8_unicode_ci;".format(name)
    
    cursor.execute(sql)
    db.conn.commit()
    
    if cursor.rowcount == 0:
        sql = "insert into product(name,price,photo,create_date) values('{}','{}','{}','{}')".format(name,price,photo,todayS)
        cursor.execute(sql)
        db.conn.commit()
        
db.conn.close()


