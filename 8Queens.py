from numpy import true_divide
from pysat.solvers import Glucose3
from pysat.solvers import Lingeling
from copy import deepcopy
SIZE = 8
f1 = open("level01", "w")
f2 = open("level02", "w")

#--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------
#Task A

#ONE QUEEN IN A ROW
def outputRowAtLeast1(f):
    """
    Outputs a row of the table at least 1.
    """
    for i in range (SIZE):
        for j in range (SIZE):
            #If it is the last element in the row, then don't add the "v"
            if (j != SIZE-1):
                f.write("p[%d][%d] v " % (i, j))
            else:
                f.write("p[%d][%d]" % (i, j))
            
            #Check whether it is the last element in the row
            if j == SIZE-1 and i != SIZE-1:
                f.write("\n")
            elif j == SIZE-1 and i == SIZE-1:
                f.write("\n")
                
def outputRowAtMost1(f):
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
def outputColumnAtLeast1(f):
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
            if j == SIZE-1 and i != SIZE-1:
                f.write("\n")
            elif j == SIZE-1 and i == SIZE-1:
                f.write("\n")
                
def outputColumnAtMost1(f):
    """
    Outputs a column of the table at most 1.
    """
    for i in range(SIZE):
        for j in range(SIZE-1):
            for k in range (j+1, SIZE):
                #Restrict element in the column to be 1
                f.write("not(p[%d][%d]) v not(p[%d][%d])\n" % (j, i , k , i)) #Similar to the row just swap the i 
    

#NO MORE THAN 1 QUEEN IN THE LEFT DIAGONAL & RIGHT DIAGONAL
def outputAtMostOneQueenInDiagonal(f):
    """
    Outputs the left diagonal and right diagonal of the table at most 1.
    """
    for i in range(SIZE*SIZE - 1):
        for j in range(i + 1, SIZE*SIZE):
             if((i % SIZE + int(i/SIZE)) == (j % SIZE + int(j/SIZE)) or  (i%SIZE - int(i/SIZE)) == (j%SIZE - int(j/SIZE))):
                    f.write("not(p[%d][%d]) v not(p[%d][%d])\n" % (i%SIZE,int(i/SIZE),j%SIZE,int(j/SIZE)))
                    
def writingRuleCNFLevel01(f):
    outputRowAtLeast1(f)
    outputRowAtMost1(f)
    outputAtMostOneQueenInDiagonal(f)
    f.close()
    
def writingRuleCNFLevel02(f):
    outputRowAtLeast1(f)
    outputRowAtMost1(f)
    outputColumnAtLeast1(f)
    outputColumnAtMost1(f)
    outputAtMostOneQueenInDiagonal(f)
    f.close()

writingRuleCNFLevel01(f1)
writingRuleCNFLevel02(f2)

#--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------
#Task B
filepath = "level02"
filetext = open(filepath, "r")

filewrite = open("SolvingTaskB", "w")

keyword = "p[3][3]"

a = True
while a:
    fileline = filetext.readline()
    if keyword in fileline:
        filewrite.write(fileline)
    
    if not fileline:
        a = False
        
filewrite.close()
filetext.close()

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

f1 = open("level01", "r")
f2 = open("level02", "r")

arraylv1 = convertRuleToArray(f1)
arraylv2 = convertRuleToArray(f2)

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
    
writeSolutionIntoFile("level01sol", arraylv1)
writeSolutionIntoFile("level02sol", arraylv2)
#--------------------------------------------------
#--------------------------------------------------
#--------------------------------------------------
#Task D
def pySATSolver(path):
    f = open(path,"w")
    
    array = Glucose3()
    #Choosing lv2 as the input file
    #SAT solver need row,column,diagonal 
    for element in arraylv2:
        array.add_clause(element)
    
    array.solve(assumptions=[6,9])
    tmpArray = array.get_model()
    
    f.write(str([element for element in tmpArray if element > 0]))
    f.close()
   
pySATSolver("SolvingTaskD") 