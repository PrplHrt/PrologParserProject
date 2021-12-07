import re
from enum import Enum


# <program> -> <clause-list> <query> | <query>


# <clause-list> -> <clause> | <clause> <clause-list>
# <clause> -> <predicate> . | <predicate> :- <predicate-list> .
# <query> -> ?- <predicate-list> .
# def query():
#     queryOperator()
#
#     predicateList()
#
#     getChar()
#     nextChar == CharClass.FULLSTOP


# <predicate-list> -> <predicate> | <predicate> , <predicate-list>
# def predicateList():
#     predicate()
#
#     while (nextToken == TokenClass.PREDICATE):
#         lex()
#         predicate()


# <predicate> -> <atom> | <atom> ( <term-list> )
# <term-list> -> <term> | <term> , <term-list>
# <term> -> <atom> | <variable> | <structure> | <numeral>

# <structure> -> <atom> ( <term-list> )
# <atom> -> <small-atom> | ' <string> '
# <small-atom> -> <lowercase-char> | <lowercase-char> <character-list>
# <variable> -> <uppercase-char> | <uppercase-char> <character-list>

# <character-list> -> <alphanumeric> | <alphanumeric> <character-list>
# <string> -> <character> | <character> <string>
# <numeral> -> <digit> | <digit> <numeral>

# <character> -> <alphanumeric> | <special>                             --> ALL
# <alphanumeric> -> <lowercase-char> | <uppercase-char> | <digit>       --> 0-2

# <lowercase-char> -> a | b | c | ... | x | y | z                       --> [a-z]
# <uppercase-char> -> A | B | C | ... | X | Y | Z | _                   --> [A-Z_]
# <digit> -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9                      --> [\d]
# <special> -> + | - | * | / | \ | ^ | ~ | : | . | ? | | # | $ | &      --> [\+\-\*\/\\\^\~\:\.\?\ \#\$\&]


SPECIAL = ['+', '-', '*', '/', '\\', '^', '~', ':', '.', '?', ' ', '\#', '$', '&']

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
    SMALL_ATOM = 7
    ATOM = 8
    STRUCTURE = 9
    TERM = 10
    TERM_LIST = 11
    PREDICATE = 12
    PREDICATE_LIST = 13
    QUERY = 14
    QUERY_SYM = 15
    IMPLY = 16
    CLAUSE = 17
    CLAUSE_LIST = 18
    PROGRAM = 19
    DELIMITER = 20
    AND_OP = 21


charClass = 0
lexeme = ''
nextChar = ''
lexLen = 0  # Not sure we need this
token = 0
nextToken = 0
inputFile = None


def getChar():
    global nextChar, charClass
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
            getChar()
        else:
            # Unrecognized character
            pass
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

    # skipped character list
    # skipped alpha num
    # skipped small atom
    # skipped character

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
        while 100 <= charClass.value <= 113:
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


if __name__ == '__main__':
    # Here we open the file and insert it into the analyzer
    try:
        outputFile = open('parser_output.txt', 'w')
        i = 1
        while True:
            file = str(i)+".txt"
            inputFile = open(file, 'r')
            outputFile.write(f'~~~~~~~~~~~ {file} ~~~~~~~~~~~~\n')
            getChar()
            while True:
                lex()
                if nextToken == CharClass.EOF:
                    break
                print(f'{lexeme} is a {nextToken}')
                outputFile.write(f'{lexeme:<30} is a {nextToken}\n')
            inputFile.close()
            i+=1
        
    except:
        outputFile.close()
        print("Done")