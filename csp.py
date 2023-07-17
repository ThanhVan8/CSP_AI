def input():
    s = open("input.txt").read()
    inp = s.split("=")
    operators = []
    operands = []
    oprd = ""
    for i in inp[0]:
        if(i.isalpha()):
            oprd += i
        else:
            operators.append(i)
            operands.append(oprd)
            oprd = ""
    operands.append(oprd)
    return operands, operators, inp[1]

def checkFirstDigit(c, value, operands):
    if value == 0:
        for op in operands:
            if(c == op[0]):
                return False
    return True

def checkValidCompute(sum, res, carry):
    carryNext = (res + 10 * carry) - sum
    if carryNext == 0 or carryNext == 1:
        return carryNext
    else:
        return -1

def checkFirstDigitRes(assignment, step, res):
    if(len(res) > step):
        assignment[res[0]] = 1

def isAssigned(ch, assignment):
    if ch in assignment:
        return True
    return False

def compute(res, val, row, operators):
    if row == 0:
        res += val
    else:
        if operators[row - 1] == '+':
            res += val
        elif operators[row - 1] == '-':
            res -= val
    return res
            

def solution():
    operands, operators, result = input()
    maxStep = max(len(op) for op in operands)
    assignment = {}
    carry = 0
    checkFirstDigitRes(assignment, maxStep, result)
    if assignment:
        carry = 1
    res = backtrack(assignment, operands, operators, result, 0, 0, 0, carry, maxStep)
    if res:
        return assignment
    else:
        return None

def backtrack(assignment, operands, operators, result, step, row, resStep, carry, maxStep):
    if step >= maxStep:
        if carry == 0:
            return True
        else:
            return False
        
    if row <= len(operands) - 1: # if assign operands
        col = len(operands[row]) - maxStep + step
        if col < 0:
            isSuccess = backtrack(assignment, operands, operators, result, step, row + 1, resStep, carry, maxStep)
            if isSuccess:
                return True
        else:
            char = operands[row][col]
            if isAssigned(char, assignment):
                resStep = compute(resStep, assignment.get(char), row, operators)
                isSuccess = backtrack(assignment, operands, operators, result, step, row + 1, resStep, carry, maxStep)
                if isSuccess:
                    return True
            else:
                i = 9
                while i >= 0: # 9-0
                    if i not in assignment.values():
                        assignment[char] = i
                        resPrev = resStep
                        resStep = compute(resStep, assignment.get(char), row, operators)
                        isSuccess = backtrack(assignment, operands, operators, result, step, row + 1, resStep, carry, maxStep)
                        if isSuccess:
                            return True
                        else:
                            resStep = resPrev
                            assignment.pop(char)
                    i -= 1
                return False
        
    else:
        char = result[len(result) - maxStep + step]
        if isAssigned(char, assignment):
            carryNext = checkValidCompute(resStep, assignment.get(char), carry)
            if carryNext != -1:
                isSuccess = backtrack(assignment, operands, operators, result, step + 1, 0, 0, carryNext, maxStep)
                if isSuccess:
                    return True
            else:
                return False
        else:
            correctDigit = resStep - 10 * carry
            if correctDigit < -1 or correctDigit > 9:
                return False
            if correctDigit == -1 or correctDigit in assignment.values(): # if digit in use
                if correctDigit + 1 in assignment.values():
                    return False
                else:
                    assignment[char] = correctDigit + 1
                    isSuccess = backtrack(assignment, operands, operators, result, step + 1, 0, 0, 1, maxStep)
                    if isSuccess:
                        return True
                    else:
                        assignment.pop(char)
            else:
                assignment[char] = correctDigit
                isSuccess = backtrack(assignment, operands, operators, result, step + 1, 0, 0, 0, maxStep)
                if isSuccess:
                    return True
                else:
                    assignment.pop(char)
    return False

assign = solution()
print(assign)