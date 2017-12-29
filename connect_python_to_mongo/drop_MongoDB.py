import sys

from pymongo import Connection
from pymongo.errors import ConnectionFailure

def main():
	""" Connect to MongoDb """
	try:
		c= Connection(host="localhost", port=27017) # be careful if you change the port, it doesn't work
		print "Connection successfully"
	except ConnectionFailure,e:
		sys.stderr.write("Could not connect to MongoDb: %s" % e)
		sys.exit(1)

	""" to can talk to the database you need know the name and password"""

	dbh = c["mydb"] #this create a hadle to 
	assert dbh.connection == c
	print "Successfully set up a database handle"
	dbh.users.remove()
	dbh.medicines.remove()
	dbh.diseases.remove()
	print "Successfully drop documents database"

if __name__ == "__main__":
	main()