# Parcel Shipping v2
# 03-17-2016

# This script takes parcel shapefiles and associated databases and 
# prepares them for upload to the FTP server.  All data is stored in 
# the project's INC directory which must be input at the beginning
# of the program.

import os, sys, shutil
from shutil import make_archive
from datetime import datetime

print 'GISMO Parcel Shipping Program'
print 'Version 2.0\n'
print '*****\n'

while True:
	try:
		
		#The flag determines what type of ValueError is raised.  1 means 
		#the user input a non-numeric input
		flag = 1
		
		#Get the INC number
		incdir2 = int(raw_input("Enter the INC #: "))
		incdir = 'INC' + str(incdir2) + '/'
		
		#Ask the user if the number is correct
		print 'Data will be stored in directory {0}.  Is this correct?'.format(incdir[0:9])
		q = raw_input('Enter "y" for Yes or any other key for No: ')
		if q != 'y':
		
			#Flag of 2 raises a ValueError and restarts the program
			flag = 2
			raise ValueError

		#Check to see if the directory already exists
		pts_path = '//ccgis1/user/gi/common/PTS_Items/'
		pts_path = pts_path + incdir
			
		if os.path.exists(pts_path) == False:
			print 'Directory does not exist.'
			print 'Creating {0} now.'.format(pts_path)
			os.makedirs(pts_path)

		#Determine what type of request it is
		while True:
			print ' '
			print 'Type of request:'
			print '1. Full Assessor Geodatabase'
			print '2. Full Assessor Shapefile or Specific Book & Section'
			
			choice = int(raw_input('-->'))
		
			if choice in (1,2):
				break
		
			print 'You did not choose wisely.  Try again.'

		#Procedure if Geodatabase
		if choice == 1:
			print ' '
			print 'Full Assessor Geodatabase selected'
			print 'Zipping file.  This will take several minutes...'
			print '...'
			
			gdb_path = '//ccgis1/gisdata/crpcl/geodb'
			
			start = datetime.now()
			
			make_archive(pts_path + '/' + 'Assessor', 'zip', gdb_path)
			
			finished = datetime.now()
			elapsed = finished - start
			minutes = elapsed.seconds / 60.00
			
			print 'Archive created.  Run time: {0} minutes.'.format(minutes)
			print ' '
			
		#Procedure if full shapefile or specific booksec are selected
		if choice == 2:
		
			import arcpy
			from arcpy import env
			
			print ' '
			print 'Full Shapefile or Specific Book & Section selected'
			print ' '
			print 'For the full shapefile, enter a "0" at the prompt.'
			print ' '
			print 'For individual sections, enter the 5 digit booksec number'
			print '  (example: 17832, 00122).'
			print 'If entering multiple sections, hit enter and input the next'
			print '  booksec.'
			print 'When you are finished enter the value "0".'
			print ' '
			
			#Check to see if the PTS directory already exists
			#If it doesn't, create the directory
			if os.path.exists(pts_path + 'parcels/shapes') == False:
				os.makedirs(pts_path + 'parcels/shapes')
			if os.path.exists(pts_path + 'parcels/database') == False:
				os.makedirs(pts_path + 'parcels/database')	
			
			booksec = []
			
			while True:
				value = str(raw_input('-->') + '%')
				if value != '0%':
					booksec.append(value)
				if value == '0%':
					print ' '
					print 'You entered {0} sections.'.format(len(booksec))
					print 'If this is correct, press "y" or any other key if not.'
					for i in booksec:
						print i[0:5]
					choice = raw_input('-->')
					if choice == 'y':
						break
					if choice != 'y':
						flag = 2
						raise ValueError
						
			print '...'
			
			
			#Path to SDE
			sdePath = "Database Connections\\CCENTGIS - Data.sde\\"

			
			#Select and extract spatial data
			#Select the ParcelPoly data from SDE
			infeat = sdePath + "GISMO.GISMO.Assessor\\GISMO.GISMO.AOParcels"
			print 'Extracting data from AOParcels...'
			arcpy.management.MakeFeatureLayer(infeat, "Parcels")
			for i in booksec:
				arcpy.SelectLayerByAttribute_management("Parcels","ADD_TO_SELECTION","APN like " + "'" + i + "'")
			arcpy.FeatureClassToShapefile_conversion("Parcels",pts_path + "parcels/shapes")
			print ' '
			

			
			#Select the SubPoly data from SDE
			infeat = sdePath + "GISMO.GISMO.Assessor\\GISMO.GISMO.AOSubdivisions"
			print 'Extracting data from AOSubdivisions...'
			arcpy.management.MakeFeatureLayer(infeat, "AOSubdivisions")
			for i in booksec:
				arcpy.SelectLayerByAttribute_management("AOSubdivisions","ADD_TO_SELECTION","PCL8 like " + "'" + i + "'")
			arcpy.FeatureClassToShapefile_conversion("AOSubdivisions",pts_path + "parcels/shapes")
			print ' '
			
			
			#The following datasets are copied in their entirety
			#Copy AOBookIndex
			infeat = sdePath + "GISMO.GISMO.Assessor\\GISMO.GISMO.AOBookIndex"
			print 'Copying AOBookindex...'
			arcpy.management.MakeFeatureLayer(infeat, "AOBookIndex")
			arcpy.FeatureClassToShapefile_conversion("AOBookIndex",pts_path + "parcels/shapes")
			print ' '
			
			#Copy AOBookSecIndex
			infeat = sdePath + "GISMO.GISMO.Assessor\\GISMO.GISMO.AOBookSecIndex"
			print 'Copying AOBookSecIndex...'
			arcpy.management.MakeFeatureLayer(infeat, "AOBookSecIndex")
			arcpy.FeatureClassToShapefile_conversion("AOBookSecIndex",pts_path + "parcels/shapes")
			print ' '
			
			#Copy AOPageIndex
			infeat = sdePath + "GISMO.GISMO.Assessor\\GISMO.GISMO.AOPageIndex"
			print 'Copying AOPageIndex...'
			arcpy.management.MakeFeatureLayer(infeat, "AOPageIndex")
			arcpy.FeatureClassToShapefile_conversion("AOPageIndex",pts_path + "parcels/shapes")
			print ' '
			
			#Copy ClarkTRS
			infeat = sdePath + "GISMO.GISMO.CLARKTRS_P"
			print 'Copying ClarkTRS_p...'
			arcpy.management.MakeFeatureLayer(infeat, "ClarkTRS_p")
			arcpy.FeatureClassToShapefile_conversion("ClarkTRS_p",pts_path + "parcels/shapes")
			print ' '
			
		
			#Select and extract the non-spatial data
			#Select records from AOCOM
			intable = sdePath + "GISMO.GISMO.AOCOM"
			print 'Extracting data from AOCOM...'
			arcpy.MakeTableView_management(intable, "AOCOM")
			for i in booksec:
				arcpy.SelectLayerByAttribute_management("AOCOM","ADD_TO_SELECTION","PARCEL like " + "'" + i + "'")
			arcpy.TableToDBASE_conversion("AOCOM",pts_path + "parcels/database")
			print ' '
			
			#Select records from AOEXTRACT
			intable = sdePath + "GISMO.GISMO.AOEXTRACT"
			print 'Extracting data from AOEXTRACT...'
			arcpy.MakeTableView_management(intable, "AOEXTRACT")
			for i in booksec:
				arcpy.SelectLayerByAttribute_management("AOEXTRACT","ADD_TO_SELECTION","PARCEL like " + "'" + i + "'")
			arcpy.TableToDBASE_conversion("AOEXTRACT",pts_path + "parcels/database")
			print ' '
			
			#Select records from AORES
			intable = sdePath + "GISMO.GISMO.AORES"
			print 'Extracting data from AORES...'
			arcpy.MakeTableView_management(intable, "AORES")
			for i in booksec:
				arcpy.SelectLayerByAttribute_management("AORES","ADD_TO_SELECTION","PARCEL like " + "'" + i + "'")
			arcpy.TableToDBASE_conversion("AORES",pts_path + "parcels/database")
			print ' '
			
			#Select records from AOROW
			intable = sdePath + "GISMO.GISMO.AOROW"
			print 'Extracting data from AOROW...'
			arcpy.MakeTableView_management(intable, "AOROW")
			for i in booksec:
				arcpy.SelectLayerByAttribute_management("AOROW","ADD_TO_SELECTION","PARCEL like " + "'" + i + "'")
			arcpy.TableToDBASE_conversion("AOROW",pts_path + "parcels/database")
			print ' '
			
			#Select records from AOSALES
			intable = sdePath + "GISMO.GISMO.AOSALES"
			print 'Extracting data from AOSALES...'
			arcpy.MakeTableView_management(intable, "AOSALES")
			for i in booksec:
				arcpy.SelectLayerByAttribute_management("AOSALES","ADD_TO_SELECTION","PARCEL like " + "'" + i + "'")
			arcpy.TableToDBASE_conversion("AOSALES",pts_path + "parcels/database")
			print ' '
			
			print ' '
			print 'Finished exporting layers and tables.'
			print ' '
		
		raw_input('Enter any key to close.')
		break
		
		
	except ValueError:
		if flag == 1:
			print 'You broke something.'
			print 'Restarting program...'
			print ' '
		if flag == 2:
			print 'Re enter your input.'