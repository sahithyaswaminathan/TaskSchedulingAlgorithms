import operator

import sys
import random


TASKGEN = {} #Mapping node-name to node-type.
TYPE_EXE = {} #Mapping type to node name and hence to execution time
RANKGEN = {}

num_process = int(sys.argv[2])

class Node:
    
    def __init__ (self, name):
        self.name = name
        self.type = ""
        self.parent = []
        self.child = []
        self.exec_time = ""
        self.rank = ""
        self.ast = 0.0
        self.aft = 0.0
        self.frequency = 0.0
        self.voltage = 0.0
        self.energy = 0.0
        self.lft = 0.0
        self.slack=0.0
        
    def nodeName(self):
        return self.name
        
    def nodeType(self):
        return self.type
    
    def setType(self,node_type):
       self.type = node_type
    
    def nodeParent(self):
        return self.parent
    
    def setParent(self,parent):
        self.parent = parent
    
    def nodeChild(self):
        return self.child
    
    def setChild(self, child):
        self.child = child
    
    def nodeExec(self):
        return self.exec_time
    
    def setExec(self,exec_time):
        self.exec_time = exec_time
        
    def getSlackTime(self):
        return self.slack
    
    def setSlackTime(self,slack):
        self.slack=slack
        
    def setStartSlack(self,start_slack):
        self.start_slack=start_slack
        
    def getStartSlack(self):
        return self.start_slack
    
    def getEndSlack(self):
        return self.end_slack
    
    def setEndSlack(self,end_slack):
        self.end_slack=end_slack
        
    def getRank(self):
        return self.rank

    def setRank(self, rank):
        self.rank = rank
        

        
def updateNodeExecution (node_type,exec_time):
        if node_type in TYPE_EXE:
            nodes = TYPE_EXE[node_type]
            for node in nodes:
                nodeobject = TASKGEN[node]
                nodeobject.setExec(exec_time)


##############################################################################

###Class to store the results###

class ResultsContainer:
	def __init__ (self):
		w, h = len(TASKGEN), num_process
		emptyMatrix = [[0 for x in range(w)] for y in range(h)]
		self.initialMatrix = emptyMatrix
		self.probabilityMatrix = emptyMatrix
		self.processorHighestValues = {}
		self.procToSumOfExecTimes = {} #Makespan
		self.localTrialsSummedUpMatrix = emptyMatrix
		self.resultSummedUpMatrix = emptyMatrix

	def getInitialMatrix(self):
		return self.initialMatrix


	def setInitialMatrix(self, _initialMatrix):
		self.initialMatrix = _initialMatrix

	def getProbabilityMatrix(self):
		return self.probabilityMatrix

	def setProbabilityMatrix(self, _probabilityMatrix):
		self.probabilityMatrix = _probabilityMatrix

	def getProcessorHighestValues(self):
		return self.processorHighestValues

	def setProcessorHighestValues(self, _processorHighestValues):
		self.processorHighestValues = _processorHighestValues

	def getMakespan(self):
		return self.procToSumOfExecTimes

	def setMakespan(self, _procToSumOfExecTimes):
		self.procToSumOfExecTimes = _procToSumOfExecTimes

	def getLocalTrialsSummedUpMatrix(self):
		return self.localTrialsSummedUpMatrix

	def setLocalTrialsSummedUpMatrix(self, _localTrialsSummedUpMatrix):
		self.localTrialsSummedUpMatrix = _localTrialsSummedUpMatrix

	def getResultSummedUpMatrix(self):
		return self.resultSummedUpMatrix

	def setResultSummedUpMatrix(self, _resultSummedUpMatrix):
		self.resultSummedUpMatrix = _resultSummedUpMatrix


###############################################################################
################  READING THE FILE ############################################

###############################################################################
#Read Lines in final.tgff file
file_name = open (sys.argv[1], "r")
line = file_name.readlines()
line = [elem.strip() for elem in line] #strip() for eliminating tab
print (line)
###############################################################################
#Remove spaces and \t \n  in the lines 
line = [elem.strip('#') for elem in line]
        
update_exe=0

update_st =0


