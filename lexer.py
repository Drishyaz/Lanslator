import re

def lexer(contents):

    #DEFINE LISTS OF TOKENS IN PYTHON
    KEYWORD = ['False', 'None', 'True', '__peg_parser__', 'and', 'as', 'assert', 'async', 'await', 'break', 'class', 'continue', 'def', 'del', 'elif', 'else', 'except', 'finally', 'for', 'from', 'global', 'if', 'import', 'in', 'is', 'lambda', 'nonlocal', 'not', 'or', 'pass', 'raise', 'return', 'try', 'while', 'with', 'yield']

    COMMENT = r'^#(.*)'
    IDENTIFIER = r'^[\w_]+'
    #DECIMAL = r'[.0-9]+'
    NUMBER = r'[+-]?([0-9]*[.])?[0-9]+'
    #functions = r''
    OPERATOR = ['+','-','*','/','//','**','%','=','==','!=','<','>','<=','>=','&','|','~','^','>>','<<','+=','-=','*=','/=','//=','**=','%=','&=','|=','^=','>>=','<<=','and','or','not','is','is not','in','not in']
    SEPARATOR = ['(',')','{','}','[',']',',','.',':','"',"'"]
    DATA_TYPE = ['int','str','float','bool','list','tuple','set','dict']
    INBUILT_FUNC = ['input','print','len','append','int','str','float','bool','list','tuple','set','dict','type','range','pop','remove','index','count','find','upper','lower','map','split','strip']

    # SPLIT ALL CONTENTS BASED ON DELIMITER NEW LINE SO IT WILL BE A LIST OF LINES
    lines = contents.split('\n')
    for line in lines:

        # IF A LINE IS A COMMENT JUST SKIP THAT LINE
        if re.match(COMMENT,line):
            continue
        # CONVERT EACH LINE INTO A LIST OF CHARACTERS
        chars = list(line)
        tokens = []
        temp_str = ""
        quote_count,brac_count = 0,0
        for char in chars:
            # CHECK IF IT IS A STRING CHARACTER OR NOT
            if char == '"' or char == "'":
                quote_count += 1
                # CHECK IF STRING CLOSED
            if quote_count % 2 == 0:
                in_quotes = False
            else:
                in_quotes = True

            # IF STRING CLOSED AND SPACE ENCOUNTERED THEN ADD STRING TO TOKENS
            if char == " " and in_quotes == False:
                tokens.append(temp_str)
                temp_str = ""
            else:
            # OTHERWISE KEEP ADDING THE STRING CHARACTERS TO TEMP_STR
                temp_str += char
        #tokens = [x for x in tokens if x]
    
        if temp_str != "":
            tokens.append(temp_str)
        # PRINT THE LIST OF TOKENS
        #print(tokens)

        # ITEMS STORES THE TYPE OF EACH TOKEN FOR E.G, KEYWORD, NUMBER, ETC
        items = []
        for token in tokens:
            # CHECK IF THE TOKEN IS A STRING
            if token[0] == '"' or token[0] == "'":
                if token[-1] == '"' or token[-1] == "'":
                    items.append(("string", token))
                else:
                    # Throw Error
                    break

            # CHECK IF THE TOKEN IS A NUMBER
            elif re.match(NUMBER,token):
                items.append(("number",token))
            # CHECK IF THE TOKEN IS AN INBUILT FUNCTION
            elif token in INBUILT_FUNC:
                items.append(("inbuilt_func",token))
            # CHECK IF THE TOKEN IS AN IDENTIFIER
            elif re.match(IDENTIFIER, token):
                items.append(("identifier", token))
            # CHECK IF THE TOKEN IS AN OPERATOR
            elif token in OPERATOR:
                items.append(("operator", token))
            # CHECK IF THE TOKEN IS A KEYWORD
            elif token in KEYWORD:
                items.append(("keyword", token))
            # CHECK IF THE TOKEN IS A SEPARATOR
            elif token in SEPARATOR:
                items.append(("separator",token))
            # CHECK IF THE TOKEN IS A DATA TYPE
            elif token in DATA_TYPE:
                items.append(("data type",token))
            
            
        # PRINT THE TYPE OF EACH TOKEN
        print(items)

'''def remove_comments(lines):
    txt = ""
    comment = r'^#(.*)'
    txt = re.sub(comment, "", lines)
    return txt'''

def parse(code):
    '''with open("demo.py","r") as file:
        contents = file.read()
        #contents = remove_comments(contents)'''
    
    contents = code
    # REPLACES THE () WITH SPACE FOR EASE IN SCANNING TOKENS
    contents = contents.replace("(", " ").replace(")", " ")

    # SEND THE CONTENTS TO LEXER() TO EXTRACT TOKENS
    tokens = lexer(contents)
    
    print(tokens)

# THIS FUNCTION WILL PARSE / SCAN THE CODE THEN EXTRACT THE TOKENS THEN CLASSIFIES THEM
if __name__ == '__main__':
    with open("demo.py","r") as f:
        tokens = f.read()
    parse(tokens)
