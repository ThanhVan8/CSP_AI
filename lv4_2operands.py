class CSP:
    assignment = {}
    def __init__(self):
        data = open("input.txt").read()

        s = ""
        operand_sign = 0
        #operand_sign
        for i in range(0, len(data)):
            if data[i].isalpha():
                s += data[i]
            else:
                if data[i] == '(':
                    if i > 0 and data[i-1] == '-':
                        operand_sign = 1
                    continue
                if data[i] == ')':
                    operand_sign = 0
                    continue

                if operand_sign == 1:
                    if data[i] == '+':
                        s += '-'
                    else:
                        if data[i] == '-':
                            s += '+'
                else:
                    s += data[i]
    
        inp = s.split("=")
        left = inp[0]
        left = left.split('*')
        operand = left[0]
        multiplier = left[1]
        self.result = inp[1]
        s = ""
        for i in range(len(multiplier)):
            s+=operand 
            for k in range (0,i):
                s+='?'
            s+='*'
            for j in range(len(operand)):
                s += multiplier[len(multiplier)-i-1]
            for k in range (0,i):
                s+='?'
            s+='+'
        s = s[0:len(s)-1]

        self.operators = []
        self.operands = []
        operandTmp = ""   
        for i in s:
            if(i.isalpha() or i == '?'):
                operandTmp += i
            else:
                self.operators.append(i)
                self.operands.append(operandTmp)
                operandTmp = ""
        self.operands.append(operandTmp)

        self.maxStep = max(max((len(op) for op in self.operands)), (len(self.result)))
        self.leadingLetters = set(x[0] for x in self.operands)  # first letter of each operands
        self.leadingLetters.add((self.result[0]))
    
    def isAssigned(self, letter):
        return True if letter in self.assignment else False

    def checkConstraints(self, letter, value):
        # gán giá trị bị trùng
        if value in self.assignment.values():
            return False
        # gán giá trị 0 cho chữ cái đầu
        if letter in self.leadingLetters and value == 0:
            return False
        # các chữ cái đầu không được <0
        return True
    
    def computeResStep(self, step, carry):
        if step > len(self.operands[0])-1:
            resMulti = 0
        else:
            char = self.operands[0][len(self.operands[0])-step-1]
            resMulti = self.assignment.get(char)
        res = carry
        for i in range(len(self.operators)):
            if step > len(self.operands[i+1])-1:
                resMulti = 0
            else:
                char = self.operands[i+1][len(self.operands[i+1])-step-1]
                if self.operators[i] == '*':
                    if char == '?':
                        resMulti = 0
                    else:
                        resMulti *= self.assignment.get(char)
                elif self.operators[i] == '+':
                    res += resMulti
                    resMulti = self.assignment.get(char)

        res += resMulti
        return res

    def solution(self):
        res = self.backtrack(0, 0, 0)
        if res:
            return self.assignment
        else:
            return None

    # step: current column being performed
    # row: current row(operand) being performed
    # resStep: result of current step
    # carry
    def backtrack(self, step, row, carry):
        if step > self.maxStep - 1:
            if carry == 0:
                return True
            else:   # at max step still have carry
                return False
                
        if row <= len(self.operands) - 1: # handle the operands (left side of '=')
            if step > len(self.operands[row]) - 1: # if go beyond the first letter of current operand (vượt ra ngoài)
                isSuccess = self.backtrack(step, row + 1, carry) # go to next row
                if isSuccess:
                    return True
            else:
                char = self.operands[row][-step-1]  # get the character of current step

                if char == '?':
                    isSuccess = self.backtrack(step, row + 1, carry)  # go to next row
                    if isSuccess:
                        return True
                else:

                    if self.isAssigned(char):   # if already assigned
                        isSuccess = self.backtrack(step, row + 1, carry)  # go to next row
                        if isSuccess:
                            return True
                    else:   # if not assigned yet
                        for i in range(10): # from 0-9
                            if self.checkConstraints(char, i):
                                self.assignment[char] = i
                                isSuccess = self.backtrack(step, row + 1, carry)  # go to next row
                                if isSuccess:
                                    return True
                                else:
                                    self.assignment.pop(char)   # pop out the value causing fail 
            
        else:   # handle the result (right side of '=')
            resStep = self.computeResStep(step, carry)

            # compute negative result
            tmpCarry = 0
            # if resStep = 10,20,30 --> standard = 10,20,30
            if resStep < 0:
                tmp = abs(int(resStep/10))
                if (resStep % 10) != 0:
                    tmp += 1
                standard = tmp*10 
                resStep = standard + resStep
                tmpCarry = -int(standard / 10)    
            strRes = str(resStep)  # convert result of current column to string
            correctDigit = int(strRes[-1])  # get the last digit
            if correctDigit == resStep: # if the result has 1 digit
                carryNext = tmpCarry
            else: 
                carryNext = int(strRes[0:len(strRes)-1])

            if step + 1 > len(self.result):
                if correctDigit == 0:
                    isSuccess = self.backtrack(step + 1, 0, carryNext) # go to next step
                    if isSuccess:
                        return True
            else:
                char = self.result[-step-1] # get the character of result
                if self.isAssigned(char):   # if already assigned
                    if self.assignment.get(char) == correctDigit:   # if the value of assigned letter is valid
                        isSuccess = self.backtrack(step + 1, 0, carryNext) # go to next step
                        if isSuccess:
                            return True
                else: # if not assigned yet
                    if self.checkConstraints(char, correctDigit):
                        self.assignment[char] = correctDigit
                        isSuccess = self.backtrack(step + 1, 0, carryNext)  # go to next step
                        if isSuccess:
                            return True
                        else:
                            self.assignment.pop(char)
        return False

problem = CSP()
res = problem.solution()
print(res)