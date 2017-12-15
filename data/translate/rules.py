from translate import spacer

def int_t(s):
    if len(s) > 4 and s[4] == '_':
        arg = s[5:]
    else:
        return 'integral'

    (first_arg, next_i) = parse_paren(arg)
    second_arg = ''
    if next_i+1 < len(arg):
        (second_arg, next_i) = parse_paren(arg[next_i+1:])

    if second_arg == '':
        return 'the integral over {} of'.format(first_arg)
    else:
        return 'the integral from {} to {} of'.format(first_arg, second_arg)

def frac_t(s):
    if len(s) > 5 and '{' in s:
        arg = s[5:]
    else:
        return 'fraction'
    try:
        (first_arg, next_i) = parse_paren(arg)
    except:
        return ''
    (second_arg, next_i) = parse_paren(arg[next_i:])
    
    return '{} over {}'.format(first_arg, second_arg)

def sqrt_t(s):
    if len(s) > 5 and '{' in s:
        arg = s[5:]
    else:
        return 'square root'

    (first_arg, next_i) = parse_paren(arg)
    return 'the square root of {}'.format(first_arg)

def lim_t(s):
    if len(s) > 4 and '{' in s:
        arg = s[5:]
    else:
        return 'limit'

    (first_arg, next_i) = parse_paren(arg)

    return 'the limit from {} of'.format(first_arg)

def oint_t(s):
    if len(s) > 5:
        arg = s[6:]
    else:
        return 'line integral'

    (first_arg, next_i) = parse_paren(arg)
    return 'the line integral over {} of'.format(first_arg)

def iint_t(s):
    if len(s) > 5:
        arg = s[6:]
    else:
        return 'double integral'

    (first_arg, next_i) = parse_paren(arg)
    return 'the double integral over {} of'.format(first_arg)

transfer_dict = {
    '\\int': int_t,
    '\\frac': frac_t,
    '\\sqrt': sqrt_t,
    '\\lim': lim_t,
    '\\oint': oint_t,
    '\\iint': iint_t,
}

def parse_paren(s):
    if s[0] != '{':
        i = 1
        for i, c in enumerate(s[1:]):
            if not c.isalpha():
                return (s[0:i+1], i+1)
        return (translate_string(spacer(s)), i)

    open_paren = False
    for i, c in enumerate(s[1:]):
        if c == '{':
            open_paren = True
        elif c == '}' and open_paren == True:
            open_paren = False
        elif c == '}' and open_paren == False:
            return (translate_string(spacer(s[1:i+1])), i+2)
            

def special_split(s):
    to_return = ['']
    index = 0

    in_bracket = 0
    for char in s:
        if char == ' ' and in_bracket != 0:
            to_return[index] += char
        elif char == ' ':
            index+=1
            to_return.append('')
        else:
            to_return[index] += char

        if char == '{':
            in_bracket += 1
        elif char == '}':
            in_bracket -= 1

    return to_return
            

def translate_string(s):
    word_list = special_split(s)

    # Translate known symbols as listed in symbol_dict.csv
    for index, word in enumerate(word_list):
        if word in symbol_dict:
            word_list[index] = symbol_dict[word]
 
    translated = ''   
    for index, word in enumerate(word_list):
        arg = argument(word)
        if arg in transfer_dict:
            translated += transfer_dict[arg](word)
        else:
            translated += word
        translated += ' '

    return translated


def argument(s):
    pos = 1
    while pos < len(s) and s[pos].isalpha():
        pos += 1
    
    return s[:pos]


symbol_dict = {}

for line in open('symbol_dict.csv'):
    key_val = line.strip().split(',')

    symbol_dict[key_val[0]] = key_val[1]