for elem in line:
    #For Storing the nodename with nodetype: If the nodename starts with TASK:
    if elem.startswith("TASK"):
        field = elem.split()
        node_name = field[1]
        node_type = field[3]
        
        if node_name in TASKGEN:
               print(node_name+ "present in TASKGEN")
        else:
               node = Node(node_name)
               node.setType(node_type)
               TASKGEN[node_name] = node #Key: node_name=string; Value: class object. Assigning an object value to the key of that dictionary
        #Mapping node name to TYPE_EXE 
        if node_type in TYPE_EXE:
                n_type = TYPE_EXE[node_type] #Key of the dictionary must be present in the square braces
                n_type.append(node_name)
        else:
                n_type = []
                n_type.append(node_name)
                TYPE_EXE[node_type] = n_type# Key: nodetype: integer Value: nodename:String
    #For storing the children of each parent node:        
    if elem.startswith("ARC"):
         field_arc = elem.split()
         parent = field_arc[3]
         child = field_arc[5]
         node_type_arc = field_arc[7]
         parent_node = TASKGEN[parent] #Accessing the parent node on TASKGEN
         parent_node.nodeChild().append(child)
         child_node = TASKGEN[child]
         child_node.setParent(parent)
        

    #To find the execution time of each node:
    if(elem.find("exec_time") != -1):
            update_exe = 1
    if (update_exe and not elem.startswith("}")):
            ex = elem.split()#array of values:
            if len(ex) > 0:# to check if the length of each node is greater than 0
                node_type = ex[0]
                exec_time = ex[1]
                updateNodeExecution(node_type, exec_time)
                print("Nodetype: "+node_type+" : Exec Time: "+exec_time)
    if elem.startswith("}") and update_exe:
              update_exe = 0


    #To store the slack time of each node:
    if (elem.find("start_time") != -1):
        print("Inside")
        update_st = 1
    if (update_st and not elem.startswith("}")):
        st = elem.split()
        if len(st) > 0:
            node_type = st[0]
            node_st = st[1]
            if node_type in TYPE_EXE:
                nodes = TYPE_EXE[node_type]
                for node in nodes:
                    y = TASKGEN[node]
                    y.setSlackTime(node_st)
                print("Nodetype: "+node_type+" : Slack Time: "+node_st)
    if elem.startswith("}") and update_st:
        update_st = 0
###############################################################################
#To get the Rank Value: using the execution time of the predecessor nodes:

def getMaximum(bottoms):
    maxvalue = bottoms[0]
    for bottom in bottoms:
        if bottom > maxvalue:
            maxvalue = bottom
    return maxvalue

def getRankValue(node):
    child = node.nodeChild()
    exec_time = node.nodeExec()
    if len(child) ==2:#If the child is greater than 2
        rank1 = getRankValue(TASKGEN[child[0]])
        rank2 = getRankValue(TASKGEN[child[1]])
        if float(rank1) > float(rank2):
            max_time = rank1
        else:
            max_time = rank2
        node.setRank(float(max_time)+float(exec_time))
        RANKGEN[node] = float(max_time)+float(exec_time)
        print(":"+str(RANKGEN[node]))
        return float(max_time)+float(exec_time)
    
    elif len(child) == 1:#If the child is 1
        max_time = getRankValue(TASKGEN[child[0]])
        node.setRank(float(max_time)+float(exec_time))
        RANKGEN[node] = float(max_time)+float(exec_time)
        print(":"+str(RANKGEN[node]))
        return float(max_time)+float(exec_time)
    
    elif len(child) >= 3:
        rank = [] #Children 
        for child_node in child:
            rank.append(getRankValue(TASKGEN[child_node]))
        if len(rank) > 0:
            max_time = getMaximum(rank)
            node.setRank((float(max_time) + float(exec_time)))
            TASKGEN[node] = float(max_time) + float(exec_time)
            return float(max_time) + float(exec_time)
        else:
            return 0
    
    else:
        node.setRank(exec_time)
        RANKGEN[node] = float(exec_time)
        print(":"+str(RANKGEN[node]))
        return exec_time
    
###############################################################################
#TO SORT THE RANK VALUES IN DESCENDING ORDER:  
for n in TASKGEN:
    nodeobject=TASKGEN[n]
    rankvalue =  getRankValue(nodeobject)

sortvalue = sorted(RANKGEN, key= RANKGEN.get)# Returns list of keys : based on values. key: node object ; value: rank value
print("Sorted:")
for k in sortvalue:
    sortvalue[0].setSlackTime(0)
    print(k.getSlackTime())

