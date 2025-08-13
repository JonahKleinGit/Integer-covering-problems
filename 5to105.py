#This code is used to verify that there are no covering system with distinct moduli in the interval [5,107]


#Import gurobi in order to use it. You need a license to use Gurobi. Licenses are available for free if you are affiliated to a valid University
import gurobipy as gp
from gurobipy import GRB

#Create a new model
model = gp.Model("smallcovering_mip")

#We store the lcm of the moduli under consideration in lcm
lcm=5040

#Store all integers to be covered, will be used to create constraints
covered=list(range(0,lcm))

#Store all preset arithmetic progressions in presets
presets=[[4,5],[6,7],[7,8],[8,9],[33,35]]

#Remove all integers from covered that satisfy an arithemtic progression in presets
for i in range(lcm):
    if i % 5==4 or i % 7==6 or i % 8==7 or i % 9==8 or i % 35==33:
        covered.remove(i)
     

    

#Define the rest of the moduli under consideration
n1=6 
n2=10
n3=12
n4=14
n5=15
n6=16
n7=18
n8=20
n9=21
n10=24
n11=28
n12=30
n13=36
n14=40
n15=42
n16=45
n17=48
n18=56
n19=60
n20=63
n21=70
n22=72
n23=80
n24=84
n25=90
n26=105


#Store all moduli in n
n=[n1,n2,n3,n4,n5,n6,n7,n8,n9,n10,n11,n12,n13,n14,n15,n16,n17,n18,n19,n20,n21,n22,n23,n24,n25,n26]

#Store the length of n, to be used in subsequent loops
numofprogs=len(n)

#Initialize a matrix to store variables
matrixvar=[]

#Store all necessary variables in matrixvar
for i in range(numofprogs):
    row = []
    for j in range(n[i]):
        # Add a binary variable for each cell in the matrix
        x = model.addVar(vtype=GRB.BINARY, name=f"x_{i}_{j}")
        row.append(x)
    matrixvar.append(row)

#Set optimization criterion; in this case there is none, so we optimize for the 0 function
model.setObjective(
   0,
    GRB.MINIMIZE
)


#Add constraints to make sure each modulus except for 48 is used at most once, and 48 is used at most twice
for i in range(numofprogs):
    if n[i]!=48:
        model.addConstr(gp.quicksum(matrixvar[i][j] for j in range(n[i])) <= 1, f"max_active_{i+1}")
    if n[i]==48:
        model.addConstr(gp.quicksum(matrixvar[i][j] for j in range(n[i])) <= 2, f"max_active_{i+1}")



#Add constraints to make sure everything in covered gets covered    
for i in covered:
    model.addConstr(
        matrixvar[0][i % n1] + 
        matrixvar[1][i % n2] + 
        matrixvar[2][i % n3] + 
        matrixvar[3][i % n4] + 
        matrixvar[4][i % n5] + 
        matrixvar[5][i % n6] + 
        matrixvar[6][i % n7] + 
        matrixvar[7][i % n8] + 
        matrixvar[8][i % n9] + 
        matrixvar[9][i % n10] + 
        matrixvar[10][i % n11] + 
        matrixvar[11][i % n12] + 
        matrixvar[12][i % n13] + 
        matrixvar[13][i % n14] + 
        matrixvar[14][i % n15] + 
        matrixvar[15][i % n16] + 
        matrixvar[16][i % n17] + 
        matrixvar[17][i % n18] +
        matrixvar[18][i % n19] +
        matrixvar[19][i % n20] +
        matrixvar[20][i % n21] +
        matrixvar[21][i % n22] +
        matrixvar[22][i % n23] +
        matrixvar[23][i % n24] +
        matrixvar[24][i % n25] +
        matrixvar[25][i % n26] 
        >=1,
         f"covconstr_{i}"
    )
 
#Here we have another model reduction. If some modulus is divisible by a modulus in presets, we may supposed the corresponding arithmetic progression is disjoint from the one in presets. We do this by
#setting the upper bound and lower bound of the corresponding variables to 0. Gurobi presolve takes care of removing the corresponding variables before optimizing
for i in range(numofprogs):
    if n[i] % 5==0:
        for j in range(n[i]):
            if j % 5==4:
                matrixvar[i][j].ub = 0
                matrixvar[i][j].lb = 0
    if n[i] % 7==0:
        for j in range(n[i]):
            if j % 7==6:
                matrixvar[i][j].ub = 0
                matrixvar[i][j].lb = 0
    if n[i] % 8==0:
        for j in range(n[i]):
            if j % 8==7:
                matrixvar[i][j].ub = 0
                matrixvar[i][j].lb = 0
    if n[i] % 9==0:
        for j in range(n[i]):
            if j % 9==8:
                matrixvar[i][j].ub = 0
                matrixvar[i][j].lb = 0
    if n[i] % 35==0:
        for j in range(n[i]):
            if j % 35==33:
                matrixvar[i][j].ub = 0
                matrixvar[i][j].lb = 0

#Optimize the model
model.optimize()

#Print the results of the computation. If there is a solution, this will return all non-zero variables. 
if model.status == GRB.OPTIMAL:
    print(f"Optimal objective value: {model.ObjVal}")
    print("\nNon-zero decision variable values:")
    for v in model.getVars():
        if v.x != 0:
            print(f"{v.varName} = {v.x}")
   

else:
    print("No optimal solution found.")