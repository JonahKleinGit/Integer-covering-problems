#This code is used for testing whether there exists a covering system with a given minimum modulus and a given lcm




#Import gurobi in order to use it. You need a license to use Gurobi. Licenses are available for free if you are affiliated to a valid University
import gurobipy as gp
from gurobipy import GRB

# Create a new model
model = gp.Model("smallcovering_mip")

#Set the lcm you wish to test
lcm=5040

#Set the minimum modulus under consideration
minmod=6

#If you believe there are no solutions to the integer covering problem, leave Heuristics at 0, this speeds up the algorithm. If you believe there is a solution and wish to find it, you should comment out this line,
#gurobi heuristics usually allow to find solutions more quickly than if they are not used 
model.Params.Heuristics=0

#Covered is a list that contains all integer from 0 to lcm that need to be covered, will be used to create the constraints
covered=list(range(0,lcm))

#Enter in presets any arithmetic progressions you wish to fix before starting computations. Use format [a,m] for the arithmetic progression a \pmod m. 
presets=[[6,7],[7,8],[8,9],[33,35]]

#Define the number of presets, to be used in subsequent loops
numofpreset=len(presets)

#Define an empty list n, which will contain all divisors of lcm that are \geq minmod and that were not used in presets
n=[]

#Add all divisors of lcm to n
for i in range(1,lcm+1):
    if lcm % i==0:
        n.append(i)

#Remove from n any divisors that are smaller than minmod
n=[item for item in n if item>=minmod]

#Print n, to make sure you have the correct list of moduli, and if you want the list of moduli. Useful for testing, can be removed
print(n)

#We can remove constraints for covering integers that are covered by preset arithmetic progressions. We start this process by removing those integers from covered
for i in range(lcm):
    for j in range(numofpreset):
        if i % presets[j][1]==presets[j][0]:
            if i in covered:
                covered.remove(i)
     
#Remove all moduli used in presets from n
for i in range(numofpreset):
    n.remove(presets[i][1])

#Print n, to make sure you have the correct list of moduli, and if you want the list of moduli. Useful for testing, can be removed
print(n)

#Define the number of progressions under consideration that are not in presets, i.e. the length of n
numofprogs=len(n)

#Define a matrix to store all variables
matrixvar=[]

#Store all relevant variables in the matrix
for i in n:
    row = []
    for j in range(i):
        # Add a binary variable for each cell in the matrix
        x = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
        row.append(x)
    matrixvar.append(row)

#Set optimization objective. Because we are only looking for a solution satisfying the constraint, we do not have an optimization objective, and so we set our objective to optimize the 0 function. 
#If you remove this, gurobi should set this by default. Can be useful to define another objective if you wish to have an objective, for example minimize the total number of arithmetic progressions used
model.setObjective(
   0,
    GRB.MINIMIZE
)

#We now define constraints. The constraints here defined guarantee that each modulus is used exactly once. Can be set to at most once if you prefer, but this runs a little faster, and if there is a solution
#in which each modulus is used exactly once, then there is also a solution in which each modulus is used at most once
for i in range(numofprogs):
    model.addConstr(gp.quicksum(matrixvar[i][j] for j in range(n[i])) == 1, f"max_active_{i+1}")
   
#The constraints here are to guarantee that every integer left in covered gets covered
for i in covered:
    model.addConstr(gp.quicksum(matrixvar[j][i % n[j]] for j in range(len(n)))>=1, f"cov_constr_{i}")
    
#Here we have another model reduction. If some modulus is divisible by a modulus in presets, we may supposed the corresponding arithmetic progression is disjoint from the one in presets. We do this by
#setting the upper bound and lower bound of the corresponding variables to 0. Gurobi presolve takes care of removing the corresponding variables before optimizing
for i in range(numofprogs):
    for k in range(numofpreset):
        if n[i] % presets[k][1]==0:
            for j in range(n[i]):
                if j % presets[k][1]==presets[k][0]:
                    matrixvar[i][j].ub = 0
                    matrixvar[i][j].lb = 0    

#Optimize the model
model.optimize()

#Print results. If gurobi finds a solution, this prints all non-zero variables. If there is no solution, this prints that there is no solution
if model.status == GRB.OPTIMAL:
    print(f"Optimal objective value: {model.ObjVal}")
    print("\nNon-zero decision variable values:")
    for v in model.getVars():
        if v.x != 0:
            print(f"{v.varName} = {v.x}")
   
 
else:
    print("No optimal solution found.")