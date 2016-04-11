import os
import bluetooth
import sys
import time

#list of recognized anchor nodes (asynchronous bluetooth server addresses). THIS WILL NEED TO BE UPDATED FOR YOUR PURPOSES
#simply run "python get_bdadrr.py" to get the bluetooth address of the base station
#known_devices = ["98:4F:EE:04:89:3F", "98:4F:EE:03:5B:7E", "98:4F:EE:03:2E:52", "98:4F:EE:03:F5:C5", "98:4F:EE:05:23:CF", "98:4F:EE:03:35:A0"]
known_devices = [THROWING AN ERROR SO YOU CAN FIX THIS PART]
MAX_CONNECTION_TIME = 30
#MAKE SURE ONLY ONE PROTOCOL AND PORT ARE UNCOMMENTED
COMM_PROTOCOL = bluetooth.L2CAP
PORT = 0x1001 #L2CAP is a little wierd, make sure you know which ports are and are not allowed to be used
#If you want to use the RFCOMM protocol uncomment the following
#COMM_PROTOCOL = bluetooth.RFCOMM
#PORT = 1

#this boots our board. On initial boot if this fails simply run the code again and it usually works
def init_connection():
	print "Booting...",
	sys.stdout.flush()
	time.sleep(0.5)
	os.system("rfkill unblock bluetooth")
	time.sleep(0.5)
	os.system("hciconfig hci0 down")
	time.sleep(0.5)
	os.system("hciconfig hci0 up")
	time.sleep(0.5)
	os.system("hciconfig hci0 piscan")
	time.sleep(0.5)
	print "completed"