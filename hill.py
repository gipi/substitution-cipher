import sys
import itertools
import numpy as np
import string

# return a list with tha abc...z translated to 0 1 2...25
encode = lambda y:[ord(x)-97 for x in y]
decode = lambda y:"".join([chr(x + 97) for x in y])

# from <http://stackoverflow.com/questions/4287721/easiest-way-to-perform-modular-matrix-inversion-with-python>
def generalizedEuclidianAlgorithm(a, b):
    if b > a:
        #print a, b
        return generalizedEuclidianAlgorithm(b,a);
    elif b == 0:
        return (1, 0);
    else:
        #print a,b
        (x, y) = generalizedEuclidianAlgorithm(b, a % b);
        return (y, x - (a / b) * y)

def inversemodp(a, p):
    a = a % p
    if (a == 0):
        print "a is 0 mod p"
        return 0
    (x,y) = generalizedEuclidianAlgorithm(p, a % p);
    return y % p

def identitymatrix(n):
    return [[long(x == y) for x in range(0, n)] for y in range(0, n)]

def inversematrix(matrix, q):
    n = len(matrix)
    A = np.matrix([[ matrix[j, i] for i in range(0,n)] for j in range(0, n)], dtype = long)
    Ainv = np.matrix(identitymatrix(n), dtype = long)
    for i in range(0, n):
        factor = inversemodp(A[i,i], q)
        A[i] = A[i] * factor % q
        Ainv[i] = Ainv[i] * factor % q
        for j in range(0, n):
            if (i != j):
                factor = A[j, i]
                A[j] = (A[j] - factor * A[i]) % q
                Ainv[j] = (Ainv[j] - factor * Ainv[i]) % q
                # print A, Ainv
                # print i, j, factor
    return Ainv

def makeKey(key, n):
    """Generate a matrix nxn with the given key"""
    assert len(key) == n*n

    k = np.array(key)
    k.shape = (n, n)

    return np.mat(k)

# http://stackoverflow.com/questions/312443/how-do-you-split-a-list-into-evenly-sized-chunks-in-python
def chunks(l, n):
    """ Yield successive n-sized chunks from l.
    """
    for i in range(0, len(l), n):
        yield l[i:i+n]

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print >> sys.stderr, "usage: %s <plaintext> <key> <size>" % sys.argv[0]
        sys.exit(0)


    cleartext = sys.argv[1]

    if len(filter(lambda x:x not in string.lowercase, cleartext)) > 0:
        print >> sys.stderr, "only a-z are permitted"
        sys.exit(1)

    cleartext = encode(cleartext)
    key_size = int(sys.argv[3])
    key = makeKey(encode(sys.argv[2]), key_size)
    ciphertext = []
    for piece in chunks(cleartext, key_size):
        a = np.mat(piece)
        ciphertext.append(np.array(np.dot(a, key))[0])

    print decode(list(itertools.chain.from_iterable([x % 26 for x in ciphertext])))
