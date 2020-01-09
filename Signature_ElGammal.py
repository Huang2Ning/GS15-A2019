import random
import time
import Fonction_Math as FM
import multiprocessing as mp
from multiprocessing import Manager
import MD5





def gcd(a,b):
    while a!=0:
        a,b = b%a,a
    return b

def findModReverse(a,m):

    if gcd(a,m)!=1:
        return None
    u1,u2,u3 = 1,0,a
    v1,v2,v3 = 0,1,m
    while v3!=0:
        q = u3//v3
        v1,v2,v3,u1,u2,u3 = (u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
    return u1%m


def gen_keys():
    [p,g] = FM.gen_prime_set_multi(512)
    priv_key = random.randint(1, p-2)
    pub_key = FM.Expo_rapide(g, priv_key, p)
    print("Public key: ", pub_key)
    print("Private key: ", priv_key)


###########Sgnature simulation with ElGamal########################
def sign_message():
    message = input("Please input the message to sign\n")
    print("generating...")
    [p,g] = FM.gen_prime_set_multi(512)
    priv_key = random.randint(1, p-2)
    pub_key = FM.Expo_rapide(g, priv_key, p)
    print("public key generated: ", pub_key)
    print("private key generated: ", priv_key)
    k = FM.gen_prime(512)
    while (k > p-2):
        k = FM.gen_prime(512)
    k_reverse = findModReverse(k, p-1)
    r = FM.Expo_rapide(g, k, p)
    s = ((int(MD5.md5(message), 16) - priv_key*r)*k_reverse)%(p-1)
    Signature = [r, s]
    print("Signature: ", Signature)


def Signature_sim():
    #global known parameters: p, g
    [p,g] = FM.gen_prime_set_multi(512)
    print("p: ", p)
    print("g: ", g)

    # p = 18949989762814550689665544419568283713542842550147948035871102421985313794580994094215156236872009333105224488587695869229596754776136431853972927455905747
    # g = 2

    priv_key_certif = random.randint(1, p-2)
    pub_key_certif = FM.Expo_rapide(g, priv_key_certif, p)

    priv_key_site = random.randint(1, p-2)
    pub_key_site = FM.Expo_rapide(g, priv_key_site, p)

    priv_key_user = random.randint(1, p-2)
    pub_key_user = FM.Expo_rapide(g, priv_key_user, p)

    print("CA public key: ", pub_key_certif)
    print("\n")
    print("CA private key: ", priv_key_certif)
    print("\n")

    print("Site public key: ", pub_key_site)
    print("\n")
    print("Site private key: ", priv_key_site)    
    print("\n")

    #Certificateur signs the public key of site with its own private key(priv_key_certif)


    
    k = FM.gen_prime(512)
    while (k > p-2):
        k = FM.gen_prime(512)
   


    k_reverse = findModReverse(k, p-1)
    r = FM.Expo_rapide(g, k, p)
    s = ((int(MD5.md5(str(pub_key_site)), 16) - priv_key_certif*r)*k_reverse)%(p-1)
    Signature = [r, s]
    print("CA signes the public key of site with CA's Private key")
    print("Certification: ", Signature)
    print("\n")
    # print(pub_key_site)
    # print(str(pub_key_site))
    # print(md5(str(pub_key_site)))
    # print(hex(int(md5(str(pub_key_site)), 16)))
    # signature = [r, s]

    # #verification of the signature
    print("Verification of certification")
    print("\n\n")
    print("Calculate from public key of site: ", FM.Expo_rapide(g, (int(MD5.md5(str(pub_key_site)), 16)), p))
    print("\n")
    print("Calculate from certification: ", (FM.Expo_rapide(pub_key_certif, r, p)*FM.Expo_rapide(r, s, p))%p)
    if ((FM.Expo_rapide(g, (int(MD5.md5(str(pub_key_site)), 16)), p)) == ((FM.Expo_rapide(pub_key_certif, r, p)*FM.Expo_rapide(r, s, p))%p)):
         print("verified")
    file_write_list = []
    file_write_list.append("CA public key: ")
    file_write_list.append(str(pub_key_certif))
    file_write_list.append("\n")
    file_write_list.append("CA private key: ")
    file_write_list.append(str(priv_key_certif))
    file_write_list.append("\n")
    file_write_list.append("Site public key: ")
    file_write_list.append(str(pub_key_site))
    file_write_list.append("\n")
    file_write_list.append("Site private key: ")
    file_write_list.append(str(priv_key_site))
    file_write_list.append("\n")
    file_write_list.append("Certification: ")
    file_write_list.append(str(Signature))
    file_write_list.append("\n")
    
    with open("certificate_file", mode ='w') as file:
        #print("file should write : ",file_write_list)
        file.write(''.join(file_write_list))
        file.close()
    print("\x1b[6;30;42mCerticicat file successfully created\x1b[0m\n")

