lines = [] # initalise to empty list
with open('input.txt') as f:
    lines = f.readlines() # read all lines into a list of strings


Tab_list=[] #finding the list of tabs in each lines of the input file
for statement in lines: # each statement is on a separate line
    tabs = 0 #initialisation
    statement = statement.replace("    ", '\t')
    while statement[tabs] == '\t':
        tabs += 1
    Tab_list.append(tabs)




# Tab_list=[0,0,1,1,0,0,0,1]
def no_of_preceedingwhileloops(Tab_list,i):  #HElper function giving the no.of preceeding while loops before an index in a tab list
    ans=0 #intialisasion
    for i in range(0,i-1):

        if Tab_list[i+1]==Tab_list[i]+1:   #whenever the tab numbers in consecutive lines increase by 1 that means a while loop
            ans+=1
    return ans
# print(no_of_preceedingwhileloops(Tab_list)) #gives 2

def destination_index(Tab_list,i):   #gives the index of destination in the instruction list corresponding to an index of branching for a while loop in the tab list i.e. actual lines in input file
    if Tab_list[i+1]!=Tab_list[i]+1: #if consecutive ab doesnt increase then it cant be while loop
        return None
    for j in range(i+1,len(Tab_list)):
        if Tab_list[j]==Tab_list[i]:  #when the no.of tabs increase and again becomes equal to prevoous tabs of the while statement
            return j+no_of_preceedingwhileloops(Tab_list,i)+1   #precedding while loops will add 1 extra unconditional while statement in the instruction list per while loop so index of branching will be given in this way
            break
# Tab_list=[0,0,1,1,2,2,1,0]
# print(destination_index(Tab_list,2))    #gives None
# print(destination_index(Tab_list,1))    #gives 7
# print(destination_index(Tab_list,3))    #gives 6
# print(destination_index(Tab_list,4))    #gives None
def unconditional_branch_index(Tab_list,i):   #gives the index of unconditional branching in the instruction list corresponding to some index of while loop loop in lines
    if i==0:   #base case
        return None
    for j in range(i-1,0,-1):
        if Tab_list[j]==Tab_list[i]-1:   #finding the index of that statment having no. of tabs 1 lesser than index of branching
            return j+no_of_preceedingwhileloops(Tab_list,i)  ##precedding while loops will add 1 extra unconditional while statement in the instruction list per while loop so index of branching will be given in this way
            break
# Tab_list=[0,0,1,1,2,2,1,0]
# print(unconditional_branch_index(Tab_list,1))   #gives None
# print(unconditional_branch_index(Tab_list,2))   #gives 1
# print(unconditional_branch_index(Tab_list,6))   #gives 3
# print(unconditional_branch_index(Tab_list,7))   #gives None

instruction_list=[]
for i in range (0,len(lines)): # each statement is on a separate line

    token_list = lines[i].split() # split a statement into a list of tokens
    if len(token_list)==3 or (len(token_list)==5 and token_list[0]!='while'):  #statemnts othen than while loop should be appended to the ins list
        instruction_list.append(lines[i].strip())
    if token_list[0]=='while':   #while loop has following possibilities
        if token_list[2]=='>':
            instruction_list.append(['BLE',token_list[1],token_list[3],destination_index(Tab_list,i)])  #we append BLE, the two terms whosd comparison is being made and the destination index corresponsing to this line in trhe ins list and similarly the below ones
        if token_list[2]=='<':
            instruction_list.append(['BLE',token_list[3],token_list[1],destination_index(Tab_list,i)])
        if token_list[2]=='>=':
            instruction_list.append(['BLT',token_list[1],token_list[3],destination_index(Tab_list,i)])
        if token_list[2]=='<=':
            instruction_list.append(['BLT',token_list[3],token_list[1],destination_index(Tab_list,i)])
        if token_list[2]=='!=':
            instruction_list.append(['BE',token_list[1],token_list[3],destination_index(Tab_list,i)])
        if token_list[2]=='==':
            instruction_list.append(['BNE',token_list[1],token_list[3],destination_index(Tab_list,i)])
    if len(token_list)==5 and token_list[0]!='while':  #at the end line of a while loop we append unconditional (bramch,index) to the ins list
        instruction_list.append(['branch',(unconditional_branch_index(Tab_list,i))])

def RHS(a):  #finds the rhs terms of a statement without while loop in a string
    return a[4:len(a)]
# print(RHS('a = 10 + 5')) #gives 10 + 5
# print(RHS('b = c'))   #gives c
# Given a list L of length n, find if a “key” element k appears in it
def find (L, k): #HELPER FUNCTION
# INPUT L is a list of elements
# INPUT k is the “key” element we try to find in list L
# OUTPUT (True, j) if k is present in L at position j
# (False, _) if k is not present in L.
    n = len(L)
    found = False
    i = 0
    # INVARIANT found == False implies forall j (0 ≤ j < i): L[j] =/= k
    # found == True implies L[i] == k
    while (i < n) & (not found):
        if (L[i] == k):
            found = True # L[i] == k
            # return (found, i)
        else: # L[i] =/= k
            i += 1
            # EXIT when found OR (i == n)
    return (found, i)
