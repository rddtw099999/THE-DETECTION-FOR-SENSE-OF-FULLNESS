import matplotlib.pyplot as plt
import numpy as np
import random
import pymysql
import json
import time
Fs = 8000
s = 10

def datareceive(): 
	print("Received 10 seconds data with 8000sps (fake)....")
	y=[]
	for i in range(Fs*s):
		tmpdata="%.4f" % (random.random()-random.random())
		y.append(float(tmpdata))

	print("Generated, Size:",len(y))
	print("saving to csv")
	np.savetxt("test.csv", y,fmt="%.4f", delimiter=",")
	print("convert to byte string")
	t=json.dumps(y)



	db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
	cursor = db.cursor() 
	cursor.execute('select RAW FROM RAWDATA')
	cursor.fetchall()
	latestid=int(cursor.rowcount)+1
	print("INSEART SQL ID:",latestid)

	sql = "INSERT INTO RAWDATA (ID, RAW) VALUES (%s, %s)"
	val = (latestid, t)
	cursor.execute(sql, val)
	db.commit()
	db.close()
	time.sleep(5)





#print(bytedata)
#print(np.fromstring(bytedata,dtype=float))

