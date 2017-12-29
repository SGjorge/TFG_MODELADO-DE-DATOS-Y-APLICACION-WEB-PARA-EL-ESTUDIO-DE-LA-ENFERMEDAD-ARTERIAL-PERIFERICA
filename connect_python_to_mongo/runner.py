"""
Contains the class to control runners in the application
@author: Oscar Barquero Perez
@date: 1-November-2015
"""

import pymongo
from pymongo import MongoClient
import gridfs
import numpy as np
from easygui import *
from os.path import *
import shutil as sh


class Runner:
    """
    This class control the runner element in the application
    """

    def __init__(self, runner_dic = None):
        """
        Initializes variables in runner class
        :return:init
        """
        self.name = ""
        self.last_name = ""
        self.weight = 0 #kg => this will be override in the mongodb app
        self.height = 0 #cm
        self.runner_id = ""  #passport or dni
        self.firstbeat_file_read = False

        if runner_dic != None:
            # TODO use information from runner_dic (given by the ddbb) to complete this information
            self.name = runner_dic["name"]
            self.last_name = runner_dic["last_name"]
            self.weight = runner_dic["weight"] #kg => this will be override in the mongodb app
            self.height = runner_dic["height"] #cm
            self.runner_id = runner_dic["runner_id"]  #passport or dni
            self.firstbeat_file_read = False

    def set_runner_data(self, name, last_name, weight, height, runner_id):
        """
        :param name:
        :param last_name:
        :param weight:
        :param height:
        :param runner_id:
        :return: void
        """
        # TODO implement a method that get runner_dic as an argument (using the data given by the ddbb) and complete all
        # the data

        self.name = name
        self.last_name = last_name
        self.weight = weight
        self.height = height
        self.runner_id = runner_id

    def get_dict(self):
        """
        Creates a dictionary to get inserted into mongodb from a runner object
        :return: dictionary runn
        """
        dict_r = {'name': self.name, 'last_name': self.last_name, 'weight': self.weight, 'height': self.height, 'runner_id': self.runner_id}

        return dict_r

    def get_firstbeat_file(self,filename = None):
        """
        This method creates a dictionary
        :param filename: filename of the firstbeat file in sdf format with a measurement of hrv
        :return rr_time_series_metadata: dictionary with metadata from the firstbeat file to be stored in the database.
        Also there is need for two more fields: sdf_id= id in the gridfs database for sdf file; and txt_id = id in the
        gridfs database for the txt with only the rr intervals file.
        """
        if filename is None:
            # ask for a file input
            print("Insert the complete path of the firstbeat filename in .sdf format\n")
            filename_path = raw_input("Filename: ")

        rr_time_series_metadata = {'runner': "", 'date': None, 'start_time': None, 'filename': None}
        # open the file and read metadata
        #
        # File structure:
        # 1) In the filename there is information about the runner and data
        # e.g.: hermenegildo_prior_id_XXXXXXXXL_01_01_1947_10_00_00.sdf
        #
        # 2) Inside the file, the first rows is some header with the following structure:
        # [HEADER]
        # NOTES=
        # STARTTIME=01.11.2015 15:59.02
        # [POINTS]
        # [CUSTOM1]
        #
        # 3) Below are the RR intervals

        # Gather all the information

        # find the name: text before the second '_'

        filename_data = basename(filename)

        idx_ = [n for n in xrange(len(filename_data)) if filename_data.find('_',n) == n]
        idx_point = filename_data.index('.')
        runner_name = filename_data[0:idx_[1]]
        dni = filename_data[idx_[2]+1:idx_[3]]
        date = filename_data[idx_[3]+1:idx_[6]]
        start_time = filename_data[idx_[6]+1:idx_point]
        rr_time_series_metadata["runner"] = runner_name
        rr_time_series_metadata["filename"] = filename
        rr_time_series_metadata["date"] = date
        rr_time_series_metadata["start_time"] = start_time

        #indicates that firstbeat is reading
        self.firstbeat_file_read = True

        return rr_time_series_metadata, filename



