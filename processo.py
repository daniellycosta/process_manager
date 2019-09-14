''' Projeto2.2 - Controle de Leds
Implemente 03 processos na Beagle Bone (P1,P2,P3).

- Processo P1, com alta prioridade, lê 02 ADCs a cada segundo.
Use esses valores para setar a prioridade de P2 e P3.
A prioridade de P1 deve ser sempremaior que a de P2 e P3, para não haver starvation.

- Processos P2 e P3: ficam num loop infinito com a seguinte execução:
  - executa uma carga.
  -  acende o Led respectivo (Led 1 ou Led2), via porta digital.
  - executa uma carga.
  -  apaga o Led respectivo (Led 1 ou Led2), via porta digital. '''

import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import time
import os


def get_priority_values(valueArrays):
  #converter os valores do adc (0-1) para uma prioridade...

#GPIO's
l0 = "P8_7"
l1 = "P8_8"


adc1 = 'P9_35'
adc2 = 'P9_36'

GPIO.setup(l0, GPIO.OUT)
GPIO.setup(l1, GPIO.OUT)

ADC.setup()

pid_pai = -1
pid_filhos = []
adcValues = [0,0]
priorities = [0,0]

try:
  pid = os.fork()

  if(pid == 0): #Filho
    pid_filho.append(os.getpid())
    GPIO.output(l0, GPIO.HIGH)
    #carga?
    GPIO.output(l0, GPIO.LOW)
  else: #Pai
    pid_pai = os.getpid()
    pid = os.fork()
    if(pid == 0): #Filho 2
      pid_filhos.append(os.getpid())
      GPIO.output(l1, GPIO.HIGH)
      #carga?
      GPIO.output(l1, GPIO.LOW)
    else:#Pai
       os.setpriority(PRIO_PROCESS,pid_pai,1)
       os.setpriority(PRIO_PROCESS,pid_filhos[0],5)
       os.setpriority(PRIO_PROCESS,pid_filhos[0],5)
      while(True):
        time.sleep(1)
        adcValues[0] = ADC.read(adc1)
        adcValues[1] = ADC.read(adc2)
        priorities = get_priority_values(adcValues)
        os.setpriority(PRIO_PROCESS,pid_filhos[0],priorities[0])
        os.setpriority(PRIO_PROCESS,pid_filhos[0],priorities[1])

except os.error as e:
    print('Erro:')
    print e
