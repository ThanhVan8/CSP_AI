def ReadFile():
    n = input('File input: ')
    
    f = open(n, 'r')
    
    data = f.read()
    
    f.close()
    
    return data

def solve_cryptarithmetic(puzzle):
    words = puzzle.replace("+", "").replace("=", "").split()
    unique_letters = set("".join(words))
    letters = list(unique_letters)
    leading_letters = set(word[0] for word in words)

    def sum_word(word_list, assignment):
        result = 0
        for word in word_list:
            multiplier = 10 ** (len(word)-1)
            for char in word:
                result += assignment[char] * multiplier
                multiplier //= 10
        return result
    
    def is_solution(assignment):
        left = sum_word(words[:-1], assignment)
        right = sum_word([words[-1]], assignment)
        return left == right


    def backtrack(index, assignment, used_digits):
        if index == len(letters):
            return is_solution(assignment)

        letter = letters[index]
        for digit in range(10):
            if digit in used_digits:
                continue
            if digit == 0 and letter in leading_letters:
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


puzzle = ReadFile()
solution = solve_cryptarithmetic(puzzle)
n = input('Output file: ')
f = open(n, 'a')
if solution != False:
    sorted_solution = dict(sorted(solution.items(), key=lambda x: x[0]))
    print("Solution:")
    for letter, digit in sorted_solution.items():
        print(f"{letter} = {digit}")
        f.write(str(digit))
        
    f.close()
else:
    print(solution)