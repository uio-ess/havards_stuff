import socket
import RPi.GPIO as GPIO
import time
import pickle

HOST = ""
PORT = 4321

GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)


class SocketTrigger(object):
        trigCountFile = "triggerCount"

        def __init__(self):
                try:
                        self.pfile = open(self.trigCountFile, mode="r+b")
                        self.triggers = pickle.load(self.pfile)
                        self.pfile.seek(0)
                except:
                        self.triggers = 0
                        self.pfile = open(self.trigCountFile, mode="wb")
                        self.saveTriggers()

        def saveTriggers(self):
                pickle.dump(self.triggers, self.pfile, -1)
                self.pfile.flush()
                self.pfile.seek(0)

        def resetCounter(self):
                self.triggers = 0
                self.saveTriggers()
                
        def listen(self):
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                        s.bind((HOST, PORT))
                        while True:
                                s.listen()
                                conn, addr = s.accept()
                                with conn:
                                        print("Connected to by " + str(addr))
                                        while(True):
                                                data = conn.recv(1024)
                                                if not data:
                                                        break
                                                print(data)
                                                if(data == b'trigger'):
                                                        print("ok!")
                                                        GPIO.output(26, True)
                                                        time.sleep(.001)
                                                        GPIO.output(26, False)
                                                        self.triggers += 1
                                                        self.saveTriggers()
                                                        conn.sendall(b"ok")
                                                elif(data == b"getTriggerNo"):
                                                        conn.sendall(str(self.triggers).encode())
                                                elif(data == b"resetCounter"):
                                                        self.triggers = 0
                                                        self.saveTriggers()
                                                else:
                                                        conn.sendall(b"no")


sc = SocketTrigger()
try:
        sc.listen()
except:
        sc.pfile.close()
