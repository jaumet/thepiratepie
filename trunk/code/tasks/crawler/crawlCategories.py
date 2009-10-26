import webcrawlerPiratebayLS
import time

# scrape procedure!

tpb = webcrawlerPiratebayLS.webcrawlerTorrent()


while 1:
	print "Started scraper at %s" % (time.strftime("%c"))
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
