# ThePiratePie.org Scraper
# Records seeders/leechers counts for most active and newest torrents on ThePirateBay.org
# By david.stolarsky@gmail.com

import webcrawlerPiratebayLS
import time
import fcntl
import os, sys

import runonce

# run only 1 copy! (cron will start me every 5 minutes so if I crash I will come back)
runonce.quitIfDuplicate()

# scrape procedure!

tpb = webcrawlerPiratebayLS.webcrawlerTorrent()

tpb.debug("Started crawler script")

while 1:
	tpb.debug("Started crawler main loop")
	tpb.recordActivityForAllSubCategories('sql')

#for cat in tpb.subCategories:
#	print "-------------\n%s\n-------------" % cat
#	print tpb.getBrowseLeechersCatPage(cat)

#tpb = webcrawlerTorrent()
#data = tpb.getSeedersAndLeechers('5130018')
#print data['seeders']
#print data['leechers']
#tpb.getTopCatPage(100)
#print time.localtime()
