import rules
import re

def spacer(s):
    char_list = []
    inside_brackets = False
    command_start = False
    for i, c in enumerate(s):
        if not c.isalpha() and command_start and c not in ['{', '^', '}', '_']:
            char_list.append(' ')
            command_start = False
        if command_start and c in ['{', '^', '}', '_']:
            command_start = False

        if c in ['/', '='] and s[i-1] != ' ':
            char_list.append(' ')

        if c == '\\':
            command_start = True
            if s[i-1] in ['_', '^']: 
                char_list.append(c)
            else:
                char_list.append(' ' + c)
        else:
            char_list.append(c)

        if c in ['/', '='] and s[i+1] != ' ':
            char_list.append(' ')

        if c == '{':
            inside_brackets = True
        elif c == '}':
            inside_brackets = False
            if i+1 < len(s) and s[i+1] not in ['{', '^', '}']:
                char_list.append(' ')


    candidate = ''.join(char_list)
    return remove_extra_spaces(candidate)

def remove_extra_spaces(s):
    char_list = []
    first = True
    spaces = False
    for c in s:
        if first and c == ' ':
            continue
        first = False

        if spaces and c == ' ':
            continue
        spaces = False

        char_list.append(c)
        if c == ' ':
            spaces=True

    return ''.join(char_list)

if __name__ == '__main__':
    DATA_PATH = '../raw/train.eq'

    translated = []
    source = []

    for line in open(DATA_PATH):
        if '' in line:
            print(line.strip())
            stripped = spacer(line.strip())
            print(stripped)
            try:
                translation = rules.translate_string(stripped)
                if '\\' in translation:
                    continue
                else:
                    source.append(stripped)
                    translated.append(re.sub(' +',' ',translation))
            except:
                print('ERROR: {}'.format(line.strip()))
    
    source_f = open('../data/untokenized/train.eq', 'w')
    for line in source:
        source_f.write(line+'\n')

    translated_f = open('../data/untokenized/train.tr', 'w')
    for line in translated:
        translated_f.write(line+'\n')
