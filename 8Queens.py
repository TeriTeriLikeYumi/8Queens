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
                f.write("not(p[%d][%d]) v not(p[%d][%d])\n" % (i, j, i, k))
               
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

    while True:
        line = fread.readline()
        if len(line) == 0:
            break
        #Find all placed related to a specific queen
        if "p[3][3]" in line:
            fwrite.write(line)
            
    fread.close()   
    fwrite.close()
    
#Follow the task, queen are placed at (3,3) by default
QueenRestriction("Level02","SolvingTaskB")

#--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------
#Task C 
def convertInteger(x,y):
    return x*8+y+1

def convertRuleToArray(f):
    """
    Converts a rule to an array.
    """
    array = []

    while True:
        lines = f.readline()
        if len(lines) == 0:
            break
        line = lines.split(" v ")
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
            
            #K for the sign
            arrayItem.append(convertInteger(i,j)*k)
            
        if len(arrayItem) != 0:
            array.append(arrayItem)
        
        #Loop out of the file
        
    f.close()
    #Copy array using deepcopy
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
def visulize(queens=[]):
    """
    Visualize the chessboard with the queens.
    """
    #Create a chessboard
    chessboard = [False for i in range(SIZE*SIZE)]
    #Place the queens
    for queen in queens:
        chessboard[queen-1] = True
    
    #Print the chessboard
    for i in range(SIZE*SIZE): 
        if i%SIZE == 0 and i != 0:
            print("\n")
        if chessboard[i]:
            print("Q", end = " ")
        else:
            print(".", end = " ")
        
 
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
        f.write("Solution found\n")
        
        tmp =[element for element in tmpArray if element > 0]
        visulize(tmp)
        f.write(str(tmp))
    else:
        print("No solution found")
        f.write("No solution found")
    f.close()

QueenPosition = [1,30] #1->64
pySATSolver("SolvingTaskD",QueenPosition) 
#--------------------------------------------------
#--------------------------------------------------
#Task E
