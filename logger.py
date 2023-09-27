import serial
import re

#WEIGHTFILE = "C:\weightSerial\it\dados.txt"
WEIGHTFILE = "dados.txt"
TERMINATION_LINE = b'\r' 
SPLIT_PATTERN = re.compile(r'\r\x021[0p] \d{06}')
SPEED_DEFAULT = 9600

with open("config.txt", "r") as fileConfig:
	portNumber = str(fileConfig.read())

serialPort = serial.Serial(portNumber, SPEED_DEFAULT)
serialPort.flushInput()

data = b''
for i in range(25):
    loop = True

    while loop == True:
        byte = serialPort.read(1)
        if byte:
            data += byte
            if data.endswith(TERMINATION_LINE):
                loop = False
                
serialPort.close()

dataDecode = data.decode('utf-8')

weights = SPLIT_PATTERN.findall(dataDecode)

normalizedWeight = [re.search(r'\d{06}', weight).group() for weight in weights]

currentWeight =[]
for weightsString in normalizedWeight:
     currentWeight.append(int(weightsString))

weightSum = sum(currentWeight)
quantity = len(currentWeight)

average = 0
if weightSum > 0:
    average = int(weightSum / quantity)

with open(WEIGHTFILE, "w") as file: 
    file.write(str(average))
    
print(average)
