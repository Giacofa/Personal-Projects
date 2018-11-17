import re
import os

SUBTITLE_TIME_FORMAT = r'((?P<hours>[0-9]+):(?P<minutes>[0-9]{1,2}):(?P<seconds>[0-9]{1,2}),(?P<milliseconds>[0-9]{1,3}))'

class HoursToMs(object):

    def __init__(self, string = '00:00:00,000'):
        self.fromstring(string)
        
    def fromstring(self,string):
        result = re.search(SUBTITLE_TIME_FORMAT, string)
        if result : 
            return result.groupdict(None)
        else
            raise IOError
            
    def toMs(self):
        return ((((self.h * 60) + self.m) * 60) + self.s) * 1000 + self.ms
        
#    def fromSeconds(self, seconds):
#        return self.fromMs(int(1000 * seconds))
    
    def fromMs(self, ms):
        assert type(ms) is int
        temp = ms
        self.ms = temp % 1000
        temp = temp / 1000
        self.s = temp % 60
        temp = temp / 60
        self.m = temp % 60
        temp = temp / 60
        self.h = temp
        
        return self
        
    def sum(self, other):
        temp = self.toMs() + other.toMs()
        return self.fromMs(temp)
        
    def subtraction(self, other) :
        temp = self.toMs() - other.toMs()
        if temp < 0:
            print "Too much backwards: beginning from 0:00:00,000"
            temp = 0
        return self.fromMs(temp)

    def toString(self):
        if self.h < 10:
            temp_h = '0'
        else :
            temp_h = ''
        if self.m < 10:
            temp_m = '0'
        else :
            temp_m = ''
        if self.s < 10:
            temp_s = '0'
        else :
            temp_s = ''
        return temp_h + str(self.h) + ':' + temp_m + str(self.m) + ':' + temp_s + str(self.s + self.ms * 0.001).replace('.',',')
        
    
input_str = raw_input('Insert file path and name: ')
timeshift = raw_input('Insert timeshift (format 01:23:45,678): ')
if timeshift.startswith('-'):
    timeshift = timeshift[1:]
    negative = True
else : negative = False

with open(input_str,'r+') as fileobj:

    counter = 1
    nextLineCounter = 0
    
    lines = fileobj.readlines()				# First reads all the lines
    fileobj.truncate(0)						# Then overwrites, starting from position 0 (beginning of the file)
    fileobj.seek(0)
    print 'Timeshift: ', HoursToMs(timeshift).toString()
    for line in lines:
        line = line.strip().strip('\n')
        
        result = re.search(SUBTITLE_TIME_FORMAT + '\s-->\s' + SUBTITLE_TIME_FORMAT, line)
        if line.isdigit():								# Subtitle counter update
            fileobj.write(str(counter) + '\n')
            counter = counter + 1
        elif result:
            if negative:
                fileobj.write(HoursToMs(result.group(1)).subtraction(HoursToMs(timeshift)).toString() + r' --> ' + HoursToMs(result.group(2)).subtraction(HoursToMs(timeshift)).toString() + '\n')
            else:
                fileobj.write(HoursToMs(result.group(1)).sum(HoursToMs(timeshift)).toString() + r' --> ' + HoursToMs(result.group(2)).sum(HoursToMs(timeshift)).toString() + '\n')
        else :
            fileobj.write(line + '\n')
