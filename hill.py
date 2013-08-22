import sys
import itertools

# return a list with tha abc...z translated to 012...25
encode = lambda y:[ord(x)-97 for x in y]
decode = lambda y:"".join([chr(x + 97) for x in y])
def matmult(a,b):# TODO: mod 26
    zip_b = zip(*b)
    return [[sum(ele_a*ele_b for ele_a, ele_b in zip(row_a, col_b)) for col_b in zip_b] for row_a in a]

IDENTITY = [
    [0, 1],
    [1, 0]
]

def makeKey(key, n):
    """Generate a matrix nxn with the given key"""
    assert len(key) == n*n

    matrix = []
    for row in chunks(key, n):
        matrix.append(row)

    return matrix

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

    cleartext = encode(sys.argv[1])
    key_size = int(sys.argv[3])
    key = makeKey(encode(sys.argv[2]), key_size)
    ciphertext = []
    for piece in chunks(cleartext, key_size):
        ciphertext.append(matmult([piece,], key)[0])

    print decode(list(itertools.chain.from_iterable(ciphertext)))
