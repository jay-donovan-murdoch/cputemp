"""Copyright (c) 2019, Douglas Otwell
Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
Modified by Jay Donovan 2020
"""
#!/usr/bin/env python3

#Python GATT server example for the Raspberry Pi
#Copyright (c) 2019, Douglas Otwell
#Distributed under the MIT license http://opensource.org/licenses/MIT


#BLE requiremetns
import dbus

from advertisement import Advertisement
from service import Application, Service, Characteristic, Descriptor

#GPIO Access
import RPi.GPIO as GPIO


GATT_CHRC_IFACE = "org.bluez.GattCharacteristic1"
NOTIFY_TIMEOUT = 5000

class LEDControlAdvertisement(Advertisement):
    def __init__(self, index):
        Advertisement.__init__(self, index, "peripheral")
        self.add_local_name("IoT Murdoch")
        self.include_tx_power = True

class BLEService(Service):
    MAIN_SVC_UUID = "00000001-710e-4a5b-8d75-3e5b444bc3cf"

    def __init__(self, index):

        Service.__init__(self, index, self.MAIN_SVC_UUID, True)
        self.add_characteristic(LEDControl(self))


class LEDControl(Characteristic):
    UNIT_CHARACTERISTIC_UUID = "00000002-710e-4a5b-8d75-3e5b444bc3cf"

    def __init__(self, service):
        Characteristic.__init__(
                self, self.UNIT_CHARACTERISTIC_UUID,
                ["write"], service)
        #self.add_descriptor(UnitDescriptor(self))

    def WriteValue(self, value, options):
        output = bytes(value).decode()
        if output == "0":
            print('turning LED off')
            GPIO.output(26,GPIO.LOW)
        elif output == "1":
            print('turning LED on')
            GPIO.output(26,GPIO.HIGH)
        else:
            print('try again')
            print(output)


#GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(26,GPIO.OUT)

app = Application()
app.add_service(BLEService(0))
app.register()

adv = LEDControlAdvertisement(0)
adv.register()

try:
    app.run()
except KeyboardInterrupt:
    app.quit()
