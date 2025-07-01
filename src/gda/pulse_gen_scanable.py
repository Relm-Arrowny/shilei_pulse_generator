'''
Created on 25 Apr 2023

@author: wvx67826
@description:
    gda scanable that take zurich client object and perform different 
    get/set function on the zurich lockin
    zurich client class:
        /dls_sw/i10/scripts/beamline/TCL_Controls/zurichHF2/ZHF2Client.py
    manual:
        https://docs.zhinst.com/pdf/ziMFIA_UserManual.pdf
@version: 1.0
     scanable require zhf2client object it return x y,R and theta from the lockin
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
