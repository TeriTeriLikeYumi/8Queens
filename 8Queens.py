from numpy import true_divide
from pysat.solvers import Glucose3
from pysat.solvers import Lingeling
from pysat.formula import CNF
from queue import PriorityQueue
import re
from copy import deepcopy
SIZE = 8

#--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------
#Task A

#ONE QUEEN IN A ROW
def Row(f):
    """
    Outputs a row o the table at least 1.
    """
    for i in range (SIZE):
        for j in range (SIZE):
            #If it is the last element in the row, then don't add the "v"
            if (j != SIZE-1):
                f.write("p[%d][%d] v " % (i, j))
            else:
                f.write("p[%d][%d]" % (i, j))
            
            #Check whether it is the last element in the row
            if j == SIZE-1:
                f.write("\n")
                
    """
    Outputs a row of the table at most 1.
    """
    for i in range (SIZE):
        for j in range (SIZE-1):
            for k in range(j+1, SIZE):
                #Restrict element in the row to be 1
                f.write("not(p[%d][%d]) v not(p[%d][%d])" % (i, j, i, k))
                f.write("\n")
               
#ONE QUEEN IN A COLUMN
def Column(f):
    """
    Outputs a column of the table at least 1.
    """
    for i in range (SIZE):
        for j in range (SIZE):
            #If it is the last element in the column, then don't add the "v"
            if (j != SIZE-1):
                f.write("p[%d][%d] v " % (j,i))
            else:
                f.write("p[%d][%d]" % (j,i))
                
            #Check whether it is the last element in the column
            if j == SIZE-1:
                f.write("\n")
    """
    Outputs a column of the table at most 1.
    """
    for i in range(SIZE):
        for j in range(SIZE-1):
            for k in range (j+1, SIZE):
                #Restrict element in the column to be 1
                f.write("not(p[%d][%d]) v not(p[%d][%d])\n" % (j, i , k , i)) #Similar to row function just swap i                 

#NO MORE THAN 1 QUEEN IN DIAGONALS
def Diagonal(f):
    """
    Outputs the left diagonal and right diagonal of the table at most 1.
    """
    for i in range(SIZE*SIZE - 1):
        for j in range(i + 1, SIZE*SIZE):
             if((i % SIZE + int(i/SIZE)) == (j % SIZE + int(j/SIZE)) or  (i%SIZE - int(i/SIZE)) == (j%SIZE - int(j/SIZE))): #Left or right diagonal cells are the same
                    f.write("not(p[%d][%d]) v not(p[%d][%d])\n" % (i%SIZE,int(i/SIZE),j%SIZE,int(j/SIZE)))

#Create file with the rules            
def writingRuleCNFLevel01(f): #Each queens can only move on a single column
    Row(f)
    Diagonal(f)
    f.close()
    
def writingRuleCNFLevel02(f): #Queens can be placed at any cell on the chessboard
    Row(f)
    Column(f)
    Diagonal(f)
    f.close()

#Two Rule CNF of Queens placement
f1 = open("Level01", "w")
f2 = open("Level02", "w")

writingRuleCNFLevel01(f1)
writingRuleCNFLevel02(f2)

#--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------
#Task B
def QueenRestriction(read,write):
    fread  = open(read, "r")
    fwrite = open(write, "w")

    advancePlaced = "p[3][3]"

    a = True
    while a:
        line = fread.readline()
        #Find all placed related to a specific queen
        if advancePlaced in line:
            fwrite.write(line)
    
        if not line:
            a = False
            
    fread.close()   
    fwrite.close()
    
#Follow the task, queen are placed at (3,3) by default
QueenRestriction("Level02","SolvingTaskB")

#--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------
#Task C 
def convertRuleToArray(f):
    """
    Converts a rule to an array.
    """
    a = True
    array = []
    k = 0
    
    while a:
        fileline = f.readline()
        line = fileline.split(" v ")
        arrayItem = []
        for element in line:
            if element == "":
                continue
            if element[0] == "n":
                #format not(p[i][j])
                i = int(element[6]) 
                j = int(element[9]) 
                k = -1
            else:
                #format p[i][j]
                i = int(element[2]) 
                j = int(element[5]) 
                k = 1
            
            z = (8 * i + j + 1) * k
            arrayItem.append(z)
            
        if len(arrayItem) != 0:
            array.append(arrayItem)
        
        #Loop out of the file
        if not fileline:
            a = False
        
    f.close()
    return deepcopy(array)

#Open 2 files to convert the rules to arrays
f1 = open("Level01", "r")
f2 = open("Level02", "r")

#Convert the each rules to arrays
arraylv01 = convertRuleToArray(f1)
arraylv02 = convertRuleToArray(f2)

#Write the array to a file
def writeSolutionIntoFile(path, array):
    f = open(path, "w")
    for items in array:
        for item in items:
            if items.index(item) != len(items) - 1:
                f.write(str(item) + " ^ ")
            else:
                f.write(str(item))
        f.write("\n")
    f.close()
    
writeSolutionIntoFile("SolvingTaskC_1", arraylv01)
writeSolutionIntoFile("SolvingTaskC_2", arraylv02)
#--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------
#Task D
def pySATSolver(path,position):
    f = open(path,"w")
    
    array = Glucose3()
    #Choosing lv2 as the input file
    #SAT solver need row,column,diagonal 
    for element in arraylv02:
        array.add_clause(element)
    
    #Pick random a solution
    if array.solve(assumptions = position):
        tmpArray = array.get_model()
        f.write(str([element for element in tmpArray if element > 0]))
    else:
        f.write("No solution")
    f.close()

QueenPosition = [1] 
pySATSolver("SolvingTaskD",QueenPosition) 
#--------------------------------------------------
#--------------------------------------------------
#Task E
