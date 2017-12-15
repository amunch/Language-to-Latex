import requests

equations = []

PREV_NO_INCLUDE = ['\\', '%', '=']

for i in open('links.txt'):
    response = requests.get(i.strip())
    s = response.text.encode('utf-8')
    curr = []
    compiling = False
    prev = ' '
    for c in s:
        if c == '\r':
            c = ' '

        if c == '$' and prev not in PREV_NO_INCLUDE:
            if len(curr) == 0:
                compiling = True
            else:
                compiling = False
                equations.append(''.join(curr)+'$')
                curr = []
        if compiling:
            if c == '\n':
                c = ' '
            curr.append(c)
        prev = c

f = open('../raw/train.eq', 'w')
for i in equations:
    f.write("%s\n" % i)