###############################################################################

#############################################################################

#Generate probability matrix

def generateProbabilityMatrix(Matrix):
	processorsCount = num_process
	nodeCount = 0
	procCount = 0
	sum = {}
	processorNodeRank = {}
	for nodename in TASKGEN:
		sumValue = 0
		while procCount < processorsCount:
			sumValue = sumValue + Matrix[procCount][nodeCount]
			procCount = procCount + 1
		sum[nodeCount] = sumValue
		nodeCount = nodeCount + 1
		procCount = 0


	procCount = 0
	nodeCount = 0
	while procCount < processorsCount:
		sumValue = 0
		for nodename in TASKGEN:
			nodeobject = TASKGEN[nodename]
			sumValue = sumValue + float(nodeobject.getRank())
			nodeCount = nodeCount + 1
		processorNodeRank[procCount] = sumValue
		procCount = procCount + 1
		nodeCount = 0


	nodeCount = 0
	procCount = 0
	while procCount < processorsCount:
		for nodename in TASKGEN:
			nodeobject = TASKGEN[nodename]
			currval = Matrix[procCount][nodeCount]
			newval = ( ((Matrix[procCount][nodeCount])**ALPHA) * (float(nodeobject.getRank()) ** BETA) ) / ( (processorNodeRank[procCount] ** BETA) * sum[nodeCount] )
			Matrix[procCount][nodeCount] = newval
			nodeCount = nodeCount + 1
		procCount = procCount + 1
		nodeCount = 0
	return Matrix

##############################################################################  

def dislayMatrix(Matrix):
	processorsCount = num_process
	nodeCount = 0
	procCount = 0            
	while procCount < processorsCount:
		for nodename in TASKGEN:
			nodeCount = nodeCount + 1
		procCount = procCount + 1
		nodeCount = 0

##############################################################################    

def getHighestValueUtil(Matrix, value, markedMatrix):
	highestVal = 0.0
	highestProcno = 0
	highestNodeno = 0
	processorsCount = num_process
	nodeCount = 0
	procCount = 0            
	while procCount < processorsCount:
		for nodename in TASKGEN:
			if(Matrix[procCount][nodeCount] > highestVal and Matrix[procCount][nodeCount] <= value and markedMatrix[nodeCount] != 1):
				#print('Inside')
				highestVal = Matrix[procCount][nodeCount]
				highestProcno = procCount
				highestNodeno = nodeCount
			nodeCount = nodeCount + 1
		procCount = procCount + 1
		nodeCount = 0
	markedMatrix[highestNodeno] = 1
	return highestProcno, highestNodeno, highestVal, markedMatrix

##############################################################################

def computeHighestValue(Matrix):
	nodeCount = 0
	value = 1000.0 #sys.float_info.max
	print('###################################################################################################')
	w, h = len(TASKGEN), num_process
	markedMatrix = {}
	while nodeCount < len(TASKGEN):
		markedMatrix[nodeCount] = 0
		nodeCount = nodeCount + 1
	
	processorHighestValues = {}
	nodeCount = 0
	while nodeCount < len(TASKGEN):
		procNo, nodeNo, value, markedMatrix = getHighestValueUtil(Matrix, value, markedMatrix)
		nodeCount = nodeCount + 1
		nodeToValueDict = {}
		nodeToValueDict[nodeNo] = value
		if procNo in processorHighestValues:
			(processorHighestValues[procNo]).append(nodeToValueDict)
		else:
			tmpList = []
			tmpList.append(nodeToValueDict)
			processorHighestValues[procNo] = tmpList
	
	return processorHighestValues

###############################################################################3

def computeMakespan(processorHighestValues):
	procToSumOfExecTimes = {}
	for proc in processorHighestValues:
		nodeToExecTimeList = processorHighestValues[proc]
		for item in nodeToExecTimeList:
			nodeToExecTime = item
			for node in nodeToExecTime:
				print(str(node)+" : "+str(nodeToExecTime[node]))
				if proc in procToSumOfExecTimes:
					procToSumOfExecTimes[proc] = procToSumOfExecTimes[proc] + nodeToExecTime[node]
				else:
					procToSumOfExecTimes[proc] = nodeToExecTime[node]
	return procToSumOfExecTimes


