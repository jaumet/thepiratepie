#!/home/david/local/bin/python2.6

# ThePiratePie.org metadata scraper
# Records metadata of torrents on ThePirateBay.org
# By david.stolarsky@gmail.com


import MySQLdb



db = MySQLdb.connect(host='mysql.thepiratepie.org', user='tpp_select', passwd='tpp_select', db='piratepie', charset='utf8')
dbc = db.cursor()



dbc.execute("SELECT COUNT(*) FROM torrentinfo")
count = 0
for row in dbc:
	count = row[0]

its = 


def crawlAndStoreTorrent(id, timeout=5):
	print "Retrieving info for %s" % (id)
	torrent = tpb.getTorrentInfo(id, timeout)


	if torrent == 'deleted':
		storeDBLock.acquire()
		storeCursor.execute("INSERT INTO deleted_torrents (id) VALUES (%s);" % (id))
		storeDBLock.release()
		return None

	if torrent != None:
		hexTorrent = torrent['torrent_file'].encode('hex').upper()

		storeDBLock.acquire()
		try:
			storeCursor.execute("""INSERT INTO torrentinfo (id, user, date, title, size, cat, description, from_crawler)
				       VALUES(%s, %s, %s, %s, %s, %s, %s, 1);""",
                                       (torrent['id'],
                                        torrent['user'],
                                        torrent['uploaded'],
                                        torrent['title'],
                                        torrent['size'],
                                        torrent['cat'],
                                        torrent['description']  )  )

			storeCursor.execute("INSERT INTO torrents (id, file) VALUES (%s, X'%s');" % (id, hexTorrent))
		except MySQLdb.IntegrityError:
			# duplicate entry most likely, is ok
			pass
		storeDBLock.release()
		print "Stored %s" % (id)

	return torrent


dbc.execute("SELECT DISTINCT(tpb_id) FROM activity WHERE tpb_id NOT IN (SELECT id FROM torrentinfo UNION SELECT id FROM deleted_torrents) LIMIT 1000;")
for row in dbc:
	request = threadpool.WorkRequest(crawlAndStoreTorrent, (row[0], 10))
	pool.putRequest(request)

pool.wait()
