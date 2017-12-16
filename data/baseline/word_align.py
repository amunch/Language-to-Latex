import numpy as np

TR = '../data/final_data/train.tr'
EQ = '../data/final_data/train.eq'

def read_file():
    split_lines = []

    tr = []
    for line in open(TR):
        tr.append(line.strip())
    
    eq = []
    for line in open(EQ):
        eq.append(line.strip()) 

    for i, c in enumerate(tr):
        split_lines.append(tuple([tr[i], eq[i]]))
    
    return split_lines

def initialize_params(lines):
    tr_vocab = []

    t = {}
    c = {}

    for line in lines:
        for tr_word in line[0].split():
            if tr_word not in tr_vocab:
                tr_vocab.append(tr_word)

            for eq_word in (line[1].split()):
                t[(tr_word, eq_word)] = 0
                c[(tr_word, eq_word)] = 0

    for el in t:
        t[el] = 1/float(len(tr_vocab))

    return(t, c, tr_vocab)

def train():
    lines = read_file()

    (t, c, target_vocab) = initialize_params(lines)

    MAX_TRAINING_STEPS = 10

    for step in range(MAX_TRAINING_STEPS):
        # E STEP
        for line in lines:
            for tr_word in line[0].split():
                eq_sentence = line[1].split()
                for eq_word in eq_sentence:
                    sum_t = sum([t[(tr_word, i)] for i in eq_sentence])
                    c[(tr_word, eq_word)] += float(t[(tr_word, eq_word)]) / sum_t
        # M STEP
        sums = {}
    
        for pair in t:
            if pair[1] in sums:
                summ = sums[pair[1]]
            else:
                summ = sum([c.get((i,pair[1]),0) for i in target_vocab])
                sums[pair[1]] = summ
            t[pair] = float(c[(pair)]) / summ

        for i in c:
            c[i] = 0

        # Log-likelihood
        log_likelihood = 0.0
        for line in lines:
            prod = []
            eq_sentence = line[1].split()
            for tr_word in line[0].split():
                prod.append((1/(len(eq_sentence)))*sum([t[(tr_word, i)] for i in eq_sentence]))
            p = (1/100.0)*np.prod(prod)
            log_likelihood += np.log(p)

        print('Log Likelihood: {}'.format(log_likelihood))

        #for key, value in sorted(t.iteritems(), key=lambda (k,v): (v,k)):
            #print(key, value)

    write_probs(t)

    return t, lines

def test():
    t, lines = train()
    to_write = []

    for line in lines:
        eq_sentence = line[1].split()
        write_line = []
        for index, tr_word in enumerate(line[0].split()):
            ts = [t[(tr_word, i)] for i in eq_sentence]
            ind = np.argmax(ts)
            inds = [i for i, val in enumerate(ts) if val==ts[ind]]
            for i in inds:
                if i != 0:
                    write_line.append('{}-{}'.format(index, i-1))
        to_write.append(write_line)                     

    outfile = open('train.model-align', 'w')
    for line in to_write:
        outfile.write(" ".join(line) + '\n')

def write_probs(t):
    outfile = open('train.probs', 'w')
    
    for translation in t:
        outfile.write('{} {} {}\n'.format(translation[0], translation[1], t[translation]))

test()
