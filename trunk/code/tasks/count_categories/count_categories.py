#!/home/piratepie/local/bin/python2.5

import MySQLdb

def pretty_filesize(bytes):
    if bytes >= 1073741824:
        return str(bytes / 1024 / 1024 / 1024) + ' GB'
    elif bytes >= 1048576:
        return str(bytes / 1024 / 1024) + ' MB'
    elif bytes >= 1024:
        return str(bytes / 1024) + ' KB'
    elif bytes < 1024:
        return str(bytes) + ' bytes'

# mysql connection
mysql = MySQLdb.connect(host='mysql.thepiratepie.org', user='tpp', passwd='tpp2009', db='piratepie')
cats = mysql.cursor()
cat_counts = mysql.cursor()

cats.execute("SELECT * FROM cat")

print "Category, Torrents, Size"

for row in cats:
	cat_counts.execute("SELECT COUNT(id), SUM(size) FROM torrentinfo WHERE cat = %s", row[0])
	for count_row in cat_counts:
		print "%s, %s, %s" % (row[1], count_row[0], pretty_filesize(count_row[1]))


