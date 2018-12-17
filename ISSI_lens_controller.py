import socket
import argparse
import time


class EF_Controller(object):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def send_message(self, message):
        print("Send: " + message)
        self.sock.sendto(message.encode(), (self.udp_ip, self.udp_port))

    def read_line(self):
        data, addr = self.sock.recvfrom(1024)
        print('Read: ' + data.decode())
        return(data.decode())

    def read_and_split_line(self, intify=True):
        data = self.read_line()
        start_pos = data.index('=') + 1
        dlist = data[start_pos:].split(',')
        if(intify):
            dlist = list(map(int, dlist))
        return(dlist)

    def ping_and_decode(self):
        self.last_ping = time.time()
        self.send_message('ping')
        dlist = self.read_and_split_line()
        self.zRange_min = dlist[0]
        self.zRange_max = dlist[1]
        dlist = self.read_and_split_line()
        self.fRange_min = dlist[0]
        self.fRange_max = dlist[1]
        dlist = self.read_and_split_line(intify=False)
        self.aRange_min = dlist[0]
        self.aRange_max = dlist[1]
        dlist = self.read_and_split_line(intify=False)
        self.focal_length = int(dlist[0])
        self.focus_pos = int(dlist[1])
        self.aperture = dlist[2]
        dlist = self.read_and_split_line()
        self.can_focus = dlist[0]
        dlist = self.read_and_split_line()
        self.can_stabilize = dlist[0]
        dlist = self.read_and_split_line()
        self.stabilization_active = dlist[0]

    def __init__(self, udp_ip="192.168.0.250", udp_port=1339):
        self.udp_ip = udp_ip
        self.udp_port = udp_port
        self.ping_and_decode()
        self.send_message('getLens')
        self.lens = self.read_line()

    def set_focus(self, focus):
        print('Try to set focus!')
        fint = int(focus)
        if (fint < self.fRange_min or fint > self.fRange_max):
            raise Exception('focus out of range')
        else:
            self.send_message('setFocus=' + str(fint))
            dlist = self.read_and_split_line()
            self.focus_pos = dlist[0]
            self.read_line()

    def set_aperture(self, str_aperture):
        print('Try to set aper!')
        legal_apers = ['1.0', '1.1', '1.2', '1.3', '1.4', '1.6', '1.8', '2.0', '2.2', '2.5', '2.8', '3.2', '3.5', '4.0', '4.5', '5.0', '5.6', '6.3', '7.1', '8.0', '9.0', '10', '11', '13', '14', '16', '18', '20', '22', '25', '29', '32', '36', '40', '45', '51', '57', '64', '72', '80', '90']
        try:
            legal_apers.index(str_aperture)
            print('asdf!')
            self.send_message('setAper='+str_aperture)
            dlist = self.read_and_split_line(intify=False)
            self.aperture = dlist[0]
        except ValueError:
            raise Exception('str_aperture should be in ' + str(legal_apers))
    
    def get_lens(self):
        self.send_message('getLens')
        self.lens = self.read_line()
        return(self.lens)

    def get_focal_length(self):
        if(time.time() - self.last_ping) > 1.0:
            self.ping_and_decode()
        return(self.focal_length)

    def get_aper(self):
        if(time.time() - self.last_ping) > 1.0:
            self.ping_and_decode()
        return(self.aperture)

    def set_ip(self):
        self.send_message('ChangeIP=192.168.0.250')


print(__name__)
namemain = (__name__ == '__main__')
if namemain:
    parser = argparse.ArgumentParser(description='Set aperture or focus of canon lens')
    parser.add_argument('-f', '--focus', type=int, default=-1, help="Set focus")
    parser.add_argument('-a', '--aper', default="-1", help="Set aperture")
    args = parser.parse_args()

    efc = EF_Controller()
    print('Hello')
    if(args.focus > 0):
        print('Setting focus')
        efc.set_focus(args.focus)
    if(args.aper != "-1"):
        print('Setting aper')
        efc.set_aperture(args.aper)
