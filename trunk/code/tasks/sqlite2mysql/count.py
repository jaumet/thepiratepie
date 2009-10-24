#!/home/piratepie/local/bin/python2.5

import sqlite3

# sqlite connection
sqlite = sqlite3.connect('../../data/tpb.db')
source = sqlite.cursor()

total = 0

source.execute( "SELECT id FROM torrentinfo" )

for row in source:
	total = total + 1
	if total % 1000 == 0:
		print total



print "final total: %s" % (total)

