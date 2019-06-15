from pybleno import *
import sys
import signal
from EchoCharacteristic import *

print('bleno - echo');

def StateOn(bleno):
    bleno.on('stateChange', onStateChange)
    bleno.on('advertisingStart', onAdvertisingStart)
    bleno.start()
    print ('Hit <ENTER> to disconnect')
def SatateOff(bleno):
    bleno.stopAdvertising()
    bleno.disconnect()

def onStateChange(state):
   print('on -> stateChange: ' + state);

   if (state == 'poweredOn'):
     bleno.startAdvertising('Wallet', ['ec00'])
   else:
     bleno.stopAdvertising();

def onAdvertisingStart(error):
    print('on -> advertisingStart: ' + ('error ' + error if error else 'success'));

    if not error:
        bleno.setServices([
            BlenoPrimaryService({
                'uuid': 'ec00',
                'characteristics': [
                    EchoCharacteristic('ec0F')
                    ]
            })
        ])
bleno = Bleno()
StateOn(bleno)
if (sys.version_info > (3, 0)):
    input()
else:
    raw_input()
SatateOff(bleno)
