import time, sys, signal, atexit
import pyupm_hm11 as upmHm11
# Instantiate a HM11 BLE Module on UART 0
my_ble_obj = upmHm11.HM11(0)
## Exit handlers ##
# This stops python from printing a stacktrace when you hit control-C
def SIGINTHandler(signum, frame):
    raise SystemExit

# This function lets you run code on exit,
# including functions from my_ble_obj
def exitHandler():
    print "Exiting"
    sys.exit(0)
    
# Register exit handlers
atexit.register(exitHandler)
signal.signal(signal.SIGINT, SIGINTHandler)
bufferLength = 256

# make sure port is initialized properly. 9600 baud is the default.
if (not my_ble_obj.setupTty(upmHm11.cvar.int_B9600)):
    print "Failed to setup tty port parameters"
    sys.exit(0)
usageStr = ("Usage:\n"
"Pass a commandline argument (any argument) to this program\n"
"to query the radio configuration and output it.  NOTE: the\n"
"radio must be in CONFIG mode for this to work.\n\n"
"Running this program without arguments will simpltransmit\n"
"'Hello World!' every second, and output any data received from\n"
"another radio.\n\n")
print usageStr
# simple helper function to send a command and wait for a response
def sendCommand(bleObj, cmd):
    bleBuffer = upmHm11.charArray(bufferLength)
    bleObj.writeData(cmd, len(cmd))
    # wait up to 1 second
    if (bleObj.dataAvailable(1000)):
        bleObj.readData(bleBuffer, bufferLength)
        bleData = ""
        # read only the number of characters
        # specified by myGPSSensor.readData
        for x in range(0, bufferLength):
            if (bleBuffer.__getitem__(x) == '\0'):
                break
            else:
                bleData += bleBuffer.__getitem__(x)
        print bleData
    else:
        print "Timed out waiting for response"

if (len(sys.argv) > 1):
    print "Sending command line argument (" + sys.argv[1] + ")..."
    sendCommand(my_ble_obj, sys.argv[1])
else:
    # query the module address
    addr = "AT+ADDR?";
    print "Querying module address (" + addr + ")..."
    sendCommand(my_ble_obj, addr)
    time.sleep(1)
    # query the module address
    pin = "AT+PASS?";
    print "Querying module PIN (" + pin + ")..."
    sendCommand(my_ble_obj, pin)