############################################################################## 

def sumMatrix(Matrix, initialMatrixCopy):
	w, h = len(TASKGEN), num_process
	sumMatrix = [[0 for x in range(w)] for y in range(h)]
	nodeCount = 0
	procCount = 0            
	while procCount < processorsCount:
		for nodename in TASKGEN:	
			sumMatrix[procCount][nodeCount] = Matrix[procCount][nodeCount] + initialMatrixCopy[procCount][nodeCount]			
			nodeCount = nodeCount + 1
		procCount = procCount + 1
		nodeCount = 0
	return sumMatrix


#############################################################################

def computeLocalTrials(Matrix, initialMatrixCopy):
	nodeCount = 0
	procCount = 0            
	while procCount < processorsCount:
		for nodename in TASKGEN:
			Matrix[procCount][nodeCount] = (1 - ROW_1) * Matrix[procCount][nodeCount]
			nodeCount = nodeCount + 1
		procCount = procCount + 1
		nodeCount = 0
	summedUpMatrix = sumMatrix(Matrix, initialMatrixCopy)
	return summedUpMatrix


##############################################################################

def sumSummedUpMatrixAndHighestValMatrix(summedUpMatrix, highestValMarix):
	nodeCount = 0
	procCount = 0 
	while procCount < processorsCount:
		for nodename in TASKGEN:
			summedUpMatrix[procCount][nodeCount] = (1 - ROW_2) * summedUpMatrix[procCount][nodeCount]
			highestValMarix[procCount][nodeCount] = (1 - ROW_3) * highestValMarix[procCount][nodeCount]
			nodeCount = nodeCount + 1
		procCount = procCount + 1
		nodeCount = 0
	summedUpMatrix = sumMatrix(summedUpMatrix, highestValMarix)
	return summedUpMatrix


##############################################################################

def computeHighestValMatrix(processorHighestValues):
	w, h = len(TASKGEN), num_process
	highestValMatrix = [[0 for x in range(w)] for y in range(h)]
	for proc in processorHighestValues:
		nodeToExecTimeList = processorHighestValues[proc]
		for item in nodeToExecTimeList:
			nodeToExecTime = item
			for node in nodeToExecTime:
				highestValMatrix[proc][node] = 1
	return highestValMatrix



##############################################################################

def computeProcessorToTaskMapping(resultSummedUpMatrix):
	processorsCount = num_process
	nodeCount = 0
	procCount = 0 
	processor2taskmap = {}
	for nodename in TASKGEN:  
		highestVal = Matrix[procCount][nodeCount]
		highestproc = procCount         
		while procCount < processorsCount:	
			#print(str(Matrix[procCount][nodeCount])+"	", end = '')  
			if Matrix[procCount][nodeCount] > highestVal:
				highestVal = Matrix[procCount][nodeCount]
				highestproc = procCount
			procCount = procCount + 1
		if highestproc in processor2taskmap:
			(processor2taskmap[highestproc]).append(nodename)
		else:
			nodes = []
			nodes.append(nodename)
			processor2taskmap[highestproc] = nodes
		nodeCount = nodeCount + 1
		procCount = 0

	print('Processor and the tasks assigned to it...')
	print("")
	print("   "+str(processor2taskmap))
	print("")
	for proc in processor2taskmap:
		print("Processor "+str(proc)+" is assigned to tasks: ")
		for task in processor2taskmap[proc]:
			print(" _______________________________________________Task: "+task)
		print("")
	print("")
	print("")
	print("")
	return processor2taskmap


##############################################################################

def computeScheduleLength(processor2taskmap):
	processor2ScheduleLength = {}
	for processor in processor2taskmap:
		procScheduleLength = 0.0
		tasks = processor2taskmap[processor]
		for task in tasks:
			nodeobject = TASKGEN[nodename]
			procScheduleLength = procScheduleLength  + float(nodeobject.nodeExec())
		processor2ScheduleLength[processor] = procScheduleLength
	return processor2ScheduleLength

##############################################################################       
#Displaying the results:
for nodename in TASKGEN:
       nodeobject =  TASKGEN[nodename]
       print("      Node Name: "+str(nodename))
       print("		Type: "+str(nodeobject.nodeType()))
       print("		Parent: "+str(nodeobject.nodeParent()))
       print("		Child count: "+str(len(nodeobject.nodeChild())))
       print("		Exec. Time: "+str(nodeobject.nodeExec()))
       print("		Rank Value: "+str(nodeobject.getRank()))
       print("                Parents count: "+str(len(nodeobject.nodeParent())))


