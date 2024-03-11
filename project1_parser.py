



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
        self.code.insert(self.position, line)

    # checks if next line starts with "else"
    def get_next_is_else(self): 
        if(self.position >= len(self.code)): return False   # Accounts for last-line "if-then"
        return self.code[self.position][0] == "else"

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
            if(self.current_token != False): self.prefix.append(self.statement(self.current_token))

        # Returns the joined stringified statements (aka program)
        return ''.join([self.parse_statement(item) for item in self.prefix])
        
    # processes next token 
    def advance(self):
        self.current_token = self.lexer.get_token()

    # stringifies a statement
    def parse_statement(self, statement, is_while = False):        
        for i in range(len(statement)): 
            # recursively parses if statement has nested components
            
            if(type(statement[i]) == list):
                if(statement[0] == "'while'" and i == 2): 
                    statement[i] = self.parse_statement(statement[i], True)
                else: 
                    statement[i] = self.parse_statement(statement[i])

            # is_digit checks if contains only digits (which matches definition of digit in grammar)
            elif(not statement[i].isdigit()):     
                statement[i] = f"'{statement[i]}'"
        
        if(is_while): return f"[({', '.join(statement)})]"
        return f"({', '.join(statement)})"
    
    # parse if, while, assignment statement.
    def statement(self, stmt):
        if(stmt[0] == 'if'): 
            return self.if_statement(['if'])
        elif(stmt[0] == 'while'): 
            return self.while_loop(['while'])
        else:   # No error-checking
            return self.assignment(['='], stmt)

    # Checks if abnormal variable during assignment (= new line)
    def assignment_new_line_check(self, exp): 
        symbols = "+-*/"
        for i in range(len(exp) - 1): 
            if((not exp[i] in symbols) and (not exp[i + 1] in symbols)): 
                self.lexer.add_line(exp[i + 1:])    # New line
                return exp[:i + 1]          # Truncated line
            
        return exp  # Normal line if no problems

    # parse assignment statements
    def assignment(self, out, line):
        out.append(line[0])
        exp = line[2:]
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
        cond, index2 = self.condition(self.current_token)
        out.append(cond)  # Appends formatted condition
        
        if(index2 == len(self.current_token)):  # Accepts next-line "then" statement
            self.advance()
            index2 = 0
        
        # Searches for "else"
        index3 = index2 + 1
        while(index3 < len(self.current_token)):    
            if(self.current_token[index3] == "else"): 
                out.append(self.statement(self.current_token[index2 : index3]))

                if(index3 == len(self.current_token) - 1):  # Accounts for separate-line statement after "else"
                    self.advance()
                    out.append(self.statement(self.current_token))
                else:   # Checks for same-line else
                    out.append(self.statement(self.current_token[index3 + 1:]))

                return out
            index3 += 1
                
        out.append(self.statement(self.current_token[index2:]))     # Adds "then" statement

        # Accepts next-line "else" statement
        if(self.lexer.get_next_is_else()):
            self.advance()
            if(len(self.current_token) == 1):   # Adds next-line "else" statement
                self.advance()
                out.append(self.statement(self.current_token))
            else: out.append(self.statement(self.current_token[1:]))    # Adds same-line "else" statement

        return out  # Returns outputted statement

    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self, out):
        cond, index2 = self.condition(self.current_token)
        out.append(cond)
        if(index2 == len(self.current_token)): 
            self.advance()
            out.append(self.statement(self.current_token))
        else: 
            out.append(self.statement(self.current_token[index2:]))
        return out
    
    
    # Returns formatted conditional + starting index
    def condition(self, line):
        index = 0
        while(line[index] not in ["==", "!=", "<", "<=", ">", ">="]): index += 1
        cond = [line[index], self.arithmetic_expression(line[1:index])]

        index2 = index
        while(line[index2] not in ["then", "do"]): index2 += 1
        cond.append(self.arithmetic_expression(line[index + 1 : index2]))
        return cond, index2 + 1     # returns full conditional, index after "then"/"do"
    

def test_parser(code):
    lex = Lexer(code)
    par = Parser(lex)
    print(par.parse())

code = '''
    x = 5 + 3
    y = 0
    if x > y then y = x
    else 
        y = 1
    '''
test_parser(code)