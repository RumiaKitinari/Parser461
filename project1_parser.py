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

                while(code[i][1] == ""):    # Counts number of blanks
                    code[i][0] += 1
                    code[i].pop(1)
                    if(len(code[i]) == 1):  # Deletes empty lines
                        code.pop(i)
                        break
                
                # Breaks code into characters/strings
                if(len(code) > i and len(code[i]) == 2): 
                    code[i][1] = code[i][1].split(" ")

        return code
    
    # given a line, gets the depth of code
    def get_depth(self, position): 
        return self.code[position][0]

    def get_nested_token(self): 
        depth = self.code[self.position - 1]
        if(self.get_depth(self.position) > depth): 
            return self.get_token()

    # move the lexer position and identify next possible tokens.
    def get_token(self):
        if(self.position > len(self.code)): # if no other code exists, terminates
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
            self.prefix.append(self.statement())

        # Returns the joined stringified statements (aka program)
        return ''.join([self.parse_statement(item) for item in self.prefix])

        
    # processes next token 
    def advance(self):
        self.current_token = self.lexer.get_token()

    # stringifies a statement
    def parse_statement(self, statement):        
        for i in range(len(statement)): 
            # recursively parses if statement has nested components
            if(type(statement[i]) == list): 
                statement[i] = self.parse_statement(statement[i])

            # is_digit checks if contains only digits (which matches definition of digit in grammar)
            elif(not statement[i].isdigit()):     
                statement[i] = f"'{statement[i]}'"
            
        return f"({', '.join(statement)})"
    
    # parse if, while, assignment statement.
    def statement(self, out = []):
        if(self.get_code()[0] == 'if'): 
            out.append('if')
            return self.if_statement(out)
        elif(self.get_code()[0] == 'while'): 
            out.append('while')
            return self.while_loop(out)
        else:   # No error-checking
            out.append('=')
            return self.assignment(out)


    # parse assignment statements
    def assignment(self):
        pass
     

    # parse arithmetic experssions
    def arithmetic_expression(self, ):
        pass
        
   
    def term(self, ):
        pass
    

    def factor(self, ):
        pass

    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self, curr_to):
        pass

    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        pass
    

    def condition(self):
        pass