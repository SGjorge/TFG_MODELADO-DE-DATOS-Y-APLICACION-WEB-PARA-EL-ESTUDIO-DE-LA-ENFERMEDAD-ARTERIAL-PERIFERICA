
def getModelsName():
	models = "<option value='dummyModel1' selected='selected'>dummyModel1</option>"
	models += "<option value='dummyModel2'>dummyModel2</option>"
	return models

def caculateRisk(userDoc,modelMLName):
	if(modelMLName == "dummyModel1"):
		return dummyModel1(userDoc)
	else:
		return dummyModel()

def dummyModel():
	return 0.5

def dummyModel1(userDoc):
	return 0.1