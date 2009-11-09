# ThePiratePie.org metadata scraper
# Records metadata of torrents on ThePirateBay.org
# By david.stolarsky@gmail.com

import webcrawlerPiratebayLS
import time

import runonce

runonce.quitIfDuplicate()

tpb = webcrawlerPiratebayLS.webcrawlerTorrent()
db = tpb.getDbConnection()
dbc = db.cursor()

dbc.execute("SELECT tpb_id FROM activity WHERE activity.tpb_id NOT IN (SELECT id FROM torrentinfo) ORDER BY gmt_time ASC LIMIT 100")
for row in dbc:
	print "Retrieving info for %s" % (row[0])
	print tpb.getTorrentInfo(row[0])



