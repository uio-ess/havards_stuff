#!/bin/sh
exec /home/haavagj/git/StreamDevice/bin/linux-x86_64/streamApp $0
dbLoadDatabase "/home/haavagj/git/StreamDevice/dbd/streamApp.dbd"
streamApp_registerRecordDeviceDriver

#where can protocols be located?
epicsEnvSet "STREAM_PROTOCOL_PATH", ".:protocols:../protocols/"

#setup the hardware

drvAsynIPPortConfigure "L0","192.168.0.250:1339 UDP*"
#vxi11Configure "L0","gpib-hostname-or-ip",0,0.0,"gpib0"

#load the records
dbLoadRecords "canoneos.db","P=DZ,BUS=L0 28"

#log debug output to file
#streamSetLogfile StreamDebug.log

iocInit

#enable debug output
#var streamDebug 1
