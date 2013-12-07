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
import threading
import copy
import time
import sequence_pb2

# Codename "TZ"

CLIENT_ACAB_HOST = '0.0.0.0'
CLIENT_ACAB_PORT = 5000

WALLS = {
  #  'fc-1': {'type':'fc', 'host':'10.23.42.102', 'port':24567, 'offset':[0,0], }, # Ollo
  #  'fc-1': {'type':'fc', 'host':'10.23.42.88', 'port':24567, 'offset':[0,0]},  # Wand
  #  'fc-1': {'type':'fc', 'host':'10.23.42.201', 'port':24567, 'offset':[0,0]}, # Mac

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
        if 'size' not in w.keys():
            w['size'] = w['socket'].request_info()
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

q = Queue.Queue(100)
qFc = Queue.Queue(10)

def handleData(x,y,cmd,r,g,b,msh,msl):
    w = findWall(x,y)

    if not w:
        return

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
                msg = "%c%cU%c%c%c%c%c" % (x ,y ,r,g,b,msh,msl)
                wa['socket'].sendto(msg, (wa['host'], wa['port']))
            elif  wa['type'] == 'fc':
                wa['socket'].sendFrame(wa['actFrame'])
                wa['actFrame'] = copy.copy(wa['frame'])
    elif cmd == 'F':
        msg = "%c%cF%c%c%c%c%c" % (x ,y ,r,g,b,msh,msl)
        w['socket'].sendto(msg, (w['host'], w['port']))

def acabHandler():
    """
    Thread für die abarbeitung der ACAB Warteschlange.
    """
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

            handleData(x,y,cmd,r,g,b,msh,msl)

        except Exception as e:
            print "Unexpected error:", e
            print "Error data: ", list(data)

def acabReader(sock):
    """
    Thread um die ACAB Warteschlange mit den UDP Paketen zu füllen
    :param sock: UDP Socket des ACAB Client
    """
    while True:
        data = sock.recv(1024)
        if not q.full():
            q.put(data)
        else:
            print 'ignoring data'


def fcHandler():
    while True:
        thr = qFc.get()
        thr.setActive()
        thr.join()
        time.sleep(1)

class FCServer(threading.Thread):
    conn = ""
    active = False

    def __init__(self, c):
        super(FCServer, self).__init__()
        self.conn = c

    def setActive(self):
        s = sequence_pb2.Snip()
        s.type = 5
        self.sendSnip(s)

        self.active = True

    def run(self):
        try:
            while True:
                rawreceive = self.conn.recv(10)
                if rawreceive:
                    length = (rawreceive[:10]).strip()
                    content = self.conn.recv(int(length))
                    incoming = sequence_pb2.Snip.FromString( content )
                    self.handleInput(incoming)
                else:
                    break
        except Exception as e:
            print e

        print "TCP Verbindung geschlossen"
        self.conn.close();

    def handleInput(self, incoming):

        if incoming.type == 4:
            if incoming.req_snip.meta.width != width or incoming.req_snip.meta.height != height:
                s = sequence_pb2.Snip()
                s.type = 3
                s.error_snip.errorcode = 10
                s.error_snip.description = "Size not correct"
                self.sendSnip(s)
                raise Exception("Client size incorrect")
            s = sequence_pb2.Snip()
            s.type = 7
            self.sendSnip(s)
        elif incoming.type == 12:
            s = sequence_pb2.Snip()
            s.type = 13
            s.infoanswer_snip.meta.frames_per_second = 12;
            s.infoanswer_snip.meta.width = width;
            s.infoanswer_snip.meta.height = height;
            s.infoanswer_snip.meta.generator_name = "fc-acab-server";
            s.infoanswer_snip.meta.generator_version = "0.0.1";
            self.sendSnip(s)
        elif incoming.type == 6 and self.active:
            for pix in incoming.frame_snip.frame.pixel:
                handleData(pix.x, pix.y, 'C', pix.red, pix.green, pix.blue, 0, 0)
            handleData(0,0,'U',0,0,0,0,0)

        else:
            print "Unbehandelter Typ: '%s'" % incoming.type
            print "Data:"
            print incoming


    def sendSnip(self, snip):
        raw2send = snip.SerializeToString()
        head = '%10d' % len(raw2send)
        self.conn.send(head + raw2send)

if __name__ == "__main__":
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((CLIENT_ACAB_HOST,CLIENT_ACAB_PORT))
    thread.start_new_thread(acabHandler, ())
    thread.start_new_thread(acabReader, (sock,))


    thread.start_new_thread(fcHandler, ())

    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.bind(("", 24567))
        s.listen(True)

        while True:
            con, addr = s.accept()
            print "New FC Connection from ", addr
            if not q.full():
                thr = FCServer(con)
                #thr.setDaemon(True)
                thr.start()
                time.sleep(1)
                qFc.put(thr)
            else:
                print "Queue full. Not longer Accepting new Connections"
            time.sleep(1)
    except Exception as e:
        print "TCP Socket konnte nicht geöffnet werden :'("
        print e
    s.close()
    sock.close()


