import lm
import fst

import math

NUM_GRAMS = 2
NUM_TOP_TRANSLATIONS = 100

def make_knes():
    eq_in = '../data/tokenized/train.eq'

    data = []

    for line in open(eq_in):
        words = line.strip().split()
        data.append(words)

    return lm.make_kneserney(data, NUM_GRAMS)

def read_translations():
    t_file = 'train.probs'
    
    translations = {}
    for t in open(t_file):
        tran = t.strip().split()
        if tran[1] == 'NULL':
            tran[1] = 'ε'
        if tran[0] in translations:
            if len(translations[tran[0]]) >= NUM_TOP_TRANSLATIONS:
                continue
            else:
                translations[tran[0]].append((tran[1], tran[2]))
        else:
            translations[tran[0]] = [(tran[1], tran[2])]

    return translations

def make_TM():
    # Code adapted from Homework 2 Solution
    translations = read_translations()
    
    tm = fst.FST()
    tm.set_start(0)
    tm.set_accept(1)
    
    tm.add_transition(fst.Transition(0, ("</s>", "</s>"), 1), wt=1)

    for t in translations:
        for prob in translations[t]:
            tm.add_transition(fst.Transition(0, (t, prob[0]), 0), wt=float(prob[1]))

    test = '../data/tokenized/train.tr'
    test_set = set()
    for test_line in open(test):
        for char in test_line.strip().split():
            test_set.add(char)

    for char in test_set:
        tm.add_transition(fst.Transition(0, (char, 'ε'), 0), wt=float('1.0e-100'))

    return tm

def make_f(f):
    # Adapted from Homework 2 Solutions
    f = f.split()
    m = fst.FST()
    m.set_start(0)
    for (i,a) in enumerate(f):
        m.add_transition(fst.Transition(i, (a, a), i+1))
    m.add_transition(fst.Transition(len(f), (fst.STOP, fst.STOP), len(f)+1))
    m.set_accept(len(f)+1)
    return m

def viterbi(composed):
    # Adapted from Homework 02 Solution
    
    vit = {}
    ptr = {}

    vit[composed.start] = 0
    ptr[composed.start] = 0

    for q in sorted(sorted(composed.states, key=lambda x: len(x[1]), reverse=True), key=lambda x: x[0][0]):
        if q == composed.start:
            continue
        vit[q] = float("-inf")
        for t, wt in composed.transitions_to[q].items():
            score = vit[t.q] + (math.log(wt) if wt > 0 else float("-inf"))
            if score > vit[q]:
                vit[q] = score
                ptr[q] = t

    path = []
    q = composed.accept
    while q != composed.start:
        if q not in ptr:
            raise ValueError("no path found")
        path.append(ptr[q])
        q = ptr[q].q
    
    path.reverse()

    reconstructed = []
    prev = ''
    for i in path:
        if len(i.q[1]) > 0:
            if i.q[1][0] != '<s>' and i.q[1][0] != prev:
                reconstructed.append(i.q[1][0])
                prev = i.q[1][0]            

    return ' '.join(reconstructed)


if __name__ == "__main__":
    M_LM = make_knes()
    M_TM = make_TM()

    test_file = '../data/tokenized/train.tr'

    to_write = []

    for i, line in enumerate(open(test_file)):

        line = line.strip()
        M_f = make_f(line)

        composed = fst.compose(fst.compose(M_f, M_TM), M_LM)

        out = viterbi(composed)
        print(i, out)
    
        to_write.append(out)


    write_file = open('test.translations', 'w')
    for line in to_write:
        write_file.write(line + '\n')
        
