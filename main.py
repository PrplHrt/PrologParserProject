import re
from enum import Enum


class error(Exception):
    def __init__(self, arg):
        global num_errors
        self.args = arg
        num_errors += 1

    def __str__(self):
        outputFile.write(''.join(self.args))
        outputFile.write('\n')
        return ''.join(self.args)


################################ SYNTAX ANALYZER ################################

# <program> -> <clause-list> <query> | <query>
def program():
    getChar()
    print("Enter Program")
    lex()
    try:
        clause_list()
    except error as e:
        print(e)
        while nextToken != TokenClass.QUERY_SYM and nextToken != CharClass.EOF:
            lex()
    try:
        query()
    except error as e:
        print(e)
        if nextToken != CharClass.EOF:
            lex()
            if nextToken == TokenClass.ATOM:
                predicateList()
            else:
                e_ = error(f"Invalid Query at line {line}, no atom found at expected predicate list.")
                print(e_)

    if nextToken == CharClass.EOF:
        print("End of File reached")


# <clause-list> -> <clause> | <clause> <clause-list>
def clause_list():
    print("Enter Clause_List")
    try:
        while nextToken == TokenClass.ATOM:
            clause()

    except error as e:
        print(e)
        while nextChar != '\n':
            lex()


# <clause> -> <predicate> . | <predicate> :- <predicate-list> .
def clause():
    print("Enter Clause")
    try:
        predicate()
    except error as e:
        print(e)
        while nextToken != TokenClass.IMPLY and nextToken != TokenClass.DELIMITER:
            lex()

    if nextToken == TokenClass.IMPLY:
        lex()
        predicateList()
    if nextToken == TokenClass.DELIMITER:
        lex()
    else:
        # Error - no Full Stop/End of Statement
        raise error(f"Invalid clause at line {line}, no Delimiter at end of clause")


# <query> -> ?- <predicate-list> .
def query():
    print("Enter Query")
    # Check if it starts with Query
    if nextToken == TokenClass.QUERY_SYM:
        # Get the next Token
        lex()
        predicateList()
        if nextToken == TokenClass.DELIMITER:
            lex()
        else:
            # Error - no ending delimiter
            raise error(f"Invalid Query at line {line}, No ending delimiter at Query")

    else:
        # Error - no query symbol
        raise error(f"Invalid Query at line {line}, No Query symbol in Query")


# <predicate-list> -> <predicate> | <predicate> , <predicate-list>
def predicateList():
    print("Enter Predicate List")
    try:
        predicate()
    except error as e:
        print(e)
        while nextToken != TokenClass.AND_OP and nextChar != '\n' and nextToken != CharClass.EOF:
            lex()

    while nextToken == TokenClass.AND_OP:
        lex()
        predicateList()


# <predicate> -> <atom> | <atom> ( <term-list> )
def predicate():
    print("Enter Predicate")
    if nextToken == TokenClass.ATOM:
        lex()
        if nextToken == CharClass.LEFT_PAREN:
            lex()
            try:
                term_list()
            except error as e:
                print(e)
                while nextToken != CharClass.RIGHT_PAREN and nextChar != '\n' and nextToken != CharClass.EOF:
                    lex()

            if nextToken == CharClass.RIGHT_PAREN:
                lex()
            else:
                # Error - no Right Parenthesis
                raise error(f"Invalid Predicate at line {line}, No Right Parenthesis at Predicate")
        else:
            pass
    else:
        # Error - no Atom
        raise error(f"Invalid Predicate at line {line}, No Atom at expected Predicate, lexeme {lexeme}")


# <term-list> -> <term> | <term> , <term-list>
def term_list():
    print("Enter term list")
    try:
        term()
    except error as e:
        print(e)
        while nextToken != TokenClass.AND_OP and nextChar != '\n':
            lex()

    while nextToken == TokenClass.AND_OP:
        lex()
        term_list()
        if nextToken == TokenClass.UNKNOWN:
            raise error(f"Invalid Term list at line {line}, lexeme {lexeme}")

    print("Exiting term_list")


