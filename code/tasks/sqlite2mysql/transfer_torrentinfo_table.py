#!/home/piratepie/local/bin/python2.5

import sqlite3
import MySQLdb

# sqlite connection
sqlite = sqlite3.connect('../../data/tpb.db')
source = sqlite.cursor()

# mysql connection
mysql = MySQLdb.connect(host='mysql.thepiratepie.org', user='tpp', passwd='tpp2009', db='piratepie')
destination = mysql.cursor()

# torrentinfo
total_succeeded = 872994
total_failed = 6
failed_ids = []

def record_failed_id(id):
	global destination
	destination.execute( """INSERT INTO not_transferred (tpb_id) VALUES (%s)""", (id) )

def resume_transfer():
	global total_succeeded
	global total_failed
	global failed_ids
	global source
	global destination

	try:
		transfer_limit( (total_succeeded+total_failed), 1000 )
	except:
		for t in range(0, 999):
			try:
				transfer_limit( (total_succeeded+total_failed), 1)
			except:
				source.execute( "SELECT id FROM torrentinfo LIMIT %s, %s" % ((total_succeeded+total_failed), 1) )
				row = source.fetchone()
				record_failed_id(row[0])
				total_failed = total_failed + 1
				pass

		pass

def transfer_limit(start, count):
	global total_succeeded
	global total_failed
	global failed_ids
	global source
	global destination

	lastid = -1

	source.execute( "SELECT * FROM torrentinfo LIMIT %s, %s" %  (start, count) )

	for row in source:
		try:
			lastid = row[0]

			destination.execute("""INSERT INTO torrentinfo (id, date, title, size, cat, rating, description)
			VALUES (%s, %s, %s, %s, %s, %s, %s)""",
			(
			row[0],
			row[1],
			row[2].encode('utf-8', 'xmlcharrefreplace'),
			row[3],
			row[4],
			row[5],
			row[6].encode('utf-8', 'xmlcharrefreplace')
			) )

			total_succeeded = total_succeeded + 1

		except:
			record_failed_id_at_start(lastid)	
			total_failed = total_failed + 1
			
	#		print "failed:"
	#		print failed_ids
			pass

		if (total_failed + total_succeeded) % 1000 == 0:
	#		destination.commit()
			print "succeeded: %s, failed: %s" % (total_succeeded, total_failed)





while 1:
	resume_transfer()
