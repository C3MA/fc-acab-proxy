# coding=utf-8
"""
Created on 06.12.2013

@author: Käptn
"""

__author__ = 'Käptn'

import Queue
import socket
import thread
from PyFullcircle import FcClient, FcFrame
import copy
import time

# Codename "TZ"

CLIENT_ACAB_HOST = '0.0.0.0'
CLIENT_ACAB_PORT = 5000

WALLS = {
  #  'fc-1': {'type':'fc', 'host':'10.23.42.102', 'port':24567, 'offset':[0,0], 'size':[10,12]}, # Ollo
  #  'fc-1': {'type':'fc', 'host':'10.23.42.88', 'port':24567, 'offset':[0,0], 'size':[10,12]},  # Wand
  #  'fc-1': {'type':'fc', 'host':'10.23.42.201', 'port':24567, 'offset':[0,0], 'size':[7,10]}, # Mac

    'fc-1' : {'type':'acab', 'host':'localhost', 'port':6000, 'offset':[0,0]}, # ACAB Sim
    'acabsim-2' : {'type':'acab', 'host':'localhost', 'port':6010, 'offset':[0,11]}, # ACAB Sim-2

    #'acab-1' : {'type':'acab', 'host':'localhost', 'port':6000, 'offset':[0,0]},
    #'fc-1': {'type':'fc', 'host':'localhost', 'port':23467, 'offset':[3,3]},
}

"""
MATRIX = {
    0 : {0:'acab-1', 1:'acab-1', 2:'acab-1', 3:'acab-1', 4:'acab-1', 5:'acab-1', 6:'acab-1', 7:'acab-1', 8:'acab-1', 9:'acab-1', 10:'acab-1'},
    1 : {0:'acab-1', 1:'acab-1', 2:'acab-1', 3:'acab-1', 4:'acab-1', 5:'acab-1', 6:'acab-1', 7:'acab-1', 8:'acab-1', 9:'acab-1', 10:'acab-1'},
    2 : {0:'acab-1', 1:'acab-1', 2:'acab-1', 3:'acab-1', 4:'acab-1', 5:'acab-1', 6:'acab-1', 7:'acab-1', 8:'acab-1', 9:'acab-1', 10:'acab-1'},
    3 : {0:'acab-1', 1:'acab-1', 2:'acab-1', 3:'fc-1',   4:'fc-1',   5:'fc-1',   6:'fc-1',   7:'fc-1',   8:'acab-1', 9:'acab-1', 10:'acab-1'},
    4 : {0:'acab-1', 1:'acab-1', 2:'acab-1', 3:'fc-1',   4:'fc-1',   5:'fc-1',   6:'fc-1',   7:'fc-1',   8:'acab-1', 9:'acab-1', 10:'acab-1'},
    5 : {0:'acab-1', 1:'acab-1', 2:'acab-1', 3:'fc-1',   4:'fc-1',   5:'fc-1',   6:'fc-1',   7:'fc-1',   8:'acab-1', 9:'acab-1', 10:'acab-1'},
    6 : {0:'acab-1', 1:'acab-1', 2:'acab-1', 3:'fc-1',   4:'fc-1',   5:'fc-1',   6:'fc-1',   7:'fc-1',   8:'acab-1', 9:'acab-1', 10:'acab-1'},
    7 : {0:'acab-1', 1:'acab-1', 2:'acab-1', 3:'fc-1',   4:'fc-1',   5:'fc-1',   6:'fc-1',   7:'fc-1',   8:'acab-1', 9:'acab-1', 10:'acab-1'},
}
"""

MATRIX = {
    0 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},
    1 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},
    2 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},
    3 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},
    4 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},
    5 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},
    6 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},
    7 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},
    8 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},
    9 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},
   10 : {0:'fc-1', 1:'fc-1', 2:'fc-1', 3:'fc-1', 4:'fc-1', 5:'fc-1', 6:'fc-1', 7:'fc-1'},

   11 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
   12 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
   13 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
   14 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
   15 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
   16 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
   17 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
   18 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
   19 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
   20 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
   21 : {0:'acabsim-2', 1:'acabsim-2', 2:'acabsim-2', 3:'acabsim-2', 4:'acabsim-2', 5:'acabsim-2', 6:'acabsim-2', 7:'acabsim-2'},
}


width = 8
height = 22

for wKey in WALLS:
    w = WALLS[wKey]
    if w['type'] == 'acab':
        w['socket'] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    else:
        w['socket'] = FcClient(w['host'])
       # w['size'] = w['socket'].request_info()
        w['socket'].initialiseConnection(w['size'][0], w['size'][1], 12, None)
        w['socket'].waitForStart()
        w['frame'] = FcFrame(w['size'][0], w['size'][1])
        w['actFrame'] = copy.copy(w['frame'])

def findWall(x, y):
    """
    Findet eine Passende Wand zu einem Pixel (oder auch net)
    :param x: X Wert des Pixels
    :param y: Y Wert des Pixels
    :return: Wand DIctionary oder None
    """
    try:
        return WALLS[MATRIX[y][x]]
    except KeyError:
        return None

q = Queue.Queue(500)

def acabHandler():
    while True:
        data = q.get()
        try:
            x = ord(data[0])
            y = ord(data[1])
            cmd = data[2]
            r = ord(data[3])
            g = ord(data[4])
            b = ord(data[5])
            msh = ord(data[6])
            msl = ord(data[7])

            w = findWall(x,y)

            if not w:
                continue

            if cmd == 'C':
                if w['type'] == 'acab':
                    msg = "%c%cC%c%c%c%c%c"% (x - w['offset'][0],y - w['offset'][1],r,g,b,msh,msl)
                    w['socket'].sendto(msg, (w['host'], w['port']))
                elif  w['type'] == 'fc':
                    w['actFrame'].setColorForPixel(x - w['offset'][0],y - w['offset'][1], r,g,b)
            elif cmd == 'U':
                for waKey in WALLS:
                    wa = WALLS[waKey]
                    if wa['type'] == 'acab':
                        wa['socket'].sendto(data, (wa['host'], wa['port']))
                    elif  wa['type'] == 'fc':
                        wa['socket'].sendFrame(wa['actFrame'])
                        wa['actFrame'] = copy.copy(wa['frame'])
            elif cmd == 'F':
                w['socket'].sendto(data, (w['host'], w['port']))
        except Exception as e:
            print "Unexpected error:", e
            print "Error data: ", list(data)

def acabReader(sock):
    while True:
        data = sock.recv(1024)
        if not q.full():
            q.put(data)
        else:
            print 'ignoring data'


if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((CLIENT_ACAB_HOST,CLIENT_ACAB_PORT))
    thread.start_new_thread(acabHandler, ())
    thread.start_new_thread(acabReader, (sock,))

    while True:
        time.sleep(5)