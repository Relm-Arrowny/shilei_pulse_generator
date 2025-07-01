'''
Created on 01 july 2025

@author: wvx67826

@description: 
    pulse generator client
    JPython class to handle all client side of HF2Sever
    It send request to the server and handle responds 
    The server and client test with python 3 can be found here@
        https://github.com/Relm-Arrowny/shilei_pulse_generator

@version: 1.0
    First implementation of all user requested functions.
    
'''

from beamline.TCL_Controls.TCPSocket.TCPSocket import TCPSocket


class PulseGenClient(TCPSocket):
    def __init__(self, bufferSize = 1048, timeout = 5):
        super(PulseGenClient,self).__init__(bufferSize, timeout)
        

#================== get data ==============================================================
    def get_delay(self):
        com = ("get_delay")
        self.sendCom(com)
        return self.readBuffer()
    
    def set_delay(self, value):
        com = "set_delay %s" %value
        self.sendCom(com)
        return self.readBuffer()
    def command(self, value):
        com = "pass_command %s" %value
        self.sendCom(com)
        return self.readBuffer()
     
         
HOST = "172.23.110.81" # The server's hostname or IP address for Hutch Windows computer
PORT = 16888  # The port used by the server

pulse_gen_client = PulseGenClient(bufferSize = 2048, timeout = 15)
print(pulse_gen_client.connection(HOST, PORT))