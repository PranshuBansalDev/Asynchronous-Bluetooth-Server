#returns the bluetooth address of the Edison it is being called on
def get_my_bdaddr():
    with open("/factory/bluetooth_address","r") as fo: 
		bd_addr = fo.read(17)
    return  bd_addr

if __name__ == "__main__":
    print get_my_bdaddr()
