
import sys
from random import randint


TASKGEN = {} #Mapping node-name to node-type.
TYPE_EXE = {} #Mapping type to node name and hence to execution time
RANKGEN = {} # Mapping Rank Values to Node objects

num_process = int(sys.argv[2])

class Node:
    
    def __init__ (self, name):
        self.name = name
        self.type = ""
        self.parent = []
        self.child = []
        self.exec_time = ""
        self.rank = ""
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
###############################################################################
line = [elem.strip('#') for elem in line]
        
update_exe=0
update_v = 0
update_f =0
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
        
   #if( elem.find("exec_time") and not elem.startswith("}")):
    #To find the execution time of each node:
    if(elem.find("exec_time") != -1):
            update_exe = 1
    if (update_exe and not elem.startswith("}")):
            ex = elem.split()#array of values:
            if len(ex) > 0:# to check if the length of each node is greater than 0
                node_type = ex[0]
                exec_time = ex[1]
                updateNodeExecution(node_type, exec_time)
                #print("Nodetype: "+node_type+" : Exec Time: "+exec_time)
    if elem.startswith("}") and update_exe:
              update_exe = 0


    #To store the slack time of each node:
    if (elem.find("start_time") != -1):
        #print("Inside")
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
                #print("Nodetype: "+node_type+" : Slack Time: "+node_st)
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
        return float(max_time)+float(exec_time)
    
    elif len(child) == 1:#If the child is 1
        max_time = getRankValue(TASKGEN[child[0]])
        node.setRank(float(max_time)+float(exec_time))
        RANKGEN[node] = float(max_time)+float(exec_time)

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
        return exec_time
    
###############################################################################
#TO SORT THE RANK VALUES IN DESCENDING ORDER:  
for n in TASKGEN:
    nodeobject=TASKGEN[n]
    rankvalue =  getRankValue(nodeobject)
sortvalue = sorted(RANKGEN, key= RANKGEN.get)# Returns list of keys : based on values. key: node object ; value: rank value
for k in sortvalue:
    sortvalue[0].setSlackTime(0)





def computeLevelWiseTasks():
    tasksMap = []
    level2TasksMap = {}
    task2levelMap = {}
    i = 0
    for nodename in TASKGEN:
        nodeobject =  TASKGEN[nodename]
        tasksMap.append(nodeobject)
    level = 0
    prevParentsList = []
    for nodeobject in tasksMap:
        if i == 0:
            levelNodes = []
            levelNodes.append(nodeobject)
            level2TasksMap[level] = levelNodes
            task2levelMap[nodeobject] = level
        else:
            if tasksMap[i].nodeParent() in prevParentsList:
                curr_level = task2levelMap[TASKGEN[tasksMap[i].nodeParent()]] + 1
                task2levelMap[nodeobject] = curr_level
                level2TasksMap[curr_level].append(nodeobject)
            else:
                level = level + 1
                prevParentsList.append(nodeobject.nodeParent())
                if TASKGEN[nodeobject.nodeParent()] not in task2levelMap:
                    task2levelMap[nodeobject] = level
                else:
                    task2levelMap[nodeobject] = task2levelMap[TASKGEN[nodeobject.nodeParent()]] + 1
                    level = task2levelMap[nodeobject]
                if level not in level2TasksMap:
                    levelNodes = []
                    levelNodes.append(nodeobject)
                    level2TasksMap[level] = levelNodes
                else:
                    level2TasksMap[level].append(nodeobject)

        i = i + 1
    return level2TasksMap,task2levelMap

############################################################################  




def getTotalChildCount(node):

    childCount = 0
    task = node
    if len(node.nodeChild()) == 0:
        return 0
    while task is not None:
        childSubTasks = task.nodeChild()
        childCount = len(childSubTasks)
        for subtask in childSubTasks:
            childCount = childCount + getTotalChildCount(TASKGEN[subtask])
    return childCount


###############################################################################

def tasksList(level2TasksMap, task2levelMap, processorsCount):
    tasksLst = []
    for level, tasks in level2TasksMap.items():

        tmpTasks = []
        prevChildCount = -1
        for task in tasks:

            if len(task.nodeChild()) < prevChildCount:
                tmpTasks.append(task)
                prevChildCount = len(task.nodeChild())
            else:
                tmpTasks.insert(0,task)
                prevChildCount = len(task.nodeChild())
        if len(tmpTasks) > 0:
            tasksLst.extend(tmpTasks)
    #Assign task to processors randomly
    tsk2processor = {}
    for tsk in tasksLst:
        randomProcessor = randint(1, processorsCount)
        tsk2processor[tsk] = randomProcessor
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("")
    print("		Results: MLSH Algorithm")
    print("")
    proc2tasks = {}
    process_dict = {}
    for tsk in tasksLst:
        print('Node Name: '+tsk.nodeName()+" Level: "+str(task2levelMap[tsk])+" Child count: "+str(len(tsk.nodeChild()))+" Parent: "+str(tsk.nodeParent())+" Assigned to processor: "+str(tsk2processor[tsk]))
        if tsk2processor[tsk] in proc2tasks:
            (proc2tasks[tsk2processor[tsk]]).append(tsk)
        else:
            tasks = []
            tasks.append(tsk)
            proc2tasks[tsk2processor[tsk]] = tasks
        if tsk2processor[tsk] in process_dict:
            (process_dict[tsk2processor[tsk]]).append(tsk.nodeName())
        else:
            tasks = []
            tasks.append(tsk.nodeName())
            process_dict[tsk2processor[tsk]] = tasks
    print(process_dict)
    print("")
    print("+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++")
    print("")
    print("")
    proc2ScheduleLength = {}
    for proc in proc2tasks:
        scheduleLength = 0.0
        for tsk in proc2tasks[proc]:
            scheduleLength = scheduleLength + float(tsk.nodeExec())
        proc2ScheduleLength[proc] = scheduleLength
    schedule_length =[]
    for proc in proc2ScheduleLength:
        print("Processor: "+str(proc)+"   Schedule Length: "+str(proc2ScheduleLength[proc]))

        schedule_length.append(proc2ScheduleLength[proc])
    print("")
    print("")
    print("")
    print(schedule_length)
    return schedule_length, process_dict


############################################################################  
#Displaying the results:
print("******************************************************")
for nodename in TASKGEN:
       nodeobject =  TASKGEN[nodename]
       print("      Node Name: "+str(nodename))
       print("		Type: "+str(nodeobject.nodeType()))
       print("		Parent: "+str(nodeobject.nodeParent()))
       print("		Child count: "+str(len(nodeobject.nodeChild())))
       print("		Exec. Time: "+str(nodeobject.nodeExec()))
       print("		Rank Value: "+str(nodeobject.getRank()))
       print("                Parents count: "+str(len(nodeobject.nodeParent())))
processorsCount = num_process
level2TasksMap,task2levelMap = computeLevelWiseTasks()
schedule_length, processor_dict = tasksList(level2TasksMap,task2levelMap, processorsCount)
max_schedule = max(schedule_length)
util = {}
average_utilization = []
for key,value in processor_dict.items():
    util[key] = len(value)/max_schedule
    average_utilization.append(len(value)/max_schedule)

total_avreage_utilization = (sum(average_utilization)/processorsCount) * 100
print("###########################################################################")
print("#### AVERAGE UTILIZATION ##################################################")
print(total_avreage_utilization)
print("#############################################################################")





	


