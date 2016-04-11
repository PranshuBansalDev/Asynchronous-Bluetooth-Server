import bluetooth
import os
from bluetooth_globs import *
from client_webserver import *

if __name__ == "__main__":
    init_connection()
	#sockets are always done by: initialize, bind, listen, accept
    listen_socket = bluetooth.BluetoothSocket( COMM_PROTOCOL )
    listen_socket.bind(("", PORT))
    listen_socket.listen(1024) #allow for up to a total of 1024 connections

    while True:
        client, addr = listen_socket.accept()
        print "accepted connection from {}".format(addr)
		
        pid = os.fork()
        if pid == 0:
            listen_socket.close()
            #try to recieve each message. If the connection is broken, simply kill the child process
			try:
                while True: 
                    msg = client.recv(1024)
                    msg = msg.split(", ")
                    print "Device {} says {}".format(addr, msg)
					#msg string format is: "device_bluetooth_address, RSSI_corresponding_to_device, my_bluetooth_address, UNUSED"
					#send_rssi_info from client_webserver.py is: send_rssi_info_basic(anchor_id, client_id, rssi, time_stamp)
					#must re-order for compatibility
					#commented out as the server may not be functional at time of use. Replace with whatever you want (print the message maybe?)
                    #send_rssi_info(msg[0], msg[2], msg[1], msg[3])
            except bluetooth.BluetoothError as e:
                print "device {} has disconnected because {}".format(addr, e)
            finally:
                os._exit(0)
        else:
            client.close()
            time.sleep(1)
