import time
import paho.mqtt.client as mqtt
import pymysql.cursors
from datetime import datetime
from datetime import date
import ping3
import logging
import pytz

logging.basicConfig(filename="/home/azureiotuser/server.log",format='%(asctime)s %(message)s',filemode='a')
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


def on_connect(client, userdata, flags, rc):
	print("Connected with result code "+str(rc))

def on_message(client, userdata, msg):
	print("Data arrived")
	print('\n')

while True:
	try:
		#print("trying")
		client = mqtt.Client()
		client.on_connect = on_connect
		client.on_message = on_message
		client.connect("20.205.208.135", 1883, 60)
	except Exception as e:
		print("Issue Found")
		raise e
	else:
		connection = pymysql.connect(host='souliot.mariadb.database.azure.com',user='okcliot@souliot',password='Siva@123',database='okcldb',cursorclass=pymysql.cursors.DictCursor)
		with connection.cursor() as cursor:
			sql = "select school_id,device_id from keonjhar_school_device where device_temp>=50 and device_mq2>=5000 and device_hum<=25 group by school_id having count(device_temp)>=2"
			cursor.execute(sql)
			result = cursor.fetchall()
			if result == ():
				print("Sensors Stable")
			else:
				print("Sensor Unstable")
				print("High Alert")
				for i in result:
					print("Initiating Alarm for School {}".format(i["school_id"]))
					school_id = i["school_id"]
					device_id = i["device_id"]
					with connection.cursor() as cursor:
						sql654 = "Select school_name from keonjhar_school where school_id=%s"
						cursor.execute(sql654,(int(school_id)))
						result44 = cursor.fetchone()
						school_name = result44["school_name"]
						send_alert_topic = str(device_id)+"/"+str(school_id)+"/"+str(school_name)+"/"+"Set_Alert"
						client.publish(send_alert_topic,"theft/alarm_on")
						print("Alert Sent")
# client.loop_forever()