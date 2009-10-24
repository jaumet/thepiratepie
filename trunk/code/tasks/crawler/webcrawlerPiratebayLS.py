from BeautifulSoup import BeautifulSoup
from urllib2 import Request, urlopen, URLError, HTTPError
import urllib
import urllib2
import time
import MySQLdb


class webcrawlerTorrent():
    def __init__(self):
        self.url = "http://thepiratebay.org/"
        self.nameDataBase = "tpb"
        self.userDataBase = "root"
        self.passwordDataBase = "root"
        self.host= "localhost"
        self.tableRealtimeDataBase = "realtimeTPB"
        self.tableTPB = "tpb"
        self.categories = [100,101,102,103,104,199,200,201,202,203,204,205,206,207,208,299,300,301,302,303,304,399,400,401,402,403,404,405,406,499,500,501,502,503,504,505,506,599,600,601,602,603,604,699]

# database *********************************************************************************************

    def recordRowTopCatItem(self, tpbid, cat, seeders, leechers):
        time =""
        sql = "INSERT INTO "+self.tableRealtimeDataBase+" ('tpb-id','time','cat','seeders','leechers') VALUES ('"+tpbid+"','"+time+"','"+cat+"','"+seeders+"','"+leechers+"')"
        # connect
        db = MySQLdb.connect(host=self.host, user=self.userDataBase, passwd=self.passwordDataBase, db=self.nameDataBase)
        # create a cursor
        cursor = db.cursor()
        # execute SQL statement
        cursor.execute(sql)

    def dbNewtorrent(self,tpbid,title,cat,size, fulldescription):
        sql = "INSERT INTO "+self.tableTPB+" ('tpb-id','title','cat','size', 'fulldescription') VALUES ('"+tpbid+"','"+title+"','"+cat+"','"+size+"','"+fulldescription+"')"
        # connect
        db = MySQLdb.connect(host=self.host, user=self.userDataBase, passwd=self.passwordDataBase, db=self.nameDataBase)
        # create a cursor
        cursor = db.cursor()
        # execute SQL statement
        cursor.execute(sql)
        
# feed methods ******************************************************************************************

    def getTPBTorrentPage(self, url, storeMethod, tpbid):
        try:
            response = urllib2.urlopen(url)
        except HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except URLError, e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        else:
        # everything is fine
            page = response.read()
            print page
            #dom = BeautifulSoup(page)      
            #td1 = dom.find(True, {'class': 'col1'})
            #td2 = dom.find(True, {'class': 'col2'})
            #print dom
            #seeders = td2.findAll('dd')[3].contents[0]
            #print +"seeders:"+ seeders
            #leechers = td2.findAll('dd')[4].contents[0]
            #print leechers
            #user = td2.find('a').contents[0]
            #print user
            #cat = td1.find('a')['href'][8:]
            #print cat
            #quality = td2.find(True, {'id': 'rating'}).contents[0]
            #print quality
            #time = td2.findAll('dd')[1].contents[0]
            #print time
            #numFiles = td1.findAll('a')[1].contents[0]
            #print numFiles
            #fulldescriptions = str(dom.find(True, {'class': 'nfo'}))[23:-13]
            #print fulldescriptions
            #comments = str(td2.findAll('dd')[5].contents[0])[23:-7]
            #print comments
            #lang = td1.findAll('dd')[4].contents[0]
            #print lang
            #if storeMethod=='TPBSavePage':
                #self.dbNewtorrent( tpbid, time, cat, size, fulldescription)

    def getTPBListPage(self, url, storeMethod):
        try:
            response = urllib2.urlopen(url)
        except HTTPError, e:
            print 'The server couldn\'t fulfill the request.'
            print 'Error code: ', e.code
        except URLError, e:
            print 'We failed to reach a server.'
            print 'Reason: ', e.reason
        else:
        # everything is fine
            page = response.read()
            dom = BeautifulSoup(page)
            td = dom.find(True, {'id': 'searchResult'})
            tr = td.findAll('tr')[1:]
            for info in tr:
                tpbid = info.findAll('a')[1]['href'].split('/')[2]
                cat = info.find('a')['href'][8:]
                title = info.findAll('a')[1]['title'][11:]
                seeders = info.findAll('td')[5].contents[0]
                leechers = info.findAll('td')[6].contents[0]
                size = info.findAll('td')[4].contents[0]
                time = info.findAll('td')[2].contents[0]
                if storeMethod=='newTorrent':
                    self.dbNewtorrent(tpbid,title,cat,size)
                if storeMethod =='realtime':
                    self.recordRowTopCatItem( tpbid, cat, seeders, leechers )
                print "%s, %s, %s" % (tpbid, seeders, leechers)

# methods parsing *********************************************************************************************

    def getSeedersAndLeechers(self, id):
        url = self.url+'torrent/'+str(id)+"/"
        data = self.getTPBTorrentPage( url, 'TPBSavePage', id  )

    def getTopCatPage(self, idcat ):
        url = self.url+'top/'+str(idcat)+"/"
        self.getTPBListPage( url , 'none' )

    def recentTorrentFile(self, page):
        url = self.url+'recent/'+str(page)
        self.getTPBListPage( url , 'newTorrent' )

    def getBrowseSeedersCatPage(self,id,page=0):
        # top seeders:
        url = self.url+'browse/'+str(id)+"/"+str(page)+"/7"
        self.getTPBListPage( url , 'realtime' )

    def getBrowseLeechersCatPage(self,id,page=0):
        url = self.url+'browse/'+str(id)+"/"+str(page)+"/9"
        self.getTPBListPage( url , 'realtime' )

    def getTop100(self,path):
        for idcat in self.categories:
            self.getTopCatPage(idcat)

tpb = webcrawlerTorrent()
tpb.getTopCatPage(205)

#tpb = webcrawlerTorrent()
#data = tpb.getSeedersAndLeechers('5130018')
#print data['seeders']
#print data['leechers']
#tpb.getTopCatPage(100)
#print time.localtime()
