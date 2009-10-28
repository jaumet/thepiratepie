from BeautifulSoup import BeautifulSoup
from urllib2 import Request, urlopen, URLError, HTTPError
import time
import calendar
import urllib
import urllib2
import time
import MySQLdb
import threadpool
import threading
import os
import simplejson as json
	
	

class activitySample:
	def __init__(self):
		self.tpbid = -1
		self.sampleTime = -1
		self.seeders = -1
		self.leechers = -1

class webcrawlerTorrent:
	
	def __init__(self):
		self.url = "http://thepiratebay.org/"
		
		self.nameDataBase = "piratepie"
		self.userDataBase = "tpp"
		
		self.dbUsernameReadOnly = "tpp_select"
		self.dbPasswordReadOnly = "tpp_select"

		self.passwordDataBase = "tpp2009"
		self.host= "mysql.thepiratepie.org"
		self.tableActivity = "activity"
		self.tableTPB = "tpb"
		self.categories = [100,101,102,103,104,199,200,201,202,203,204,205,206,207,208,299,300,301,302,303,304,399,400,401,402,403,404,405,406,499,500,501,502,503,504,505,506,599,600,601,602,603,604,699]
		self.subCategories = [101,102,103,104,199,201,202,203,204,205,206,207,208,299,301,302,303,304,399,401,402,403,404,405,406,499,501,502,503,504,505,506,599,601,602,603,604,699]

		self.sortBy = { 'seeders' : { 'descending' : 7 }, 'leechers' : { 'descending' : 9 }, 'newest' : { 'descending' : 3 } }

		self.pendingTasks = 0
		self.pendingTasksLock = threading.Lock()
		
		self.dbLock = threading.Lock()
		self.debugDbLock = threading.Lock()
		
		self.haveDebugSQL = False
		self.haveSQL = False
		
		try:
			self.debugDB = MySQLdb.connect(host=self.host, user=self.userDataBase, passwd=self.passwordDataBase, db=self.nameDataBase)
			self.debugDBCursor = self.debugDB.cursor()
			self.haveDebugSQL = True
		except:
			print "Could not connect to MySQL!"

		try:
			self.db = MySQLdb.connect(host=self.host, user=self.userDataBase, passwd=self.passwordDataBase, db=self.nameDataBase)
			self.dbc = self.db.cursor()
			self.haveSQL = True
		except:
			print "Could not connect to MySQL!"
			
	
	def debug(self, msg):
		print "pid %s - %s: %s" % (os.getpid(), time.strftime("%c"), msg)
		sql = "INSERT INTO log_crawler (message, pid) VALUES ('%s', %s);" % (msg, os.getpid())
		#print sql

		if self.haveDebugSQL:
			self.debugDbLock.acquire()
			self.debugDBCursor.execute( sql )
			self.debugDbLock.release()
		
# database *********************************************************************************************
	
	def getDbConnection(self):
		try:
			db = MySQLdb.connect(host=self.host, user=self.userDataBase, passwd=self.passwordDataBase, db=self.nameDataBase)
			return db
		except:
			print "Could not get a MySQL connection."
			return None

	def getReadOnlyDbConnection(self):
		try:
			db = MySQLdb.connect(host=self.host, user=self.dbUsernameReadOnly, passwd=self.dbPasswordReadOnly, db=self.nameDataBase)
			return db
		except:
			print "Could not get a readonly MySQL connection."
			return None

	
	def safeDbQuery(self, sql):
		self.dbLock.acquire()
		if self.haveSQL:
			self.dbc.execute(sql)
		else:
			print "No SQL.  otherwise would run:\n%s" % (sql)
		self.dbLock.release()
	
