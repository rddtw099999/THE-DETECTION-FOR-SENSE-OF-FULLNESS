import matplotlib.pyplot as plt
import numpy as np
import random
import pymysql
import json
import time



if(input(r'"yes" to truncate all:')=="yes"):
	db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
	cursor = db.cursor()
	cursor.execute('TRUNCATE RT_Time')
	db.commit()	

	db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
	cursor = db.cursor()
	cursor.execute('TRUNCATE RAWDATA')	
	db.commit()

	db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
	cursor = db.cursor()
	cursor.execute('TRUNCATE ComDATA')	
	db.commit()
	
	db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
	cursor = db.cursor()
	cursor.execute('TRUNCATE ResDATA')	
	db.commit()



	db.close()

	print("All tables in SmartHealthyLossWeight Datebase has been truncated")
else:
	print("exit")


