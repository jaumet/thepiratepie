from BeautifulSoup import BeautifulSoup
from urllib2 import Request, urlopen, URLError, HTTPError
import re
import time
import calendar
import datetime
import urllib
import urllib2
import time
import MySQLdb
import threadpool
import threading
import os
	
	

class activitySample:
	def __init__(self):
		self.tpbid = -1
		self.sampleTime = -1
		self.seeders = -1
		self.leechers = -1

#class jobResult

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
			for row in self.dbc:
				print row
		else:
			print "No SQL.  otherwise would run:\n%s" % (sql)
		self.dbLock.release()
	
# feed methods ******************************************************************************************

	def downloadTorrentFileToDb(self, tpbid):
		True
	
	def getTorrentInfo(self, tpbid):
		url = "http://thepiratebay.org/torrent/%s" % (tpbid)

		

		try:
			#page = os.popen("wget -q -O- http://thepiratebay.org/torrent/%s" % (tpbid) ).read()
			response = urllib2.urlopen(url)
			page = response.read()
		except:
			return None
		else:
		# everything is fine
			torrent = {}
			torrent['id'] = tpbid
			dom = BeautifulSoup(page)

			# bail if 404
			title = dom.find('head').find('title').string
			if title.find('Not Found') > -1:
				return None

			#print dom
			details = dom.find('div', {'id' : 'detailsframe'})
			td1 = dom.find(True, {'class': 'col1'})
			td2 = dom.find(True, {'class': 'col2'})


			torrent['title'] = details.find('div', {'id' : 'title'}).string.strip()

			torrent['torrent_url'] = details.find('a', {'title' : 'Download this torrent'})['href']

			try:
				torrentResponse = urllib2.urlopen(torrent['torrent_url'])
				torrentFile = torrentResponse.read()
				torrent['torrent_file'] = torrentFile
			except:
				return None

			torrent['cat'] = td1.find('a', {'title' : 'More from this category'})['href'][8:]

			sizeString = details.find('dt', text='Size:').parent.nextSibling.nextSibling.string
			openParen = sizeString.find('(')
			torrent['size'] = re.findall("[0-9]*", sizeString[openParen+1:])[0]
			
			try:
				torrent['user'] = details.find('dt', text='By:').parent.nextSibling.nextSibling.find('a')['href'].split('/')[2]
			except:
				torrent['user'] = 'Anonymous'

			uploadedLabel = details.find(text='Uploaded:')
			dateString = uploadedLabel.parent.nextSibling.nextSibling.string
			"2009-10-10 04:04:20 GMT" # just here for reference...
			tuple = [dateString[0:4], dateString[5:7], dateString[8:10], dateString[11:13], dateString[14:16], dateString[17:19]]
			date = datetime.datetime(int(tuple[0]), int(tuple[1]), int(tuple[2]), int(tuple[3]), int(tuple[4]), int(tuple[5]))
			torrent['uploaded'] = calendar.timegm(date.timetuple())

			torrent['description'] = str(dom.find(True, {'class': 'nfo'}).find('pre'))[5:-6]
	
			return torrent

	def scrapeListPage(self, cat, page, sortingCode):
		

		url = self.url+'browse/'+str(cat)+"/"+str(page)+str(sortingCode)
		
		sampleTime = calendar.timegm(time.gmtime())
		try:
			response = urllib2.urlopen(url)
		except:
			print 'The server couldn\'t fulfill the request.'
		else:
		# everything is fine
			count = 0
			html = response.read()
			dom = BeautifulSoup(html)
			td = dom.find(True, {'id': 'searchResult'})

			tr = []
			if(td != None):
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
				
				sql = ''
				sql = sql + "INSERT INTO activity (tpb_id, gmt_time, seeders, leechers) VALUES \n"
				for sample in samples:
					sql = sql + "(%s, UTC_TIMESTAMP(), %s, %s),\n" % (sample.tpbid, sample.seeders, sample.leechers)
				sql = sql[0:len(sql)-2] + ";\n"
				self.safeDbQuery(sql)

				sql = "UPDATE `crawler_jobs` SET last_run_utc=UTC_TIMESTAMP() WHERE cat=%s AND page=%s AND sortCode=%s;\n" % (cat, page, sortingCode)
				#print "added %s samples" % (count)				

				self.safeDbQuery(sql)
				#print sql
				
				
			return count

# tasks info *********************************************************************************************
	"""def taskFinished(self, workRequest, result):
		self.pendingTasksLock.acquire()
		self.pendingTasks = self.pendingTasks - 1
		if self.pendingTasks % 100 == 0:
			self.debug( "Pending tasks: %s" % (self.pendingTasks) )
		self.pendingTasksLock.release()"""
	

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
		pool = threadpool.ThreadPool( 64 )
		self.pendingTasks = 0




		# do the 1,000 oldest jobs, then quit.  cron will start me again
		db = self.getDbConnection()
		dbc = db.cursor()
		dbc.execute("SELECT cat, page, sortCode FROM crawler_jobs ORDER BY last_run_utc ASC LIMIT 1000")
		for job in dbc:
			request = threadpool.WorkRequest(self.scrapeListPage, (job[0], job[1], job[2]) )
			pool.putRequest(request)
			"""self.pendingTasksLock.acquire()
			self.pendingTasks = self.pendingTasks + 1
			self.pendingTasksLock.release()"""
			#time.sleep(1)


		
		"""for currentPage in range(0, 100):
			for cat in self.subCategories:
				# scrape by top leechers and by newest
				request1 = threadpool.WorkRequest(self.scrapeListPage( cat, currentPage, self.sortBy['leechers']['descending'] ) )
				request2 = threadpool.WorkRequest(self.scrapeListPage( cat, currentPage, self.sortBy['newest']['descending'] ) )

				pool.putRequest(request1)
				pool.putRequest(request2)


				self.pendingTasksLock.acquire()
				self.pendingTasks = self.pendingTasks + 2
				self.pendingTasksLock.release()"""
							
			
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


