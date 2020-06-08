class Literal():
    def __init__(self,inChar=str):
        #self.cLit          :character of literal
        #self.isNegative    :is Negative?
        if inChar == '':
            self.cLit = ''
            self.isNegative = False
        else:
            if len(inChar)>2:
                raise TypeError("Wrong type of literal")
            if inChar[0]=='-':
                self.isNegative = True
                if inChar[1] < 'A' or inChar[1] > 'Z':
                    raise TypeError("Wrong type of literal")
                self.cLit = inChar[1]
            else:
                if inChar[0] < 'A' or inChar[0] > 'Z':
                    raise TypeError("Wrong type of literal")
                self.cLit = inChar[0]
                self.isNegative = False

    def showLit(self):
        if self.isNegative == True:
            return '-' + self.cLit
        else:
            return self.cLit
        

class Clauses():
    def __init__(self,strInput = str):
        self.clauses = self.getClauseFromInput(strInput)
    
    def getClauseFromInput(self,strInput):
        out = []
        strOut = []
        while strInput.find('OR') >=0:
            inChar=strInput[:strInput.find('OR')].strip()
            strOut.append(inChar)
            strInput=strInput[strInput.find('OR')+2:].strip()
        strOut.append(strInput)
        #sort strOut
        strOut.sort()
        for i in range(len(strOut)):
            for j in range(i+1,len(strOut)):
                if len(strOut[i])==2:
                    tempi = strOut[i][1]
                else:
                    tempi = strOut[i][0]
                if len(strOut[j])==2:
                    tempj = strOut[j][1]
                else:
                    tempj = strOut[j][0]
                if tempi > tempj:
                    temp = strOut[i]
                    strOut[i] = strOut[j]
                    strOut[j] = temp
        #Remove any duplicates from a List
        strOut = list(dict.fromkeys(strOut))
        #Change type to Literal
        for i in strOut:
            out.append(Literal(i))
        return out

    def RemoveLiteralInClauses(self,signal: str):
        i = 0
        while i < len(self.clauses):
            if self.clauses[i].cLit == signal:
                del self.clauses[i]
                i = i-1
            i = i + 1

    def CheckClausesIsAllTrue(self):
        for i in range(len(self.clauses)):
            for j in range(i+1,len(self.clauses)):
                if self.clauses[i].cLit == self.clauses[j].cLit and self.clauses[i].isNegative != self.clauses[j].isNegative:
                    return True
        return False

    def showClauses(self):
        out = ''
        if len(self.clauses) < 1:
            return ''
        for i in range(len(self.clauses)-1):
            out = out + (self.clauses[i].showLit()) + ' ' + 'OR' + ' '
        out = out + self.clauses[-1].showLit()
        return out.strip()


class KB():
    def __init__(self,inListClauses=None):
        self.inListClauses = []

    def addClauses(self,inputClauses=Clauses):
        self.inListClauses.append(inputClauses)
    
    def printKB(self):
        for i in self.inListClauses:
            print(i.showClauses())
