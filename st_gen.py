import os
import subprocess
import usb

print(os.getcwd())

manta125 = False
manta235 = False
ccs100 = False
PM100 = False
LPR59 = False

# Check for camera
arv_output = str(subprocess.check_output(['arv-tool-0.4', 'control', 'DeviceModelName']))
if(not(arv_output.find('235B') == -1)):
    manta235 = True

if(not(arv_output.find('125B') == -1)):
    manta125B = True

# Check for known USB devices
for bus in usb.busses():
    for dev in bus.devices:
        if(dev.idVendor == 4883 and dev.idProduct == 32882):
            print('Found PM100')
            PM100 = True
        if(dev.idVendor == 4883 and
           (dev.idProduct == 32897 or dev.idProduct == 32896)):
            print('Fount ccs100')
            ccs100 = True


def dump_file_to_file(in_name, out_file):
    with open(in_name, 'r') as in_file:
        input = in_file.read()
        out_file.write(input)


with open('/tmp/st_gen.cmd', 'w') as f:
    dump_file_to_file('/home/dev/git/havards_stuff/st_components/init.txt', f)
    if(manta125):
        dump_file_to_file('/home/dev/git/havards_stuff/st_components/manta125.txt', f)
    if(manta235):
        dump_file_to_file('/home/dev/git/havards_stuff/st_components/manta235.txt', f)
    if(ccs100):
        dump_file_to_file('/home/dev/git/havards_stuff/st_components/ccs100.txt', f)
    if(PM100):
        dump_file_to_file('/home/dev/git/havards_stuff/st_components/PM100.txt', f)
    if(LPR59):
        dump_file_to_file('/home/dev/git/havards_stuff/st_components/LPR59.txt', f)
    dump_file_to_file('/home/dev/git/havards_stuff/st_components/tail.txt', f)
