eq = ['(', ')', '^', '_', '{', '}', ',', '-', '+', '/', '|', '\\int', '\\frac', '\\sqrt', \
        '\\lim', '\\oint', '\\iint', 'unk']
tr = ['integral', 'the', 'over', 'from', 'to', 'of', 'fraction', 'square', 'root', \
        'limit', 'line', 'double', 'unk']

for line in open('../../translate/symbol_dict.csv'):
    l = line.strip().split(',')
    eq.append(l[0])
    for word in l[1].split(' '):
        tr.append(word)

outfile = open('../final_data/vocab.eq', 'w')
for line in eq:
    outfile.write(line + '\n')

outfile = open('../final_data/vocab.tr', 'w')
for line in tr:
    outfile.write(line + '\n')