# <term> -> <atom> | <structure> | <variable> | <numeral>
# <term> -> <predicate> | <variable> | <numeral>

def term():
    print("Enter Term")
    if nextToken == TokenClass.VARIABLE:
        lex()
    elif nextToken == TokenClass.NUMERAL:
        lex()
    elif nextToken == TokenClass.ATOM:
        lex()
        if nextToken == CharClass.LEFT_PAREN:
            lex()
            try:
                term_list()
            except error as e:
                print(e)
            if nextToken == CharClass.RIGHT_PAREN:
                lex()
            else:
                # no right parenthesis
                raise error(f"Invalid structure at line {line}, missing right parenthesis")
        else:
            pass
    else:
        raise error(f"Invalid Term at line {line}, Invalid Token, lexeme {lexeme}.")


# <structure> -> <atom> ( <term-list> )
# def structure():
#     print("Enter Structure")
#     if nextToken == TokenClass.ATOM:
#         lex()
#         if nextToken == CharClass.LEFT_PAREN:
#             lex()
#             term_list()
#             if nextToken == CharClass.RIGHT_PAREN:
#                 lex()


################################ LEXICAL ANALYZER ################################

class CharClass(Enum):
    LOWERCASE = 0
    UPPERCASE = 1
    DIGIT = 2
    COLON = 100
    BACKSLASH = 101
    CARET = 102
    TILD = 103
    FULLSTOP = 104
    QUESTIONMARK = 105
    HASH = 106
    DOLLARSIGN = 107
    AMPERSAND = 108
    ADD_OP = 109
    SUB_OP = 110
    MULT_OP = 111
    DIV_OP = 112
    SPACE = 113
    LEFT_PAREN = 3
    RIGHT_PAREN = 4
    SINGLEQUOTE = 5
    COMMA = 6
    EOF = 666
    UNKNOWN = 777


class TokenClass(Enum):
    SPECIAL = 0
    CHARACTER = 1
    STRING = 2
    NUMERAL = 3
    ALPHANUMERIC = 4
    CHAR_LIST = 5
    VARIABLE = 6
    ATOM = 8
    QUERY_SYM = 15
    IMPLY = 16
    DELIMITER = 20
    AND_OP = 21
    UNKNOWN = -1


line = 1
num_errors = 0
charClass = 0
lexeme = ''
nextChar = ''
nextToken = 0
inputFile = None
SPECIAL = ['+', '-', '*', '/', '\\', '^', '~', ':', '.', '?', ' ', '\#', '$', '&']


def getChar():
    global nextChar, charClass, line, num_errors
    nextChar = inputFile.read(1)
    if nextChar:
        if re.match('[A-Z_]', nextChar):
            charClass = CharClass.UPPERCASE
        elif re.match('[a-z]', nextChar):
            charClass = CharClass.LOWERCASE
        elif re.match(r'\d', nextChar):
            charClass = CharClass.DIGIT
        elif nextChar == '.':
            charClass = CharClass.FULLSTOP
        elif nextChar == '(':
            charClass = CharClass.LEFT_PAREN
        elif nextChar == ')':
            charClass = CharClass.RIGHT_PAREN
        elif nextChar == "'":
            charClass = CharClass.SINGLEQUOTE
        elif nextChar == '+':
            charClass = CharClass.ADD_OP
        elif nextChar == '-':
            charClass = CharClass.SUB_OP
        elif nextChar == '*':
            charClass = CharClass.MULT_OP
        elif nextChar == '/':
            charClass = CharClass.DIV_OP
        elif nextChar == '\\':
            charClass = CharClass.BACKSLASH
        elif nextChar == ':':
            charClass = CharClass.COLON
        elif nextChar == '&':
            charClass = CharClass.AMPERSAND
        elif nextChar == '^':
            charClass = CharClass.CARET
        elif nextChar == '$':
            charClass = CharClass.DOLLARSIGN
        elif nextChar == '~':
            charClass = CharClass.TILD
        elif nextChar == '?':
            charClass = CharClass.QUESTIONMARK
        elif nextChar == '#':
            charClass = CharClass.HASH
        elif nextChar == ' ':
            charClass = CharClass.SPACE
        elif nextChar == ',':
            charClass = CharClass.COMMA
        elif nextChar == '\n':
            line += 1
            charClass = CharClass.UNKNOWN
        else:
            print(f'Error - unrecognized character {nextChar} at line {line}')
            outputFile.write(f'Error - unrecognized character {nextChar} at line {line}\n')
            num_errors += 1
            charClass = CharClass.UNKNOWN
    else:
        charClass = CharClass.EOF


