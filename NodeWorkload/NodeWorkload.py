from operator import attrgetter
import matplotlib.pyplot as plt
import re
from datetime import datetime
import sys
import os

class dataClass:

	def __init__(self, urlPath, timeStamp):
		self.urlPath = urlPath
		self.timeStamp = timeStamp
		

def plotGraph(yAxisCount, style, startDate1, endDate1):
	dataSet = []

	#ask user for dates
	startDate = datetime.strptime( startDate1, '%Y-%m-%d %H:%M:%S.%f')
	endDate = datetime.strptime( endDate1, '%Y-%m-%d %H:%M:%S.%f')	
	
	#Create a dataset of the timeStamp for the urlPath (provided in the function argument)
	for data in logObj:
		
		#When a particular service name is provided
		if yAxisCount != "CompleteSet":
			if data.urlPath==yAxisCount:
				if ( data.timeStamp >= startDate and data.timeStamp <=endDate ):
					dataSet.append(data.timeStamp)
		
		#When a service name is not provided, rather user wants the workload of all service names combined
		if yAxisCount == "CompleteSet":
				if ( data.timeStamp >= startDate and data.timeStamp <=endDate ):
					dataSet.append(data.timeStamp)

			
	#print(min(dataSet))
	#print(max(dataSet))
	#print( (max(dataSet)-datetime(1970,1,1)).total_seconds()-(min(dataSet)-datetime(1970,1,1)).total_seconds() )
	
	#save the plot, when style=="Bulk"
	if style=="Bulk":
		#print(yAxisCount + " - " + str(len(dataSet)))
		return(yAxisCount + " - " + str(len(dataSet)))
		
	# function to show the plot, when style=="Individual"
	if style=="Individual":

		
		if len(dataSet) != 0 :
				
			range = (min(dataSet), max(dataSet))
			timeDiff = (max(dataSet)-datetime(1970,1,1)).total_seconds()-(min(dataSet)-datetime(1970,1,1)).total_seconds()
			
			if ( ( (timeDiff)/3600 ) > int( (timeDiff)/3600 ) ):
				bin = int( (timeDiff)/3600 ) + 1
			else:
				bin=int( (timeDiff)/3600 )
				
			if bin==0:
				bin=1
			#print(bin)
			
			# plotting a histogram
		#	plt.hist(dataSet, 10, range, color = 'green',histtype = 'bar', rwidth = 0.5)
			plt.hist(dataSet, bin, range, color = 'green',histtype = 'bar', rwidth = 0.5)

			# x-axis label
			plt.xlabel('Time Stamp')
			# frequency label
			plt.ylabel('Count')
			# plot title
			plt.title(yAxisCount+" (60 min average)" )
			
			#set size - 8" * 6"
			plt.gcf().set_size_inches(10, 5)
			

			print(yAxisCount + " graph is now open. Close the graph to continue.....")
			plt.show()
			plt.close('all')
			wayToTheGraph()
		

				
		else:
			print(yAxisCount + " url was not found in the logs for the period you provided")


		input("Press Any key to continure....")
		wayToTheGraph()
		
		
		
		

def wayToTheGraph():
	print("")
	print("Option 1 - To view workload of a any single service - Type the url path at prompt and press enter (The url path is provided in the file named 'serviceNames.txt'. Please copy paste the entire row, and paste it at prompt, and press Enter")
	print("Option 2 - To view workload of all services combined - Type 'CompleteSet' at prompt and press Enter")
	print("Option 3 - To save workload counts into an output file - Type 'Bulk' at prompt and press Enter. (Workload Count will be calculated for every url in the 'servicenmaes.txt' file. Please Edit the file if you want to do so)")
	print("or type 'Quit' to exit....")
	serviceName=input(">") 	
	
	if ( serviceName != 'Quit' and serviceName != 'quit' ):
	
		startDate1 = input("Enter Start Time (yyyy-mm-dd HH:MM:SS): ") + ".000"
		endDate1 = input("Enter End Time (yyyy-mm-dd HH:MM:SS): ") + ".999"
	
		if serviceName != "Bulk":
			plotGraph(serviceName, "Individual", startDate1, endDate1)
		
		if serviceName == "Bulk":
			print("")
			print("Processing....")
			print("")
			f1 = open('serviceNames.txt', 'rt')
			f2 = open('BulkOutput.txt', 'w')
			for y in f1:
				f2.write( (plotGraph(y.replace("\n",""), "Bulk", startDate1, endDate1))  + "\n")
				
			f1.close()
			f2.close()
			input("Workload  output is in the 'BulkOutput' file. Press any key to continue.....")
			wayToTheGraph()
			
	sys.exit()


		
logObj = []		

#Open every app file in the directory
for filename in os.listdir():
	if filename.count("app") != 0:
		print("Parsing " + filename + " .......")

		#enter php logfile name here
		logfile = open(filename, "rt")
		t=0




		## Write content of the file into objects
		for x in logfile:
			try:
				if x.count("path") != 0:		##check if the row is empty

					urlPathInLog=x.rsplit('path\":\"')[1].split('\"},\"msg\":\"\",\"time\":\"')[0]
					
					if ( (urlPathInLog.count(".") == 0) or (urlPathInLog.count("viewer.html") > 0) ):
						if urlPathInLog.count("viewer.html") > 0:
							urlPathInLog=urlPathInLog.split('&')[0]
						timeStampInLog=datetime.strptime(x.rsplit('path\":\"')[1].split('\"},\"msg\":\"\",\"time\":\"')[1].split('Z\",\"v\"')[0], '%Y-%m-%dT%H:%M:%S.%f')
						#print(urlPath + " ," + timeStamp)
						
						
						constructedString = dataClass(urlPathInLog, timeStampInLog)
						logObj.append(constructedString)
				#else:
					#print("Row " + str(t+1) + " in " + filename +" has no 'path' string")
			except	:
				 print("Row " + str(t) + "in " + filename + " has bad data")
			t=t+1	

		logfile.close()

		
dataSet2 = []

for data in logObj:
	dataSet2.append(data.urlPath)

sorted_dataSet2 = sorted(dataSet2)

f = open("serviceNames.txt", "w")

text = ""
for data in sorted_dataSet2:
	if data != text:
		#print(data)
		f.write(data + "\n")
	text = data

f.close()

print(" ")
print ("All the logs in the current directory have been parsed")
print("All the service names from these logs have now been written into the file named 'serviceNames.txt' in the current directory") 
	
wayToTheGraph()



