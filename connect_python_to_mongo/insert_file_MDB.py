import pymongo
from pymongo import Connection
from pymongo.errors import ConnectionFailure
from termcolor import colored
import gridfs

def getFile(dbh,file_id):
	file_saved = dbh.patientsFiles.chunks.find_one({'files_id':file_id})
	print colored(file_saved,'red')
	return file_saved

def insertFile(idPatient, filename,dbh):
	print "------------- insert ------------"
	print "Patient --> " + idPatient
	print "File    --> " + filename

	patient = dbh.users.find_one({'idPatient': idPatient})
	print colored(patient,'green')

	grid = gridfs.GridFS(dbh,"patientsFiles")
	print colored(grid,'blue')
	with open(filename, "r") as fin:
		sdf_id = grid.put(fin)
	print colored(sdf_id,'yellow')
	return sdf_id

def main():
	print "---------------------- insert a file into MDB ---------------------"
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

	file_id = insertFile("id1",'/home/jorge/tfg/uploaded_files/JDTD_27_04_2015_hrv.txt',dbh)
	file_saved = getFile(dbh,file_id)

if __name__ == "__main__":
	main()