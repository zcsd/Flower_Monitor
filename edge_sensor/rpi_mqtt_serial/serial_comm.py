import serial

class SerialComm:
    def __init__(self):
        # usb port connection, /dev/ttyACM0
        self.ser = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
        self.ser.reset_input_buffer()
        self.ser.readline()
        self.ser.readline()
        print("Serial communication initialized.")

    def get_soil_moisture(self):
        self.ser.write(b"sm\n")
        line = self.ser.readline().decode('utf-8').rstrip() # sm_1001
        mo = line.split("_")[1]
        return mo

    def get_temperature_humidity(self):
        self.ser.write(b"th\n")
        line = self.ser.readline().decode('utf-8').rstrip() # t_25.80_h_57.70
        te = line.split("_")[1]
        hu = line.split("_")[3]
        return [te[:-1], hu[:-1]] # [:-1] remove last char

    def get_illuminance(self):
        self.ser.write(b"lu\n")
        line = self.ser.readline().decode('utf-8').rstrip() # lu_4704.17
        lu  = line.split("_")[1]
        return lu[:-1]
