import sys
import gridfs
from termcolor import colored

from pymongo import Connection
from pymongo.errors import ConnectionFailure

def __getPatientFilesDoc(idPatient,dictIdDoc):
	patient_file_doc = {
		"idPatient": idPatient,
		"files": dictIdDoc
	}
	return patient_file_doc

def __getPatientDoc__(idPatient,dictDoc):
	patient_doc = {
		"idPatient": idPatient,
		"age": dictDoc['age'],
		"sex": dictDoc['sex'],
		"type": dictDoc['typePatient'],
		"height": dictDoc['height'],
		"weight": dictDoc['weight'],
		"athletic": dictDoc['athletic'],
		"smoker": dictDoc['smoker'],
		"flat-concave foot": dictDoc['flat-concave foot'],
		"template": dictDoc['template'],
		"leg": dictDoc['leg']
	}
	return patient_doc

def __getMedicineDoc__(idPatient,dictDoc):
	medicine_doc = {
		"medicine" : dictDoc['medicine'],
		"idPatient": idPatient
	}
	return medicine_doc

def __getDiseaseDoc__(idPatient,dictDoc):
	disease_doc = {
		"disease" : dictDoc['disease'],
		"idPatient": idPatient
	}
	return disease_doc

############################ Public Methods API ######################################

def openConectionMDB(h,p):
	""" Connect to MongoDb """
	try:
		c= Connection(host=h, port=p) # be careful if you change the port, it doesn't work
		print colored("Connection successfully","yellow")
	except ConnectionFailure,e:
		sys.stderr.write("Could not connect to MongoDb: %s" % e)
		sys.exit(1)

	""" to can talk to the database you need know the name and password"""
	dbh = c["mydb"] #this create a hadle to 
	assert dbh.connection == c
	print colored("Successfully set up a database handle","yellow")
	return dbh


######################################### Files Table ###################################################
def addFileToPatientMDB(dbh,idPatient,filename, idFile):
	print colored(idPatient,"red")
	print colored(idFile,"red")
	patients_filesCursor = dbh.patientsFilesLinked.find_one({"idPatient":idPatient})
	print colored(patients_filesCursor,"red")
	filename = filename.replace('.','\u002E')
	if not patients_filesCursor:
		dictIdDoc = {}
		dictIdDoc[filename] = idFile
		new_patient_files = __getPatientFilesDoc(idPatient,dictIdDoc)
		dbh.patientsFilesLinked.insert(new_patient_files,safe=True)
		print colored("add a files test patient: %s" % new_patient_files,"yellow")
	else:
		print colored(patients_filesCursor,"red")
		new_files = patients_filesCursor.get("files")
		print colored(new_files,'red')
		new_files[filename] = idFile
		new_patient_files = __getPatientFilesDoc(idPatient,new_files)
		dbh.patientsFilesLinked.update({"idPatient":idPatient},new_patient_files)
		print colored("update a files test patient:" + str(idPatient) + ":" + str(new_files),"yellow")

def getFileMDB(dbh,file_id):
	file_saved = dbh.patientsFiles.chunks.find_one({'files_id':file_id})
	print colored(file_saved,'red')
	return file_saved

def getDictFilesIdsMDB(dbh,idPatient):
	patients_filesCursor = dbh.patientsFilesLinked.find_one({"idPatient":idPatient})
	if not patients_filesCursor:
		return None
	dictIdObject = patients_filesCursor.get("files")
	return dictIdObject

def insertFileMDB(idPatient, filename,dbh):
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

######################################### Medicines Table ###############################################
def addMedicineMDB(dbh,idPatient,dictDoc):
	medicine_doc = __getMedicineDoc__(idPatient,dictDoc)
	dbh.medicines.insert(medicine_doc,safe=True)
	print colored("add a medicine: %s" % medicine_doc,"yellow")

def getAllMedicinesMDB(dbh):
	medicines = dbh.medicines.find({"idPatient":"root"})
	#print colored("medicines docs founded: %s" % medicines,"yellow")
	rMedicines = []
	for record in medicines:
		rMedicines.append(record)
	return rMedicines

