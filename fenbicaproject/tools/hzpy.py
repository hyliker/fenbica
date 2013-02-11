#!/usr/bin/env python
#coding: utf-8
import sqlite3


DB_PATH = "tools/hzpy.db3"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()
def hz2py(hzs):
    print hzs
    pinyins = []
    hzs = hzs.strip()
    for hz in hzs:
        hz_placeholder = (hz,)
        result = cur.execute(u"select py from hzpy where hz = ?", hz_placeholder)
        only_py = result.fetchone()[0][:-1]
        pinyins.append(only_py)
    print "".join(pinyins)
    return "".join(pinyins)

#print hz2py(u"中国2")
