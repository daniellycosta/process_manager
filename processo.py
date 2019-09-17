'''
 Leds Control Using Process
This code implements 03 process on Beagle Bone.

- The process 01, that have max priority, reads 02 ADCs and 
uses this values for setting the others process priorities.

- The others two child process run a infinite loop that:
runs a task, turns on the respective led using a digital port,
runs a task again and turns the respective led off.

P.S.: Process 01 priority must be higher than the others, to avoid starvation
'''

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
import os

def load():
  cont = 0
  for item in range(100000):
    cont+=1

def childProcessJob(led):
  GPIO.output(led, GPIO.HIGH)
  state=True
  while(True):
    load()
    GPIO.output(led, GPIO.LOW if state else GPIO.HIGH)
    state=not state

def normalizeADC(num):
  return round((num*18)+1) 

#GPIO's
LEDs=["P8_7","P8_8"]

ADCs = ['P9_35','P9_36']

GPIO.setup(LEDs[0], GPIO.OUT)
GPIO.setup(LEDs[1], GPIO.OUT)

ADC.setup()

childrenPIDs = []
ADCValues = [0,0]
os.setpriority(os.PRIO_PROCESS,os.getpid(),0)

try:
  pid = os.fork()

  if(pid == 0):
    #Child 1
    childProcessJob(LEDs[0])
  else:
    #Parent
    childrenPIDs.append(pid)
    pid = os.fork()
    os.setpriority(os.PRIO_PROCESS,childrenPIDs[0],ADCValues[0])
    if(pid == 0):
      #Child 2
      childProcessJob(LEDs[1])
    else:
      #Parent
      childrenPIDs.append(pid)
      os.setpriority(os.PRIO_PROCESS,childrenPIDs[1],ADCValues[1])
      while(True):
        time.sleep(1)
        ADCValues[0] = normalizeADC(ADC.read(ADCs[0]))
        ADCValues[1] = normalizeADC(ADC.read(ADCs[1]))
        ADCValues[0] = normalizeADC(ADC.read(ADCs[0]))
        ADCValues[1] = normalizeADC(ADC.read(ADCs[1]))
        print(ADCValues)
        os.setpriority(os.PRIO_PROCESS,childrenPIDs[0],ADCValues[0])
        os.setpriority(os.PRIO_PROCESS,childrenPIDs[1],ADCValues[1])

except os.error as e:
    print('Error:')
    print (e)
