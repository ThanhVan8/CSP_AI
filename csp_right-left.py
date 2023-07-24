class CSP:
    assignment = {}
    
    def __init__(self):
        s = open("input.txt").read()
        inp = s.split("=")
        self.result = inp[1]

        self.operators = []
        self.operands = []
        operandTmp = ""   # each operand
        for i in inp[0]:
            if(i.isalpha()):
                operandTmp += i
            else:
                self.operators.append(i)
                self.operands.append(operandTmp)
                operandTmp = ""
        self.operands.append(operandTmp)

        self.maxStep = max(max((len(op) for op in self.operands)), (len(self.result)))
        self.leadingLetters = set(x[0] for x in self.operands)  # first letter of each operands
        
    def isAssigned(self, letter):
        return True if letter in self.assignment else False
    
    def compute(self, res, val, row):   # compute the 'val' into 'res' at operand 'row'
        if row == 0:
            res += val
        else:
            if self.operators[row - 1] == '+':
                res += val
            elif self.operators[row - 1] == '-':
                res -= val
        return res

    def checkConstraints(self, letter, value):
        if value in self.assignment.values():
            return False
        if letter in self.leadingLetters and value == 0:
            return False
        return True

    def solution(self):
        res = self.backtrack(0, 0, 0, 0)
        if res:
            return self.assignment
        else:
            return None

    # step: current column being performed
    # row: current row(operand) being performed
    # resStep: result of current step
    # carry
    def backtrack(self, step, row, resStep, carry):
        # print(step,row)
        # print(self.assignment)
        if step > self.maxStep - 1:
            if carry == 0:
                return True
            else:
                return False
                
        if row <= len(self.operands) - 1: # handle the operands (left side of '=')
            if step > len(self.operands[row]) - 1: # if go beyond the first letter of current operand
                isSuccess = self.backtrack(step, row + 1, resStep, carry) # go to next row
                if isSuccess:
                    return True
            else:
                char = self.operands[row][-step-1]  # get the character of current step
                if self.isAssigned(char):   # if already assigned
                    resStep = self.compute(resStep, self.assignment.get(char), row) # calculate the result
                    isSuccess = self.backtrack(step, row + 1, resStep, carry)  # go to next row
                    if isSuccess:
                        return True
                else:   # if not assigned yet
                    for i in range(10): # from 0-9
                    # for i in range(9,-1,-1):
                        if self.checkConstraints(char, i):
                            self.assignment[char] = i
                            resPrev = resStep   # store the old result in case backtrack fail
                            resStep = self.compute(resStep, self.assignment.get(char), row)
                            isSuccess = self.backtrack(step, row + 1, resStep, carry)  # go to next row
                            if isSuccess:
                                return True
                            else:
                                resStep = resPrev   # back to the old result
                                self.assignment.pop(char)   # pop out the value causing fail 
            
        else:   # handle the result (right side of '=')
            strRes = str(resStep)  # convert result of current column to string
            if resStep < 0:
                tmp = 0
                if abs(resStep) % 10 == 0:
                    tmp = abs(resStep) // 10
                else:
                    tmp = len(strRes) - 1
                correctDigit = tmp*10 + resStep
                carryNext = -tmp
            else:
                correctDigit = int(strRes[-1])  # get the last digit
                if correctDigit == resStep: # if the result has 1 digit
                    carryNext = 0
                else:
                    carryNext = int(strRes[0:len(strRes)-1])

            if step > len(self.result) - 1: # if go beyond the first letter of result
                # print(correctDigit)
                if correctDigit == 0:
                    isSuccess = self.backtrack(step + 1, 0, carryNext, carryNext) # go to next step
                    if isSuccess:
                        return True
                    else:
                        return False
                else:
                    return False
                
            char = self.result[-step-1] # get the character of result
            if self.isAssigned(char):   # if already assigned
                if self.assignment.get(char) == correctDigit:   # if the value of assigned letter is valid
                    isSuccess = self.backtrack(step + 1, 0, carryNext, carryNext) # go to next step
                    if isSuccess:
                        return True
            else:   # if not assigned yet
                if self.checkConstraints(char, correctDigit):
                    self.assignment[char] = correctDigit
                    isSuccess = self.backtrack(step + 1, 0, carryNext, carryNext)  # go to next step
                    if isSuccess:
                        return True
                    else:
                        self.assignment.pop(char)
        return False

problem = CSP()
res = problem.solution()
print(res)