translations = []

for line in open('test.translations'):
    translations.append(line.strip().split(' '))

unks = []
for line in open('../data/final_data/test.tr-unk'):
    unks.append(line.strip().split(' '))

print(unks)

recovered = []
for i, line in enumerate(translations):
    unk_index = 0
    recover = []
    for w in line:
        if w == '<unk>':
            if unk_index < len(unks[i]):
                recover.append(unks[i][unk_index])
            else:
                continue
            unk_index += 1
        else:
            recover.append(w)

    recovered.append(' '.join(recover))
    
outfile = open('test.translations-recovered', 'w')
for line in recovered:
    outfile.write(line + '\n')
