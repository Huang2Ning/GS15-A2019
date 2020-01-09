A = 0x67452301
B = 0xefcdab89
C = 0x98badcfe
D = 0x10325476

# ENDFLAG
ENDFLAG = "1"

L = lambda    x,n: (((x & 0xffffffff) << n) | ((x & 0xffffffff) >> (32 - n))) & (0xffffffff)
R = lambda char,n: (char*n)

F = lambda  x,y,z: ((x & y) | ((~x) & z))
G = lambda  x,y,z: ((x & z) | (y & (~z)))
H = lambda  x,y,z: (x ^ y ^ z)
I = lambda  x,y,z: (y ^ (x | (~z)))


LE32 = lambda s: ("".join(chunk(s, 8)[::-1]))
LE64 = lambda s: ("".join([LE32(i) for i in chunk(s, 32)][::-1]))
LE   = lambda s: ("".join(chunk(s.replace("0x", ""), 2)[::-1]))

k = [0xd76aa478,0xe8c7b756,0x242070db,0xc1bdceee,
     0xf57c0faf,0x4787c62a,0xa8304613,0xfd469501,0x698098d8,
     0x8b44f7af,0xffff5bb1,0x895cd7be,0x6b901122,0xfd987193,
     0xa679438e,0x49b40821,0xf61e2562,0xc040b340,0x265e5a51,
     0xe9b6c7aa,0xd62f105d,0x02441453,0xd8a1e681,0xe7d3fbc8,
     0x21e1cde6,0xc33707d6,0xf4d50d87,0x455a14ed,0xa9e3e905,
     0xfcefa3f8,0x676f02d9,0x8d2a4c8a,0xfffa3942,0x8771f681,
     0x6d9d6122,0xfde5380c,0xa4beea44,0x4bdecfa9,0xf6bb4b60,
     0xbebfbc70,0x289b7ec6,0xeaa127fa,0xd4ef3085,0x04881d05,
     0xd9d4d039,0xe6db99e5,0x1fa27cf8,0xc4ac5665,0xf4292244,
     0x432aff97,0xab9423a7,0xfc93a039,0x655b59c3,0x8f0ccc92,
     0xffeff47d,0x85845dd1,0x6fa87e4f,0xfe2ce6e0,0xa3014314,
     0x4e0811a1,0xf7537e82,0xbd3af235,0x2ad7d2bb,0xeb86d391]

s = [7,12,17,22,7,12,17,22,7,12,17,22,7,12,17,22,
     5,9,14,20, 5,9,14,20,  5,9,14,20, 5,9,14,20,
     4,11,16,23,4,11,16,23,4,11,16,23,4,11,16,23,
     6,10,15,21,6,10,15,21,6,10,15,21,6,10,15,21]


def mainLoop(m):
    global A,B,C,D

    a, b, c, d = A, B, C, D

    for i in range(64):
        if i < 16:
            f = F(b, c, d)
            g = i
        elif i < 32:
            f = G(b, c, d)
            g = (5 * i + 1) % 16
        elif i < 48:
            f = H(b, c, d)
            g = (3 * i + 5) % 16
        else:
            f = I(b, c, d)
            g = (7 * i) % 16

        d, c, b, a = c, b, (b + L(a + f + k[i] + int(LE32(m[g]), 2), s[i])) & 0xffffffff, d

    A = (A + a) & 0xffffffff
    B = (B + b) & 0xffffffff
    C = (C + c) & 0xffffffff
    D = (D + d) & 0xffffffff


def fill(bt):
    bArr = [PR(bin(i).replace("0b",""), "0", 8) for i in bt]
    bStr = "".join(bArr)
    L = len(bStr) % 512

    if L == 0:
        bStr += ENDFLAG
        bStr += R("0", 447)
        bStr += LE64(PR(bin((len(bArr)*8)%(1<<64)).replace("0b",""), "0", 64))
    elif L < 448:
        bStr += ENDFLAG
        bStr += R("0", 447 - L)
        bStr += LE64(PR(bin((len(bArr)*8)%(1<<64)).replace("0b",""), "0", 64))
    elif L == 448:
        bStr += LE64(PR(bin((len(bArr)*8)%(1<<64)).replace("0b",""), "0", 64))
    elif L > 448:
        bStr += ENDFLAG
        bStr += R("", 959 - L)
        bStr += LE64(PR(bin((len(bArr)*8)%(1<<64)).replace("0b",""), "0", 64))

    chunked = chunk(bStr, 512)
    return [chunk(i, 32) for i in chunked]


