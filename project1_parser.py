def reduce_code(code): 
    code = code.splitlines()

    # Converts code into an itemized list
    for i in range(len(code) - 1, -1, -1): 
        if(len(code[i]) == 0): code.pop(i)  # Removes empty strings
        else:
            # Associates lines of code with depth
            code[i] = code[i].split("    ")
            code[i][0] = 0
            keep = True

            if(len(code[i]) > 1):   # Accounts for empty (blank) lines
                while(code[i][1] == ""):    # Counts number of blanks (depth)
                    code[i][0] += 1
                    code[i].pop(1)
                    if(len(code[i]) <= 1):  # Deletes empty (string) lines
                        keep = False
                        break
                
                if(keep == True): 
                    code[i][1] = code[i][1].split(" ")  # Breaks code into characters/strings
                    code[i][1] = [item for item in code[i][1] if item != ""]    # Filters empty items

            else: keep = False

            if(keep == False): code.pop(i)  # Removes empty lines

    return code

def reduce_code2(code): 
    code = code.splitlines()

    # Converts code into an itemized list
    for i in range(len(code) - 1, -1, -1): 
        if(len(code[i]) == 0): code.pop(i)  # Removes empty strings
        else:
            code[i] = code[i].split(" ")  # Breaks code into characters/strings
            code[i] = [item for item in code[i] if item != ""]    # Filters empty items
            if(len(code[i]) == 0): code.pop(i)

    return code

code_5 = '''
    x = 5 + 3 + 10
    y = x + 3
    if y > 8 then z = y - x else z = y + x
    x = x / y
    x = y + x * x
    while x > 0 do
        while y > 0 do
            x = x - 1
    '''

print(reduce_code(code_5))
print()
print(reduce_code2(code_5))



# Lexer
class Lexer:
    def __init__(self, code):
        self.code = self.reduce_code(code)
        self.position = 0

    def reduce_code(self, code): 
        code = code.splitlines()

        # Converts code into an itemized list
        for i in range(len(code) - 1, -1, -1): 
            if(len(code[i]) == 0): code.pop(i)  # Removes empty strings
            else:
                code[i] = code[i].split(" ")  # Breaks code into characters/strings
                code[i] = [item for item in code[i] if item != ""]    # Filters empty items
                if(len(code[i]) == 0): code.pop(i)

        return code
    
    # inserts a new line into (directly after) current position
    def add_line(self, line):
        depth = self.get_depth(self.position - 1)
        self.code.insert(self.position, [depth, line])

    # move the lexer position and identify next possible tokens.
    def get_token(self):
        if(self.position >= len(self.code)): # if no other code exists, terminates
            return False
        else:   # gets a line of code
            self.position += 1
            return self.code[self.position - 1]

# Parser
# Input : lexer object
# Output: AST program representation.


# First and foremost, to successfully complete this project you have to understand
# the grammar of the language correctly.

# We advise(not forcing you to stick to it) you to complete the following function 
# declarations.

# Basic idea is to walk over the program by each statement and emit a AST representation
# in list. And the test_utility expects parse function to return a AST representation in list.
# Return empty list for ill-formed programs.

# A minimal(basic) working parser must have working implementation for all functions except:
# if_statment, while_loop, condition.



class Parser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = None
        self.prefix = []    # stores all lines in prefix notation
    
    # function to parse the entire program
    def parse(self):
        # iterates through and processes all tokens
        while(self.current_token != False): 
            self.advance() 
            if(self.current_token != False): self.prefix.append(self.statement())

        # Returns the joined stringified statements (aka program)
        return ''.join([self.parse_statement(item) for item in self.prefix])
        
    # processes next token 
    def advance(self):
        self.current_token = self.lexer.get_token()

    # stringifies a statement
    def parse_statement(self, statement):        
        if(statement == None): return "(NONE)"
        for i in range(len(statement)): 
            # recursively parses if statement has nested components
            if(type(statement[i]) == list): 
                statement[i] = self.parse_statement(statement[i])

            # is_digit checks if contains only digits (which matches definition of digit in grammar)
            elif(not statement[i].isdigit()):     
                statement[i] = f"'{statement[i]}'"
            
        return f"({', '.join(statement)})"
    
    # parse if, while, assignment statement.
    def statement(self):
        if(self.current_token[0] == 'if'): 
            return self.if_statement(['if'])
        elif(self.current_token[0] == 'while'): 
            return self.while_loop(['while'])
        else:   # No error-checking
            return self.assignment(['='])

    # Checks if abnormal variable during assignment (= new line)
    def assignment_new_line_check(self, exp): 
        symbols = "+-*/"
        for i in range(len(exp) - 1): 
            if((not exp[i] in symbols) and (not exp[i + 1] in symbols)): 
                self.lexer.add_line(exp[i + 1:])    # New line
                return exp[:i + 1]          # Truncated line
            
        return exp  # Normal line if no problems

    # parse assignment statements
    def assignment(self, out):
        out.append(self.current_token[0])
        exp = self.current_token[2:]
        exp = self.assignment_new_line_check(exp)
        out.append(self.arithmetic_expression(exp))
        return out

    # parse arithmetic experssions
    def arithmetic_expression(self, exp, first = True):
        exp = self.factor(exp)

        index = 0
        while(index < len(exp)): 
            # Creates a new term for every add/sub
            if(exp[index] == "+" or exp[index] == "-"): 
                exp[index - 1] = [exp[index], exp[index - 1], exp[index + 1]]
                for i in range(2): exp.pop(index)
            else: index += 1
        
        # No (more) adds or subs
        if(first): return exp[0]  
        return exp
                
    # Checks for mults/divs
    def term(self, exp):
        index = 0
        while(index < len(exp)): 
            # Creates a new term for every mult/div
            if(exp[index] == "/" or exp[index] == "*"): 
                exp[index - 1] = [exp[index], exp[index - 1], exp[index + 1]]
                for i in range(2): exp.pop(index)
            else: index += 1
        
        return exp  # No (more) mults or divs
    
    # Checks if nested arithmetic expression
    def factor(self, exp, index = 0):
        while(index < len(exp)): 
            if(exp[index][0] == "("): 
                exp[index] = exp[index][1:]     # Removes the "("
                while(exp[index][-1] != ")"): index += 1
                exp[index] = exp[index][:-1]    # Removes the ")"
                return self.arithmetic_expression(self.arithmetic_expression(exp[0:index + 1], False) + exp[index + 1:], False)
            else: index += 1
        return self.term(exp)
        

    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self, out):
        cond, index = self.condition(self.current_token)
        out.append(cond)
        if(index == len(self.current_token) - 1): 
            self.advance()
            out.append(self.statement())
        else: 
            index2 = index + 1
            while(index2 < len(self.current_token)): 
                if()


        return out

    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self, out):
        pass
    
    
    # Returns formatted conditional + starting index
    def condition(self, line):
        index = 0
        while(line[index] not in ["==", "!=", "<", "<=", ">", ">="]): index += 1
        cond = [line[index], self.arithmetic_expression(line[:index - 1])],

        index2 = 0
        while(line[index2] not in ["then", "do"]): index2 += 1
        cond.append[self.arithmetic_expression[index + 1, index2 - 1]]
        return cond, index2