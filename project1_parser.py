# Lexer
class Lexer:
    def __init__(self, code):
        self.code = code
        self.position = 0

    # move the lexer position and identify next possible tokens.
    def get_token(self):
        pass

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

    # function to parse the entire program
    def parse(self):
        pass
        
    # move to the next token.
    def advance(self):
        pass

    # parse the one or multiple statements
    def program(self):
        pass
        
    
    # parse if, while, assignment statement.
    def statement(self):
        pass


    # parse assignment statements
    def assignment(self):
        pass
     

    # parse arithmetic experssions
    def arithmetic_expression(self):
        pass
        
   
    def term(self):
        pass
    

    def factor(self):
        pass

    # parse if statement, you can handle then and else part here.
    # you also have to check for condition.
    def if_statement(self):
        pass

    
    # implement while statment, check for condition
    # possibly make a call to statement?
    def while_loop(self):
        pass
    

    def condition(self):
        pass