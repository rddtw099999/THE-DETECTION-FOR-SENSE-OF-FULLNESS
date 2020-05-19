import matplotlib.pyplot as plt
import numpy as np
import random
import pymysql
import json
import time
import datetime
import pyaudio
import wave
import threading

#global latestid
#global Fs
#global s
#global currentprocess
#global fetched

#==== parameter for recording==========
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 30
#==== parameter for recording==========


#======= parameter for fake data generation==========
Fs = 8000
#s = 10
currentprocess=0
a=False
frames=[]
raw=[]
temp_frames=[]
fetched=""
latestid=0
startupload=False
#======= parameter for fake data generation==========



# def fetchdata(exe,cmd):
# 	db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
# 	cursor = db.cursor() 
# 	cursor.execute(cmd)

# 	if(exe=="fetchall"):
# 		temp=cursor.fetchall()
# 		db.close()
# 		return temp
# 	elif(exe=="count"):
# 		cursor.fetchall()
# 		count=cursor.rowcount()
# 		db.close()
# 		return count
# 	elif(exe=="insert"):
# 		db.commit()
# 		db.close()
# 		return 0




#聲音錄製主處理程序 永久執行
def SoundRecord():
	global frames
	global raw
	global startupload
	global temp_frames
	audio = pyaudio.PyAudio()
	# start Recording
	stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                frames_per_buffer=CHUNK)
	print("Recording 30s Data...")

	while(1):
		frames=[]
		for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
			data = stream.read(CHUNK)
			frames.append(np.frombuffer(data,dtype=np.int16))
			#print(type(frames))
			raw=np.frombuffer(data,dtype=np.int16)
		temp_frames=frames
		#with open("file.txt", 'w') as output:
 		#   for row in temp_frames:
     	#			output.write(str(row) + '\n')
				
		#np.savetxt("test.csv", frames,fmt="%.4f", delimiter=",")
		startupload=True
		print("Record Finish...")
			
			
#間隔取樣 建立縮圖
def graphdatagenerate():
	
	global raw
	while(1):

		if(raw!=[]):
			
			db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
			cursor = db.cursor()
			cursor.execute('DELETE from RT_Time')	
			sql='INSERT INTO RT_Time (DATA) VALUES (%s)'
			tmpdata="%.4f" % max(raw)
			val = float(tmpdata)/32767
			cursor.execute(sql, val)
			db.commit()
			db.close()

	
	
	

#不斷執行
def dataupload(): 	#把收取到的資料上傳到資料庫  
	global startupload
	global temp_frames
	while(1):
		if(startupload==True):
			#print("DataReceive : Received 10 seconds data with 8000sps (fake)....")
			y=[]
			finaldata=[]
			#for i in range(Fs*s):
			#	tmpdata="%.4f" % (random.random()-random.random())
			#	y.append(float(tmpdata))

			#print("DataReceive : Generated, Size:",len(y))
			#print("DataReceive : saving to csv")
			#np.savetxt("test.csv", y,fmt="%.4f", delimiter=",")
			
			print("DataReceive : convert to json format")
			for i in range(len(temp_frames)):
				for j in temp_frames[i]:
					finaldata.append(str(j))
			
			t=json.dumps(finaldata)
			db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
			cursor = db.cursor() 
			cursor.execute('select RAW FROM RAWDATA')
			cursor.fetchall()
			latestid=cursor.rowcount+1
			print("DataReceive : INSERT SQL ID ",latestid)
			sql = "INSERT INTO RAWDATA (ID, RAW ,Processed) VALUES (%s, %s, %s)"
			val = (latestid, t, False)
			cursor.execute(sql, val)
			db.commit()
			db.close()
			#latestdata=latestid
			startupload=False



#執行序1 不斷連結資料庫 取得還未處理的資料,并執行資料處理與模型運算

#不斷執行

def ProcessingData():    #從資料庫中抓取尚未處理完的資料
	global currentprocess
	while(1):
		
		#print("DataProcess : Current Process ID:",currentprocess)
		db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
		cursor = db.cursor() 
		cursor.execute('select * FROM RAWDATA WHERE Processed = False')
		fetched=cursor.fetchall()
		rowcount=int(cursor.rowcount)
		if(rowcount>0):
			#======================================================
			latest=json.loads(fetched[0][1])
			db.close()
			#time.sleep(2)
			print("DataProcess : Processing Done WHERE ID is",fetched[0][0])
			
			db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
			cursor = db.cursor() 
			cursor.execute('UPDATE RAWDATA SET Processed = True where ID=%s',fetched[0][0])
			db.commit()
			db.close()
			#============================DATA Compress ============
			compressed=latest[::400]
			compressed_json=json.dumps(compressed)

			
			db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
			cursor = db.cursor() 

			print("DataDataProcess : Compressed and INSERT SQL ID ",fetched[0][0])
			sql="INSERT INTO ComDATA (ID,DATA,TIME) VALUES (%s,%s,%s)"
			val=(fetched[0][0],compressed_json,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			
			cursor.execute(sql, val)
			db.commit()
			db.close()
			print("DataProcess : Running Model! WHERE ID is",fetched[0][0])
			#========================
			#Here to put all data and running Model 
			#=======================
			Fulliness=(random.randint(0,100))/100
			print("Result is",Fulliness)
			db = pymysql.connect(host='192.168.123.100', port=3306, user='USERNAME', passwd='PASSWORD', db='SmartHealthyLossWeight', charset='utf8')
			cursor = db.cursor() 

			print("DataDataProcess : Compressed and INSERT SQL ID ",fetched[0][0])
			sql="INSERT INTO ResDATA (ID,Date,Time,Result) VALUES (%s,%s,%s,%s)"
			
			val=(fetched[0][0],datetime.datetime.now().strftime("%Y-%m-%d"),datetime.datetime.now().strftime("%H:%M:%S.000000"),Fulliness)
			cursor.execute(sql, val)
			db.commit()
			db.close()
		
			#======================================================

			print("DataProcess : Success! ,waiting for 10s")
			







# Main 主程式控制區
if __name__ == '__main__':
	t = threading.Thread(target=SoundRecord)	
	t.start()	
	f = threading.Thread(target=dataupload)	
	f.start()	
	d = threading.Thread(target=ProcessingData)
	d.start()
	x = threading.Thread(target=graphdatagenerate)
	x.start()
	

