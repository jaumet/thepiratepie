#
#	El manager v.0.01 - Derivart (http://www.derivart.info)
#	@Coded: Mar Cane / Martin Nadal (2009)
#   Adapted for the piratePie.org
#
from time import sleep
from threadPool import threadPool
from webcrawlerPiratebayLS import  webcrawlerTorrent

class threadManager():

    def __init__(self):
        self.totalPoolTasks = 10
        self.poolTPB = threadPool(self.totalPoolTasks)
        self.tpb = webcrawlerTorrent()
        self.totalAnalyse = 0

    #  TPB pull ***************************************************************************************

    def taskTPB(self, idTorrent):
        self.tpb.getSeedersAndLeechers(idTorrent)
        return idTorrent

    def taskTPBCallback(self, idTorrent):
        self.totalAnalyse +=1

    def addTPBFeedData(self, id):
        # Insert tasks into the queue and let them run        
        self.poolTPB.queueTask(self.taskTPB, id, self.taskTPBCallback)

    # When all tasks are finished, allow the threads to terminate
    def endTPBFinishProcess(self):
        self.poolTPB.joinAll()

    #  ***********************************************************************************************
    def takeFromDatabaseTorrents():
        #from myql
        


TM.addTPBFeedData('5130018')
TM.addTPBFeedData('5130019')
TM.addTPBFeedData('5130020')
TM.endTPBFinishProcess()