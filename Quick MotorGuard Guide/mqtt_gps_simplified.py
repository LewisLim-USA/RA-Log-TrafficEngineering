import json, re, threading, smbus2, math, serial, time, pynmea2, os

# Coded and Enhanced by Steve Teoh (c) 2025 All rights reserved.
# --------------------------------------------------------------
# Hardware Used:
# RaspberryPi - Pi 3 B+
# GPS/GNSS    - SIM7670SA GNSS 
# MQTT        - SIM A7670SA 4G LTE transceiver with 5G/4G sim card.Caution: Note that the AT commands are very specific and hence
#               it cannot be universally applied to other tranceiver models such as the SIM7000E!
# Motion+Temp - MPU6050 Gyro
# 
# This is a simple integrated program that will send telemetry data from MPU6050 sensor via LTE to MQTT Broker.
# You can use any MQTT broker for testing. Here I am using test.mosquitto.org for testing without cert validation.
#
# Steps to Test the program
# 1. Ensure all libraries above are installed using pip3 on your RPi
# 2. Run this Python code on a RPi, with MPU 6050 and SIM A7670SA installed (sensor node). This node will be publishing MQTT messages
# 3. Create a test client in any platform, or use an online client such as https://testclient-cloud.mqtt.cool/ to subscribe to a topic 
# 4. From the client, connect to the broker e.g. test.mosquitto.org, then subscribe to the topic, i.e. Mybike/A7670SA
#    The name of the topic can be changed to anything suitable for your own use.    

ID = "Mybike1"
ModuleID = "A7670SA"
sub = ID + "/" + ModuleID             
pub = ID + "/" + ModuleID     

mqtt_server = 'test.mosquitto.org'     # "mqtt.waveshare.cloud", "test.mosquitto.org", "broker.mqtt.cool", "broker.hivemq.com", "iot.eclipse.org",
                                       # default mqtt is on tcp port 1883
#some MPU6050 Registers and their Address
PWR_MGMT_1   = 0x6B
SMPLRT_DIV   = 0x19
CONFIG       = 0x1A
GYRO_CONFIG  = 0x1B
INT_ENABLE   = 0x38
ACCEL_XOUT_H = 0x3B
ACCEL_YOUT_H = 0x3D
ACCEL_ZOUT_H = 0x3F
GYRO_XOUT_H  = 0x43
GYRO_YOUT_H  = 0x45
GYRO_ZOUT_H  = 0x47


bus = smbus2.SMBus(1)    # or bus = smbus.SMBus(0) for older version boards
Device_Address = 0x68   # MPU6050 device address
TEMP_OUT_REG = 0x41

def MPU_Init():
    #write to sample rate register
    bus.write_byte_data(Device_Address, SMPLRT_DIV, 7)
    #Write to power management register
    bus.write_byte_data(Device_Address, PWR_MGMT_1, 1)
    #Write to Configuration register
    bus.write_byte_data(Device_Address, CONFIG, 0)
    #Write to Gyro configuration register
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 24)
    #Write to interrupt enable register
    bus.write_byte_data(Device_Address, INT_ENABLE, 1)
    
def read_raw_data(addr):
    #Accelero and Gyro value are 16-bit
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)

    #concatenate higher and lower value
    value = ((high << 8) | low)
    
    #to get signed value from mpu6050
    if(value > 32768):
            value = value - 65536
    return value

def pitch(x, y, z):
    p_angle = - (math.atan2(x, math.sqrt(y*y + z*z))*180) / math.pi       # formula added by Steve
    return p_angle

def roll(y,z):
    a_angle = (math.atan2(y, z)*180.0) / math.pi                          # formula added by Steve
    return a_angle

def yaw(x,z):
    y_angle = 180 * math.atan(z / math.sqrt(x * x + z * z)) / math.pi     # formula added by Steve
    return y_angle

def readSensorData():
    #Read Accelerometer raw value
    acc_x = read_raw_data(ACCEL_XOUT_H)
    acc_y = read_raw_data(ACCEL_YOUT_H)
    acc_z = read_raw_data(ACCEL_ZOUT_H)

    #Read Gyroscope raw value
    gyro_x = read_raw_data(GYRO_XOUT_H)
    gyro_y = read_raw_data(GYRO_YOUT_H)
    gyro_z = read_raw_data(GYRO_ZOUT_H)

    #Full scale range +/- 250 degree/C as per sensitivity scale factor
    Ax = acc_x/16384.0
    Ay = acc_y/16384.0
    Az = acc_z/16384.0
    Gx = gyro_x/131.0
    Gy = gyro_y/131.0
    Gz = gyro_z/131.0
    Temp = read_temperature()
    return Ax,Ay,Az,Gx,Gy,Gz,Temp    # returns a tuple of values

def read_temperature():
    try:                                                            # modified by Steve
        high = bus.read_byte_data(Device_Address, TEMP_OUT_REG)
        low =   bus.read_byte_data(Device_Address, TEMP_OUT_REG)
        value = (high << 8) + low
        if (value >= 0x8000):                                       # need to have this!
            value= -((65535 - value) +1)
        temperature = (value / 340.0) + 36.53 # Convert F to C
        return temperature
    except Exception as e:
        print (f'Error reading temperature: {e}')
        return None
    
