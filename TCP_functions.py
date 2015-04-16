#--------------------------------------------------
#Redeclared this for use in this file

def recvall(sock, length):
    data = b''
    while len(data) < length:
        more = sock.recv(length - len(data))
        if not more:
            raise EOFError('was expecting %d bytes but only received' ' %d bytes before the socket closed' % (length, len(data)))
        data += more
    return data




#--------------------------------------------------
#Redeclared this for use in this file

def recvVar(sock):
    data = b''
    more = b''
    while (more != b'^'):
        more = sock.recv(1)
        if (more != b'^'):
            data += more

    print(data.decode('ascii'))
    return data


#--------------------------------------------------

def mainMenu():
    print("\nEmployee FMS \n \n Select one of the following \n \n    1) Add a new employee \n    2) Search for an employee \n    3) Remove an employee from FMS \n    4) Display entire employee FMS \n    5) Quit \n")

    line = input()

    return line



#--------------------------------------------------

def checkForEmployee(dic,empID):
#checks to see if employeeID already exists and returns a boolean value

    for ID in dic:
        if ID == empID:
            return True
            
    return False



#--------------------------------------------------

def addNewEmployee(sc):
#Gathers info, calls searchForEmployee, if EmpID doesn't exist, adds new employee and asks to do it again


    dic = {}

    try:
        infile = open("TCP_database.txt","r")
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except FileNotFoundError as err:
        errno, strerror = err.args
        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except NameError as err:
        errno, strerror = err.args
        print("NameError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message

    for rec in infile:
        ID,rest = rec.split(":",1)
        dic[ID] = rest
    infile.close()
    #updates here as opposed to inside the while loop in loop on server





    sc.sendall(b'\nPlease enter ID number#^')
    a = (recvVar(sc)).decode('ascii')
    #print(a + "++++++")
    #print(len(a))



    if (len(a) != 4):
    #checks to see if ID is proper length
        sc.sendall(b"ID number must be 4 numbers long.  Enter 'y' to try again?#^")
        addResponse = (recvVar(sc)).decode('ascii')
        if addResponse == 'y':
            return "redo"
        else:
            return ""

    if not (int(a)):
        print("are we here?")
        sc.sendall(b"ID number must be 4 numbers long.  Enter 'y' to try again?#^")
        addResponse = (recvVar(sc)).decode('ascii')
        if addResponse == 'y':
            return "redo"
        else:
            return ""


    if checkForEmployee(dic,a) == True:
    #checks to see if ID already exists
        sc.sendall(b"Employee ID already exists \n Enter 'y' to try again#^")
        #if ID already exists, asks user if they want to try again
        addResponse = (recvVar(sc)).decode('ascii')
        if addResponse == 'y':
            return "redo"
        else:
            return ""

    fNameNeeded = True
    while fNameNeeded:
        sc.sendall(b"Please enter first name#^")
        b = ((recvVar(sc)).decode('ascii'))
        if b.isalpha():
            fNameNeeded = False
            
            
    lNameNeeded = True
    while lNameNeeded:    
        sc.sendall(b"Please enter last name#^")
        c = ((recvVar(sc)).decode('ascii'))
        if c.isalpha():
            lNameNeeded = False


    deptNeeded = True
    while deptNeeded:
        sc.sendall(b"Please enter dept#^")
        d = ((recvVar(sc)).decode('ascii'))
        if d.isalpha():
            deptNeeded = False


    newLine = [a,":",b,":",c,":",d]

    try:
        infile = open("TCP_database.txt","a")
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except FileNotFoundError as err:
        errno, strerror = err.args
        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except NameError as err:
        errno, strerror = err.args
        print("NameError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message

    infile.writelines(newLine)
    infile.write("\n")
    infile.close()
    #appends newLine to textfile



    sc.sendall(b"\nEmployee has been added \n Enter 'y' to add another#^")
        #Confirms addition and if user wants to add another
    addResponse = (recvVar(sc)).decode('ascii')
    if addResponse == 'y':
        return "redo"
    else:
        return ""



#--------------------------------------------------

def searchForEmployee(sc):
#checks for employee and if found, display details

    mess = ""
    dic = {}

    try:
        infile = open("TCP_database.txt","r")
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except FileNotFoundError as err:
        errno, strerror = err.args
        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except NameError as err:
        errno, strerror = err.args
        print("NameError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message

    for rec in infile:
        ID,rest = rec.split(":",1)
        dic[ID] = rest
    infile.close()
    #updates here as opposed to inside the while loop on server





    sc.sendall(b'\nPlease enter ID number#^')
    a = (recvVar(sc)).decode('ascii')




    if (len(a) != 4):
    #checks to see if ID is proper length
        sc.sendall(b"ID number must be 4 numbers long.  Enter 'y' to try again?#^")
        searchForResponse = (recvVar(sc)).decode('ascii')
        if searchForResponse == 'y':
            return "redo"
        else:
            return ""

    if not (int(a)):
        print("are we here?")
        sc.sendall(b"ID number must be 4 numbers long.  Enter 'y' to try again?#^")
        searchForResponse = (recvVar(sc)).decode('ascii')
        if searchForResponse == 'y':
            return "redo"
        else:
            return ""




    if checkForEmployee(dic,a) == False:
    #checks to see if ID already exists
        sc.sendall(b"Employee ID does not exist \n Enter 'y' to try again#^")
        #if ID already exists, asks user if they want to try again
        searchForResponse = (recvVar(sc)).decode('ascii')
        if searchForResponse == 'y':
            return "redo"
        else:
            return ""



    for ID in dic:
        if ID == a:
            #print(dic[ID].split(":"))      prints in different format
            for key in dic[ID]:
                mess += key
                #displays tuples by line (doesn't reprint 'a' or EmployeeID).  Instructions do not mention formatting rules

    

       
    sc.sendall(b'\n' + mess.encode('ascii') + b"\nEnter 'y' to display another employee#^")
        #Confirms addition and if user wants to add another
    searchForResponse = (recvVar(sc)).decode('ascii')
    if searchForResponse == 'y':
        return "redo"
    else:
        return ""



#--------------------------------------------------

def removeEmployee(sc):
#checks for employee and if found removes it from text file


    dic = {}

    try:
        infile = open("TCP_database.txt","r")
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except FileNotFoundError as err:
        errno, strerror = err.args
        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except NameError as err:
        errno, strerror = err.args
        print("NameError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message

    for rec in infile:
        ID,rest = rec.split(":",1)
        dic[ID] = rest
    infile.close()
    #updates here as opposed to inside the while loop on server



    
    sc.sendall(b'\nPlease enter ID number#^')
    a = (recvVar(sc)).decode('ascii')




    if (len(a) != 4):
    #checks to see if ID is proper length
        sc.sendall(b"ID number must be 4 numbers long.  Enter 'y' to try again?#^")
        removeResponse = (recvVar(sc)).decode('ascii')
        if removeResponse == 'y':
            return "redo"
        else:
            return ""

    if not (int(a)):
        print("are we here?")
        sc.sendall(b"ID number must be 4 numbers long.  Enter 'y' to try again?#^")
        removeResponse = (recvVar(sc)).decode('ascii')
        if removeResponse == 'y':
            return "redo"
        else:
            return ""




    if checkForEmployee(dic,a) == False:
    #checks to see if ID already exists
        sc.sendall(b"Employee ID does not exist \n Enter 'y' to try again#^")
        #if ID already exists, asks user if they want to try again
        removeResponse = (recvVar(sc)).decode('ascii')
        if removeResponse == 'y':
            return "redo"
        else:
            return ""



    try:
        infile = open("TCP_database.txt","w")
    except IOError as err:
        errno, strerror = err.args
        print("I/O error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except FileNotFoundError as err:
        errno, strerror = err.args
        print("FileNotFoundError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message
    except NameError as err:
        errno, strerror = err.args
        print("NameError error({0}): {1}".format(errno, strerror))
        sys.exit()
        #detects open error and outputs error code and message


    for ID in dic:
        if ID != a:
            newLine = [ID,":",dic[ID]]
            infile.writelines(newLine)

    infile.close()
    #opens up text file, and writes over it (except the line with the matching empID)


    sc.sendall(b"\nEmployee has been removed \n Enter 'y' to try again#^")
    removeResponse = (recvVar(sc)).decode('ascii')
    if removeResponse == 'y':
        return "redo"
    else:
        return ""



#--------------------------------------------------

def displayDatabase():
    mess = ""

    #just for spacing

    infile = open("TCP_database.txt","r")
    
    for line in infile:
        mess += line
        #prints text file line by line
    infile.close()

    
    return mess
        
