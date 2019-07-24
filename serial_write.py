# /usr/bin/env python 
import time 
import serial 

ser = serial.Serial( 
  port = "/dev/ttyACM1", 
  baudrate = 9600, 
  parity = serial.PARITY_NONE, 
  stopbits = serial.STOPBITS_OBNE, 
  bytesize = serial.EIGHTBITS, 
  timeout = 0
  )
  
  counter = 0 
  
  while 1: 
    ser.write('Write counter: %d \n'%(counter)) 
    time.sleep(1) 
    counter+ = 1