def getClock():
    res = os.popen('sudo hwclock -r').readline().replace("'C\n", "")
    # Use only if you have an RTC (e.g. PCF8543) aka hardware clock installed on your board.
    # To overcome situation where GPS UTC time signal is not available.
    return res

#---------------------------------------------------------------------------------------

# AT Command Class
class AT:
      # GPS output avaiable at /dev/ttyAMA0. Control port is /dev/ttyUSB1
    def __init__(self, port='/dev/ttyUSB1', gpsport='/dev/ttyAMA0', baud_rate=115200):
        self.port = port
        self.gpsport = gpsport
        self.baud_rate = baud_rate
        self.ser = serial.Serial(self.port, self.baud_rate, timeout=1)
        self.ser2 = serial.Serial(self.gpsport, self.baud_rate, timeout=1)
        self.initialize_gnss()
        self.destory_mqtt_init()

    def open_serial_connection(self):
        try:
            return self.send_at_command('AT', True)[1].decode('utf-8').strip() == "OK"
        except serial.SerialException as e:
            raise Exception(f"Error opening serial connection: {e}")

    def open_serial2_connection(self):        
        try:
           return self.send_gps_at_command('AT', True)[1].decode('utf-8').strip() == "OK"
        except serial.SerialException as e:
            raise Exception(f"Error opening serial2 connection: {e}")
        
    def destory_mqtt_init(self):
        try:
            self.send_at_command('AT+CMQTTDISC=0,120', True)
            self.send_at_command('AT+CMQTTREL=0', True)
            self.send_at_command('AT+CMQTTSTOP', True)
        except serial.SerialException as e:
            raise Exception(f"Error initializing MQTT: {e}")

    def send_at_command(self, command, wait_for_response=False):
        try:
            encoded_command = command.encode('utf-8') + b'\r\n'
            self.ser.write(encoded_command)
            if wait_for_response:
                print(f"Sent command: {command}")
                response = self.ser.readlines()
                if len(response) > 1:
                   print(f"Response: {response[1].decode('utf-8').strip()}")
                return response
            else:
                time.sleep(0.5)
                return None
        except serial.SerialException as e:
            raise Exception(f"Error sending AT command: {e}")
        
    def init_mqtt(self):
        self.send_at_command('AT+CMQTTSTART', True)  # START MQTT
        self.send_at_command(f'AT+CMQTTACCQ=0,"{ID}",0', True)    
        res = self.send_at_command(f'AT+CMQTTCONNECT=0,"tcp://{mqtt_server}",80,1', True)[3].decode('utf-8').strip()   # connection may fail if server is busy. Just rerun it again.
        status = int(res.split("+CMQTTCONNECT: 0,")[1])
        if status != 0:
            raise Exception(f"Error MQTT Response:{status}")
        else:
            print(f"MQTT Server: {mqtt_server} Connect Successful!")
            return True

    def publish_message(self, message):
        self.send_at_command(f'AT+CMQTTTOPIC=0,{len(pub)}')
        self.send_at_command(f'{pub}')
        self.send_at_command(f'AT+CMQTTPAYLOAD=0,{len(message)}')
        self.send_at_command(f'{message}')
        self.send_at_command('AT+CMQTTPUB=0,0,60')

    def subscribe_message(self):
        self.send_at_command(f'AT+CMQTTSUB=0,{len(sub)},1', True)
        self.send_at_command(f'{sub}', True)

    def subscribe_messages(self):
        while True:
            response = self.ser.readline().decode("utf-8")
            # print(response,end='')
            if response.startswith('+CMQTTRXPAYLOAD:'):
                next_line = self.ser.readline().decode('utf-8')
                print("Subscribe Message:", json.loads(next_line), end='\n')

    def start_subscribe_thread(self):
        self.thread_response_stop_flag = threading.Event()
        thread_response = threading.Thread(target=self.subscribe_messages)
        thread_response.daemon = True
        thread_response.start()

    def destroy(self):
        if hasattr(self, 'thread_response'):
            print("Destroying thread response...")
            self.thread_response_stop_flag.set()
        self.destory_mqtt_init()
        self.ser.close()
        
    # GPS/GNSS
    # ---------------------------------------------------------------------
    def send_gps_at_command(self, command, wait_for_response=True):
        try:
            encoded_command = command.encode('utf-8') + b'\r\n'
            print(f"Sent GPS command: {command}")
            self.ser2.write(encoded_command)
            
            if wait_for_response:
                print(f"Serial2: Sent GPS command: {command}")
                response = self.ser2.readlines()[1].decode('utf-8').strip()                
                print(f"Serial2 GPS Response: {response}")
                return response
            else:
                time.sleep(0.5)
                return None
        except serial.SerialException as e:
            raise Exception(f"Serial2 Error sending AT command: {e}")
        
    def initialize_gnss(self):
        try:
            self.ser2 = serial.Serial(self.gpsport, self.baud_rate, timeout=1)
            self.send_gps_at_command('AT+CGNSSPORTSWITCH=0,0')
            self.send_gps_at_command('AT+CGNSSTST=0')
            #self.send_gps_at_command('AT+CGNSSPWR=0')
        except serial.SerialException as e:
            raise Exception(f"Error initializing GNSS: {e}")

    def gnss_pwr_open(self, enable):
        command = f'AT+CGNSSPWR={int(enable)}'
        return self.send_gps_at_command(command) == "OK"

    def gnss_layout(self):
        return self.send_gps_at_command('AT+CGNSSTST=1') == "OK"

    def gnss_layout_switch(self):
        time.sleep(3) # be careful to provide sufficient delay but not too long
        self.send_gps_at_command('AT+CGNSSPORTSWITCH=1,0', wait_for_response=False)
        #<parse_data_port> 0 output the parsed data of NMEA to USB AT port.
        #                  1 output the parsed data of NMEA to UART port.
        #<nmea_data_port>  0 output raw NMEA data to USB NMEA port.
        #                  1 output raw NMEA data to UART port.
        return True

    def gnss_params(self):
        try:
            response = str(self.ser.readline(), encoding='utf-8')
            if response.startswith("$GNRMC") or response.startswith("$GPRMC"):
                rmc = pynmea2.parse(response)
                return rmc
            else:
                return None
        except serial.SerialException as e:
            raise Exception(f"Error reading GNSS params: {e}")
    
    def gnss_get_position(self):
        position =  self.send_gps_at_command('AT+CGNSSINFO')
        # +CGNSSINFO: 2,09,05,00,3113.330650,N,12121.262554,E, 131117, 091918.0, 32.9, 0.0, 255.0, 1.1, 0.8, 0.7
        # +CGNSSINFO: [<mode>],[<GPS-SVs>],[<GLONASS-SVs>],[BEIDOU-SVs],[<lat>],[<N/S>],[<log>],[<E/W>],[<date>],[<UTC-time>],[<alt>],[<speed>],[<course>],[<PDOP>],[HDOP],[VDOP]
        return position
        

