import RPi.GPIO as GPIO
import time
import smbus
import ctypes
import pickle

class MoveStage(object):
    count_file = 'moveCounter'

    def __init__(self):
        # Set up pins
        GPIO.setmode(GPIO.BOARD)
        self.outpin = 37
        self.inpin = 35
        GPIO.setup(self.inpin,GPIO.OUT)
        GPIO.output(self.inpin, False)
        GPIO.setup(self.outpin,GPIO.OUT)
        GPIO.output(self.outpin, False)
        
        # Set up I2C
        self.bus = smbus.SMBus(1)
        self.address = 0x40
        self.bus.write_word_data(self.address, 5, 300)

        # Set up actuation count
        try:
            self.pfile = open(self.count_file, mode='r+b')
            self.counter = pickle.load(self.pfile)
            self.pfile.seek(0)
        except:
            self.counter = 0
            self.pfile = open(self.count_file, mode='wb')
            self.save_count()

    def save_count(self):
        pickle.dump(self.counter, self.pfile, -1)
        self.pfile.flush()
        self.pfile.seek(0)
        
    def poll_i2c(self, current_limit):
        while(True):
            time.sleep(0.1)
            cur = self.bus.read_word_data(self.address, 4)
            lsb = ctypes.c_byte(cur & 0b0000000011111111).value
            print('Polling shows LSB ' + str(lsb))
            if(current_limit(lsb)):
                break
    
    def move(self, pin, current_limit):
        GPIO.output(pin, True)
        self.poll_i2c(current_limit)
        GPIO.output(pin, False)

    def extend(self):
        print('extending!')
        self.move(self.inpin, lambda x: abs(x) < 3)
        print('STOP!')
    
    def retract(self):
        print('Retracting')
        self.move(self.outpin, lambda x: abs(x) > 127)
        print('STOP!')

    def n_moves(self, n):
        for x in range(n):
            print('Move ' + str(self.counter))
            self.retract()
            self.extend()
            self.counter += 1
            self.save_count()
        

ms = MoveStage()
ms.n_moves(3000)
    