def addChar():
    global lexeme
    lexeme += nextChar


def getNonBlank():
    while nextChar.isspace():
        getChar()


def lex():
    global nextToken, lexeme
    lexeme = ''

    getNonBlank()

    # End of program
    if not charClass or charClass == CharClass.EOF:
        nextToken = CharClass.EOF

    # Parse variable
    elif charClass == CharClass.UPPERCASE:
        addChar()
        getChar()
        while 0 <= charClass.value <= 2:
            addChar()
            getChar()

        nextToken = TokenClass.VARIABLE

    # Parse numeral
    elif charClass == CharClass.DIGIT:
        addChar()
        getChar()
        while charClass == CharClass.DIGIT:
            addChar()
            getChar()

        nextToken = TokenClass.NUMERAL

    # Parse Query
    elif charClass == CharClass.QUESTIONMARK:
        addChar()
        getChar()
        if charClass == CharClass.SUB_OP:
            addChar()
            getChar()
            nextToken = TokenClass.QUERY_SYM
        else:
            # ERROR
            pass

    # Parse Implied By
    elif charClass == CharClass.COLON:
        addChar()
        getChar()
        if charClass == CharClass.SUB_OP:
            addChar()
            getChar()
            nextToken = TokenClass.IMPLY
        else:
            # ERROR
            pass

    # Parse String into Atom
    elif charClass == CharClass.SINGLEQUOTE:
        addChar()
        getChar()
        while 100 <= charClass.value <= 113 or 0 <= charClass.value <= 2:
            addChar()
            getChar()

        if charClass == CharClass.SINGLEQUOTE:
            addChar()
            getChar()
            nextToken = TokenClass.ATOM
        else:
            # ERROR
            pass

    # Parse Small Atom into Atom
    # A small atom is also an atom. Think about combining with string rule if possible
    elif charClass == CharClass.LOWERCASE:
        addChar()
        getChar()
        while 0 <= charClass.value <= 2:
            addChar()
            getChar()

        nextToken = TokenClass.ATOM

    # Parse And Operator
    elif charClass == CharClass.COMMA:
        addChar()
        getChar()
        nextToken = TokenClass.AND_OP

    # Parse Delimiter (End of Statement)
    elif charClass == CharClass.FULLSTOP:
        addChar()
        getChar()
        nextToken = TokenClass.DELIMITER

    # Parse Left Parenthesis
    elif charClass == CharClass.LEFT_PAREN:
        addChar()
        getChar()
        nextToken = CharClass.LEFT_PAREN

    # Parse Right Parenthesis
    elif charClass == CharClass.RIGHT_PAREN:
        addChar()
        getChar()
        nextToken = CharClass.RIGHT_PAREN

    else:
        addChar()
        getChar()
        nextToken = TokenClass.UNKNOWN
    print(f'{lexeme:<20} is a {nextToken:20}')


################################ MAIN ################################


if __name__ == '__main__':
    # Here we open the file and insert it into the analyzer
    try:
        try:
            outputFile = open('parser_output.txt', 'w')
            i = 1
            while True:
                line = 1
                num_errors = 0
                file = f"{i}.txt"
                inputFile = open(file, 'r')
                outputFile.write(file.center(30, '~') + '\n')
                print(file.center(30, '~'))
                program()
                if num_errors == 0:
                    outputFile.write('Syntactically Correct\n')
                else:
                    outputFile.write(f'{num_errors} error(s) found\n')
                inputFile.close()
                i += 1
            outputFile.close()
        except Exception:
            outputFile.close()
            print("Done")
    except Exception as e:
        print(e)
