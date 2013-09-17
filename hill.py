import sys
import itertools
import numpy as np
import string

# return a list with tha abc...z translated to 0 1 2...25
encode = lambda y:[ord(x)-97 for x in y]
decode = lambda y:"".join([chr(x + 97) for x in y])

def matmult(a, b):
    zip_b = b.T.tolist()
    zip_a = a.tolist()
    return [[sum((ele_a*ele_b) % 26 for ele_a, ele_b in zip(row_a, col_b)) % 26 for col_b in zip_b] for row_a in zip_a]
# from <http://stackoverflow.com/questions/4287721/easiest-way-to-perform-modular-matrix-inversion-with-python>
# http://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
def egcd(a, b):
    """
    Return a triple (g, x, y), such that ax + by = g = gcd(a, b).

    >>> egcd(3, 2)
    (1, 1, -1)
    >>> egcd(5, 10)
    (5, 1, 0)
    >>> egcd(1, 0)
    (1, 1, 0)
    """
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)

def modinv(a, m):
    """
    >>> modinv(3, 5)
    2
    """
    g, x, y = egcd(a, m)
    if g != 1:
        raise AttributeError("%d mod %d has not inverse" % (a, m))  # modular inverse does not exist
    else:
        return x % m

def inversemodp(a, p):
    a = a % p
    if (a == 0):
        print "a is 0 mod p"
        return 0
    (x, y) = generalizedEuclidianAlgorithm(p, a % p);
    return y % p

def identitymatrix(n):
    return [[long(x == y) for x in range(0, n)] for y in range(0, n)]

def inversematrix(matrix, q):
    """
    >>> k = np.array([2, 1, 3, 4])
    >>> k.shape = (2, 2)
    >>> inversematrix(np.mat(k), 26)
    """
    n = len(matrix)
    A = np.matrix(matrix)
    Ainv = np.matrix(identitymatrix(n), dtype = long)
    for i in range(0, n):
        factor = modinv(A[i,i], q)
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

    print 'key:', key

    reversekey = np.array(inversematrix(key, 26))

    print 'inverse', decode(itertools.chain.from_iterable([reversekey[0], reversekey[1]]))

    ciphertext = []
    for piece in chunks(cleartext, key_size):
        a = np.mat(piece)
        ciphertext.append(np.array(matmult(a, key))[0])

    print decode(list(itertools.chain.from_iterable([x % 26 for x in ciphertext])))
