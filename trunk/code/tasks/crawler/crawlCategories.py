import webcrawlerPiratebayLS

# scrape procedure!

tpb = webcrawlerPiratebayLS.webcrawlerTorrent()


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
