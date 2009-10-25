from BeautifulSoup import BeautifulSoup
from urllib2 import Request, urlopen, URLError, HTTPError
import time
import calendar
import urllib
import urllib2
import time
import MySQLdb


class activitySample():
	def __init__(self):
		self.tpbid = -1
		self.sampleTime = -1
		self.seeders = -1
		self.leechers = -1

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
		self.subCategories = [101,102,103,104,199,201,202,203,204,205,206,207,208,299,301,302,303,304,399,401,402,403,404,405,406,499,501,502,503,504,505,506,599,601,602,603,604,699]

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
		sampleTime = calendar.timegm(time.gmtime())
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
			count = 0
			page = response.read()
			dom = BeautifulSoup(page)
			td = dom.find(True, {'id': 'searchResult'})
			tr = td.findAll('tr')[1:]
			
			samples = []

			for info in tr:
				if len(info.findAll('td')) == 1:
					continue
				tpbid = info.findAll('a')[1]['href'].split('/')[2]
				cat = info.find('a')['href'][8:]
				title = info.findAll('a')[1]['title'][11:]
				seeders = info.findAll('td')[5].contents[0]
				leechers = info.findAll('td')[6].contents[0]
				size = info.findAll('td')[4].contents[0]
				creationTime = info.findAll('td')[2].contents[0]
				if storeMethod=='newTorrent':
					self.dbNewtorrent(tpbid,title,cat,size)
				if storeMethod =='sql':
					sample = activitySample()
					sample.tpbid = tpbid
					sample.sampleTime = sampleTime
					sample.seeders = seeders
					sample.leechers = leechers
					samples.append(sample)
				if storeMethod =='print':
					print "%s, %s, %s, %s" % (sampleTime, tpbid, seeders, leechers)
				count = count + 1
			
			if storeMethod == 'sql':
				sql = "INSERT INTO activity (tpb_id, gmt_time, seeders, leechers) VALUES \n"
				for sample in samples:
					sql = sql + "(%s, %s, %s, %s),\n" % (sample.tpbid, sample.sampleTime, sample.seeders, sample.leechers)
				sql = sql[0:len(sql)-2] + ";"
				print sql
				
				
			return count

# methods parsing *********************************************************************************************
	
	def getSeedersAndLeechers(self, id):
		url = self.url+'torrent/'+str(id)+"/"
		data = self.getTPBTorrentPage( url, 'TPBSavePage', id  )
	
	def getTopCatPage(self, idcat ):
		url = self.url+'top/'+str(idcat)+"/"
		self.getTPBListPage( url , 'print' )
	
	def recentTorrentFile(self, page):
		url = self.url+'recent/'+str(page)
		self.getTPBListPage( url , 'newTorrent' )
	
	def getBrowseSeedersCatPage(self,id,page=0):
		# top seeders:
		url = self.url+'browse/'+str(id)+"/"+str(page)+"/7"
		return self.getTPBListPage( url , 'print' )
	
	def getBrowseLeechersCatPage(self,id,page=0, method="print"):
		url = self.url+'browse/'+str(id)+"/"+str(page)+"/9"
		return self.getTPBListPage( url , method )

	def getBrowseNewestCatPage(self, id, page=0, method="print"):
		url = self.url+'browse/'+str(id)+"/"+str(page)+"/3"
		return self.getTPBListPage( url , method )
	
	def getTop100(self,path):
		for idcat in self.categories:
			self.getTopCatPage(idcat)

	
	def recordActivityForCategory(self, cat, method="print"):
		for currentPage in range(0, 100):
			self.getBrowseLeechersCatPage(cat, currentPage, method)
			self.getBrowseNewestCatPage(cat, currentPage, method)
			
	def recordActivityForAllSubCategories(self, method="print"):
		for cat in self.subCategories:
			self.recordActivityForCategory(cat, method)


#tpb = webcrawlerTorrent()
#data = tpb.getSeedersAndLeechers('5130018')
#print data['seeders']
#print data['leechers']
#tpb.getTopCatPage(100)
#print time.localtime()
