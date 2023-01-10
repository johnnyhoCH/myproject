# -*- coding: utf-8 -*-
"""
Created on Thu Sep 29 20:56:03 2022

@author: user
"""

import pymysql

dbsetting = {
    "host":"127.0.0.1",
    "port":3306,
    "user":"root",
    "password":"",
    "db":"myproject",
    "charset":"utf8"
    
    }

conn = pymysql.connect(**dbsetting)