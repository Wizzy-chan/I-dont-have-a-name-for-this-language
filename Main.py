# Instructions take form ( instr, ) with any additional data (i.e end of a block) stored in the tuple

import sys
import re

LITERAL = 0
PRINT = 1
COPY = 2
DROP = 3
ADD = 4
SUB = 5
MULT = 6
DIV = 7
MOD = 8
IF = 9
FOR = 10
END = 11
NOT = 12
AND = 13
OR = 14
SWAP = 15
CLEAR = 16
INPI = 17
INPS = 18
WHILE = 19

fp = sys.argv[1]
with open(fp) as file:
    program = file.read()

parsed = []
consts = {}
whitespace = ["\n", " ", "\t"]
quotes = ["\"", "\'"]
digits = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]

def check_string(program, curr, string):
    length = len(string)
    if program[curr:curr+length] == string:
        return True
    return False

def check_char(program, curr, char):
    if program[curr] == char:
        return True
    return False

def parse_num(program, curr):
    close = curr+1
    # Find first non numeric character
    while program[close] in digits:
        close += 1
    num = int( program[curr:close] )
    curr = close+1 # Continue after int literal
    return num, curr

# Parse file
curr = 0
while curr < len(program):
    if program[curr] in whitespace:
        curr += 1 # Ignore whitespace

    # String Literal
    elif program[curr] in quotes:
        quote = program[curr]
        # Find closing quotation
        close = curr+1
        while program[close] != quote:
            close += 1
        string = program[curr+1:close]
        string = re.sub(r'\\n', '\n', string)

        parsed.append((LITERAL, string))
        curr = close+1 # Continue after string literal

    # Int Literal
    elif program[curr] in digits:
        num, curr = parse_num(program, curr)
        parsed.append((LITERAL, num))

    # Const Declaration
    elif check_string(program, curr, "const"):
        curr += 6
        close = curr + 1
        # Find end of const name
        while program[close] not in whitespace:
            close += 1
        const_name = program[curr:close]
        curr = close+1 # Skip following space too :)
        if curr in quotes:
            quote = program[curr]
            # Find closing quotation
            close = curr+1
            while program[close] != quote:
                close += 1
            string = program[curr+1:close]
            string = re.sub(r'\\n', '\n', string)
            consts[const_name] = string
            curr = close+1 # Continue after string literal
        else:
            num, curr = parse_num(program, curr)
            consts[const_name] = num

    # Keyword or operation
    else:
        if   check_string(program, curr, "print"):
            parsed.append((PRINT,))
            curr += 5
        elif check_string(program, curr, "drop" ):
            parsed.append((DROP,))
            curr += 4
        elif check_string(program, curr, "copy" ):
            parsed.append((COPY,))
            curr += 4
        elif check_char  (program, curr, "+"    ):
            parsed.append((ADD,))
            curr += 1
        elif check_char  (program, curr, "-"    ):
            parsed.append((SUB,))
            curr += 1
        elif check_char  (program, curr, "*"    ):
            parsed.append((MULT,))
            curr += 1
        elif check_char  (program, curr, "/"    ):
            parsed.append((DIV,))
            curr += 1
        elif check_char  (program, curr, "%"    ):
            parsed.append((MOD,))
            curr += 1
        elif check_string(program, curr, "if"   ):
            parsed.append((IF,))
            curr += 2
        elif check_string(program, curr, "end"  ):
            parsed.append((END,))
            curr += 3
        elif check_string(program, curr, "not"  ):
            parsed.append((NOT,))
            curr += 3
        elif check_string(program, curr, "and"  ):
            parsed.append((AND,))
            curr += 3
        elif check_string(program, curr, "or"   ):
            parsed.append((OR,))
            curr += 2
        elif check_string(program, curr, "swap" ):
            parsed.append((SWAP,))
            curr += 4
        elif check_string(program, curr, "clear"):
            parsed.append((CLEAR,))
            curr += 5
        elif check_string(program, curr, "inpi" ):
            parsed.append((INPI,))
            curr += 4
        elif check_string(program, curr, "inps" ):
            parsed.append((INPS,))
            curr += 4
        elif check_string(program, curr, "while"):
            parsed.append((WHILE,))
            curr += 5
        elif check_string(program, curr, "for"  ):
            curr += 4 # length of "for" plus following space
            # Find out the bounds
            first, curr = parse_num(program, curr)
            curr += 1
            second, curr = parse_num(program, curr)
            parsed.append((FOR, first, second, first))
        else:
            valid_const = False
            for const in consts:
                if check_string(program, curr, const):
                    parsed.append((LITERAL, consts[const]))
                    curr += len(const)
                    valid_const = True
                    break
            if not valid_const:
                print("Error while parsing char", f"{curr=} {program[curr]=}")
                exit(1)

