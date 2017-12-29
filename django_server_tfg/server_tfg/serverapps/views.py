import sys
sys.path.append("/home/jorge/tfg/connect_python_to_mongo/")
sys.path.append("/home/jorge/tfg/statistics_functions/")

import csv
import zipfile
import StringIO
import os

from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.template.loader import get_template
from django.template import Context
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt

from django.core.files.storage import FileSystemStorage
from django.core.files.base import ContentFile
from django.utils.encoding import smart_str

from api_MDB_server_django import *
#from statistics_api import *
from modelsML import *

from termcolor import colored

# Create your views here.
############################### Others Methods ################################

# change Form to python Dictionary 
def parsedForm(dataForm):
	form = dataForm.split("&")
	Dictionary = {}
	for f in form:
		tupla = f.split("=")
		Dictionary[str(tupla[0])] = str(tupla[1])
	return Dictionary

def deleteDuplicates(array,key):
	arrayNotDuplicated = []
	for a in array:
		disease = a[key]
		#print colored(a[key],"green")
		try:
			arrayNotDuplicated.index(disease)
		except (ValueError):
			arrayNotDuplicated.append(disease)
	return arrayNotDuplicated

def getLabelSelectForm(typeOption,index,value):
	SelectedForm = '<div class="checkbox">'
	SelectedForm += '<label><input type="checkbox" value="' + str(value) +'"' 
	SelectedForm += 'name="'+ str(typeOption) + str(index) +'">' + str(value) +'</label></div>'
	return SelectedForm

def getEmptyParagraph(id,value):
	paragraph = "<p id='" + id.replace(" ","_")
	paragraph += "'>" + str(value)
	paragraph += "</p>"
	return paragraph

def getItemize(array):
	itemize = "<ul>"
	for a in array:
		itemize += "<li>" + str(a) + "</li>"
	itemize += "</ul>"
	return itemize

def getForm(form,typeForm):
	notDuplicated = deleteDuplicates(form,typeForm)
	form = ""
	index = 0
	for nd in notDuplicated:
		index += 1
		form += getLabelSelectForm(typeForm,index,nd)
	return form

def getValues(pForm,key):
	values = []
	for f in pForm:
		if (str(f).find(key) != -1):
			values.append(pForm[f].replace("+"," "))
	return values

def selectValue(arrayDic,key):
	aux = []
	for a in arrayDic:
		aux.append(a[key])
	return aux

def checkSingForm(pForm):
	try:
		pForm['smoker']
	except KeyError:
		pForm['smoker'] = False
	try:
		pForm['athletic']
	except KeyError:
		pForm['athletic'] = False
	try:
		pForm['flat-concave foot']
	except KeyError:
		pForm['flat-concave foot'] = False
	try:
		pForm['template']
	except KeyError:
		pForm['template'] = False
	return pForm

def patientsToCsv(patients,writer):
	for patient in patients:
		writer.writerow([patient['idPatient'], patient['age'], patient['sex'], patient['type'], patient['weight'], patient['height'], patient['athletic'], patient['smoker'], patient['flat-concave foot'], patient['template'], patient['leg']])

def getTypesPatientsValues():
	queryControlType = {'type':'Control'}
	patientsControlType = getAllPatients(queryControlType)
	controlTypeCount = len(patientsControlType)
	querySintomaticType = {'type':'Asintomatico'}
	patientsSintomaticType = getAllPatients(querySintomaticType)
	sintomaticTypeCount = len(patientsSintomaticType)
	queryClauType = {'type':'Claudicante'}
	patientsClauType = getAllPatients(queryClauType)
	clauTypeCount = len(patientsClauType)
	paragraphs = getEmptyParagraph("Control",controlTypeCount) + getEmptyParagraph("Asintomatico",sintomaticTypeCount) + getEmptyParagraph("Claudicante",clauTypeCount)
	return paragraphs

def getAllOneAtrib(query,typeAtrib):
	patients = getAllPatients(query)
	paragraphs = ""
	for patient in patients:
		paragraphs += getEmptyParagraph(patient['idPatient'],patient[typeAtrib])
	return paragraphs

def getAgesPatientValues():
	query = {}
	atrib = 'age'
	paragraphs = getAllOneAtrib(query,atrib)
	return paragraphs

def getWeigthPatientValues():
	query = {}
	atrib = 'weight'
	paragraphs = getAllOneAtrib(query,atrib)
	return paragraphs

