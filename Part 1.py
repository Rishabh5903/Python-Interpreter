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

lines = [] # initalise to empty list
with open('/home/mt1210924/Lab1/input_file.txt') as f:

    lines = f.readlines() # read all lines into a list of strings

DATA=[] #Initialising data list as empty list
def RHS(L): #finds the list containing terms in RHS of a statement
    return L[2:len(L)] #first term is variable ans 2nd term is = sign so 3rd term i.e. 2nd index onwards is the RHS
OPERATORS=['+', '-', '*', '/', '>', '<', '>=', '<=', '==', '!=', 'and', 'or', 'not'] #list containing all the possible unary and binary operators
for l in range(0,len(lines)): #interpreting each line one by one from the list 'lines' containing all lines
    terms=lines[l].split() #splitting each line and separating each term and operators
    for i in range(0,len(RHS(terms))): #interpreting the RHS of each line
        if len(RHS(terms))==2: #when rhs is of the form  UNARY_OPERATOR TERM

            if RHS(terms)[0]=='-' and RHS(terms)[1].isnumeric(): #when we have negative of an integer as the RHS of a line

                if (str((-1)*eval(RHS(terms)[1])) in DATA)==False: #we check the presence of the negative number in the DATA list by multiplying the posiitve number in that line by -1

                    DATA.append(str((-1)*eval(RHS(terms)[1]))) #if that negative no. is not already present in the DATA list then we append it in DATA
                    break #breaking the if statement so that the positive int part of the -ve int does not get appended in DATA in the further steps inside this if statement
            elif RHS(terms)[0]=='-' and RHS(terms)[1].isalpha(): #when RHS is negative of some variable

                    for k in range(0,len(DATA)): #checking if the tuple of that variable with some index is already presetn in DATA or not
                        (found_2,j_2)=find(DATA,(str(RHS(terms)[1]),k))
                        if found_2==True:
                            break #breaking the loop when we find some tuple present in the DATA with this variable and its referrence,if none of found_2 is true then found_2 gets False value
                    if found_2==False: #if that variable is not present in DATA then it is a new varible which is not defined

                        print("variable",RHS(terms)[1],"is not defined") #hence print an error and exit
                        exit()

        (found,j)=find(DATA,RHS(terms)[i]) #when RHS is of the form TERM or  TERM BINARY_OPERATOR TERM
        if (('True' in RHS(terms)[i]) or ('False' in RHS(terms)[i])) and found==False: #when we find booleans True or False in RHS when they are not already present in DATA
            DATA.append(RHS(terms)[i])     #then we append  it in DATA
        elif RHS(terms)[i].isnumeric() and (found==False) : #when we find an integer which is not already present in DATA
            DATA.append(RHS(terms)[i]) #then we append it in DATA
        elif RHS(terms)[i].isalpha(): #we check for a variable in RHS that is not already present in DATA
            for k in range(0,len(DATA)): #checking if the tuple of that variable with some index is already presetn in DATA or not
                (found_2,j_2)=find(DATA,(str(RHS(terms)[i]),k))
                if found_2==True:
                    break #breaking the loop when we find some tuple present in the DATA with this variable and its referrence,if none of found_2 is true then found_2 gets False value
            if found_2==False and found==False and (RHS(terms)[i] in OPERATORS)==False: #if that variable is not in DATA,not a boolean(if it is boolena then will get appended in DATA in above steps) and also not an operator then it will be some other variable which is not defined
                print("variable",RHS(terms)[i],"is not defined") #hence we raise an error and exit the program
                exit()

        elif ((RHS(terms)[i] in OPERATORS)==False) and (RHS(terms)[i].isnumeric()==False) and (RHS(terms)[i].isalpha()==False): #if the term is not an operator,not an integer,not an alphabetical term then it will be some other type of term which is not allowed

            print("type() of term",RHS(terms)[i],"is not defined") #hence we raise a type error and exit the program
            exit()

    expression=lines[l].split(" = ") #we divide each line in two parts separated by = sign
    val=eval(expression[1]) #we evaluate the RHS since it has index 1 in the expression list
    if type(val)==bool: #when val is a bool then it is an acceptable type
        value=val
    elif type(val)==int: #when val is an integer then it is an acceptable type
        value=val
    else:
        value=int(val) #other possibility is that val is a float(when division of integers give decimal ans) so we have to take its greatest integer(which is similar to replacing the / operator by // since all other operations will give integer output for integer inputs)
    (found_1,j_1)=find(DATA,str(value)) #we check is that val is already present in DATA or not
    for k in range(0,len(DATA)): #we check that the variable on LHS is already referred to some value in DATA or not
        (found_2,j_2)=find(DATA,(str(expression[0]),k)) #checking if a tuple containing that variable and an idex is present in DATA or not
        if found_2==True:
            break    #breaking the loop when we find some tuple present in the DATA with this variable and its referrence,if none of found_2 is true then found_2 gets False value
    if (found_2==True) and (found_1==True): #if both the variable on LHS and val on RHS are present in DATA
        DATA[j_2]=(str(expression[0]),j_1) #then we replace the older reference of that that variable with the new reference of the RHS value

    else:
        if found_1==False: #if RHS value is not present in DATA
            DATA.append(str(value)) #then we append it in DATA
            if found_2==True: #again checking the presence of variable on LHS in the DATA after appending the RHS value if it was not already present in DATA
                DATA[j_2]=(str(expression[0]),j_1)   #replacing the older reference of the variable by the new reference of the RHS value appended later
            else:
                DATA.append((str(expression[0]),len(DATA)-1)) #if the varible is not already present in DATA then we appended the tuple containing the varible and the reference of value of RHS which was just appended in DATA and so has index len(DATA)-1
        else:
            DATA.append((str(expression[0]),j_1)) #if RHS was already present in DATA but variable was not present then we append the typle containing variable and the reference of the RHS already present in DATA
    locals()[expression[0]]=int(val) #we assign the value of RHS to the variable on LHS for the further lines

REFERRED_indices=[] #list containing all the references of varibles present in DATA
GARBAGE=[] #list containing garbage integers which are no more referred to any variable

for i in DATA:
    if type(i)==tuple: #for tuples present in DATA containing variables and their refrences
        (a,b)=i
        REFERRED_indices.append(b) #appending the indices of all the variables in list REFERRED_indices=[]
        print(a, '=' ,DATA[b]) #printing the final values of all the variables

for j in range(0,len(DATA)):
    if type(DATA[j])!=tuple: #for integers and booleans present in DATA list

        (found_3,j_3)=find(REFERRED_indices,j) #checking which indices are not present in REFERRED_indices list and hence are not referred to any variable
        if found_3==False and DATA[j].isalpha()==False: #those integers whose indices are not present in REFERRED_indices list are the garbage values
            GARBAGE.append(DATA[j]) #hence we append the garbage values to the GARBAGE list
print("GARBAGE" ,'=' ,GARBAGE) #printing the GARBAGE list