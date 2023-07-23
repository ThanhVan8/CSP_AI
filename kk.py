class CSP:
    assignment = {}
    # negCarry = 0
    # ONE + ONE = TWO 
    def __init__(self):
        s = open("input.txt").read()
        # inp = [[ONE+ONE], [TWO]] 
        inp = s.split("=")
        # result = TWO
        self.result = inp[1]

        self.operators = []
        self.operands = []
        operandTmp = ""   # each operand
        for i in inp[0]:
            if(i.isalpha()):
                # operandTmp = [ONE]
                operandTmp += i
            else:
                # operators = [+]
                self.operators.append(i)
                # operands = [ONE, ONE]
                self.operands.append(operandTmp)
                operandTmp = ""
        self.operands.append(operandTmp)

        # lấy số lượng từ dài nhất
        self.maxStep = max(max((len(op) for op in self.operands)), (len(self.result)))
        self.leadingLetters = set(x[0] for x in self.operands)  # first letter of each operands
        self.leadingLetters.add((self.result[0]))
        
        
    
    def isAssigned(self, letter):
        return True if letter in self.assignment else False
    
    def compute(self, res, val, row):   # compute the 'val' into 'res' at operand 'row'
        if row == 0:
            res += val
        else:
            if self.operators[row - 1] == '+':
                res += val
            elif self.operators[row - 1] == '-':
                if(res<val):
                    # if(abs(res)<val):
                    #     # tăng biến nhớ lên
                    #     res = abs(res)+10 - val
                    # elif (abs(res)>=val): 
                    #     res = abs(res)-val   
                    # return -res
                    # # self.negCarry +=-1\
                    # nếu số bị trừ nhỏ hơn, mượn 10 - đi số trừ
                    res = res*10 - val
                    # đánh dấu là có mượn 10
                    return -res
                else: res -= val
        return res

    def checkConstraints(self, letter, value):
        # gán giá trị bị trùng
        if value in self.assignment.values():
            return False
        # gán giá trị 0 cho chữ cái đầu
        if letter in self.leadingLetters and value == 0:
            return False
        # gán giá trị âm cho kết quả cuối cùng
        if letter == self.result[0] and value < 0:
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
        # điểm dừng
        if step > self.maxStep - 1:
            return True
                
        if row <= len(self.operands) - 1: # handle the operands (left side of '=')
            if step > len(self.operands[row]) - 1: # if go beyond the first letter of current operand (vượt ra ngoài)
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
                        if self.checkConstraints(char, i):
                            self.assignment[char] = i
                            resPrev = resStep   # store the old result in case backtrack fail
                            resStep = self.compute(resStep, self.assignment.get(char), row)
                            isSuccess = self.backtrack(step, row + 1, resStep, carry)  # go to next row
                            if isSuccess:
                                print(resStep)
                                return True
                            else:
                                resStep = resPrev   # back to the old result
                                self.assignment.pop(char)   # pop out the value causing fail 
            
        else:   # handle the result (right side of '=')
            if(abs(-step-1) > len(self.result)):
                char = '0'
            else: char = self.result[-step-1] # get the character of result

            # xử lý kq âm
            # kiểm tra coi có mượn 10 khong
            if(resStep<0):
                # biến nhớ được gán tại đây
                carry = -1
                resStep *=-1
            else: carry= 0

            strRes = str(resStep)  # convert result of current column to string
            correctDigit = int(strRes[-1])  # get the last digit
            if correctDigit == resStep: # if the result has 1 digit
                carryNext = carry
            else: 
                carryNext = int(strRes[0:len(strRes)-1])
            if(char =='0'):
                isSuccess = self.backtrack(step + 1, 0, carryNext, carryNext) # go to next step
                if isSuccess:
                    return True
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


# CODE CHẠY ĐC TRỪ TRỪ CÁC SỐ HẠNG CÓ CÙNG ĐỘ DÀI