def getHeightPatientValues():
	query = {}
	atrib = 'height'
	paragraphs = getAllOneAtrib(query,atrib)
	return paragraphs

def handlerFiles(request):
	for afile in request.FILES.getlist('patientFiles'):
		myfile = afile
		fs = FileSystemStorage()
		filename = settings.MEDIA_ROOT + "/" + myfile.name
		f = open(filename,'w')
		f.write(myfile.read())
		f.close()

################################ MDB Methods ##################################
def checkInPatient(idPatient):
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	return checkPatientMDB(dbh,idPatient)

def getIdPatient():
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	nextId = "id" + str(getNextIdPatientMDB(dbh))
	return nextId

def addMedicinesPatient(dbh,idPatient,pForm):
	medicines = getValues(pForm,"medicine")
	for medicine in medicines:
		mForm = {"medicine": medicine}
		addMedicineMDB(dbh,idPatient,mForm)
	print colored("proceso para anadir las medicinas que toma un paciente", "green")

def addDiseasesPatient(dbh,idPatient,pForm):
	diseases = getValues(pForm,"disease")
	for disease in diseases:
		dForm = {"disease":disease}
		addDiseaseMDB(dbh,idPatient,dForm)
	print colored("proceso para anadir las enfermedades que tiene un paciente", "green")

def addPatient(pForm):
	idPatient = getIdPatient()
	#print (idPatient)
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	addPatientMDB(dbh,idPatient,pForm)
	addMedicinesPatient(dbh,idPatient,pForm)
	addDiseasesPatient(dbh,idPatient,pForm)
	print colored("Added " + str(idPatient), "green")
	return idPatient

def getPatient(idPatient):
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	p = getPatientMDB(dbh,idPatient)
	print colored("patient search " + str(idPatient) + ",result: %s" %p, "green")
	return(p)

def getAllPatients(query):
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	patients = getAllPatientWithMDB(dbh,query)
	return patients

def getAllMedicines():
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	medicines = getAllMedicinesMDB(dbh)
	return getForm(medicines,"medicine")

def getPatientMedicines(idPatient):
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	medicines = getPatientMedicinesMDB(dbh,idPatient)
	return getItemize(medicines)

def getMedicinesValues():
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	medicines = getAllMedicinesMDB(dbh)
	paragraphs = ""
	for medicine in medicines:
		c = getNumberOfPatientsMedicineMDB(dbh,medicine['medicine'])
		paragraphs += getEmptyParagraph(medicine['medicine'],c)
	return paragraphs

def getAllDiseases():
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	diseases = getAllDiseasesMDB(dbh)
	return getForm(diseases,"disease")

def getPatientDiseases(idPatient):
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	diseases = getPatientDiseasesMDB(dbh,idPatient)
	return getItemize(diseases)

def getDiseasesValues():
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	diseases = getAllDiseasesMDB(dbh)
	paragraphs = ""
	for disease in diseases:
		c = getNumberOfPatientsDiseaseMDB(dbh,disease['disease'])
		paragraphs += getEmptyParagraph(disease['disease'],c)
	return paragraphs

def getSexAgeRelationValues():
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	maleQuery = {"sex":'Varon'}
	femaleQuery = {"sex":'Hembra'}
	maleAges = selectValue(getAllPatientWithMDB(dbh,maleQuery),'age')
	print(maleAges)
	femaleAges = selectValue(getAllPatientWithMDB(dbh,femaleQuery),'age')
	print(femaleAges)
	paragraphs = ""
	paragraphs += getEmptyParagraph('maleAgeVal',maleAges)
	paragraphs += getEmptyParagraph('femaleAgeVal',femaleAges)
	return paragraphs

def deletePatient(idPatient):
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	deletePatientMDB(dbh,idPatient)

def updatePatient(idPatient,pForm):
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	updatePatientMDB(dbh,idPatient,"cosas")

def restartUsers():
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	deleteAllPatientsMDB(dbh)
	deleteAllMedicinesMDB(dbh)
	deleteAllDiseasesMDB(dbh)
	loadindAllDiseasesMDB(dbh,settings.DISEASES_TXT)
	loadindAllMedicinesMDB(dbh,settings.MEDICINES_TXT)