def getPatientMedicinesMDB(dbh,idPatient):
	medicinesCursor = dbh.medicines.find({'idPatient':idPatient})
	if not medicinesCursor:
		return ""
	medicines = []
	for medicine in medicinesCursor:
		medicines.append(medicine['medicine'])
	return medicines

def getNumberOfPatientsMedicineMDB(dbh,medicine):
	medicinesCursor = dbh.medicines.find({'medicine':medicine})
	c = medicinesCursor.count() - 1
	return c

def deleteAllMedicinesMDB(dbh):
	dbh.medicines.remove()
	print colored("all medicines remove","yellow")

def loadindAllMedicinesMDB(dbh,medicinesDoc):
	f = open(medicinesDoc,"r")
	for line in f:
		line = line.split("\n")[0].lower()
		print line
		dictDoc = {"medicine": line}
		addMedicineMDB(dbh,"root",dictDoc)
	print colored("loaded medicines table","yellow")

######################################### Diseases Table ###############################################
def addDiseaseMDB(dbh,idPatient,dictDoc):
	disease_doc = __getDiseaseDoc__(idPatient,dictDoc)
	dbh.diseases.insert(disease_doc,safe=True)
	print colored("add a disease: %s" % disease_doc,"yellow")

def getAllDiseasesMDB(dbh):
	diseases = dbh.diseases.find({"idPatient":"root"})
	#print colored("diseases docs founded: %s" % diseases,"yellow")
	rDiseases = []
	for record in diseases:
		rDiseases.append(record)
	return rDiseases

def getPatientDiseasesMDB(dbh,idPatient):
	diseasesCursor = dbh.diseases.find({'idPatient':idPatient})
	if not diseasesCursor:
		return ""
	diseases = []
	for disease in diseasesCursor:
		diseases.append(disease['disease'])
	return diseases

def deleteAllDiseasesMDB(dbh):
	dbh.diseases.remove()
	print colored("all patients remove","yellow")

def getNumberOfPatientsDiseaseMDB(dbh,disease):
	diseasesCursor = dbh.diseases.find({'disease':disease})
	c = diseasesCursor.count() - 1
	return c

def loadindAllDiseasesMDB(dbh,diseasesDoc):
	f = open(diseasesDoc,"r")
	for line in f:
		print line
		line = line.split("\n")[0].lower()
		print line
		dictDoc = {"disease": line}
		addDiseaseMDB(dbh,"root",dictDoc)
	print colored("loaded diseases table","yellow")

######################################### Patients Table ############################################### 
def checkPatientMDB(dbh,idP):
	user_doc = dbh.users.find_one(idP)
	if not user_doc:
		print colored("no document found for idPatient: " + str(idP),"yellow")
		return (False)
	print colored("document found for idPatient: " + str(idP),"yellow")
	return (True)

def addPatientMDB(dbh,idPatient,dictDoc):
	patient_doc = __getPatientDoc__(idPatient,dictDoc)
	dbh.users.insert(patient_doc,safe=True)
	print colored("add a patient: %s" % patient_doc,"yellow")

def getPatientMDB(dbh,idP):
	user_doc = dbh.users.find_one(idP)
	return(user_doc)

def deletePatientMDB(dbh,idPatient):
	dbh.users.remove(idPatient,safe=True)
	print colored("delete a patient:" + str(idPatient),"yellow")

def updatePatientMDB(dbh,idPatient,updates):
	print colored("updates","yellow")

def deleteAllPatientsMDB(dbh):
	dbh.users.remove()
	print colored("all patients remove","yellow")

def getNextIdPatientMDB(dbh):
	next = dbh.users.count() + 1
	return str(next)

def getAllPatientWithMDB(dbh,query):
	queryCursor = dbh.users.find(query)
	if not queryCursor:
		return ""
	results = []
	for result in queryCursor:
		results.append(result)
	return results

####################### Hacer una API mas generica ##########################################
"""
def addPatient(dictPatient,arrayMedicines,arrayDiseases):

def getPatient():
"""
