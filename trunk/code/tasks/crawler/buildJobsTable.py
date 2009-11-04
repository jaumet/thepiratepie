# ThePiratePie.org Scraper Job Table builder
# Builds table tracking which crawl jobs were done when
# By david.stolarsky@gmail.com

import webcrawlerPiratebayLS


# scrape procedure!

tpb = webcrawlerPiratebayLS.webcrawlerTorrent()
db = tpb.getDbConnection()
dbc = db.cursor()


sql = "INSERT INTO `crawler_jobs` (cat, page, sortCode) VALUES\n"

for page in range(0, 100):
	for cat in tpb.subCategories:
		sql = sql + "(%s, %s, %s),\n" % (cat, page, tpb.sortBy['leechers']['descending'])
		sql = sql + "(%s, %s, %s),\n" % (cat, page, tpb.sortBy['newest']['descending'])

sql = sql[0:len(sql)-2] + ";"

dbc.execute(sql)