def addFileToPatient(idPatient,fileName):
	print colored("----------------- eadimos en la ddbb-----------------------" + fileName,'blue')
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)
	idFile = insertFileMDB(idPatient, fileName,dbh)
	addFileToPatientMDB(dbh,idPatient,fileName,idFile)
	print colored("----------------- eadido en la ddbb:" + str(idPatient) + ":" + str(idFile),'blue')

def getDictFilesIds(idPatient):
	dbh = openConectionMDB(settings.HOST_MONGO,settings.PORT_MONGO)	
	filesId = getDictFilesIdsMDB(dbh,idPatient)
	if not filesId:
		return None
	files = []
	for f in filesId:
		files.append(getFileMDB(dbh,f))
	return [files,filesId]

############################### Process request ###############################
def index(request):
	r = renderIndex()
	return HttpResponse(r)

def manejoficheros(request,idPatient):
	try:
		print colored("----------------- empezamos con el manejo de ficheros-----------------------",'blue')
		print colored(request.FILES,'blue')
		for afile in request.FILES.getlist('patientFiles'):
			myfile = afile
			print colored("*-1-*" + str(myfile),'blue')
			fs = FileSystemStorage()
			print colored("*-2-*" + str(fs),'blue')
			filename = settings.MEDIA_ROOT + "/" + myfile.name
			f = open(filename,'w')
			print colored(f,'blue')
			f.write(myfile.read())
			f.close()
	        filename = fs.save(myfile.name, myfile)
	        """print colored("*-3-*" + str(filename),'blue')
	        uploaded_file_url = fs.url(filename)
	        print colored("*-4-*" + str(uploaded_file_url),'blue')
	        filename = settings.MEDIA_ROOT + "/" + myfile.name"""

		for afile in request.FILES.getlist('patientFiles'):
			filename = settings.MEDIA_ROOT + "/" + afile.name
			addFileToPatient(idPatient,filename)

		print colored("-------------------------------------------------- FIN ---------------------------",'blue')
	except:
		print colored("without files",'blue')

@csrf_exempt
def formSingupPatient(request,formu):
	print colored(request,'blue')
	print colored(formu,'blue')
	pForm = request.POST
	pForm = checkSingForm(pForm)
	idPatient = addPatient(pForm)
	redirect = "/formSearchPatient?idPatient=" + str(idPatient)
	manejoficheros(request,idPatient)
	return HttpResponseRedirect(redirect)

def formSearchPatient(request,formu):
	form = str(request).split(" ")[2].split("?")[1].split("'")[0]
	pForm = parsedForm(form)
	print colored(str(pForm),'red')
	isPatient = checkInPatient(pForm)
	print colored(isPatient,"green")
	if not(isPatient):
		return HttpResponseRedirect("/")
	patient = getPatient(pForm)
	print colored(patient,'red')
	r = renderUserPage(patient)
	return HttpResponse(r)

def formCalculateRisk(request,formu):
	form = str(request).split(" ")[2].split("?")[1].split("'")[0]
	idP = form.split("&")[0];
	modelMLName = form.split("&")[1].split("=")[1]
	pForm = parsedForm(idP)
	print colored(form,"green")
	print colored(idP,"green")
	print colored(modelMLName,"green")
	print colored(pForm,"green")
	isPatient = checkInPatient(pForm)
	print colored(isPatient,"green")
	if not(isPatient):
		return HttpResponseRedirect("/")
	patient = getPatient(pForm)
	r = renderRiskUserPage(patient,modelMLName)
	return HttpResponse(r)

def formDeleteUser(request,formu):
	form = str(request).split(" ")[2].split("?")[1].split("'")[0]
	pForm = parsedForm(form)
	isPatient = checkInPatient(pForm)
	print colored(isPatient,"green")
	if not(isPatient):
		return HttpResponseRedirect("/")
	deletePatient(pForm)
	print colored("user delete:" + str(pForm), "green")
	return HttpResponseRedirect("/")

def formRestartUsers(request,formu):
	restartUsers()
	print colored("restart users", "green")
	return HttpResponseRedirect("/")

@csrf_exempt
def formUpdateTest(request,idPatient):
	print colored(request,'blue')
	print colored(request.FILES,'blue')
	print colored(idPatient,'blue')
	manejoficheros(request,idPatient)
	return HttpResponseRedirect('/formSearchPatient?idPatient=' + idPatient)



