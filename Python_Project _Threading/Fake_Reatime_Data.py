import matplotlib.pyplot as plt
import numpy as np
import random
import pymysql
import json
import time



while(1):
	db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
	cursor = db.cursor()
	cursor.execute('DELETE from RT_Time')	
	sql='INSERT INTO RT_Time (DATA) VALUES (%s)'
	tmpdata="%.4f" % (random.random()-random.random())
	val = float(tmpdata)
	cursor.execute(sql, val)
	db.commit()
	db.close()
	time.sleep(0.05)

