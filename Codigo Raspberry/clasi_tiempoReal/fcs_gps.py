import serial
import time
import string
import pynmea2


def getPosGps():
        parar = True
        pos = []
        while parar:
                port="/dev/ttyUSB0"
                ser=serial.Serial(port, baudrate=9600, timeout=0.5)
                dataout = pynmea2.NMEAStreamReader()
                newdata=ser.readline()
                #print(newdata[2:8])
                if newdata[0:6] == b'$GPRMC':
                        aux = str(newdata)[2:-5] #para quedarnos con la parte del strin>
                        newmsg=pynmea2.parse(aux)
                        lat=newmsg.latitude
                        lng=newmsg.longitude
                        gps = "Latitude=" + str(lat) + "and Longitude=" + str(lng)
                        print(gps)
                        parar = False
                        pos = [lat,lng]
        return pos
#----------------------------------------------------------
#posic=getPosGps()
#print(str(posic[0])+str(posic[1]))
