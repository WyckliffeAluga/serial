# pip install pyserial if not already installed

import serial
import time
import csv
import os

# Set the static name for the sensors and symlink in linux
port1 = "/dev/tty.usbmodem5660931"
baud = 9600
ser1 = serial.Serial(port1, baud, timeout=0.01)
print("Inlet Port Opened")

port2 = "/dev/tty.usbmodem4350051"
ser2 = serial.Serial(port2, baud2, timeout=0.01)
print("Outlet Port Opened")

# File handling
readable_time = time.strftime('%Y-%m-%d_%Hh%Mm%Ss', time.localtime())
filename1 = 'massFlowIn' + readable_time + '.csv'
filename2 = 'massFlowOut + readable_time + '.csv'


# headers
headers = ["massFlowRate[ul/min]"]

with open(filename1, "a") as f:
   writer = csv.writer(f,delimiter=",")
   writer.writerow(['Time'] + headers)
   f.close()

with open(filename2, "a") as f:
   writer = csv.writer(f,delimiter=",")
   writer.writerow(['Time'] + headers)
   f.close()

def teensyWrite(teensy_ser):
   ser = teensy_ser
   ser.write("read_massFlow\r\n".encode("utf-8"))

def teensyRead(ser):

   data = ["-","-"]

   while True:
       try:
           ser_bytes = ser.readline()
           decoded_bytes = ser_bytes[0:len(ser_bytes)-2].decode("utf-8")
           ser_data = decoded_bytes.split()

           print(ser_bytes)
           data[1] = float(ser_data[4])
       except:
           break   
   return data
   
while True:
   try:
       teensyWrite(ser1)
       teensyWrite(ser2)
       
       time.sleep(5)

       data1 = teensyRead(ser1)
       data2 = teensyRead(ser2)

       print('teensy1: ', data1)
       print('teensy2: ', data2)

       readable_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
       with open(filename1, "a") as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow([readable_time] + data1 )
       with open(filename2, "a") as f:
            writer = csv.writer(f,delimiter=",")
            writer.writerow([readable_time] + data2 )

   except Exception as e:
       print(e)
       pass
