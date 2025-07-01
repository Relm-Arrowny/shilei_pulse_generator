'''
Created on 01 july 2025

@author: wvx67826
@description:
    gda scanable that take pulse generator client object and perform different 
    get/set function
    pulse generator client class:
        /dls_sw/i10/scripts/beamline/TCL_Controls/pulse generator/pulse_gen_client.py
@version: 1.0
'''
from gda.device.scannable import ScannableBase


class Pulse_Gen_Scanable(ScannableBase):
    def __init__(self,name, pgs):
        
        self.pgs = pgs
        self.setName(name);
        self.setInputNames(["delay"])
        self.setOutputFormat(["%.6g"])
        self.level = 50
        self.data = 0
        
    def atScanStart(self):
        pass
    def atPointStart(self):
        pass
        
    def rawGetPosition(self):
        self.iambusy = 1
        
        self.data = float(self.pgs.get_delay().split("=")[-1])
        self.iambusy = 0
        return self.data
    
    def rawAsynchronousMoveTo(self,new_position):
        self.iambusy = 1
        self.pgs.set_delay(new_position)
        
        self.iambusy = 0

    def isBusy(self):
        return self.iambusy
    
    def atPointEnd(self):
        pass
    
    def atScanEnd(self):
        pass
pg= Pulse_Gen_Scanable(name ="pulse generator",pgs=pulse_gen_client)
