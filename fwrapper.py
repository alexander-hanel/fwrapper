# Name: 
#    fwrapper.py
# Version: 
#    0.2
        # removed static instance name 
# Description: 
#    This script can be used to carve out data and work with data in IDA.           
# Author
#    alexander<dot>hanel<at>gmail<dot>com

import sys 
import idaapi 

class fwrapper():
    def __init__(self):
        self.start = SelStart()
        self.end = SelEnd()
        self.buffer = ''
        self.ogLen = None
        self.status = True
        self.run()
        
    def checkBounds(self):
        if self.start is BADADDR or self.end is BADADDR:
            self.status = False 

    def getData(self):
        
        self.ogLen = self.end - self.start  
        try:
            for byte in GetManyBytes(self.start, self.ogLen):
                self.buffer = self.buffer + byte
        except:
            self.status = False
        return
        
    def run(self):
        self.checkBounds()
        if self.status == False:
            sys.stdout.write('ERROR: Please select valid data')
            return 
        self.getData()
         
    def patch(self):
        'patch idb with data in fwrapper.buffer'
        for index, byte in enumerate(self.buffer):
             PatchByte(self.start+index, ord(byte))
             
    def importb(self):
        'import file to save to buffer'
        fileName = AskFile(0, "*.*", 'Import File')
        try:
            self.buffer = open(fileName, 'r').read()
        except:
            sys.stdout.write('ERROR: Cannot access file')
               
    def export(self):
        'save the selected buffer to a file'
        exportFile = AskFile(1, "*.*", 'Export Buffer')
        f = open(exportFile, 'wb')
        f.write(self.buffer)
        f.close()
        