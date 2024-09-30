import serial
import serial.tools.list_ports
from pynput.keyboard import Key, Controller
import time
keyboard = Controller()

print('Searching serial port...')
ports = serial.tools.list_ports.comports(include_links=False)
for port in ports :
    print('Find port '+ port.device)
serial_port = serial.Serial()
serial_port.baudrate = 115200
serial_port.port = port.device
serial_port.set_buffer_size(16) # reduces the size of the input buffer
serial_port.timeout = 1
error = False
time.sleep(2) # gives you time to open the desired target for the inputs
try:
    serial_port.open()
except:
    error = True

if not serial_port.is_open or error:
    print("Something went wrong!")
    time.sleep(1)
    exit()

while 1:
    try:
        serial_port.reset_input_buffer()
        # _____________________________ Input Buffer Full _____________________________
        if serial_port.in_waiting!=0:
            key = serial_port.read().decode('ascii').strip('\n').strip('\r')
            keyboard.press(key)
            time.sleep(0.1)
        # _____________________________________________________________________________
        # _____________________________ Input Buffer Empty ____________________________
        elif serial_port.in_waiting==0:
            if key == "a" or key == "d" or key == "w" or key == "s" or key == " ":
                keyboard.release(key) # key is released only if it is either "a","d","w","s" or spacebar
                key = "" # sets key to be null in order not to execute the previous 
                         # command line the next cycle iteration
        # _____________________________________________________________________________
    except:
        pass