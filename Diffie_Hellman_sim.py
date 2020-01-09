import time
import Fonction_Math as FM
import random

def Diffie_Hellman_sim():
    # prime = 0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF
    # g = 2
    gen_start = time.process_time()
    [prime,g] = FM.gen_prime_set_multi(512)
    gen_stop = time.process_time()
    # print("prime number documented in RFC3526: ", prime)
    # print("along with a generator: ", g)
    print("prime number found: ", prime)
    print("generator found: ", g)
    # print("calculation time: ", gen_stop-gen_start)
    print("Diffie Hellman key exchange statrts")
    #Alice picks a random number
    A_rand = random.randint(1,10000)
    print("Alice picks a random number A_rand", A_rand)
    # Alive send A to Bob
    A = (g**A_rand)%prime
    print("Alice calculates A = ", A, " and sends it to Bob")
    #Bob picks a random number
    B_rand = random.randint(1,10000)
    print("Bob picks a random number B_rand", B_rand)
    #B is to send ot Alice
    B = (g**B_rand)%prime
    print("Bob calculates B = ", B, " and sends it to Alice")
    #Alice calculates the key
    key_A = (B**A_rand)%prime
    #Bob calculates the key
    key_B = (A**B_rand)%prime
    print("Alice finds key: ", key_A)
    print("Bob finds key: ", key_B)