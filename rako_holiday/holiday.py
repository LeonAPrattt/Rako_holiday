import datetime
import time
import socket
import logging
#enter the names of the log files
lognames = ["rako-04-04-22.log","rako-03-04-22.log"]
lognames = sorted(lognames)

prev_room = ""
prev_channel = ""
prev_scene = ""

def set_scene( room, channel, scene):
    BRIDGE_IP = "192.168.1.34"
    PORT = "9761"
    data = bytearray.fromhex('000000000000000000')

    data[0] = 0x52
    data[1] = 7
    data[2] = room >> 8
    data[3] = room & 0xff
    data[4] = channel
    data[5] = 0x31
    data[6] = 0x1
    data[7] = scene

    sum = 0
    for x in data[1:]:
        sum += x

    data[8] = 0x100 - (sum & 0xff)

    print(data)
    soc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
    soc.connect((BRIDGE_IP, PORT))
    soc.send(data)
    soc.close()





def readlogs():
    full_log = []

    for x in range(len(lognames)):
        f = open(lognames[x], "r")
        file = f.readlines()
        for y in range(len(file)):
            full_log.append(file[y].strip("\n"))





    for x in range(len(full_log)):
        current_time = ""
        date = full_log[x].split(" ")[0]
        tod = date.split("T")[1] 
        send = False

        t=datetime.datetime.now(datetime.timezone.utc)
        T=t.astimezone().isoformat(timespec='seconds')
        current_time = T.split("T")[1]

        
        if tod > current_time:
            send = True

        elif tod < current_time:
            send = False
            print("less")
            continue
        while send == True:

            t=datetime.datetime.now(datetime.timezone.utc)
            T=t.astimezone().isoformat(timespec='seconds')
            current_time = T.split("T")[1]
            print(tod, current_time)

            if tod == current_time:
                    splt = full_log[x].split(" ")
                    room = splt[5].split("=")[1]

                    channel = splt[7].split("=")[1]

                    scene = splt[8].split("=")[1]
                    if room != prev_room or channel != prev_channel or scene != prev_scene:
                        set_scene(room,channel,scene)    
                        print("send")
                                            
                        logger = logging.getLogger()
                        logger.setLevel(logging.DEBUG)

                        formatter = logging.Formatter('%(asctime)s - %(message)s')

                        fh = logging.FileHandler('holiday_debug_log.txt')
                        fh.setLevel(logging.DEBUG)
                        fh.setFormatter(formatter)
                        logger.addHandler(fh)

                        sh = logging.StreamHandler()
                        sh.setLevel(logging.DEBUG)
                        sh.setFormatter(formatter)
                        logger.addHandler(sh)

                        logger.debug("log_time=%s room=%s channel=%s scene=%s" %(tod, room,channel,scene))

                        prev_room = room
                        prev_channel = channel
                        prev_scene = scene
                        send = False
      
        
while True:
    readlogs()
    time.sleep(1)