def find_2(L,a):  #helper function,finds the presence of an element inside a list in form of some tuple
    found=False
    i=0
    index=0
    while i<len(L) and not(found):
        (found_1,j)=find(L,(a,i))
        if found_1==True:
            found=True
            index=j
        else:
            i+=1
    return (found,index)   #returns found and the index at which the tuple is found
# print(find_2([2,3,5,7,9,(4,3),(5,6),8],5))   #gives(TRue,6)
# print(find_2([2,3,5,7,9,(4,3),(5,6),8],7))   #gives(False,8)

DATA=[]
def execute(instruction):  #common execute function for different types of statement
#BELOW CODES ARE TALEN FROM ASSIGNMWNT 5 PART 1 WITH SOME MODIFICATIONS IN NAMINGS
        if type(instruction)==str:

            val=eval(RHS(instruction))
            value=int(val) #other possibility is that val is a float(when division of integers give decimal ans) so we have to take its greatest integer(which is similar to replacing the / operator by // since all other operations will give integer output for integer inputs)
            (found_1,j_1)=find(DATA,str(value)) #we check is that val is already present in DATA or not
            (found_2,j_2)=find_2(DATA,instruction[0])

            if (found_2==True) and (found_1==True): #if both the variable on LHS and val on RHS are present in DATA
                DATA[j_2]=(str(instruction[0]),j_1) #then we replace the older reference of that that variable with the new reference of the RHS value

            else:
                if found_1==False: #if RHS value is not present in DATA
                    DATA.append(str(value)) #then we append it in DATA
                    if found_2==True: #again checking the presence of variable on LHS in the DATA after appending the RHS value if it was not already present in DATA
                        DATA[j_2]=(str(instruction[0]),j_1)   #replacing the older reference of the variable by the new reference of the RHS value appended later
                    else:
                        DATA.append((str(instruction[0]),len(DATA)-1)) #if the varible is not already present in DATA then we appended the tuple containing the varible and the reference of value of RHS which was just appended in DATA and so has index len(DATA)-1
                else:
                    DATA.append((str(instruction[0]),j_1)) #if RHS was already present in DATA but variable was not present then we append the typle containing variable and the reference of the RHS already present in DATA
            globals()[instruction[0]]=int(val) #we assign the value of RHS to the variable on LHS for the further lines

            for i in range(0,len(instruction_list)-1):
                if instruction_list[i]==instruction:
                    return execute(instruction_list[i+1])    #finding the indexof ins in the ins list and also starting the execution of the next instruction in the ins list after one is completed



        elif type(instruction)==list:

            if instruction[0]=='BLE': #executing based on the conditions of functions defined above

                if eval(instruction[1])<=eval(instruction[2]):

                    return execute(instruction_list[instruction[3]])
                else:
                    for i in range(0,len(instruction_list)-1):
                        if instruction_list[i]==instruction:
                            print(DATA)
                            REFERRED_indices=[] #list containing all the references of varibles present in DATA
                            GARBAGE=[] #list containing garbage integers which are no more referred to any variable

                            for j in DATA:
                                if type(j)==tuple: #for tuples present in DATA containing variables and their refrences
                                    (a,b)=j
                                    REFERRED_indices.append(b) #appending the indices of all the variables in list REFERRED_indices=[]
                                    print(a, '=' ,DATA[b]) #printing the final values of all the variables

                            for k in range(0,len(DATA)):
                                if type(DATA[k])!=tuple: #for integers and booleans present in DATA list

                                    (found_3,j_3)=find(REFERRED_indices,k) #checking which indices are not present in REFERRED_indices list and hence are not referred to any variable
                                    if found_3==False and DATA[k].isalpha()==False: #those integers whose indices are not present in REFERRED_indices list are the garbage values
                                        GARBAGE.append(DATA[k]) #hence we append the garbage values to the GARBAGE list
                            print("GARBAGE" ,'=' ,GARBAGE) #printing the GARBAGE list
                            return execute(instruction_list[i+1])  #starting the execution of next instruction

            elif instruction[0]=='BLT':
                if eval(instruction[1])<eval(instruction[2]):
                    return execute(instruction_list[instruction[3]])
                else:
                    for i in range(0,len(instruction_list)-1):
                        if instruction_list[i]==instruction:
                            return execute(instruction_list[i+1])
            elif instruction[0]=='BE':
                if eval(instruction[1])==eval(instruction[2]):
                    return execute(instruction_list[instruction[3]])
                else:
                    for i in range(0,len(instruction_list)-1):
                        if instruction_list[i]==instruction:
                            return execute(instruction_list[i+1])
            elif instruction[0]=='BNE':
                if eval(instruction[1])!=eval(instruction[2]):
                    return execute(instruction_list[instruction[3]])
                else:
                    for i in range(0,len(instruction_list)-1):
                        if instruction_list[i]==instruction:
                            return execute(instruction_list[i+1])
            elif instruction[0]=='branch':
                return execute(instruction_list[instruction[1]])



