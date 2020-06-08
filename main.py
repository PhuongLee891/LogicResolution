#Library
import datastructures as myStruct
import os

#Func
def getInputFile(myKB: myStruct.KB):
    myFile = open(os.getcwd()+"/input.txt","r")
    fileData = myFile.read().split("\n")
    myAlpha = myStruct.Literal(fileData[0])
    for i in range(2,2+int(fileData[1])):
        myKB.addClauses(myStruct.Clauses(fileData[i]))
    myFile.close()
    if myAlpha.isNegative == False:
        temp = "-" + myAlpha.cLit
    else:
        temp = myAlpha.cLit
    myKB.addClauses(myStruct.Clauses(temp))
    return myAlpha

def printListOutputToFile(ListOutput: list):
    try:
        oFile = open(os.getcwd()+"/output.txt","a")
    except IOError:
        print("Can't open output.txt")
    for i in ListOutput:
        oFile.write(i+"\n")
    oFile.close()

def uniqueClauses(clausA: myStruct.Clauses, clausB: myStruct.Clauses,Signal: str):
    newClauses = myStruct.Clauses(clausA.showClauses() + " OR " + clausB.showClauses())
    newClauses.RemoveLiteralInClauses(Signal)
    return newClauses

def isClausesA_equal_ClausesB(clausA: myStruct.Clauses, clausB: myStruct.Clauses):
    if len(clausA.clauses) != len(clausB.clauses):
        return False
    for i in range(len(clausA.clauses)):
        if clausA.clauses[i].cLit == clausB.clauses[i].cLit and clausA.clauses[i].isNegative == clausB.clauses[i].isNegative:
            continue
        else:
            return False
    return True

def IsNewClausesExistInList(myList: list, MyClause: myStruct.Clauses):
    for Clausesi in myList:
        if isClausesA_equal_ClausesB(Clausesi,MyClause) == True:
            return True
    return False

def pl_resolve(ci,cj):
    for di in ci.clauses:
        for dj in cj.clauses:
            if (di.cLit == dj.cLit) and (di.isNegative != dj.isNegative):
                newClauses = uniqueClauses(ci,cj,di.cLit)
                if newClauses.CheckClausesIsAllTrue() == True:
                    return False
                else:
                    return newClauses
    return False

def pl_resolution(myKB: myStruct.KB,myAlpha: myStruct.Literal):
    while True:
        n = len(myKB.inListClauses)
        resolvents = []
        # pairs = [(myKB.inListClauses[i],myKB.inListClauses[j]) for i in range(n) for j in range(i+1,n)]
        # for (ci,cj) in pairs:
        for i in range(n):
            for j in range(i+1,n):
                ci = myKB.inListClauses[i]
                cj = myKB.inListClauses[j]
                newClauses = pl_resolve(ci,cj)
                if newClauses != False:
                    if IsNewClausesExistInList(myKB.inListClauses,newClauses) == False:
                        if IsNewClausesExistInList(resolvents,newClauses) == False:
                            resolvents.append(newClauses)

        #print result to file .txt
        temp = 0        #temp = 0: No new clauses (all is False)
        count = 0       #number of new clauses
        isEnd = 0       #isEnd = 1 when find None clauses ({})
        ListOutput = []
        for i in range(len(resolvents)):
            if resolvents[i] != False:
                count += 1
                temp = 1
                if resolvents[i].clauses == []:
                    ListOutput.append("{}")
                    isEnd = 1
                    continue
                ListOutput.append(resolvents[i].showClauses())
                #Insert List of new Clauses to myKB
                myKB.addClauses(resolvents[i])

        ListOutput.insert(0,str(count))
        if isEnd == 1:
            ListOutput.append("YES")
            print(ListOutput)
            printListOutputToFile(ListOutput)
            return True
        if temp == 0:
            ListOutput.append("NO")
            print(ListOutput)
            printListOutputToFile(ListOutput)
            return False
        
        printListOutputToFile(ListOutput)
        print(ListOutput)


#Main
if __name__== "__main__":
    #delete old Output.txt
    if os.path.exists("output.txt"):
        os.remove("output.txt")
    myKB = myStruct.KB()
    myAlpha = getInputFile(myKB)
    pl_resolution(myKB,myAlpha)


    