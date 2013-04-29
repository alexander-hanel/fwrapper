# Name: 
#    fwrapper.py
# Version: 
#    0.4
        # 0.2 - removed static instance name
	# 0.3 - added usage function and add the option to pass a buffer to the patch function.
	# 0.4 - added stats function to display info. Updated getData to delete the contents of
	#       the obj.buffer. Removes user error if obj.buffer is not cleared. 
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

    def usage(self):
	print '''
	example:
	select data then execute the below command. The data will be automatically populated. It 
	should be noted that the whole instruction line will be added to the buffer. If the whole
	line is not intended the obj.start or obj.end will need to be manually changed. 

	obj = fwrapper()	 
	for x in obj.buffer: print hex(ord(x)) // will print each item in thebuffer			

	- data -
	obj.start               contains the address of the start of the selected instruction.
	obj.end                 contains the address of the end of the selected instruction. 
	obj.buffer              contains the binary data.   
	obj.ogLen               contains the size of the buffer. 

	- function -
	obj.usage()             print this 
	obj.checkBounds()       checks that obj.start and obj.end is valid addresses. 
	obj.getData()           copies the binary data between obj.start and obj.end to obj.buffer
	obj.run()               the selected data is copied to the buffer in a binary format
	obj.patch()             patch the IDB at obj.start with the data in the obj.buffer. 
	obj.patch(d)            patch the IDB at obj.start with the argument data. 
	obj.importb()           opens a file and saves the data in obj.buffer.
	obj.export()            exports the data in obj.buffer to a save as file.
	obj.stats()             print hex of obj.start, obj.end and obj.buffer length.
	'''
        
    def checkBounds(self):
        if self.start is BADADDR or self.end is BADADDR:
            self.status = False 

    def getData(self):
        '''get data betweeen start and end put them into object.buffer'''
        self.ogLen = self.end - self.start
	self.buffer = ''
        try:
            for byte in GetManyBytes(self.start, self.ogLen):
                self.buffer = self.buffer + byte
        except:
            self.status = False
        return
        
    def run(self):
	'''basically main'''
        self.checkBounds()
        if self.status == False:
            sys.stdout.write('ERROR: Please select valid data\n')
            return 
        self.getData()
         
    def patch(self, temp = None):
        '''patch idb with data in fwrapper.buffer'''
	if temp != None:
		self.buffer = temp
        for index, byte in enumerate(self.buffer):
             PatchByte(self.start+index, ord(byte))
             
    def importb(self):
        '''import file to save to buffer'''
        fileName = AskFile(0, "*.*", 'Import File')
        try:
            self.buffer = open(fileName, 'r').read()
        except:
            sys.stdout.write('ERROR: Cannot access file')
               
    def export(self):
        '''save the selected buffer to a file'''
        exportFile = AskFile(1, "*.*", 'Export Buffer')
        f = open(exportFile, 'wb')
        f.write(self.buffer)
        f.close()
       
    def stats(self):
	print "start: %s" % hex(self.start)
	print "end:   %s" % hex(self.end)
	print "len:   %s" % hex(len(self.buffer))
