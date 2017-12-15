eq_ok = ['(', ')', '^', '_', '{', '}', ',', '-', '+', '/', '|', '\\int', '\\frac', '\\sqrt', \
         '\\lim', '\\oint', '\\iint']
tr_ok = ['integral', 'the', 'over', 'from', 'to', 'of', 'fraction', 'square', 'root', \
         'limit', 'line', 'double']

for line in open('../../translate/symbol_dict.csv'):
    l = line.strip().split(',')
    eq_ok.append(l[0])
    for word in l[1].split(' '):
        tr_ok.append(word)

eq_out = []
for line in open('../untokenized/train.eq-spaced'):
    eq = []
    for word in line.strip().split(' '):
        if word in eq_ok:
            eq.append(word)
        else:
            eq.append('<unk>')

    eq_out.append(' '.join(eq))

out_file = open('../tokenized/train.eq', 'w')
for line in eq_out:
    out_file.write(line + '\n')

tr_out = []
for line in open('../untokenized/train.tr'):
    tr = []
    for word in line.strip().split(' '):
        if word in tr_ok:
            tr.append(word)
        else:
            tr.append('<unk>')

    tr_out.append(' '.join(tr))

out_file = open('../tokenized/train.tr', 'w')
for line in tr_out:
    out_file.write(line + '\n')


