import bluetooth
import datetime
import os
import sys
import time
from bluetooth_globs import *
from bluetooth_rssi import get_closest_device
from bluetooth_rssi import get_devices
from bluetooth_rssi import get_my_bdaddr

connected_device = [""]

def connect_bluetooth(known_devices, p):
	"""
	This function will scan the area for bluetooth devices. 
	If a bluetooth device that is recognized is found it will attempt to establish a bluetooth connection with it. 
	If no bluetooth device is found, it will re-scan until a bluetooth device is found.
	ARGUMENTS:
		known_devices: list of strings containing recognized bluetooth device addresses
		p: port to connect
	RETURNS:
		Nothing
	"""
    sock = None
    while sock is None:
        print "finding closest device..."
        while True:
            device_tuple = get_closest_device(known_devices) #get closest device returns a tuple (device_address, device_RSSI)
            if device_tuple is not None:
				print "Device found: {} with RSSI: {}".format(device_tuple[0], device_tuple[1])
				connected_device[0] = device_tuple[0] #let our program know that we are connected to this device.
				break
            print "No recognized device found, looking again..."
        device = device_tuple[0]
        print "Attempting to establish connection with device {}...".format(device)
        try:
            sock = bluetooth.BluetoothSocket( COMM_PROTOCOL )
            sock.connect((device, p))
            print "Connection established"
            return sock
        except bluetooth.btcommon.BluetoothError as e:
            print e
            sock = None

def send_rssi(sock, known_devices):
	"""
	Given a socket, will send RSSI information about connection to nearest anchor node
	Will break socket connection after MAX_CONNECTION_TIME seconds as defined in bluetooth_globs.py
	ARGUMENTS:
		sock: established bluetooth socket communication
		known_devices: same as above
	"""
    i = 0
    start = datetime.datetime.now()
    while True:
        devices = get_devices(False)
        for device in devices:
			#information being sent: "device_bluetooth_address, RSSI_corresponding_to_device, my_bluetooth_address, UNUSED" - in format of string
            if device[0] == connected_device[0]: sock.send("{}, {}, {}, {}".format(device[0], device[1], get_my_bdaddr(), i))
        i+=1
        now = datetime.datetime.now()
        if (now-start).seconds >= MAX_CONNECTION_TIME: #timeout for connection, can be removed if not testing
            print "Disconnecting, has been longer than {} seconds".format(MAX_CONNECTION_TIME)
            sock.close()

if __name__ == "__main__":
    init_connection()
    sock = connect_bluetooth(known_devices, PORT)
    while True:
        try:
            send_rssi(sock, known_devices)
        except bluetooth.btcommon.BluetoothError as e: #if our connection dies, re-establish it
            sock = connect_bluetooth(known_devices, PORT)
    sock.close()
