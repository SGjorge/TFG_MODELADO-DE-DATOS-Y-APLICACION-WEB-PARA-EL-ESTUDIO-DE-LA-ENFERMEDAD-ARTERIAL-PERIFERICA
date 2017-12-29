#!/usr/bin/python

""" the package to connect MDB"""
from pymongo import Connection
from pymongo.errors import ConnectionFailure

medicine_doc = {
	"medicine" : "pantoprazol",
	"username" : "jorgesimon"
}

disease_doc = {
	"disease" : "acido urico",
	"username" : "jorgesimon"
}

def main():
	print "---------------------- insert and write into MDB ---------------------"

	try:
		c=Connection(host="localhost",port=27017)
	except ConnectionFailure,e:
		sys.stderr.write("Could not connect to MDB: %s" %e)
		sys.exit(1)

	dbh= c["mydb"]
	assert dbh.connection == c

	""" insert a collection into MDB """
	dbh.medicines.insert(medicine_doc,safe=True)
	print "Successfully inserted document: %s" % medicine_doc
	dbh.diseases.insert(disease_doc,safe=True)
	print "Successfully inserted document: %s" % disease_doc

	""" insert,update, remove and findAndModify """

if __name__=="__main__":
	print "donde se me crea la base de datos?"
	main()