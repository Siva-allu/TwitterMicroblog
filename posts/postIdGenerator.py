import time
# Generates Unique PostId.
# ReportId is of 6 Bytes (48 bits) => timestamp (41 bits) + report counter (7 bits)
# for every milliSecond 127 unique Posts Ids are Possible
class PostIdGenerator:
    
    def __init__(self):
        self.counter=0
        self.lastTimeStamp=0
        
    def generateId(self):
        
        currentTimeStamp=int(time.time()*1000)
        
        if currentTimeStamp==self.lastTimeStamp:
            self.counter=(self.counter+1)%(2**7)  # to ensure counter always lies between 0 to 127
        else:
            self.counter=0
            self.lastTimeStamp=currentTimeStamp
        return (currentTimeStamp<<7)|self.counter