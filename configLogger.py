import re
from tkinter import Tk, ttk, Label, Button
import serial, serial.tools.list_ports as SerialPortsLister

def listSerialPorts():
    ports = SerialPortsLister.comports()
    return [port.device for port in ports]

def saveConfiguration():
    CONFIGURATION = "C:\serial\it\config.txt"
    
    com = ttkSerialComboBox.get()

    with open(CONFIGURATION,  "w") as file: 
        file.write(com)
    
    canvas.destroy() 

    canvasCallBack = Tk()
    canvasCallBack.title("Serial configuration")
    canvasCallBack.geometry("250x150")

    ttkLabelSerialComboBox = Label(canvasCallBack, text = f"{com} Successful configuration.")
    ttkOkButton = Button(canvasCallBack, text = "    Ok    ", command = canvasCallBack.destroy)
    ttkLabelCentralize = Label(canvasCallBack, text = "              ")
    ttkLabelSerialComboBox.grid(column = 1, row = 1)
    ttkLabelCentralize.grid(column = 0, row = 0)
    ttkOkButton.grid(column = 1, row = 2)

    canvasCallBack.mainloop()

def serialPortTester():
    TERMINATION_LINE = b'\r'
    SPLIT_PATTERN = re.compile(r'\r\x021[0p] \d{06}') 
    SPEED_DEFAULT = 9600
    portNumber = str(ttkSerialComboBox.get())

    serialPort = serial.Serial(portNumber, SPEED_DEFAULT)
    serialPort.flushInput()

    data = b''
    for i in range(2):
        loop = True

        while loop == True:
            byte = serialPort.read(1)
            if byte:
                data += byte
                if data.endswith(TERMINATION_LINE):
                    loop = False

    dataDecode = data.decode('utf-8')
    
    weights = SPLIT_PATTERN.findall(dataDecode)
    
    normalizedWeight = [re.search(r'\d{06}', weight).group() for weight in weights]
    
    ttkLabelTester.config(text = f"Weight: {normalizedWeight}")

serialPorts = listSerialPorts()    

canvas = Tk()
canvas.title("Serial configuration")
canvas.geometry("300x200")

ttkLabelSerialComboBox = Label(canvas, text = "COM")
ttkLabelCentralize = Label(canvas, text = "              ")
ttkLabelSerialComboBox.grid(column = 1, row = 3)
ttkLabelCentralize.grid(column = 0, row = 0)

# Mocked values for testing
#serialPorts = ["COM1", "COM2", "COM3", "COM4", "COM5", "COM6"]

ttkSerialComboBox = ttk.Combobox(canvas, values = serialPorts)
ttkSerialComboBox.set("Disconnected")
ttkCancelButton = Button(canvas, text = " Cancel ", command = canvas.destroy) 

ttkSerialComboBox.grid(column = 2, row = 3)
ttkCancelButton.grid(column = 2, row = 4, padx = 5, pady = 5)

if serialPorts:
    ttkSerialComboBox.set("--")
    ttkSaveButton = Button(canvas, text = "   Save   ", command = saveConfiguration)
    ttkTesterButton = Button(canvas, text = "   Teste   ", command = serialPortTester)
    ttkLabelTester = Label(text = "")    
    ttkSaveButton.grid(column = 2, row = 5, padx = 5, pady = 5)
    ttkTesterButton.grid(column = 2, row = 8, padx = 5, pady = 5)
    ttkLabelTester.grid(column = 2, row = 9, padx = 5, pady = 5)

canvas.mainloop()