def downloadCsv(request,user):
	print colored(user,'red')
	response = HttpResponse(content_type='text/csv')
	response['Content-Disposition'] = 'attachment; filename=' + user
	writer = csv.writer(response)
	writer.writerow(['id','age','sex','type','weight', 'height','athletic','smoker','foot','template','leg'])
	if user.split(".")[0] == "users":
		query = {}
		patients = getAllPatients(query)
		patientsToCsv(patients,writer)
	else:
		query = {'idPatient':user.split(".")[0]}
		patient = getPatient(query)
		writer.writerow([patient['idPatient'], patient['age'], patient['sex'], patient['type'], patient['weight'], patient['height'], patient['athletic'], patient['smoker'], patient['flat-concave foot'], patient['template'], patient['leg']])
	return response

def downloadMedicalTest(request,user):
	
	#response['Content-Disposition'] = 'attachment; filename=' + user
	tupla = getDictFilesIds(user)
	if not tupla:
		resp = HttpResponse(content_type='text/json')
		resp['Content-Disposition'] = 'attachment; filename=%s' % user
		return resp

	files = tupla[1]
	filenames = files.keys()

    # Folder name in ZIP archive which contains the above files
    # E.g [thearchive.zip]/somefiles/file2.txt
    # FIXME: Set this to something better
	zip_subdir = str(user)
	zip_filename = "%s.zip" % zip_subdir

    # Open StringIO to grab in-memory ZIP contents
	s = StringIO.StringIO()

    # The zip compressor
	zf = zipfile.ZipFile(s, "w")

	for fpath in filenames:
		fpath = fpath.replace('\u002E','.')
        # Calculate path for file in zip
		fdir, fname = os.path.split(fpath)
		zip_path = os.path.join(zip_subdir, fname)

        # Add file, at correct path
		zf.write(fpath, zip_path)

    # Must close zip for all contents to be written
	zf.close()

    # Grab ZIP file from in-memory, make response with correct MIME-type
	resp = HttpResponse(s.getvalue(), content_type = "application/x-zip-compressed")
    # ..and correct content-disposition
	resp['Content-Disposition'] = 'attachment; filename=%s' % zip_filename

	return resp

	#path = settings.MEDIA_ROOT + "/" + afile.name
	#response = HttpResponse(content_type='application/force-download') # mimetype is replaced by content_type for django 1.7
	#for f in filesKeys:
	#	f = f.replace('\u002E','.')
	#	response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(f)
	#	response['X-Sendfile'] = str(f)
	#	# It's usually a good idea to set the 'Content-Length' header too.
	#	# You can also set any other required headers: Cache-Control, etc.
	#	print colored(f,"red")
	#	return response

############################ Render Pages ####################################
def renderRiskUserPage(userDoc,modelMLName):
	risk = caculateRisk(userDoc,modelMLName)
	template = get_template('userRisk.html')
	c = Context({'idPatient':userDoc['idPatient'],'risk':risk,'modelName':modelMLName})
	render = template.render(c)
	return render

def renderUserPage(userDoc):
	template = get_template('user.html')
	medicines = getPatientMedicines(userDoc['idPatient'])
	diseases = getPatientDiseases(userDoc['idPatient'])
	c = Context({'idPatient':userDoc['idPatient'],'age':userDoc['age'],'sex':userDoc['sex'], 'weight':userDoc['weight'],'height':userDoc['height'],'type':userDoc['type'], 'athletic':userDoc['athletic'], 'smoker':userDoc['smoker'],'foot':userDoc['flat-concave foot'],'template':userDoc['template'],'diseases':diseases, 'medicines':medicines})
	render = template.render(c)
	return render

def renderIndex():
    template = get_template('index.html')
    diseasesForm = getAllDiseases()
    diseasesVal = getDiseasesValues()
    medicinesForm = getAllMedicines()
    medicinesVal = getMedicinesValues()
    typeVal = getTypesPatientsValues()
    ageVal = getAgesPatientValues()
    weightVal = getWeigthPatientValues()
    heightVal = getHeightPatientValues()
    sexAgeRelationVal = getSexAgeRelationValues()
    modelsMLVal = getModelsName()
    c = Context({"diseases":diseasesForm,"medicines":medicinesForm,"diseasesVal":diseasesVal,"medicinesVal":medicinesVal,"typeVal":typeVal,'ageVal':ageVal,'weightVal':weightVal, 'heightVal':heightVal,'sexVal':sexAgeRelationVal, 'modelsML':modelsMLVal})
    render = template.render(c)
    return render