# Link block statements together for control flow
blocks = [ IF, FOR, WHILE ]

for i, instr in enumerate(parsed):
    if instr[0] in blocks:
        end = i
        nests = 1
        while parsed[end] != (END, ) or nests != 0:
            end += 1
            if parsed[end][0] in blocks:
                nests += 1
            if parsed[end] == (END, ):
                nests -= 1
        if instr[0] == IF:
            parsed[i] = (IF, end)
            parsed[end] = (END, IF, i)
        elif instr[0] == FOR:
            parsed[i] = (FOR, end, instr[1], instr[2], instr[3])
            parsed[end] = (END, FOR, i)
        elif instr[0] == WHILE:
            parsed[i] = (WHILE, end)
            parsed[end] = (END, WHILE, i)

# Block checking code: Uncomment to print out how blocks are linked (Does not interpret code if done so)

# for i, instr in enumerate(parsed):
#     if instr[0] in blocks:
#         print(f"{i} - {instr[1]}")
#         print(f"{instr[1]} - {parsed[instr[1]][2]}")
# exit()

# Interpret code
stack = []
pointer = 0
while pointer < len(parsed):
    instr = parsed[pointer]
    if instr[0] == LITERAL:
        stack.append(instr[1])
    elif instr[0] == PRINT:
        print(stack.pop(), end="")
    elif instr[0] == COPY:
        top = stack.pop()
        stack.append(top)
        stack.append(top)
    elif instr[0] == DROP:
        stack.pop()
    elif instr[0] == ADD:
        a = stack.pop()
        b = stack.pop()
        stack.append(a+b)
    elif instr[0] == SUB:
        a = stack.pop()
        b = stack.pop()
        stack.append(b-a)
    elif instr[0] == MULT:
        a = stack.pop()
        b = stack.pop()
        stack.append(a*b)
    elif instr[0] == DIV:
        a = stack.pop()
        b = stack.pop()
        stack.append(b//a)
    elif instr[0] == MOD:
        a = stack.pop()
        b = stack.pop()
        stack.append(b%a)
    elif instr[0] == IF:
        a = stack.pop()
        if not a:
            pointer = instr[1]
    elif instr[0] == FOR:
        if instr[4] == instr[3] + 1:
            parsed[pointer] = (instr[0], instr[1], instr[2], instr[3], instr[2]) # Reset loop and jump to the end
            pointer = instr[4]
        else:
            stack.append(instr[4])
            parsed[pointer] = (instr[0], instr[1], instr[2], instr[3], instr[4]+1) # Add one to the next value
    elif instr[0] == END:
        if instr[1] == FOR or instr[1] == WHILE:
            pointer = instr[2]-1
        elif instr[1] == IF:
            pass
    elif instr[0] == NOT:
        a = stack.pop()
        if a:
            stack.append(False)
        else:
            stack.append(True)
    elif instr[0] == OR:
        a = stack.pop()
        b = stack.pop()
        if a or b:
            stack.append(True)
        else:
            stack.append(False)
    elif instr[0] == AND:
        a = stack.pop()
        b = stack.pop()
        if a and b:
            stack.append(True)
        else:
            stack.append(False)
    elif instr[0] == SWAP:
        a = stack.pop()
        b = stack.pop()
        stack.append(a)
        stack.append(b)
    elif instr[0] == CLEAR:
        stack = []
    elif instr[0] == INPI:
        stack.append( int( input() ) )
    elif instr[0] == INPS:
        stack.append( input() )
    elif instr[0] == WHILE:
        a = stack.pop()
        if not a:
            pointer = instr[1]
            
    pointer += 1