print(len(TASKGEN))
processorsCount = num_process
w, h = len(TASKGEN), num_process
Matrix = [[round(random.uniform(0.1, 1.0), 10)  for x in range(w)] for y in range(h)]
print(Matrix[0][6])
ALPHA = 0.6
BETA = 0.7
ROW_1 = 0.6
ROW_2 = 0.1
ROW_3 = 0.6
tmpProcessorsCount = 0
while tmpProcessorsCount < processorsCount:
	initialMatrixCopy = Matrix
	Matrix = generateProbabilityMatrix(Matrix)
	processorHighestValues = computeHighestValue(Matrix)
	procToSumOfExecTimes = computeMakespan(processorHighestValues)
	summedUpMatrix = computeLocalTrials(Matrix, initialMatrixCopy)
	highestValMatrix = computeHighestValMatrix(processorHighestValues)
	resultSummedUpMatrix = sumSummedUpMatrixAndHighestValMatrix(summedUpMatrix, highestValMatrix)
	tmpProcessorsCount = tmpProcessorsCount + 1

resultsContainer = ResultsContainer()
resultsContainer.setInitialMatrix(initialMatrixCopy)
resultsContainer.setProbabilityMatrix(Matrix)
resultsContainer.setProcessorHighestValues(processorHighestValues)
resultsContainer.setMakespan(procToSumOfExecTimes)
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")
dislayMatrix(summedUpMatrix)
resultsContainer.setLocalTrialsSummedUpMatrix(summedUpMatrix)
resultsContainer.setResultSummedUpMatrix(resultSummedUpMatrix)
#Displaying results
print("")
print("")
print("")
print("################################## Initial Matrix ###########################")
dislayMatrix(resultsContainer.getInitialMatrix())
print("#############################################################################")
print("")
print("")
print("")
print("################################## Probability Matrix #######################")
dislayMatrix(resultsContainer.getProbabilityMatrix())
print("#############################################################################")
print("")
print("")
print("")
print("################################## Processor Highest Values #################")
print(str(resultsContainer.getProcessorHighestValues()))
print("#############################################################################")
print("")
print("")
print("")
print("################################## Makespan #################################")
print(str(resultsContainer.getMakespan()))
print("#############################################################################")
print("")
print("")
print("")
print("################################## Local Trials SummedUp Matrix #############")
dislayMatrix(resultsContainer.getLocalTrialsSummedUpMatrix())
print("#############################################################################")
print("")
print("")
print("")
print("################################## Results SummedUp Matrix ##################")
dislayMatrix(resultsContainer.getResultSummedUpMatrix())
print("#############################################################################")
print("")
print("")
print("")
processor2taskmap = computeProcessorToTaskMapping(resultsContainer.getResultSummedUpMatrix())
print("#############################################################################")
processor2ScheduleLength = computeScheduleLength(processor2taskmap)
for proc in processor2ScheduleLength:
	print("Processor: "+str(proc)+"    "+"Schedule Length: "+str(processor2ScheduleLength[proc]))
print("#############################################################################")
print("")
print("")
print("")
tsk2processorMap = {}
for processor,task in processor2taskmap.items():
	#print(str(task)+" : "+str(processor))
	tasks = task
	for tsk in tasks:
		print(tsk+" "+str(processor))
		tsk2processorMap[tsk] = processor

taskProcList = []
for nodename in TASKGEN:
	taskProcList.append(tsk2processorMap[nodename])
print(str(taskProcList))

	

#######################Genetic ###################################################
####################################################################################



def generateCombinations(processorscount, nodes_len, taskProcList):
	processorsList = []
	count = 1
	while count <= processorscount:
		processorsList.append(count)
		count = count + 1
	t = []
	
	t.append(tuple(taskProcList))
	updatedlist = set(t)
	return updatedlist

####################################################################################

