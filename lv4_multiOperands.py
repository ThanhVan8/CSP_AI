def readFile():    
    f = open("input.txt", 'r')
    data = f.read()
    f.close()
    return data

def solve_cryptarithmetic(puzzle):
    inp = puzzle.split("=")
    words = puzzle.replace("+", "").replace("=", "").replace("*", "").split()
    letters = list(set("".join(words)))

    result = [inp[1]]

    operators = []
    operands = []
    operandTmp = ""   
    for i in inp[0]:
        if i.isalpha():
            operandTmp += i
        else:
            operators.append(i)
            operands.append(operandTmp)
            operandTmp = ""
    operands.append(operandTmp)
    leadingLetters = set(x[0] for x in operands)  # first letter of each operands
    leadingLetters.add((result[0]))

    def sum_word(word_list, assignment):
        result = 0
        resultMul = 1
        for word in word_list:
            multiplier = 10 ** (len(word)-1)
            for char in word:
                result += assignment[char] * multiplier
                multiplier //= 10
            resultMul *= result
            result = 0
        return resultMul
    
    def is_solution(assignment):
        left = sum_word(operands, assignment)
        right = sum_word(result, assignment)
        return left == right

    def backtrack(index, assignment, used_digits):
        if index == len(letters):
            return is_solution(assignment)

        letter = letters[index]
        for digit in range(10):
            if digit in used_digits:
                continue
            if digit == 0 and letter in leadingLetters:
                continue

            assignment[letter] = digit
            used_digits.add(digit)

            if backtrack(index + 1, assignment, used_digits):
                return True

            del assignment[letter]
            used_digits.remove(digit)

        return False

    assignment = {}
    used_digits = set()
    if backtrack(0, assignment, used_digits):
        return assignment
    else:
        return False


puzzle = readFile()
solution = solve_cryptarithmetic(puzzle)
f = open("output.txt", 'w')
if solution != False:
    sorted_solution = dict(sorted(solution.items(), key=lambda x: x[0]))
    print("Solution:")
    for letter, digit in sorted_solution.items():
        print(f"{letter} = {digit}")
        f.write(str(digit))
        
    f.close()
else:
    print(solution)