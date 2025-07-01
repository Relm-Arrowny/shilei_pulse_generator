import socket
import numpy as np
from time import time, sleep
from usbserial import USBSerial

class Pulse_G_Sever():
    
    def __init__(self, ip ="", port = 8888):
        self.HOST = ip # The server's hostname or IP address
        self.PORT = port  # The port used by the server
        self.serverRunning = False
        self.conn = None
        self.daq = None
        self.device = None
        
    def start(self):
        self.serverRunning = True
        self.device = USBSerial(port = 'COM4', baudrate = 9600, timeout = 3, open = True)
        self.device.write("AT\r\n")
        print(f"usb connection: {self.device.readline()}")
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.HOST, self.PORT))
            s.listen()
            self.conn, addr = s.accept()
            print(f"Connected: {addr}")
            try:
                s.bind((self.HOST, self.PORT))
                s.listen()
                self.conn, addr = s.accept()
                print(addr)
                print("Connected: %s" %addr)
            except:
                print("fail to start server")
            
            
            while self.serverRunning:
                self.processRequest(s)      

        return True
    def set_delay_time(self, value):
        if 1024>value>=0:
            self.device.write("AT+DLSET=%i\r\n" %value)
            return self.device.readline()
        else:
            self.sendError("Delay must be between 0 and 1023")
    
    def get_delay_time(self):
        self.device.write("AT+DLSET=?\r\n")
        data = self.device.readline()
        if  self.device.readline() == 'OK':
            return data
        else:
            return "Fail to read"        
            
    def processRequest(self, s):
        print("waiting for command")
        queued_data = self.conn.recv(1024).splitlines()
        print(queued_data)
        
        if not queued_data:
            queued_data =  [b"close"]
            
        for data in queued_data:
            
            data = data.split()   
            if data[0] == b"stopSever":
                self.serverRunning = False
                self.conn.sendall(b"server stopping")
                print("Server stopping")
                self.conn.close()
                self.daq.disconnect()
                
            elif data[0] == b"check_status":
                try:
                    self.device.write("AT\r\n")
                    send_data = self.device.readline()
                    self.conn.sendall(send_data.encode("utf_8"))
                except Exception as e:
                    self.sendError("data read failed: %s" %e)
            elif data[0] == b"set_delay":
                if len(data)>1:
                    value = float (data[1])
                try:
                    send_data= self.set_delay_time(value)

                    self.conn.sendall(send_data.encode("utf_8"))
                except Exception as e:
                    self.sendError("data read failed: %s" %e)
            elif data[0] == b"get_delay":
                try:
                    send_data= self.get_delay_time()

                    self.conn.sendall(send_data.encode("utf_8"))
                except Exception as e:
                    self.sendError("data read failed: %s" %e)
#=====================================================================================================================
    def sendError(self, errorMessage = "Unknown request"):
        self.conn.sendall(errorMessage.encode("utf_8"))
    
    def sendAck(self):
        sendData = b"1"
        self.conn.sendall(sendData)