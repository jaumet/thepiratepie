# pool of database connections

import MySQLdb
import threading

class DBPool():
	def __init__(self, theHost, theUser, thePassword, theDatabase, theConnectionCount=1):
		self.connections = []
		self.connectionLocks = []
		for c in range(1, theConnectionCount):
			self.connections.append(MySQLdb.connect(host=theHost, user=theUser, passwd=thePassword, db=theDatabase))
			self.connectionLocks.append(threading.Lock())
