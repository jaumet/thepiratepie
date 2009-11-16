# ThePiratePie.org metadata scraper
# Records metadata of torrents on ThePirateBay.org
# By david.stolarsky@gmail.com

import webcrawlerPiratebayLS
import time

import runonce

import MySQLdb

runonce.quitIfDuplicate()


tpb = webcrawlerPiratebayLS.webcrawlerTorrent()
db = tpb.getDbConnection()
dbc = db.cursor()

storeDB = MySQLdb.connect(host='mysql.thepiratepie.org', user='tpp', passwd='tpp2009', db='test_piratepie')
storeCursor = storeDB.cursor()


pool = threadpool.ThreadPool( 64 )

dbc.execute("SELECT tpb_id FROM activity WHERE activity.tpb_id NOT IN (SELECT id FROM torrentinfo) ORDER BY gmt_time ASC LIMIT 100")
for row in dbc:
	print "Retrieving info for %s" % (row[0])
	torrent = tpb.getTorrentInfo(row[0])
	if torrent != None:
		print type(torrent['description'])
		hexTorrent = torrent['torrent_file'].encode('hex').upper()
		storeCursor.execute("""INSERT INTO torrentinfo (id, user, date, title, size, cat, description, from_crawler)
				       VALUES(%s, %s, %s, %s, %s, %s, %s, 1)""", (torrent['id'], torrent['user'], torrent['uploaded'], torrent['title'], torrent['size'], torrent['cat'], torrent['description'] )  )
		storeCursor.execute("INSERT INTO torrents (id, file) VALUES (%s, X'%s')" % (row[0], hexTorrent))


		request = threadpool.WorkRequest(crawlAndStoreTorrent(






		# do the 1,000 oldest jobs, then quit.  cron will start me again
		db = self.getDbConnection()
		dbc = db.cursor()
		dbc.execute("SELECT cat, page, sortCode FROM crawler_jobs ORDER BY last_run_utc ASC LIMIT 1000")
		for job in dbc:
			request = threadpool.WorkRequest(self.scrapeListPage( job[0], job[1], job[2] ))
			pool.putRequest(request)
			"""self.pendingTasksLock.acquire()
			self.pendingTasks = self.pendingTasks + 1
			self.pendingTasksLock.release()"""
			#time.sleep(1)


