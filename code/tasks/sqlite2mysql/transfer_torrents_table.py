#!/home/piratepie/local/bin/python2.5

import sqlite3
import MySQLdb

import dump_buffer

# sqlite connection
sqlite = sqlite3.connect('../../data/tpb.db')
source = sqlite.cursor()

# mysql connection
mysql = MySQLdb.connect(host='mysql.thepiratepie.org', user='tpp', passwd='tpp2009', db='piratepie')
destination = mysql.cursor()

# torrentinfo
total_succeeded = 0
total_failed = 0
failed_ids = []



def record_failed_id(id):
	global destination
	destination.execute( """INSERT INTO torrents_not_transferred (tpb_id) VALUES (%s)""", (id) )

def resume_transfer(count=1):
	global total_succeeded
	global total_failed
	global failed_ids
	global source
	global destination

	try:
		transfer_limit( (total_succeeded+total_failed), count )
	except:
		for t in range(0, count-1):
			try:
				transfer_limit( (total_succeeded+total_failed), 1)
			except:
				source.execute( "SELECT id FROM torrentinfo LIMIT %s, %s" % ((total_succeeded+total_failed), 1) )
				row = source.fetchone()
				record_failed_id(row[0])
				total_failed = total_failed + 1
#				pass

#		pass

def transfer():
	global total_succeeded
	global total_failed
	global failed_ids
	global source
	global destination

	lastid = -1

	source.execute( "SELECT * FROM torrents"  )

	for row in source:
#		try:
#		lastid = row[0]


		destination.execute("INSERT INTO torrents (id, file) VALUES (%s, X'%s')" % (row[0], ("%s" % row[1]).encode('hex').upper()))

		total_succeeded = total_succeeded + 1

#		except:
#			record_failed_id_at_start(lastid)	
#			total_failed = total_failed + 1
			
	#		print "failed:"
	#		print failed_ids
#			pass

		if (total_failed + total_succeeded) % 1000 == 0:
	#		destination.commit()
			print "succeeded: %s, failed: %s" % (total_succeeded, total_failed)

	print "final: %s" % (total_succeeded)



#while 1:
#resume_transfer(1)
transfer()
