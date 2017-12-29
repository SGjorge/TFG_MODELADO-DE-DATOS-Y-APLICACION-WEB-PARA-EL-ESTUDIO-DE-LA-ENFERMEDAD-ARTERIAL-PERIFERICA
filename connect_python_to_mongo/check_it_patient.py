#!/usr/bin/python
import sys

from pymongo import Connection
from pymongo.errors import ConnectionFailure

def main(username):
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
	user_doc = dbh.users.find_one({"username": username})
	if not user_doc:
		print "no document found for firstname " + username
		return (False)
	return (True)
	sys.exit(0)

if __name__ == "__main__":
	try:
		main(sys.argv[1])
	except IndexError:
		sys.stderr.write("Argument number isn't correct")
		sys.exit(1)
