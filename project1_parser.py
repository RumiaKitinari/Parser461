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
    
    # given a line, gets the depth of code
    def get_depth(self, position): 
        return self.code[position][0]

    # retrieves a nested token if possible, False o/w
    def get_nested_token(self): 
        depth = self.code[self.position - 1]
        if(self.get_depth(self.position) > depth): 
            return self.get_token()
        return False
    
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
    
    # returns the code part of current token
    def get_code(self): return self.current_token[1]

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
        if(self.get_code()[0] == 'if'): 
            return self.if_statement(['if'])
        elif(self.get_code()[0] == 'while'): 
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
        out.append(self.get_code()[0])
        exp = self.get_code()[2:]
        exp = self.assignment_new_line_check(exp)
        out.append(self.arithmetic_expression(self.get_code()[2:]))
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
        pass

    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self, out):
        pass
    

    def condition(self, out):
        pass