if __name__ == '__main__':     
    try:
        # Initialize MPU6050 Accelerometer
        MPU_Init()
        # AT Command for SIM A7670SA
        at_instance = AT()      
        
        if at_instance.open_serial_connection():
            print('serial1 connected')
            at_instance.gnss_pwr_open(1)
            at_instance.gnss_layout()
            at_instance.gnss_layout_switch()
             
            if at_instance.init_mqtt():
                at_instance.subscribe_message()
                at_instance.start_subscribe_thread()
                
                while True:
                    Lat = "N"
                    Lon = "E"
                    Alt = "0"
                    Speed = "0"
                    Course = "0"
                    CGNSSINFO = at_instance.gnss_get_position().replace(' ','').replace('+CGNSSINFO:','').split(',')
                    if not CGNSSINFO[0] == 'ERROR' and len(CGNSSINFO) > 12:
                       Lat = CGNSSINFO[5] + " " + CGNSSINFO[6]
                       Lon = CGNSSINFO[7] + " " + CGNSSINFO[8]
                       Alt = CGNSSINFO[11]
                       Speed = CGNSSINFO[12]
                       Course = CGNSSINFO[13]
                    # decoding RMC signals - parsing NMEA sentence (the traditional way! :(
                    #response = at_instance.gnss_params()
                    #if response:
                    #    if re.match("^\d+?\.\d+?$", response.lat) is not None:
                    #        Lat = response.latitude
                    #        Lon = response.longitude
                    #        print(f"Latitude: {response.latitude}, Longitude: {response.longitude}")
                    #    else:
                    #        print(response)                    
                    time.sleep(3)
                    Ax,Ay,Az,Gx,Gy,Gz,Temp = readSensorData()                    
                    updateMsn = {
                        'data':
                            {
                                'datetime' : getClock(),
                                'Lat' : Lat,
                                'Lon' : Lon,
                                'Alt' : Alt,
                                'Speed' : Speed,
                                'Course' : Course,
                                'CGNSSINFO' : CGNSSINFO,
                                'vehicle' : ID,
                                'board_temperature': Temp,
                                'yaw' : yaw(Ax,Az),
                                'pitch' : pitch(Ax,Ay,Az),
                                'roll' : roll(Ay,Az),
                                'Ax' : Ax,
                                'Ay' : Ay,
                                'Az' : Az,
                                'Gx' : Gx,
                                'Gy' : Gy,
                                'Gz' : Gz,
                            }
                    }
                    JsonUpdataMsn = json.dumps(updateMsn)
                    at_instance.publish_message(JsonUpdataMsn)
                    #print("json = " + JsonUpdataMsn)  # For verification. Not required to show in actual implementation

    except KeyboardInterrupt:
        print("KeyboardInterrupt received. Cleaning up before exiting.")
        AT().destroy()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Program terminated.")


