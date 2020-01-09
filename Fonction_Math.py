import random
import time
import multiprocessing as mp
from multiprocessing import Manager

global share 
share = mp.Manager().list([False, 0, 0])


def Expo_rapide(a, exposant, modulo):
    if exposant==1: return a%modulo
    resultat = 1
    while exposant > 0:
        if exposant%2==1 :
            resultat = (resultat*a)%modulo

        exposant = exposant//2
        a = (a*a)%modulo

    #print(a_original, "^", exposant_original, "mod", modulo, "=", resultat)
    return resultat



def Rabin_Miller_test(prime):
    if prime < 5:
        return prime in [2, 3]

    # set: prime = q * 2**r + 1
    q, r = prime - 1, 0
    while not q & 1:
        q >>= 1
        r += 1
    # test repeatedly
    for _ in range(64):
        a = random.randint(2, prime - 1)
        # pass if: a**q == 1
        x = pow(a, q, prime)
        if x in [1, prime - 1]:
            continue
        # pass if: a**(q * 2**s) == -1, s < r
        for _ in range(r - 1):
            x = pow(x, 2, prime)
            if x == prime - 1:
                break
        else:
            return False
    return True

def proBin(longeur):
    list = []
    list.append(1)
    for i in range(longeur - 2):
        c = random.randint(0, 1)
        list.append(c)
    list.append(1)
    ls2 = [str(j) for j in list]
    ls3 = ''.join(ls2)
    b = int(ls3[0])
    for i2 in range(len(ls3) - 1):
        b = b << 1
        b = b + int(ls3[i2 + 1])
    d = int(b)
    return d


def gen_prime(bits):
    isPrime = False
    while (isPrime == False):
        prime = proBin(bits)
        if (Rabin_Miller_test(prime)):
            isPrime = True

    return prime

def Fermat_test(n):
    Isprime = True
    for i in range(1,32):
        a  = random.randint(1,n-1)
        #a = random.randrange(1,n-1)
        #print("\n random test a=", a, "\n")
        #if (a%n) != Expo_rapide(a, n, n):
        #if Expo_rapide(a, n, n) != a:

        if Expo_rapide(a, n-1, n) !=1:
            Isprime = False

    return Isprime


def get_cores():
    return mp.cpu_count()


def gen_prime_set_multi(bit_size):
    #share = mp.Manager().list([False])
    share[0] = False
    gen_prime_procs = []
    for i in range(get_cores()):
        gen_prime_procs.append(mp.Process(target=gen_prime_set_task, args=(bit_size,)))
        gen_prime_procs[i].start()
    for proc in gen_prime_procs:
        proc.join()

    p = share[1]
    g = share[2]

    return [p, g]

def gen_prime_set_task(bit_size):
    #print(share[0])
    start = time.process_time()
    q = gen_prime(bit_size)
    stop_gen_prime = time.process_time()
    #print("gen prime time: ", stop_gen_prime-start)
    p = 2*q+1
    while Rabin_Miller_test(p) != True:
        if share[0] == False:
            q = gen_prime(bit_size)
            p = 2*q+1
        else:
            return 0
    share[0] = True
    share[1] = p
    stop_while = time.process_time()
    print("calculation time: ", stop_while-stop_gen_prime-start)
    #g = random.randint(2,p)
    g = 2
    while ((Expo_rapide(g,2,p)==1) | (Expo_rapide(g,q,p)==1)):
        #g = random.randint(2,p)
        g = g + 1

    share[2] = g
    stop = time.process_time()
    # print("generator found in: ", stop-start)
    # print("prime number: ", p, "generator: ", g)
    return p,g