execute(instruction_list[0])    #starting the execution of 1st ins and since all execution starts the execution of next ins as well so ultimately the execution of all ins in the ins lsit will be made
print(DATA) #printing data and other reqd things after the end of program
REFERRED_indices=[] #list containing all the references of varibles present in DATA
GARBAGE=[] #list containing garbage integers which are no more referred to any variable

for j in DATA:
    if type(j)==tuple: #for tuples present in DATA containing variables and their refrences
        (a,b)=j
        REFERRED_indices.append(b) #appending the indices of all the variables in list REFERRED_indices=[]
        print(a, '=' ,DATA[b]) #printing the final values of all the variables

for k in range(0,len(DATA)):
    if type(DATA[k])!=tuple: #for integers and booleans present in DATA list

        (found_3,j_3)=find(REFERRED_indices,k) #checking which indices are not present in REFERRED_indices list and hence are not referred to any variable
        if found_3==False and DATA[k].isalpha()==False: #those integers whose indices are not present in REFERRED_indices list are the garbage values
            GARBAGE.append(DATA[k]) #hence we append the garbage values to the GARBAGE list
print("GARBAGE" ,'=' ,GARBAGE) #printing the GARBAGE list

'''
Test case 1:
a = 10
b = 1
while a > b :
	a = a - 1
c = 1
Output:
['10', ('a', 0), '1', ('b', 2)]
a = 10
b = 1
GARBAGE = []
['10', ('a', 4), '1', ('b', 2), '9']
a = 9
b = 1
GARBAGE = ['10']
['10', ('a', 5), '1', ('b', 2), '9', '8']
a = 8
b = 1
GARBAGE = ['10', '9']
['10', ('a', 6), '1', ('b', 2), '9', '8', '7']
a = 7
b = 1
GARBAGE = ['10', '9', '8']
['10', ('a', 7), '1', ('b', 2), '9', '8', '7', '6']
a = 6
b = 1
GARBAGE = ['10', '9', '8', '7']
['10', ('a', 8), '1', ('b', 2), '9', '8', '7', '6', '5']
a = 5
b = 1
GARBAGE = ['10', '9', '8', '7', '6']
['10', ('a', 9), '1', ('b', 2), '9', '8', '7', '6', '5', '4']
a = 4
b = 1
GARBAGE = ['10', '9', '8', '7', '6', '5']
['10', ('a', 10), '1', ('b', 2), '9', '8', '7', '6', '5', '4', '3']
a = 3
b = 1
GARBAGE = ['10', '9', '8', '7', '6', '5', '4']
['10', ('a', 11), '1', ('b', 2), '9', '8', '7', '6', '5', '4', '3', '2']
a = 2
b = 1
GARBAGE = ['10', '9', '8', '7', '6', '5', '4', '3']
['10', ('a', 2), '1', ('b', 2), '9', '8', '7', '6', '5', '4', '3', '2', ('c', 2)]
a = 1
b = 1
c = 1
GARBAGE = ['10', '9', '8', '7', '6', '5', '4', '3', '2']
'''

'''
Test case 2:
a = 10
b = 1
while a > b :
	a = a - 1
c = 1
d = 4
while d != 7 :
	d = d + 1
e = 12
Output:
['10', ('a', 0), '1', ('b', 2)]
a = 10
b = 1
GARBAGE = []
['10', ('a', 4), '1', ('b', 2), '9']
a = 9
b = 1
GARBAGE = ['10']
['10', ('a', 5), '1', ('b', 2), '9', '8']
a = 8
b = 1
GARBAGE = ['10', '9']
['10', ('a', 6), '1', ('b', 2), '9', '8', '7']
a = 7
b = 1
GARBAGE = ['10', '9', '8']
['10', ('a', 7), '1', ('b', 2), '9', '8', '7', '6']
a = 6
b = 1
GARBAGE = ['10', '9', '8', '7']
['10', ('a', 8), '1', ('b', 2), '9', '8', '7', '6', '5']
a = 5
b = 1
GARBAGE = ['10', '9', '8', '7', '6']
['10', ('a', 9), '1', ('b', 2), '9', '8', '7', '6', '5', '4']
a = 4
b = 1
GARBAGE = ['10', '9', '8', '7', '6', '5']
['10', ('a', 10), '1', ('b', 2), '9', '8', '7', '6', '5', '4', '3']
a = 3
b = 1
GARBAGE = ['10', '9', '8', '7', '6', '5', '4']
['10', ('a', 11), '1', ('b', 2), '9', '8', '7', '6', '5', '4', '3', '2']
a = 2
b = 1
GARBAGE = ['10', '9', '8', '7', '6', '5', '4', '3']
['10', ('a', 2), '1', ('b', 2), '9', '8', '7', '6', '5', '4', '3', '2', ('c', 2), ('d', 6), '12', ('e', 14)]
a = 1
b = 1
c = 1
d = 7
e = 12
GARBAGE = ['10', '9', '8', '6', '5', '4', '3', '2']
'''
