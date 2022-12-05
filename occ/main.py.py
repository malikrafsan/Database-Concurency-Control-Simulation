class Transaction:
    def __init__(self, transID):
        self.transID = transID

    def __str__(self):
        return 'T' + str(self.transID)
    
    def __eq__(self, trans):
        return (self.transID == trans.transID)
            
class ProcessTransaction:
    def __init__ (self, trans=None, action=None, data=None, process=None):
        if (not process):
            self.trans = trans
            self.action = action
            self.data = data
        else:
            self.trans = process.trans
            self.action = process.action
            self.data = process.data
    
    def __str__(self):
        data = f'({self.data})' if (self.action == 'R' or self.action == 'W') else ""
        return f'{self.action}{self.trans.transID}{data}'

class OCC(Transaction):
    def __init__(self, trans):
        super().__init__(trans.transID)
        self.write = []
        self.read = []
        self.startTimeStamp= float('inf')
        self.finishTimeStamp = float('inf')
    
    def writeTrans(self, i ,  data):
        if(self.startTimeStamp == float('inf')):
            self.startTimeStamp = i
        if (data not in self.write):
            self.write.append(data)
        return True
    
    def readTrans(self, i, data):
        if(self.startTimeStamp == float('inf')):
            self.startTimeStamp = i
        if (data not in self.read):
            self.read.append(data)
        return True
    
    def commitTrans(self, i, arrTransaction):
        valCommit = True
        for i in range(self.transID-1):
            trans = arrTransaction[i]
            if trans.transID == self.transID:
                continue
            if not(trans.finishTimeStamp < self.startTimeStamp):
                valCommit = False
            if (not valCommit) and set(trans.write).isdisjoint(self.read):
                valCommit = True
            
            if not valCommit:
                break
        
        self.finishTimeStamp = i

        return valCommit
    
    def runningTransaction(self):
        return (self.startTimeStamp != float('inf')) and (self.finishTimeStamp == float('inf'))

    def transactionOutput(self):
        exec = '"executing"' if self.runningTransaction() else '"not executing"'
        print(f"T{self.transID} : {exec}, R[", end="")
        for i, x in enumerate(self.read):
            if (i == len(self.read)-1):
                print(x, end="")
            else:
                print(x, end=",")
        print("], ", end="")
        print(f"W[", end="")
        for i, x in enumerate(self.write):
            if (i == len(self.write)-1):
                print(x, end="")
            else:
                print(x, end=",")
        print("]")


class ProcessOCC(ProcessTransaction):
    def __init__(self, process):
        super().__init__(process = process)
    
    def execute(self, i, arrTransaction):
        suc = True
        if (self.action == 'R'):
            suc = self.trans.readTrans(i, self.data)
        elif (self.action == 'W'):
            suc = self.trans.writeTrans(i, self.data)
        elif (self.action == 'C'):
            suc = self.trans.commitTrans(i, arrTransaction)

        if(not(suc)):
            print(f"Transaction {self.trans.transID} Aborted")
        return suc

def readFile(fileName):
    transactionArr = []
    processArr = []
    f = open(fileName, "r")
    file = f.read()
    parsedString = file.split('\n')
    
    transactionNumber = int(parsedString.pop(0))
    
    for i in range(transactionNumber):
        transactionArr.append(Transaction(i+1))
    
    parsedString.pop(0).split(' ')

    for c in parsedString:
        c = c.replace('(', '')
        c = c.replace(')', '')
        if len(c) > 2:
            
            processArr.append(
                ProcessTransaction(
                    transactionArr[int(c[1])-1],
                    c[0],
                    c[2]
                )
            )
        else:
            processArr.append(
                ProcessTransaction(
                    transactionArr[int(c[1])-1],
                    c[0]
                )
            )
    return transactionArr, processArr

file_input = input("Masukkan file input:")
transactionArr, processArr = readFile(file_input)
occTransArr = []
occProcArr = []
for i in range(len(transactionArr)):
    occTransArr.append(OCC(transactionArr[i]))

for i in range(len(processArr)):
    occProcArr.append(ProcessOCC(processArr[i]))
    proc = occProcArr[-1]
    proc.trans = occTransArr[proc.trans.transID-1]

txn = []

for i, p in enumerate(occProcArr, 1):
    if (p.trans in txn):
        print(f"Transaction {p.trans} is aborted\n")
    else:
        print(p)
        print(f"Transaction with smaller timestamp is:", end=" ")
        for i in range(p.trans.transID-1):
            print(occTransArr[i], end=" ")
        print()

        succ = p.execute(i, occTransArr)
        for trans in occTransArr:
            trans.transactionOutput()

        if (not succ):
            txn.append(p.trans)
        
        input()

