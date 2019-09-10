import time
import serial
import sys
import os
import sty
from sty import fg, bg, ef, rs


class ATEL(object):

    def __init__(self, serial_port='/dev/tty.usbserial'):
        self.ser = serial.Serial(
            port=serial_port,
            baudrate=115200,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            timeout=10.0)

        os.system('clear')
        print()
        print(fg.red + '    ***  PYSENSE LTE-M 450 MHZ COVERAGE TESTER  ***    ' + fg.rs)
        print()
        print(bg.blue + fg.black + '  Signal Quality: ' + bg.rs, end=' ')
        time.sleep(5)

    def __send_atc(self, command, bytes=100, timeout=0.5, end=b'\r\n'):
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

    def AT(self):
        rcv = self.__send_atc(b'AT')
        if rcv.find(b'OK') != -1:
            return (1, rcv)
        else:
            return (-1, rcv)

    def MEAS_8(self):
        rcv = self.__send_atc(b'AT%MEAS="8"')
        if rcv.find(b'OK') != -1:
            return (1, rcv)
        else:
            return (-1, rcv)

    def MEAS_95(self):
        rcv = self.__send_atc(b'AT%MEAS="95"', bytes=400)
        if rcv.find(b'OK') != -1:
            return (1, rcv)
        else:
            return (-1, rcv)

    def CGPADDR_1(self):
        rcv = self.__send_atc(b'AT+CGPADDR=1', bytes=100)
        if rcv.find(b'OK') != -1:
            return (1, rcv)
        else:
            return (-1, rcv)


if __name__ == '__main__':

    lm66 = ATEL()

    while True:
        x = lm66.AT()
        if x[0] == 1:
            #print(x)
            print('### ATEL LM66 UART interface activated ')
            break
        else:
            #print(x)
            time.sleep(2)
            continue

    while True:
        x = lm66.MEAS_8()
        y = lm66.MEAS_95()
        z = lm66.CGPADDR_1()

        if x[0] == 1 and y[0] == 1 and z[0] == 1:
            os.system('clear')
            print()
            print(fg.red + '    ***  PYSENSE LTE-M 450 MHZ COVERAGE TESTER  ***    ' + fg.rs)
            print()

            print(bg.da_red + fg.black + '  Network: ' + bg.rs, end=' ')
            print('Ericsson LTE-M 450 MHz (B31)')

            print(bg.da_yellow + fg.black + '  APN Context: ' + bg.rs, end=' ')
            print('gold')

            print(bg.da_magenta + fg.black + '  IPv4 Address: ' + bg.rs, end=' ')
            print(z[1])

            print(bg.da_blue + fg.black + '  Signal Quality: ' + bg.rs, end=' ')
            print(x[1])

            print(bg.da_green + fg.black + '  ECID Measurements: ' + bg.rs, end=' ')
            print(y[1])

            print()
            print(fg.red + '    ***  WWW.PYSENSE.COM  ***    ' + fg.rs)
            print()








