'''
Projeto2.2 - Controle de Leds
Implemente 03 processos na Beagle Bone (P1,P2,P3).

- Processo P1, com alta prioridade, le 02 ADCs a cada segundo.
Use esses valores para setar a prioridade de P2 e P3.
A prioridade de P1 deve ser sempre maior que a de P2 e P3, para nao haver starvation.

- Processos P2 e P3: ficam num loop infinito com a seguinte execucao:
  - executa uma carga.
  - acende o Led respectivo (Led 1 ou Led2), via porta digital.
  - executa uma carga.
  - apaga o Led respectivo (Led 1 ou Led2), via porta digital.
'''

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
import os

def carga():
  cont = 0
  for item in range(100000):
    cont+=1

def childProcessJob(led):
  GPIO.output(led, GPIO.HIGH)
  state=True
  while(True):
    carga()
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
    #Filho 1
    childProcessJob(LEDs[0])
  else:
    #Pai
    childrenPIDs.append(pid)
    pid = os.fork()
    os.setpriority(os.PRIO_PROCESS,childrenPIDs[0],ADCValues[0])
    if(pid == 0):
      #Filho 2
      childProcessJob(LEDs[1])
    else:
      #Pai
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
    print('Erro:')
    print (e)
