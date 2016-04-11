# API to send data to a webserver
import datetime, time
import json
import os
import socket
import sys
import urllib

def wake_server():
	print "The server is being waken up..."
	feed = urllib.urlopen("http://164.67.194.243/ee202c_BT/run_server")

def send_rssi_info_basic(anchor_id, client_id, rssi, time_stamp):
	#### Connect to host, build socket connection
	HOST = '164.67.194.243'    # The remote host
	WEB_PORT = 5000              # The same WEB_PORT as used by the server
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((HOST, WEB_PORT))
	response_dict = {"anchor_id":anchor_id,"client_id":client_id,"RSSI":str(rssi),"time":str(time_stamp)}
	response_str = json.dumps(response_dict)
	s.sendall(response_str)	
	
def send_rssi_info(anchor_id, client_id, rssi, time_stamp):
	#### Connect to host, build socket connection
	HOST = '164.67.194.243'    # The remote host
	WEB_PORT = 5000              # The same WEB_PORT as used by the server

	try:
		s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		s.connect((HOST, WEB_PORT))
		response_dict = {"anchor_id":anchor_id,"client_id":client_id,"RSSI":str(rssi),"time":str(time_stamp)}
		response_str = json.dumps(response_dict)
		s.sendall(response_str)
	except socket.error as e:
		pid = os.fork()
		if pid == 0:
			print e
			wake_server()
			os._exit(0)
		else:
			s.close()
			s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
			time.sleep(2)
			s.connect((HOST, WEB_PORT))
			response_dict = {"anchor_id":anchor_id,"client_id":client_id,"RSSI":str(rssi),"time":str(time_stamp)}
			response_str = json.dumps(response_dict)
			s.sendall(response_str)

if __name__ == "__main__":
	send_rssi_info_basic("1234", "5678", -45, datetime.datetime.now())