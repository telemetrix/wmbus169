import RPi.GPIO as GPIO
import time
import serial

from TR50 import TR50http

class WMbus(object):

    def __init__(self, serial_port='/dev/ttyS0'):
        self.ser = serial.Serial(
            port=serial_port,
            baudrate=19200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            timeout=10.0)

        switch_pin = 18
        wakeup_pin = 22  # wybudzenie telita
        reset_pin = 23
        status_pin = 2
        standby_pin = 3
        pdi_pin = 10
        prog_pin = 24

        GPIO.setmode(GPIO.BCM)

        GPIO.setup(switch_pin, GPIO.OUT)
        GPIO.output(switch_pin, GPIO.HIGH)  # LOW = RADIO, HIGH = RS485

        GPIO.setup(wakeup_pin, GPIO.OUT)
        GPIO.output(wakeup_pin, GPIO.HIGH)  # HIGH = wlaczenie telita

        GPIO.setup(reset_pin, GPIO.OUT)
        GPIO.output(reset_pin, GPIO.LOW)

        GPIO.setup(status_pin, GPIO.IN)
        GPIO.add_event_detect(status_pin, GPIO.BOTH)
        # GPIO.add_event_callback(status_pin, callback=pin_callback_status)

        GPIO.setup(standby_pin, GPIO.IN)
        GPIO.add_event_detect(standby_pin, GPIO.BOTH)
        # GPIO.add_event_callback(standby_pin, callback=pin_callback_standby)

        GPIO.setup(pdi_pin, GPIO.OUT)
        GPIO.output(pdi_pin, GPIO.LOW)

        GPIO.setup(prog_pin, GPIO.OUT)
        GPIO.output(prog_pin, GPIO.LOW)

        print('Module RESET ...')
        time.sleep(5)
        GPIO.output(reset_pin, GPIO.HIGH)
        time.sleep(5)

    def __send_atc(self, command, bytes=100, timeout=1, end=b'\r\n'):
        self.ser.flush()
        self.ser.timeout = timeout
        self.ser.write(command + end)
        rcv = self.ser.read(bytes)

        return rcv

        # Switch do COMMAND_MODE

    def COMMAND_MODE(self):
        rcv = self.__send_atc(b'+++', end=b'')
        if rcv.find(b'OK') != -1:
            return (1, rcv)
        else:
            return (-1, rcv)

    def ATV(self):
        rcv = self.__send_atc(b'AT/V', end=b'\r')
        if rcv.find(b'OK') != -1:
            return (1, rcv)
        else:
            return (-1, rcv)



if __name__ == '__main__':

    wmbus169 = WMbus()
    print(wmbus169.COMMAND_MODE())
    print(wmbus169.ATV())

    dwConfig = {
        'endpoint': 'http://api-de.devicewise.com/api',
        'app_id': '0000001',
        # it has to be locked ID value for each logic device. (generating from serial numbers?)
        'app_token': 'hzFldHm60s4vaYzW',
        'thing_key': 'wmbus169_gateway_100'
    }

    tr50http = TR50http.TR50http(dwConfig)

    while 1:
        atv = wmbus169.ATV()
        result = tr50http.execute('log.publish', {'msg': atv[1]})
        print(tr50http.get_response())
        time.sleep(30)




