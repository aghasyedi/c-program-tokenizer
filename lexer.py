import re

class Token:
    def __init__(self, type, content="", rep="", r=None):
        self.type, self.content, self.rep, self.r = type, content or str(type), rep, r

    def __repr__(self):
        return self.content

    def __str__(self):
        return self.rep or self.content

class Location:
    def __init__(self, file, line, col, full_line):
        self.file = file
        self.line = line
        self.col = col
        self.full_line = full_line

    def __add__(self, other):
        return Location(self.file, self.line, self.col + 1, self.full_line)

class Range:
    def __init__(self, start, end=None):
        self.start = start
        self.end = end or start

    def __add__(self, other):
        return Range(self.start, other.end)

class Tag:

    def __init__(self, c, p):
        self.c = c
        self.p = p
        self.r = Range(p, p)

keywords = ["auto", "break", "case", "char", "const", "continue", "default","do",
            "double", "else", "enum", "extern", "float", "for", "goto", "if",
            "int", "long", "register", "return", "short", "signed","sizeof", "static",
            "struct", "switch", "typedef", "union", "unsigned", "void", "volatile", "while"]

#   All symbols, seperate in other part of the program
symbols = ['+', '-', '*', '**', '/', '//', '%', '<<', '>>', '&', '|', '^', 
           '~', '<', '>', '<=', '>=', '==', '!=', '<>', '+=', '-=', '*=', 
           '/=', '//=', '%=', '**=', '&=', '|=', '^=', '>>=', '<<=', '(', 
           ')', '[', ']', '{', '}', ',', ':', '=', ';','#','"',"'"]


star, slash, pound, dquote,squote = '*', '/','#','"',"'"

identifier = number = string = char_string = include_file = None

def tokenizer(code, filename):
    tokens = []
    tokens_type = []
    lines = to_tag_lines(code, filename)
    comment = False

    for line in lines:
        line_tokens, comment, token_type = token_gen(line, comment)
        tokens += line_tokens
        tokens_type+=token_type
    tokens,tokens_type = tokens[:-1], tokens_type[:-1] #remove extra line at the bottom (iteration problem)
    tokens.append("Created By")
    tokens_type.append("Agha")
    i = 0
    while i < len(tokens) - 1:
        if tokens[i] == '--blank--' and tokens[i+1] == '--blank--':
            tokens.pop(i)
            tokens_type.pop(-(len(tokens))+i)
            i -= 1  # Adjust index to recheck after deletion
        i += 1
        
    return tokens,tokens_type[-len(tokens):]

def to_tag_lines(text, filename):
    lines = text.splitlines()
    tagged_lines = []
    for line_num, line in enumerate(lines):
        tagged_line = []
        for col, char in enumerate(line):
            p = Location(filename, line_num + 1, col + 1, line)
            tagged_line.append(Tag(char, p))
        tagged_lines.append(tagged_line)

    # for i in range(len(tagged_lines)):
    #     for j in range(len(tagged_lines[i])):
    #         print(tagged_lines[i][j].c)

    return tagged_lines

token_type = []

def token_gen(line, comment):
    tokens = []
    top = 0
    bottom = 0

    while bottom < len(line):
        symbol_type = match_symbol_type_at(line, bottom)
        next_symbol_type = match_symbol_type_at(line, bottom + 1)
        #for comments
        if comment: 
            if (symbol_type == star and
                    next_symbol_type == slash):
                comment = False
                top = bottom + 2
                bottom = top
            
            else:
                top = bottom + 1
                bottom = top

        elif (symbol_type == slash and
                next_symbol_type == star):
            comment = True

        
        elif (symbol_type == slash and
                next_symbol_type == slash):
            break

        
        elif line[bottom].c.isspace():
            add_buffer(line[top:bottom], tokens)
            top = bottom + 1
            bottom = top
            
        elif (len(tokens) == 2 and
            tokens[-2].type == pound and
            tokens[-1].type == identifier and
            tokens[-1].content == "include"):

            filename, end = read_include_filename(line, bottom)
            tokens.append(Token(include_file, filename,
                                r=Range(line[bottom].p, line[end].p)))
            
            token_type.append("Pre-Processer")
            top = end + 1
            bottom = top
        
        elif symbol_type in {dquote, squote}:
            if symbol_type == dquote:
                quote_str = '"'
                type = string
                add_null = True
            else:
                quote_str = "'"
                type = char_string
                add_null = False

            chars, end = read_string(line, bottom + 1, quote_str, add_null)
            rep = buffer_to_str(line[bottom:end + 1])
            r = Range(line[bottom].p, line[end].p)

            tokens.append(Token(type, chars, rep, r=r))
            token_type.append("Constant")
            top = end + 1
            bottom = top
        
        elif symbol_type:
            symbol_start_index = bottom
            symbol_end_index = bottom + len(symbol_type) - 1

            r = Range(line[symbol_start_index].p, line[symbol_end_index].p)
            symbol_token = Token(symbol_type, r=r)

            add_buffer(line[top:bottom], tokens)
            tokens.append(symbol_token)
            token_type.append("Symbols")
            top = bottom + len(symbol_type)
            bottom = top
        
        else:
            bottom += 1

    if top == bottom:
        if bottom == len(line):
            add_buffer(line[top:bottom], tokens)
            tokens.append("--blank--")
            token_type.append("Line Break")
    add_buffer(line[top:bottom], tokens)
    return tokens, comment, token_type