def computeFitnessFunction(combinationsMapsList):
	combination2FitnessFunctionTuplesList = []
	for combinationMap in combinationsMapsList:
		#print(combinationMap)
		processor2ExecTimeSum = {}
		for nodeObject,processor in combinationMap.items():
			#print('Nodename: '+nodeObject.nodeName()+" : "+' processor is: '+str(processor))
			if processor in processor2ExecTimeSum:
				processor2ExecTimeSum[processor] = processor2ExecTimeSum[processor] + float(nodeObject.nodeExec())
			else:
				processor2ExecTimeSum[processor] = float(nodeObject.nodeExec())
		
		fitnessFunction = -1
		for processor,execTime in processor2ExecTimeSum.items():
			if execTime > fitnessFunction:
				fitnessFunction = execTime
		

		combination2FitnessFunctionTuple = (combinationMap, fitnessFunction)
		combination2FitnessFunctionTuplesList.append(combination2FitnessFunctionTuple)
		#print("+++++++++++++++++++++++++++++++")

	#print('Len of combination2FitnessFunctionMap is: '+str(len(combination2FitnessFunctionTuplesList)))
	return combination2FitnessFunctionTuplesList

####################################################################################

processorsCount = 2
combinationsSet = generateCombinations(processorsCount, len(TASKGEN), taskProcList)
print(combinationsSet)
print("*****************************")
combinationsMapsList = []
for combination in combinationsSet:
	i = 0
	combinationsMap = {}
	for nodename in TASKGEN:
		nodeobject =  TASKGEN[nodename]
		combinationsMap[nodeobject] = combination[i]
		i = i + 1
	combinationsMapsList.append(combinationsMap)
population_size = len(combinationsMapsList)
print("")
print('Population size is: '+str(population_size))
print("")
pool_size = population_size/2
combination2FitnessFunctionTuplesList = computeFitnessFunction(combinationsMapsList)
index2FitnessMap = {}
index = 0
for combination2FitnessFunctionTuple in combination2FitnessFunctionTuplesList:
	index2FitnessMap[index] = combination2FitnessFunctionTuple[1]
	index = index + 1


sortedindex2FitnessMapList = sorted(index2FitnessMap.items(), key=operator.itemgetter(1))

count = 1
sortedIndicesLength = len(sortedindex2FitnessMapList)
poolMap = []
while count <= pool_size:
	combinationFitnessTuple = (combination2FitnessFunctionTuplesList[sortedIndicesLength-1][0], sortedindex2FitnessMapList[sortedIndicesLength-1][1])
	poolMap.append(combinationFitnessTuple)
	sortedIndicesLength = sortedIndicesLength - 1
	count = count + 1


lowestCombinationFitnessTuple =  (combination2FitnessFunctionTuplesList[0][0], sortedindex2FitnessMapList[0][1])
print("****************** Result: GAACO  LOWEST COMBINATION ************")
print("")
print("Lowest combination:    Node Name to processor:::")
print("")
for node,processor in lowestCombinationFitnessTuple[0].items():
	print("	  Node Name: "+node.nodeName()+" : assigned to processor: "+str(processor))
print("")
print("Lowest combination:    Fitness Function Value::: "+str(lowestCombinationFitnessTuple[1]))
print("++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
print("")
print("")

def computeScheduleLength(processor2taskmap):
    processor2ScheduleLength = {}
    for processor in processor2taskmap:
        procScheduleLength = 0.0
        tasks = processor2taskmap[processor]
        for task in tasks:
            nodeobject = TASKGEN[nodename]
            procScheduleLength = procScheduleLength + float(nodeobject.nodeExec())
        processor2ScheduleLength[processor] = procScheduleLength
    return processor2ScheduleLength

processor2ScheduleLength = computeScheduleLength(processor2taskmap)
process_schedule = []
for proc in processor2ScheduleLength:
    print("Processor: " + str(proc) + "    " + "Schedule Length: " + str(processor2ScheduleLength[proc]))
    process_schedule.append(processor2ScheduleLength[proc])
max_schedule = max(process_schedule)
util = {}
average_utilization = []
for key,value in processor2taskmap.items():
    util[key] = len(value)/max_schedule
    average_utilization.append(len(value)/max_schedule)
print(util)
total_avreage_utilization = (sum(average_utilization)/processorsCount) * 100
print("#############################################################################")
print("###################   AVERAGE UTILIZATION  ##################################################")
print(total_avreage_utilization)
print("#############################################################################")


















	


