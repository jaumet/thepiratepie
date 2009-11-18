#!/home/david/local/bin/python2.6

# ThePiratePie.org metadata scraper
# Records metadata of torrents on ThePirateBay.org
# By david.stolarsky@gmail.com

import MySQLdb




db = MySQLdb.connect(host='mysql.thepiratepie.org', user='tpp', passwd='tpp2009', db='test_piratepie', charset='utf8')
cursor = db.cursor()

cursor.execute("TRUNCATE torrents; TRUNCATE torrentinfo;")
