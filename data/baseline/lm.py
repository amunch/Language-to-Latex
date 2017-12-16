import collections
import fst

class Uniform(object):
    """Uniform distribution."""
    def __init__(self, data):
        vocab = {"<unk>", "</s>"}
        for words in data:
            vocab.update(words)
        self.vocab = vocab
    def prob(self, u, w):
        return 1/len(self.vocab)

class KneserNey(object):
    def __init__(self, data, n, bom=None):
        self.bom = bom
        
        # Collect n-gram counts
        cuw = collections.defaultdict(collections.Counter)
        cu = collections.Counter()
        for line in data:
            u = ("<s>",)*(n-1)
            for w in line + ["</s>"]:
                cuw[u][w] += 1
                cu[u] += 1
                u = (u+(w,))[1:]

        # Compute discount
        cc = collections.Counter()
        for u in cuw:
            for w in cuw[u]:
                cc[cuw[u][w]] += 1
        d = cc[1] / (cc[1] + 2*cc[2])

        # Compute probabilities and backoff weights
        self._prob = collections.defaultdict(dict)
        self._bow = {}
        for u in cuw:
            for w in cuw[u]:
                self._prob[u][w] = (cuw[u][w]-d) / cu[u]
            self._bow[u] = len(cuw[u])*d / cu[u]

    def prob(self, u, w):
        if u in self._prob:
            return self._prob[u].get(w, 0) + self._bow[u] * self.bom.prob(u[1:], w)
        else:
            return self.bom.prob(u[1:], w)

def make_kneserney(data, n):
    """Create a Kneser-Ney smoothed language model of order `n`, 
    trained on `data`, as a `FST`.

    Note that the returned FST has epsilon transitions. To iterate
    over states in topological order, sort them using `lambda q:
    -len(q)` as the key.
    """

    # Estimate KN-smoothed models for orders 1, ..., n
    kn = {}
    for i in range(1, n+1):
        kn[i] = KneserNey(data, i)

    # Create the FST. It has a state for every possible k-gram for k = 0, ..., n-1.
    m = fst.FST()
    m.set_start(("<s>",) * (n-1))
    m.set_accept(("</s>",))
    
    for i in range(1, n+1):
        for u in kn[i]._prob:
            if i > 1:
                # Add an epsilon transition that backs off from the i-gram model to the (i-1)-gram model
                m.add_transition(fst.Transition(u, (fst.EPSILON, fst.EPSILON), u[1:]), kn[i]._bow[u])
            else:
                # Smooth 1-gram model with uniform distribution
                types = len(kn[i]._prob[u])+1
                for w in kn[i]._prob[u]:
                    m.add_transition(fst.Transition(u, (w, w), (w,)), 1/types)
                m.add_transition(fst.Transition(u, ("<unk>", "<unk>"), ()), 1/types)

            # Create transitions for word probabilities
            for w in kn[i]._prob[u]:
                # If we are in state u and read w, then v is the new state.
                # This should be the longest suffix of uw that is observed
                # in the training data.
                if w == "</s>":
                    v = ("</s>",)
                else:
                    v = u+(w,)
                    while len(v) > 0 and (len(v) >= n or v not in kn[len(v)+1]._prob):
                        v = v[1:]
                m.add_transition(fst.Transition(u, (w, w), v), kn[i]._prob[u][w])
    return m

if __name__ == "__main__":
    # This demonstrates how to create a Kneser-Ney smoothed language
    # model by directly using the KneserNey class, without using FSTs.

    n = 3
    
    import fileinput
    data = []
    for line in fileinput.input():
        words = line.split()
        data.append(words)

    lm = Uniform(data)
    for i in range(1, n+1):
        lm = KneserNey(data, i, lm)

