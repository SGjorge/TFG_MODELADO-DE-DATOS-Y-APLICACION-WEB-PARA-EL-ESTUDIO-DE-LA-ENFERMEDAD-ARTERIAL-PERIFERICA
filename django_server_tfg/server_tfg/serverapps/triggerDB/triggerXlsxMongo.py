#!/usr/bin/env python
# -*- coding: utf-8 -*-
import xlrd
import datetime
import sys
import os

sys.path.append("/home/jorge/tfg/connect_python_to_mongo/")
from api_MDB_server_django import *

def getDiseases(wsheet):
	diseases = wsheet.cell(7, 2).value
	diseases = diseases.split(",")
	lastDiseases = diseases[-1].split('y')
	if (len(lastDiseases) > 1) :
		diseases[-1] = lastDiseases[0]
		diseases.append(lastDiseases[-1])
	return diseases

def getMedicines(wsheet):
	medicines = wsheet.cell(8, 2).value
	medicines = medicines.split(",")
	lastMedicines = medicines[-1].split('y')
	if (len(lastMedicines) > 1) :
		medicines[-1] = lastMedicines[0]
		medicines.append(lastMedicines[-1])
	return medicines

def getTypePatient(wsheet):
	control = wsheet.cell(3, 3).value
	asintomatico = wsheet.cell(4, 3).value
	claudicante = wsheet.cell(5, 3).value
	if(control):
		return "Control"
	if(asintomatico):
		return "Asintomatico"
	if(claudicante):
		return "Claudicante"

def getAge(birthdate):
	now = int(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S").split("-")[0])
	year = int(birthdate[0])
	return (now - year)

def getPatientDic(codePatient,sex,age,hight,weight,typePatient,smoker,athletic,foot,template,leg):
	patientDic = {}
	patientDic['idPatient'] = codePatient
	patientDic['age'] = age
	patientDic['sex'] = sex
	patientDic['height'] = hight
	patientDic['weight'] = weight
	patientDic['typePatient'] = typePatient
	patientDic['smoker'] = smoker
	patientDic['athletic'] = athletic
	patientDic['flat-concave foot'] = foot
	patientDic['template'] = template
	patientDic['leg'] = leg
	return patientDic

def getPatientToXlsx(nameFile):
	wb = xlrd.open_workbook(nameFile)
	wsheet = wb.sheet_by_index(0)
	codigo_paciente = wsheet.cell(1, 2).value
	nombre = wsheet.cell(1, 4).value
	apellido = wsheet.cell(1, 6).value
	fecha_de_nacimiento = xlrd.xldate_as_tuple(wsheet.cell(2, 2).value,0)
	age = getAge(fecha_de_nacimiento)
	altura = wsheet.cell(2, 4).value
	peso = wsheet.cell(2, 6).value
	tipo_de_paciente = getTypePatient(wsheet)
	fumador = wsheet.cell(6, 4).value.encode("utf-8").replace('\xc3\xb1','nn').replace('\xc3\xb3','o').replace('\xc3\xad','i').replace('\xc3\xa9','e').replace('\xc3\xba','u').replace('\xc3\xa1','a')
	atletico = wsheet.cell(9, 2).value.encode("utf-8").replace('\xc3\xb1','nn').replace('\xc3\xb3','o').replace('\xc3\xad','i').replace('\xc3\xa9','e').replace('\xc3\xba','u').replace('\xc3\xa1','a')
	pies_planoscavos = wsheet.cell(10, 2).value.encode("utf-8").replace('\xc3\xb1','nn').replace('\xc3\xb3','o').replace('\xc3\xad','i').replace('\xc3\xa9','e').replace('\xc3\xba','u').replace('\xc3\xa1','a')
	plantillas = wsheet.cell(10, 4).value.encode("utf-8").replace('\xc3\xb1','nn').replace('\xc3\xb3','o').replace('\xc3\xad','i').replace('\xc3\xa9','e').replace('\xc3\xba','u').replace('\xc3\xa1','a')
	pierna_dominante = wsheet.cell(10, 7).value.encode("utf-8").replace('\xc3\xb1','nn').replace('\xc3\xb3','o').replace('\xc3\xad','i').replace('\xc3\xa9','e').replace('\xc3\xba','u').replace('\xc3\xa1','a')
	if(pierna_dominante == "D"):
		pierna_dominante = "Derecha"
	elif(pierna_dominante == "I"):
		pierna_dominante = "Izquierda"
	enfermedades = getDiseases(wsheet)
	medicinas = getMedicines(wsheet)

	dbh = openConectionMDB('localhost',27017)
	idPatient = 'id'+str(getNextIdPatientMDB(dbh))
	dictDoc = getPatientDic(idPatient,'Varon',age,altura,peso,tipo_de_paciente,fumador,atletico,pies_planoscavos,plantillas,pierna_dominante)
	addPatientMDB(dbh,idPatient,dictDoc)

	dictEnf = {}
	for e in enfermedades:
		dictEnf['disease'] = e.lower().strip().encode("utf-8").replace('\xc3\xb1','nn').replace('\xc3\xb3','o').replace('\xc3\xad','i').replace('\xc3\xa9','e').replace('\xc3\xba','u').replace('\xc3\xa1','a')
		addDiseaseMDB(dbh,idPatient,dictEnf)
		
	dictMed = {}
	for m in medicinas:
		dictMed['medicine'] = m.lower().strip().encode("utf-8").replace('\xc3\xb1','nn').replace('\xc3\xb3','o').replace('\xc3\xad','i').replace('\xc3\xa9','e').replace('\xc3\xba','u').replace('\xc3\xa1','a')
		addMedicineMDB(dbh,idPatient,dictMed)


def addAllXlsInformation():
	directory = os.walk('.')

	for dirname, dirnames, filenames in os.walk('./xlsData/'):
		for filename in filenames:

			f = os.path.join(dirname, filename)
			print(f)
			getPatientToXlsx(f)
			
	 
def main():
	addAllXlsInformation()


if __name__ == "__main__":
	main()
