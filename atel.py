import time
import serial

class ATEL(object):

    def __init__(self, serial_port='/dev/ttUSB0'):
        self.ser = serial.Serial(
            port=serial_port,
            baudrate=11500,
            bytesize=serial.EIGHTBITS,
            parity=serial.PARITY_NONE,
            timeout=10.0)

        print('### ATEL LM66 Module Activated ')
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

    def ATI(self):
        rcv = self.__send_atc(b'ATI', end=b'\r')
        if rcv.find(b'OK') != -1:
            return (1, rcv)
        else:
            return (-1, rcv)


if __name__ == '__main__':

    atelLM66 = ATEL();
    print(atelLM66.ATI()[1])
