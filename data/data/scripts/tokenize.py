import random

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
eq_unk = []
eq_clean = []
for line in open('../untokenized/train.eq-spaced'):
    if line.strip() == '':
        continue
    
    eq = []
    unk = []
    clean = []
    for word in line.strip().split(' '):
        if word in eq_ok:
            eq.append(word)
        else:
            unk.append(word)
            eq.append('unk')
        clean.append(word)

    eq_out.append(' '.join(eq))
    eq_unk.append(' '.join(unk))
    eq_clean.append(' '.join(clean))

tr_out = []
tr_unk = []
tr_clean = []
for line in open('../untokenized/train.tr'):
    if line.strip() == '':
        continue

    tr = []
    unk = []
    clean = []
    for word in line.strip().split(' '):
        if word in tr_ok:
            tr.append(word)
        else:
            tr.append('unk')
            unk.append(word)
        clean.append(word)

    tr_out.append(' '.join(tr))
    tr_unk.append(' '.join(unk))
    tr_clean.append(' '.join(clean))

print(len(tr_out), len(eq_out))

indices = [i for i in range(len(eq_out))]
random.shuffle(indices)

train_indices = indices[0:int(len(eq_out)*.8)]
test_indices  = indices[int(len(eq_out)*.8):int(len(eq_out)*.9)]
dev_indices   = indices[int(len(eq_out)*.9):]

out_file = open('../final_data/train.eq', 'w')
for index in train_indices:
    out_file.write(eq_out[index] + '\n')

out_file = open('../final_data/train.eq-unk', 'w')
for index in train_indices:
    out_file.write(eq_unk[index] + '\n')

out_file = open('../final_data/train.eq-clean', 'w')
for index in train_indices:
    out_file.write(eq_clean[index] + '\n')

out_file = open('../final_data/dev.eq', 'w')
for index in dev_indices:
    out_file.write(eq_out[index] + '\n')

out_file = open('../final_data/dev.eq-unk', 'w')
for index in dev_indices:
    out_file.write(eq_unk[index] + '\n')

out_file = open('../final_data/dev.eq-clean', 'w')
for index in dev_indices:
    out_file.write(eq_clean[index] + '\n')

out_file = open('../final_data/test.eq', 'w')
for index in test_indices:
    out_file.write(eq_out[index] + '\n')

out_file = open('../final_data/test.eq-unk', 'w')
for index in test_indices:
    out_file.write(eq_unk[index] + '\n')

out_file = open('../final_data/test.eq-clean', 'w')
for index in test_indices:
    out_file.write(eq_clean[index] + '\n')

out_file = open('../final_data/train.tr', 'w')
for index in train_indices:
    out_file.write(tr_out[index] + '\n')

out_file = open('../final_data/train.tr-unk', 'w')
for index in train_indices:
    out_file.write(tr_unk[index] + '\n')

out_file = open('../final_data/train.tr-clean', 'w')
for index in train_indices:
    out_file.write(tr_clean[index] + '\n')

out_file = open('../final_data/dev.tr', 'w')
for index in dev_indices:
    out_file.write(tr_out[index] + '\n')

out_file = open('../final_data/dev.tr-unk', 'w')
for index in dev_indices:
    out_file.write(tr_unk[index] + '\n')

out_file = open('../final_data/dev.tr-clean', 'w')
for index in dev_indices:
    out_file.write(tr_clean[index] + '\n')

out_file = open('../final_data/test.tr', 'w')
for index in test_indices:
    out_file.write(eq_out[index] + '\n')

out_file = open('../final_data/test.tr-unk', 'w')
for index in test_indices:
    out_file.write(tr_unk[index] + '\n')

out_file = open('../final_data/test.tr-clean', 'w')
for index in test_indices:
    out_file.write(tr_clean[index] + '\n')
