from operator import attrgetter
import matplotlib.pyplot as plt
import re
from datetime import datetime


class dataClass:

	def __init__(self, timestamp, userID, serviceName, subServiceName, startTime, endTime, responseTime, concatServiceName):
		self.timestamp = timestamp
		self.userID = userID
		self.serviceName = serviceName
		self.subServiceName = subServiceName
		self.startTime = startTime
		self.endTime = endTime
		self.responseTime = responseTime
		self.concatServiceName = concatServiceName
		
	# def output(self):
		# print(self.timestamp+", "+self.userID+", "+self.serviceName+", "+self.subServiceName+", "+str(self.startTime)+", "+str(self.endTime)+", "+str(self.responseTime))

def plotGraph(yAxisCount):
	dataSet = []

	#Create a dataset of the startTime for the service name (provided in the function argument)
	for data in logObj:
		if data.concatServiceName==yAxisCount:
			dataSet.append(data.startTime)
	print(yAxisCount)
	
			
	range = (min(dataSet), max(dataSet))
	bin = round(((max(dataSet)-min(dataSet)).seconds)/900)
	if (((max(dataSet)-min(dataSet)).seconds)/900) > int((((max(dataSet)-min(dataSet)).seconds)/900)):
		bin = int((((max(dataSet)-min(dataSet)).seconds)/900)) + 1
	else:
		bin=int((((max(dataSet)-min(dataSet)).seconds)/900))
		
	if bin==0:
		bin=1
	print(bin)
		
	# plotting a histogram
#	plt.hist(dataSet, 10, range, color = 'green',histtype = 'bar', rwidth = 0.5)
	plt.hist(dataSet, bin, range, color = 'green',histtype = 'bar', rwidth = 0.5)

	# x-axis label
	plt.xlabel('Time Stamp')
	# frequency label
	plt.ylabel('Count')
	# plot title
	plt.title(yAxisCount+" (15 min average)" )
	
	#set size - 8" * 6"
	plt.gcf().set_size_inches(20, 10.5)
	
	# function to show the plot
	#plt.show()
	
	#save the plot
	plt.savefig(yAxisCount+".png",bbox_inches='tight')
	
	plt.close('all')




		
logObj = []		

#enter php logfile name here
logfile = open("performance-08-21-2021.log", "rt")
t=0




## Write content of the file into objects
for x in logfile:
	try:
		if x.count("|") == 10:		##check if the row is empty
			splitString=re.sub(r' \[Somno.*INFO  ', "||", x).split("||")	#Remove everythign until "INFO". Then split string at ||
			
			# print(splitString[0])
			# print(splitString[1])
			# print(splitString[2])
			# print(splitString[3])
			# print(datetime.strptime(splitString[4], '%Y-%m-%d %H:%M:%S.%f'))
			# print(datetime.strptime(splitString[5], '%Y-%m-%d %H:%M:%S.%f'))
			# print(datetime.strptime(re.sub(r'\n', "", splitString[6]), '%H:%M:%S').time())
			
			constructedString = dataClass(splitString[0],splitString[1],splitString[2],splitString[3],datetime.strptime(splitString[4], '%Y-%m-%d %H:%M:%S.%f'),datetime.strptime(splitString[5], '%Y-%m-%d %H:%M:%S.%f'),datetime.strptime(re.sub(r'\n', "", splitString[6]), '%H:%M:%S').time(),splitString[2]+"_"+splitString[3])
			logObj.append(constructedString)
			
	except	:
		print("Row " + str(t) + " has bad data")
	t=t+1	

logfile.close()

#Sort the objects in accordance with a parameter - in this case start time - and save it to object list called sorted_logObj
#sorted_logObj = sorted(logObj, key=attrgetter('startTime'))

#Print the contents of the logObj
#for data in logObj:
		#print(data.timestamp+","+data.userID+","+data.serviceName+","+data.subServiceName+","+str(data.startTime)+","+str(data.endTime)+","+str(data.responseTime))
		#print(data.startTime.strftime("%H:%M:%S"))

#Create a graph for the provided Concatenated serviceName_subServiceName
# plotGraph("DmeOrderService_getDmeOrders")
# plotGraph("DmeOrderService_getDmeReportSwfPath")


dataSet2 = []
for data in logObj:
	dataSet2.append(data.serviceName+"_"+data.subServiceName)

sorted_dataSet2 = sorted(dataSet2)

text = ""
for data in sorted_dataSet2:
	if data != text:
		#print(data)
		plotGraph(data)
	text = data
	