def reset():
    global A, B, C, D
    A = 0x67452301
    B = 0xefcdab89
    C = 0x98badcfe
    D = 0x10325476


def md5(s):
    m = fill(bytes(s, encoding="utf8"))

    
    for i in range(len(m)):
        M = []
        for j in range(16):
            M.append(m[i][j])
        mainLoop(M)
    
    Sum = "".join([LE(hex(i)) for i in [A, B, C, D]])
    reset()
    return Sum


def md5fic(fic):
    with open(fic, 'r') as f:
        s = md5(f.read())
    
    return s
    # with open(fic, 'w+') as f:
    #     f.write(s)


def chunk(arr, n):
    newArr = []
    idx = 0
    length = len(arr)
    while idx < length:
        newArr.append(arr[idx:idx+n])
        idx += n
    return newArr

def dechunk(arr):
    return [i for sublist in arr for i in sublist]

def PL(s, char, n):
    return ('{:' + char + '<' + str(n) + '}').format(s)


def PR(s, char, n):
    return ('{:' + char + '>' + str(n) + '}').format(s)

def fill_ep(bt):
    bArr = [PR(bin(i).replace("0b",""), "0", 8) for i in bt]
    bStr = "".join(bArr)
    L = len(bStr) % 512

    if L == 0:
        bStr += ENDFLAG
        bStr += R("0", 447)
        bStr += LE64(PR(bin((len(bArr)*8)%(1<<64)).replace("0b",""), "0", 64))
    elif L < 448:
        bStr += ENDFLAG
        bStr += R("0", 447 - L)
        bStr += LE64(PR(bin((len(bArr)*8)%(1<<64)).replace("0b",""), "0", 64))
    elif L == 448:
        bStr += LE64(PR(bin((len(bArr)*8)%(1<<64)).replace("0b",""), "0", 64))
    elif L > 448:
        bStr += ENDFLAG
        bStr += R("", 959 - L)
        bStr += LE64(PR(bin((len(bArr)*8)%(1<<64)).replace("0b",""), "0", 64))

    chunked = chunk(bStr, 120)
    return [chunk(i, 32) for i in chunked]

def mainLoop_ep(m):
    global A,B,C,D

    a, b, c, d = A, B, C, D

    for i in range(64):
        if i < 16:
            f = F(b, c, d)
            g = i
        elif i < 32:
            f = G(b, c, d)
            g = (5 * i + 1) % 16
        elif i < 48:
            f = H(b, c, d)
            g = (3 * i + 5) % 16
        else:
            f = I(b, c, d)
            g = (7 * i) % 16

        d, c, b, a = c, b, (b + L(a + f + k[i] + int(m, 2), s[i])) & 0xffffffff, d

    A = (A + a) & 0xffffffff
    B = (B + b) & 0xffffffff
    C = (C + c) & 0xffffffff
    D = (D + d) & 0xffffffff
    
def eponge(s):
    m = fill_ep(bytes(s, encoding="utf8"))
    b = 0
    s = ''
    for i in range(len(m)):
        for j in range(len(m[i])):
            M = []
            m_int = int(m[i][j],2)
            b = b ^ (m_int<<8)
            mainLoop(str(bin(b)[2:]))
            Sum = "".join([LE(hex(j)) for j in [A, B, C, D]])
            b = int(Sum,16)
            reset()
    hash_digest = []
    for i in range(len(m)):
        for j in range(len(m[i])):
            hash_digest.append(b >> 8)
            mainLoop_ep(str(bin(b)[2:]))
            Sum = "".join([LE(hex(j)) for j in [A, B, C, D]])
            b = int(Sum,16)
    
    return hash_digest