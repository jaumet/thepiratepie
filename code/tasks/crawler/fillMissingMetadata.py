# ThePiratePie.org metadata scraper
# Records metadata of torrents on ThePirateBay.org
# By david.stolarsky@gmail.com

import webcrawlerPiratebayLS
import time

import runonce

import MySQLdb
import threadpool
import threading

runonce.quitIfDuplicate()


tpb = webcrawlerPiratebayLS.webcrawlerTorrent()
db = tpb.getDbConnection()
dbc = db.cursor()

storeDB = MySQLdb.connect(host='mysql.thepiratepie.org', user='tpp', passwd='tpp2009', db='test_piratepie', charset='utf8')
storeCursor = storeDB.cursor()

pool = threadpool.ThreadPool( 32 )
storeDBLock = threading.Lock()


def crawlAndStoreTorrent(id):
	print "Retrieving info for %s" % (id)
	torrent = tpb.getTorrentInfo(id)
	if torrent != None:
		hexTorrent = torrent['torrent_file'].encode('hex').upper()

		storeDBLock.acquire()
		storeCursor.execute("""INSERT INTO torrentinfo (id, user, date, title, size, cat, description, from_crawler)
				       VALUES(%s, %s, %s, %s, %s, %s, %s, 1)""",
                                       (torrent['id'],
                                        torrent['user'],
                                        torrent['uploaded'],
                                        torrent['title'],
                                        torrent['size'],
                                        torrent['cat'],
                                        torrent['description']  )  )
		storeCursor.execute("INSERT INTO torrents (id, file) VALUES (%s, X'%s')" % (id, hexTorrent))
		storeDBLock.release()



crawlAndStoreTorrent(5135917)

dbc.execute("SELECT DISTINCT(tpb_id) FROM activity WHERE activity.tpb_id NOT IN (SELECT id FROM torrentinfo) ORDER BY gmt_time ASC LIMIT 100")
for row in dbc:
	request = threadpool.WorkRequest(crawlAndStoreTorrent, (row[0],))
	pool.putRequest(request)

pool.wait()
#pool.joinAllDismissedWorkers()