class MongodbConnection:
    """
    This class allows to interact with mongodb to insert runners in it
    """

    def __init__(self):
        """
        Initializes the connection if db is passed as argument. Otherwise does nothing
        :return:
        """

        self.connection = MongoClient("localhost")
        self.db = self.connection.running_hrv
        self.runners = self.db.runners

    def check_runner(self, runner_id):
        """
        Check if a runner is in the ddbb. If the runner is not in the ddbb then it returns false
        :param runner_id:
        :return: runner_in_ddbb = False if the runner is not in the ddbb
        """
        runner_in_ddbb = True
        run_ddbb = self.runners.find_one({"runner_id":runner_id}, {"_id": runner_id})

        if not run_ddbb:
            runner_in_ddbb = False

        return runner_in_ddbb


    def insert_runner(self,runner_obj):
        """
        :param runner_obj: is an object of the class runner
        :return:
        """
        dict_runner = runner_obj.get_dict()
        self.runners.insert(dict_runner)

    def insert_firstbeat_file(self, runner_id, filename_path):
        """
        Insert a firstbeat file into database.
        In runners collection
        db.runners.update({},{$push:{"rr_files_3":{"new_doc":2}}})
        :return:
        """
        # TODO use this check if runner_obj.firstbeat_file_read == False:
        # TODO check if a runner is passed by argument
        # 1) Ask for a runner

        # print("Insert the complete DNI to select a runner (12345678L)\n")
        #dni = raw_input("DNI: ")

        # runner_id = runner_obj.runner_id

        runner_dic = self.runners.find_one({"runner_id": runner_id})

        runner_obj = Runner(runner_dic)

        # get metadata from file using running_obj

        rr_time_series_metadata, foo = runner_obj.get_firstbeat_file(filename_path)

        # 2) Save the firstbeat.sdf file into ddbb gridfs
        grid = gridfs.GridFS(self.db,"firstbeat_sdf_files")
        with open(filename_path, "r") as fin:
            sdf_id = grid.put(fin)

        # 2) Extract the rr intervals and create an rr.txt file to be saved
        rr_interval_raw = np.genfromtxt(filename_path,skip_header = 5)

        #save into txt
        filename = basename(filename_path)
        filename_txt = filename[0:-3]+"txt"
        filename_txt_path = join(dirname(filename_path),filename_txt)
        np.savetxt(filename_txt_path,rr_interval_raw)

        #save into the ddbb
        with open(filename_txt_path, "r") as fin:
            txt_id = grid.put(fin)

        # 3) Link the rr_times_series array to the files: a) firstbeat.sdf and rr.txt
        #build dic to save
        rr_time_series_metadata["firstbeat_file_id"] = sdf_id
        rr_time_series_metadata["rr_txt_id"] = txt_id
        rr_time_series_metadata["sdf_filename"] = filename # TODO check if the file is already into the ddbb

        # 4) Move files into folder for already into ddbb files
        into_ddbb_files_path = '/home/obarquero/Documents/runners_app/running_hrv/firstbeat_files/firstbeat_in_ddbb'
        sh.move(filename_path,join(into_ddbb_files_path, filename)) #move sdf file
        sh.move(filename_txt_path,join(into_ddbb_files_path, filename_txt)) #move txt file

        result = self.runners.update_one({"runner_id": runner_dic["runner_id"]},{'$push': {'rr_intervals_hrv_analysis': rr_time_series_metadata}})
        return result


# TODO work on a gui interface
"""
class GuiInterface:

    def __init__(self):


    def mainMenu
"""

def get_runner_data_gui():
    """
    Function that prompt text edit boxes to introduce a new runner into the database
    It calls runner and connection to store the new runner into data base
    :return: fieldValues: a list of the values enter for the runner
    """
    msg = "Enter runner information"
    title = "Runner app"
    fieldNames = ["Name","Last Name","ID","Repeat ID","Weight (kg)","Height (cm)"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = multenterbox(msg,title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "": break # no problems found
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

    return fieldValues


def get_sdf_gui():
    """
    Function that opens a window to open a file and then return the complete path to store the sdf file into a runner
    :return: runner_id,
             filepath
    """

    # First get runner_id to store the sdf
    msg = "Select runner id to store the sdf file"
    title = "Runner app"
    fieldNames = ["Runner ID"]
    fieldValues = []  # we start with blanks for the values
    fieldValues = multenterbox(msg,title, fieldNames)

    # make sure that none of the fields was left blank
    while 1:
        if fieldValues == None: break
        errmsg = ""
        for i in range(len(fieldNames)):
            if fieldValues[i].strip() == "":
                errmsg = errmsg + ('"%s" is a required field.\n\n' % fieldNames[i])
        if errmsg == "": break # no problems found
        fieldValues = multenterbox(errmsg, title, fieldNames, fieldValues)

    runner_id = fieldValues[0]

    # Now open file open window
    filepath = fileopenbox(title = "Choose sdf file for runner ID: "+runner_id, filetypes = ["*.sdf"])

    return runner_id, filepath

mn_db = MongodbConnection()
choice = 1

while choice != None:

    msg ="Select your action"
    title = "Runner DB managment"
    choices = ["Insert a new runner", "Insert a new RR-interval time series (.sdf file)"]
    choice = choicebox(msg, title, choices)

    if choice == choices[0]:
        # open the easygui window to gather runner data
        runner_data = get_runner_data_gui()
        # TODO check if runner_data[2]==runner_data[3] compare id repeated
        runner_in_ddbb = mn_db.check_runner(runner_data[2])

        if runner_in_ddbb:
            msgbox("Runner is already in the ddbb. No action perform")
        else:
            r_1 = Runner()
            r_1.set_runner_data(runner_data[0], runner_data[1], int(runner_data[4]), int(runner_data[5]), runner_data[2])
            mn_db.insert_runner(r_1)


    elif choice == choices[1]:
        # open the easygui window to gather sdf, id data and input the sdf file into ddbb.
        runner_id, filepath = get_sdf_gui()
        mn_db.insert_firstbeat_file(runner_id, filepath)
# get runner data

    # TODO recover rr interval time series from ddbb
    # TODO print a message of exit when the insert of a file is done or when the insert of a new runner is done ok

"""
name = raw_input("Name: ")
last_name = raw_input("Last name: ")

# TODO implement exception catching in the inputs

weight = input("Weight (kg): ")
height = input("height (cm): ")
runner_id = raw_input("ID :")

# TODO check if there exists that runner


r_1.set_runner_data(name, last_name, weight, height, runner_id)
"""



