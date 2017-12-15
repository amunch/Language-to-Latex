import re

in_file = open('../untokenized/train.eq')

spaced = []

for line in in_file:
    in_command = False
    out = []
    for i, c in enumerate(line.strip()):
        if c in ['{', '_', '^', '}']:
            if line[i-1] != ' ':
                out.append(' ')

        if c == '\\':
            in_command = True
        elif not c.isalpha() and in_command == True:
            in_command = False
            if c is not ' ':
                out.append(' ')


        out.append(c)

        if c in ['{', '_', '^', '}']:
            if line[i+1] != ' ':
                out.append(' ')

    spaced.append(re.sub(' +',' ',''.join(out)))

out_file = open('../untokenized/train.eq-spaced', 'w')
for line in spaced:
    out_file.write(line + '\n')
