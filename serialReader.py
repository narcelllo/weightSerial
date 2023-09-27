from tkinter import Tk, ttk, Label, Button
import serial, serial.tools.list_ports as SerialPortsLister

def listSerialPorts():
    ports = SerialPortsLister.comports()
    return [port.device for port in ports]

def readerSerial():
    WEIGHTFILEDECODE = "readerSerialDecode.txt"
    WEIGHTFILEDATA = "readerSerialData.txt"
    SPEED_DEFAULT = 9600
    portNumber = ttkSerialComboBox.get()

    serialPort = serial.Serial(portNumber, SPEED_DEFAULT)
    serialPort.flushInput()

    data = b''

    for i in range(520):

        byte = serialPort.read(1)
        if byte:
            data += byte
                
                    
    serialPort.close()
    
    dataDecode = data.decode('utf-8')

    with open(WEIGHTFILEDATA, "w") as file: 
        file.write(str(data))

    with open(WEIGHTFILEDECODE, "w") as file: 
        file.write(str(dataDecode))
    canvas.destroy()
    
    canvasCallBack = Tk()
    canvasCallBack.title("Serial configuration")
    canvasCallBack.geometry("300x150")

    ttkLabelSerialComboBox = Label(canvasCallBack, text = f"{WEIGHTFILEDECODE} and {WEIGHTFILEDATA} \n Successful configuration.")
    ttkOkButton = Button(canvasCallBack, text = "    Ok    ", command = canvasCallBack.destroy)
    ttkLabelCentralize = Label(canvasCallBack, text = "        ")
    ttkLabelSerialComboBox.grid(column = 1, row = 1)
    ttkLabelCentralize.grid(column = 0, row = 0)
    ttkOkButton.grid(column = 1, row = 2)

    canvasCallBack.mainloop()

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
    ttkSaveButton = Button(canvas, text = "   Save   ", command = readerSerial)
    ttkSaveButton.grid(column = 2, row = 5, padx = 5, pady = 5)

canvas.mainloop()