def buffer_to_str(buffer):
    return "".join(c.c for c in buffer)

def match_symbol_type_at(content, start):
    for symbol_type in symbols:
        try:
            for i, c in enumerate(symbol_type):
                if content[start + i].c != c:
                    break
            else:
                return symbol_type
        except IndexError:
            pass
    return None

def match_include_command(tokens):
    return (len(tokens) == 2 and
            tokens[-2].type == pound and
            tokens[-1].type == identifier and
            tokens[-1].content == "include")

def read_string(line, start, delim, null):
    i = start
    chars = []
    escapes = {"'": 39,'"': 34,"?": 63,"\\": 92,"a": 7,
               "b": 8,"f": 12,"n": 10,"r": 13,"t": 9,"v": 11}
    octdigits = "01234567"
    hexdigits = "0123456789abcdefABCDEF"

    while True:
        if line[i].c == delim:
            if null: chars.append(0)
            return chars, i
        elif (i + 1 < len(line)
              and line[i].c == "\\"
              and line[i + 1].c in escapes):
            chars.append(escapes[line[i + 1].c])
            i += 2
        elif (i + 1 < len(line)
              and line[i].c == "\\"
              and line[i + 1].c in octdigits):
            octal = line[i + 1].c
            i += 2
            while (i < len(line)
                   and len(octal) < 3
                   and line[i].c in octdigits):
                octal += line[i].c
                i += 1
            chars.append(int(octal, 8))
        elif (i + 2 < len(line)
              and line[i].c == "\\"
              and line[i + 1].c == "x"
              and line[i + 2].c in hexdigits):
            hexa = line[i + 2].c
            i += 3
            while i < len(line) and line[i].c in hexdigits:
                hexa += line[i].c
                i += 1
            chars.append(int(hexa, 16))
        else:
            chars.append(ord(line[i].c))
            i += 1

def read_include_filename(line, start):
    if start < len(line) and line[start].c == '"':
        end = '"'
    elif start < len(line) and line[start].c == "<":
        end = ">"

    i = start + 1
    while line[i].c != end:
        i += 1

    return buffer_to_str(line[start:i + 1]), i

def add_buffer(buffer, tokens):
    if buffer:
        range = Range(buffer[0].p, buffer[-1].p)

        keyword_type = match_keyword_type(buffer)
        if keyword_type:
            tokens.append(Token(keyword_type, r=range))
            token_type.append("Keyword")
            return

        number_string = match_number_string(buffer)
        if number_string:
            tokens.append(Token(number, number_string, r=range))
            token_type.append("Constant")
            return

        identifier_name = match_identifier_name(buffer)
        if identifier_name:
            tokens.append(Token(
                identifier, identifier_name, r=range))
            token_type.append("Identifier")
            return

def match_keyword_type(token_repr):
    token_str = buffer_to_str(token_repr)
    for keyword_type in keywords:
        if keyword_type == token_str:
            return keyword_type
    return None

def match_number_string(token_repr):
    token_str = buffer_to_str(token_repr)
    return token_str if token_str.isdigit() else None

def match_identifier_name(token_repr):
    token_str = buffer_to_str(token_repr)
    if re.match(r"[_a-zA-Z][_a-zA-Z0-9]*$", token_str):
        return token_str
    else:
        return None