# feed methods ******************************************************************************************
	
	def getTPBTorrentPage(self, tpbid):
		url = "http://www.thepiratebay.org/torrent/%s" % (tpbid)

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
			#print page
			dom = BeautifulSoup(page)
			td1 = dom.find(True, {'class': 'col1'})
			td2 = dom.find(True, {'class': 'col2'})
			#print dom
			#seeders = td2.findAll('dd')[3].contents[0]
			#print +"seeders:"+ seeders
			#leechers = td2.findAll('dd')[4].contents[0]
			#print leechers
			#user = td2.find('a').contents[0]
			#print user
			cat = td1.find('a')['href'][8:]
			#print cat
			#quality = td2.find(True, {'id': 'rating'}).contents[0]
			#print quality
			time = td2.findAll('dd')[1].contents[0]
			#print time
			#numFiles = td1.findAll('a')[1].contents[0]
			#print numFiles
			fulldescriptions = str(dom.find(True, {'class': 'nfo'}))[23:-13]
			#print fulldescriptions
			#comments = str(td2.findAll('dd')[5].contents[0])[23:-7]
			#print comments
			#lang = td1.findAll('dd')[4].contents[0]
			#print lang
			#if storeMethod=='TPBSavePage':
				#self.dbNewtorrent( tpbid, time, cat, size, fulldescription)
			print "%s, %s, %s" % (tpbid, cat, time)
	
	def scrapeListPage(self, cat, page, sortingCode):
		

		url = self.url+'browse/'+str(cat)+"/"+str(page)+str(sortingCode)
		
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
			html = response.read()
			dom = BeautifulSoup(html)
			td = dom.find(True, {'id': 'searchResult'})
			tr = td.findAll('tr')[1:]
			
			samples = []

			for info in tr:
				if len(info.findAll('td')) == 1:
					continue


				sample = activitySample()
				sample.sampleTime = sampleTime

				sample.tpbid = info.findAll('a')[1]['href'].split('/')[2]
				#cat = info.find('a')['href'][8:]
				#title = info.findAll('a')[1]['title'][11:]
				sample.seeders = info.findAll('td')[5].contents[0]
				sample.leechers = info.findAll('td')[6].contents[0]
				#size = info.findAll('td')[4].contents[0]
				#creationTime = info.findAll('td')[2].contents[0]
				
				samples.append(sample)
				
				count = count + 1
			
			if count > 0:
				
				updateJSON = json.dumps( { 'cat' : cat, 'page' : page, 'sortingCode' : sortingCode } )

				sql = "START TRANSACTION;\n" 
				sql = sql + "INSERT INTO activity (tpb_id, gmt_time, seeders, leechers) VALUES \n"
				for sample in samples:
					sql = sql + "(%s, UTC_TIMESTAMP(), %s, %s),\n" % (sample.tpbid, sample.seeders, sample.leechers)
				sql = sql[0:len(sql)-2] + ";\n"
				sql = sql + "UPDATE crawler_state (value) WHERE key = 'last_batch_insert' VALUES (%s);\n" % (updateJSON)
				sql = sql + "COMMIT;"
				#print sql
				self.safeDbQuery(sql)
				#threading.local().dbc.execute(sql)
				
				
			return count

# tasks info *********************************************************************************************
	def taskFinished(self, workRequest, result):
		self.pendingTasksLock.acquire()
		self.pendingTasks = self.pendingTasks - 1
		if self.pendingTasks % 100 == 0:
			self.debug( "Pending tasks: %s" % (self.pendingTasks) )
		self.pendingTasksLock.release()
	

# methods parsing *********************************************************************************************
	
	def getSeedersAndLeechers(self, id):
		url = self.url+'torrent/'+str(id)+"/"
		data = self.getTPBTorrentPage( url, 'TPBSavePage', id  )
	
	def getTopCatPage(self, idcat ):
		url = self.url+'top/'+str(idcat)+"/"
		self.scrapeListPage( url , 'print' )
	
	def recentTorrentFile(self, page):
		url = self.url+'recent/'+str(page)
		self.scrapeListPage( url , 'newTorrent' )
	
	def getBrowseSeedersCatPage(self,id,page=0):
		# top seeders:
		url = self.url+'browse/'+str(id)+"/"+str(page)+"/7"
		return self.scrapeListPage( url , 'print' )
	
	
	def getTop100(self,path):
		for idcat in self.categories:
			self.getTopCatPage(idcat)

			
	def recordActivityForAllSubCategories(self, method="print"):
		pool = threadpool.ThreadPool( 50 )
		self.pendingTasks = 0
		
		for currentPage in range(0, 100):
			for cat in self.subCategories:
				# scrape by top leechers and by newest
				request1 = threadpool.WorkRequest(self.scrapeListPage( cat, currentPage, self.sortBy['leechers']['descending'] ) )
				request2 = threadpool.WorkRequest(self.scrapeListPage( cat, currentPage, self.sortBy['newest']['descending'] ) )

				pool.putRequest(request1)
				pool.putRequest(request2)


				self.pendingTasksLock.acquire()
				self.pendingTasks = self.pendingTasks + 2
				self.pendingTasksLock.release()
							
			
		pool.wait()

	def fillMissingMetadata(self):
		#pool = threadpool.ThreadPool(50)
		#self.pendingTasks = 0

		db = self.getReadOnlyDbConnection()
		c = db.cursor()
		c.execute("SELECT DISTINCT tpb_id FROM `activity` WHERE activity.tpb_id NOT IN (SELECT id FROM torrentinfo) LIMIT 100;")

		for id in c:
			print "scraping %s..." % (id[0])
			self.getTPBTorrentPage( id[0] )


