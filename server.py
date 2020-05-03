import socket 
from _thread import *
import pickle 
import random
server = ""
port = 5555 
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try: 
    s.bind((server,port))
except socket.error as e:
    str(e)

s.listen(2)
print("Waiting for a connection, server started")

players = {}
colors = [(255,0,0),(0,255,0),(0,0,255),(23,47,75)]
_id = 0
def threaded_client(conn, player):
    global players
    current_id = _id

    ###get nickname###
    data = conn.recv(16)
    name = data.decode('utf-8')
    print("[LOG]", name, "connected to the server.")

    ### setup player's properties###
    color = colors[current_id]
    x, y = random.randint(50,100), random.randint(50,100)
    players[current_id] = {"x":x, "y":y, "color":color}

    ###reply to client###
    conn.send(str.encode(str(current_id)))

    while True:
        try:
            data = conn.recv(32)
            if not data:
                break

            data = data.decode("utf-8")

            ##update players moves list
            if data.split(" ")[0] == "move":
                split_data = data.split(" ")
                x = int(split_data[1])
                y = int(split_data[2])
                players[current_id]["x"] = x
                players[current_id]["y"] = y

                send_data = pickle.dumps((players))

            ###just send back players list
            else:
                send_data = pickle.dumps((players))
            
            conn.send(send_data)

        except Exception as e:
            print(e)

    del players[current_id]
    conn.close()

while True:
    conn, addr = s.accept()
    print("Connected to: ", addr)

    start_new_thread(threaded_client, (conn, _id))
    _id += 1