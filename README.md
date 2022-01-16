# PrologParserProject
 CMP 321 - Prolog Parser Project in Python.
 
 Assigned by Dr. Michel of the CSE Department at the American University of Sharjah, for Fall 2021.
 
## Project Overview
In this project, you are to implement a Recursive Descent Parser that determines whether a given Prolog program is correct, or whether it contains syntax errors, according to the simplified BNF grammar given hereafter. You are strongly advised to follow the programming style of the class textbook when implementing both lexical analyzer (cf. section 4.2) and syntax analyzer (cf. section 4.4). Coding a parser is essentially about implementing sequential steps, strictly as defined by the rules of the language’s grammar. In this assignment, you must use either of C, C++, Java, or Python. Using regular expressions is optional.

## Prolog Grammar in BNF
    <program> -> <clause-list> <query> | <query>
    <clause-list> -> <clause> | <clause> <clause-list>
    <clause> -> <predicate> . | <predicate> :- <predicate-list> .
    <query> -> ?- <predicate-list> .
    <predicate-list> -> <predicate> | <predicate> , <predicate-list>
    <predicate> -> <atom> | <atom> ( <term-list> )
    <term-list> -> <term> | <term> , <term-list>
    <term> -> <atom> | <variable> | <structure> | <numeral>
    <structure> -> <atom> ( <term-list> )
    <atom> -> <small-atom> | ' <string> '
    <small-atom> -> <lowercase-char> | <lowercase-char> <character-list>
    <variable> -> <uppercase-char> | <uppercase-char> <character-list>
    <character-list> -> <alphanumeric> | <alphanumeric> <character-list>
    <alphanumeric> -> <lowercase-char> | <uppercase-char> | <digit>
    <lowercase-char> -> a | b | c | ... | x | y | z
    <uppercase-char> -> A | B | C | ... | X | Y | Z | _
    <numeral> -> <digit> | <digit> <numeral>
    <digit> -> 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9
    <string> -> <character> | <character> <string>
    <character> -> <alphanumeric> | <special>
    <special> -> + | - | * | / | \ | ^ | ~ | : | . | ? | | # | $ | & 

Note that, for instance, this simplified grammar does not include arithmetic, lists, I/O, special operators, etc. Yet it contains all the core features needed for logic programming – in only half a page!

 
