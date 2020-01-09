import base64
import sys
import textwrap
import utils
import Camellia


MASK8 = 0xff
MASK32 = 0xffffffff
MASK64 = 0xffffffffffffffff
MASK128 = 0xffffffffffffffffffffffffffffffff


Sigma1 = 0xA09E667f3BCC908B
Sigma2 = 0xB67AE8584CAA73B2
Sigma3 = 0xC6Ef372fE94f82BE
Sigma4 = 0x54ff53A5f1D36f1C
Sigma5 = 0x10E527fADE682d1D
Sigma6 = 0xB05688C2B3E6C1fD



####################################################################################
#################################calcul d'exponentiel###############################
####################################################################################
Expo_X = []
Expo_X.append(0b1)
#print ('X',0,' = ', bin(0b1))
for i in range (1,256):
    val = Expo_X[i-1]<<1
    if (val & 0b100000000):
        val = val & MASK8 ^ 0b00101101
    #print ('X',i,' = ', bin(val))
    Expo_X.append(val)



def SBOX1(t) :
    t = t<<6

    #print('t = ', bin(t))
    resultat = t & MASK8
    #print('resultat = ', bin(resultat))
    for i in range(8,16):
        #print('i = ', i, ' 0b1<<i : ', bin(0b1<<i))
        #print('exec? : ', bin(t & (0b1<<i)))
        if (t & (0b1<<i)):

            #print('Expo_X[i] = ', bin(Expo_X[i]))
            #resultat = resultat ^ Expo_X[i+1]
            resultat = resultat ^ Expo_X[i]
            #print('i = ', bin(resultat), ' resultat = ', bin(resultat))


    resultat = resultat ^ Expo_X[4]^ Expo_X[3]^ Expo_X[1]
    return resultat

def SBOX2(t):
    if (t==0):
        resultat = 0
    else:
        indice = Expo_X.index(t)
        #print('Indice de t = ', indice)
        #print('Indice de inverse = ', 255 - indice)
        i_inverse = 255 - indice
        resultat = Expo_X[i_inverse]
    #print('inverse = ', bin(resultat))
    return resultat



def SBOX3(t) :
    resultat = t ^ Expo_X[7] ^ Expo_X[6] ^ Expo_X[5] ^ Expo_X[4] ^ Expo_X[3] ^ Expo_X[2] ^ Expo_X[1] ^ Expo_X[0]
    return resultat

def SBOX4(t) :
    t = t ^ Expo_X[6] ^ Expo_X[4] ^ Expo_X[2] ^ Expo_X[0]
    t = t<<7
    #print('t = ', bin(t))
    resultat = t & MASK8
    #print('resultat = ', bin(resultat))
    for i in range(8,16):
        #print('i = ', i, ' 0b1<<i : ', bin(0b1<<i))
        #print('exec? : ', bin(t & (0b1<<i)))
        if (t & (0b1<<i)):

            #print('Expo_X[i] = ', bin(Expo_X[i]))
            #resultat = resultat ^ Expo_X[i+1]
            resultat = resultat ^ Expo_X[i]
            #print('i = ', bin(resultat), ' resultat = ', bin(resultat))

    resultat = resultat ^ Expo_X[5] ^ Expo_X[3] ^ Expo_X[1]
    return resultat




def SBOX5(t):
    t = t<<5
    #print('t = ', bin(t))
    resultat = t & MASK8
    #print('resultat = ', bin(resultat))
    for i in range(8,16):
        #print('i = ', i, ' 0b1<<i : ', bin(0b1<<i))
        #print('exec? : ', bin(t & (0b1<<i)))
        if (t & (0b1<<i)):

            #print('Expo_X[i] = ', bin(Expo_X[i]))
            #resultat = resultat ^ Expo_X[i+1]
            resultat = resultat ^ Expo_X[i]
            #print('i = ', bin(resultat), ' resultat = ', bin(resultat))


    resultat = resultat ^ Expo_X[2] ^ Expo_X[0]

    return resultat



def SBOX6(t):
    t = t<<3
    #print('t = ', bin(t))
    resultat = t & MASK8
    #print('resultat = ', bin(resultat))
    for i in range(8,16):
        #print('i = ', i, ' 0b1<<i : ', bin(0b1<<i))
        #print('exec? : ', bin(t & (0b1<<i)))
        if (t & (0b1<<i)):

            #print('Expo_X[i] = ', bin(Expo_X[i]))
            #resultat = resultat ^ Expo_X[i+1]
            resultat = resultat ^ Expo_X[i]
            #print('i = ', bin(resultat), ' resultat = ', bin(resultat))


    resultat = resultat ^ Expo_X[3] ^ Expo_X[2] ^ Expo_X[1] ^ Expo_X[0]


    ######reverse
    resultat =  SBOX2(resultat)

    return resultat

def SBOX7(t):
    resultat = t ^ Expo_X[7] ^ Expo_X[6] ^ Expo_X[5] ^ Expo_X[4] ^ Expo_X[3] ^ Expo_X[2] ^ Expo_X[1] ^ Expo_X[0]
    return resultat



def SBOX8(t) :
    t = t ^ Expo_X[7] ^ Expo_X[5] ^ Expo_X[3] ^ Expo_X[1]
    t = t<<6
    #print('t = ', bin(t))
    resultat = t & MASK8
    #print('resultat = ', bin(resultat))
    for i in range(8,16):
        #print('i = ', i, ' 0b1<<i : ', bin(0b1<<i))
        #print('exec? : ', bin(t & (0b1<<i)))
        if (t & (0b1<<i)):

            #print('Expo_X[i] = ', bin(Expo_X[i]))
            #resultat = resultat ^ Expo_X[i+1]
            resultat = resultat ^ Expo_X[i]
            #print('i = ', bin(resultat), ' resultat = ', bin(resultat))

    resultat = resultat ^ Expo_X[4] ^ Expo_X[2] ^ Expo_X[0]
    return resultat

###########64 bits f_in
###########64 bits ke
###########64bits f_out
def func_f(f_in , ke) :
    x = f_in ^ ke
    t1 =  x >> 56
    t2 = (x >> 48) & MASK8
    t3 = (x >> 40) & MASK8
    t4 = (x >> 32) & MASK8
    t5 = (x >> 24) & MASK8
    t6 = (x >> 16) & MASK8
    t7 = (x >>  8) & MASK8
    t8 =  x        & MASK8
    t1 = SBOX1(t1)
    t2 = SBOX2(t2)
    t3 = SBOX3(t3)
    t4 = SBOX4(t4)
    t5 = SBOX2(t5)
    t6 = SBOX3(t6)
    t7 = SBOX4(t7)
    t8 = SBOX1(t8)
    y1 = t1 ^ t3 ^ t4 ^ t6 ^ t7 ^ t8
    y2 = t1 ^ t2 ^ t4 ^ t5 ^ t7 ^ t8
    y3 = t1 ^ t2 ^ t3 ^ t5 ^ t6 ^ t8
    y4 = t2 ^ t3 ^ t4 ^ t5 ^ t6 ^ t7
    y5 = t1 ^ t2 ^ t6 ^ t7 ^ t8
    y6 = t2 ^ t3 ^ t5 ^ t7 ^ t8
    y7 = t3 ^ t4 ^ t5 ^ t6 ^ t8
    y8 = t1 ^ t4 ^ t5 ^ t6 ^ t7
    f_out = (y1 << 56) | (y2 << 48) | (y3 << 40) | (y4 << 32)| (y5 << 24) | (y6 << 16) | (y7 <<  8) | y8
    return f_out



k = 0xffffffffffffffffffffffffffffffff
k = 0x11111111111111111111111111111111
# Partie "key Scheduling" (Pas de KB dans cas 128bits)
#k = 0
kl = k
kr = 0
d1 = (kl ^ kr) >> 64
d2 = (kl ^ kr) & MASK64



d2 = d2 ^ func_f(d1 , Sigma1)
d1 = d1 ^ func_f(d2 , Sigma2)
d1 = d1 ^ (kl >> 64)
d2 = d2 ^ (kl & MASK64)
d2 = d2 ^ func_f(d1 , Sigma3)
d1 = d1 ^ func_f(d2 , Sigma4)
ka = (d1 << 64) | d2
d1 = (ka ^ kr) >> 64
d2 = d2 ^ func_f(d1 , Sigma5)
d1 = d1 ^ func_f(d2 , Sigma6)




def rol(int_value,k,size_value):
    #int_value = 0b0000000011111111
    string_bin_value = str(bin(int_value))[2:]
    #print(len(string_bin_value))
    #size_value = 16
    for i in range(0,size_value-len(string_bin_value)):
        string_bin_value = '0' + string_bin_value

    #print(len(string_bin_value))
    #k = 8
    shifted_string_value = string_bin_value[k:] + string_bin_value[:k]
    #print('shifted_string_value',shifted_string_value)
    resultat_int = 0
    for j in range(1,len(shifted_string_value)+1):
        resultat_int = resultat_int + int(shifted_string_value[len(shifted_string_value)-j])*(2**(j-1))
        #print('j = ', j, shifted_string_value[:j])
        #print('resulta_int = ', bin(resultat_int))

    return resultat_int




# Generation de 64-bit subkeys kw1, ..., kw4, k1, ..., k18, ke1, ..., ke4
kw1 = rol(kl,0,128) >> 64
kw2 = rol(kl,0,128) & MASK64
k1  = rol(ka,0,128) >> 64
k2  = rol(ka,0,128) & MASK64
k3  = rol(kl,15,128) >> 64
k4  = rol(kl,15,128) & MASK64
k5  = rol(ka,15,128) >> 64
k6  = rol(ka,15,128) & MASK64
ke1 = rol(ka,30,128) >> 64
ke2 = rol(ka,30,128) & MASK64
k7  = rol(kl,45,128) >> 64
k8  = rol(kl,45,128) & MASK64
k9  = rol(ka,45,128) >> 64
k10 = rol(kl,60,128) & MASK64
k11 = rol(ka,60,128) >> 64
k12 = rol(ka,60,128) & MASK64
ke3 = rol(kl,77,128) >> 64
ke4 = rol(kl,77,128) & MASK64
k13 = rol(kl,94,128) >> 64
k14 = rol(kl,94,128) & MASK64
k15 = rol(ka,94,128) >> 64
k16 = rol(ka,94,128) & MASK64
k17 = rol(kl,111,128) >> 64
k18 = rol(kl,111,128) & MASK64
kw3 = rol(ka,111,128) >> 64
kw4 = rol(ka,111,128) & MASK64






# fl-function
def fl(fl_in , ke) :
    x1 = fl_in >> 32
    x2 = fl_in & MASK32
    k1 = ke >> 32
    k2 = ke & MASK32
    x2 = x2 ^ rol((x1 & k1),1,32)
    x1 = x1 ^ (x2 | k2)
    fl_out = (x1 << 32) | x2
    return fl_out

# flinv-funtion
def flinv(flinv_in , ke) :
    y1 = flinv_in >> 32
    y2 = flinv_in & MASK32
    k1 = ke >> 32
    k2 = ke & MASK32
    y1 = y1 ^ (y2 | k2)
    y2 = y2 ^ rol((y1 & k1),1,32)
    flinv_out = (y1 << 32) | y2
    return flinv_out

def read_file(path):
    message = []
    with open(path, "rb") as f:
        byte = f.read(16)
        while byte != b"":
            print("length = ", len(byte), byte)
            message.append(byte)
            byte = f.read(16)

    return(message)

def encryption(M) :
    d1 = M >> 64
    d2 = M & MASK64
    d1 = d1 ^ kw1            # Prewhitening
    d2 = d2 ^ kw2
    d2 = d2 ^ func_f(d1, k1)      # tour 1
    d1 = d1 ^ func_f(d2, k2)      # tour 2
    d2 = d2 ^ func_f(d1, k3)      # tour 3
    d1 = d1 ^ func_f(d2, k4)      # tour 4
    d2 = d2 ^ func_f(d1, k5)      # tour 5
    d1 = d1 ^ func_f(d2, k6)      # tour 6
    d1 = fl(d1, ke1)      # fl
    d2 = flinv(d2, ke2)      # flinv
    d2 = d2 ^ func_f(d1, k7)      # tour 7
    d1 = d1 ^ func_f(d2, k8)      # tour 8
    d2 = d2 ^ func_f(d1, k9)      # tour 9
    d1 = d1 ^ func_f(d2, k10)     # tour 10
    d2 = d2 ^ func_f(d1, k11)     # tour 11
    d1 = d1 ^ func_f(d2, k12)     # tour 12
    d1 = fl(d1, ke3)      # fl
    d2 = flinv(d2, ke4)      # flinv
    d2 = d2 ^ func_f(d1, k13)     # tour 13
    d1 = d1 ^ func_f(d2, k14)     # tour 14
    d2 = d2 ^ func_f(d1, k15)     # tour 15
    d1 = d1 ^ func_f(d2, k16)     # tour 16
    d2 = d2 ^ func_f(d1, k17)     # tour 17
    d1 = d1 ^ func_f(d2, k18)     # tour 18
    d2 = d2 ^ kw3            # Postwhitening
    d1 = d1 ^ kw4

    c = (d2 << 64) | d1 # 128 ciphertext
    return c




def decryption(c):
    d1 = c >> 64
    d2 = c & MASK64
    d1 = d1 ^ kw3            # Prewhitening
    d2 = d2 ^ kw4
    d2 = d2 ^ func_f(d1, k18)      # tour 1
    d1 = d1 ^ func_f(d2, k17)      # tour 2
    d2 = d2 ^ func_f(d1, k16)      # tour 3
    d1 = d1 ^ func_f(d2, k15)      # tour 4
    d2 = d2 ^ func_f(d1, k14)      # tour 5
    d1 = d1 ^ func_f(d2, k13)      # tour 6
    d1 = fl   (d1, ke4)      # fl
    d2 = flinv(d2, ke3)      # flinv
    d2 = d2 ^ func_f(d1, k12)      # tour 7
    d1 = d1 ^ func_f(d2, k11)      # tour 8
    d2 = d2 ^ func_f(d1, k10)      # tour 9
    d1 = d1 ^ func_f(d2, k9)     # tour 10
    d2 = d2 ^ func_f(d1, k8)     # tour 11
    d1 = d1 ^ func_f(d2, k7)     # tour 12
    d1 = fl   (d1, ke2)      # fl
    d2 = flinv(d2, ke1)      # flinv
    d2 = d2 ^ func_f(d1, k6)     # tour 13
    d1 = d1 ^ func_f(d2, k5)     # tour 14
    d2 = d2 ^ func_f(d1, k4)     # tour 15
    d1 = d1 ^ func_f(d2, k3)     # tour 16
    d2 = d2 ^ func_f(d1, k2)     # tour 17
    d1 = d1 ^ func_f(d2, k1)     # tour 18
    d2 = d2 ^ kw1            # Postwhitening
    d1 = d1 ^ kw2

    M = (d2 << 64) | d1 # 128 ciphertext
    return M



########################################Encryption modes#########################################


# -*- coding: <utf-8> -*-

def int_to_bytes(x: int) -> bytes:
    return x.to_bytes((x.bit_length() + 7) // 8, 'big')

def int_from_bytes(xbytes: bytes) -> int:
    return int.from_bytes(xbytes, 'big')

def ECB_encry():
    filename = utils.get_filename()
    cypher_file = filename + '_ECB' + '.cypher'
    # Fonction de coupage
    M_cut = []
    M_cut = utils.read_file(filename)
    # Liste des blocs chiffres
    C_bloc = []

    for i in range(0,len(M_cut)):
        M_cut_int = int_from_bytes(M_cut[i])
        c_i = encryption(M_cut_int)
        C_bloc.append(c_i)
    # Print tous les éléments #
    message_chiffre = C_bloc[0]

    for i in range(1,len(C_bloc)):
        C_bloc_bytes = int_to_bytes(C_bloc[i])
        message_chiffre = message_chiffre<<(len(C_bloc_bytes)*8) ^ C_bloc[i]
    message_chiffre_bytes = int_to_bytes(message_chiffre)
    ######################<Generate a file>#########################
    utils.write_cypher_file(cypher_file,int_to_bytes(message_chiffre)) 
    #################################################################


def ECB_decry():
    filename = utils.get_filename()
    print("File to Decrypt:", filename)

    # Grabbing original file extension
    file_extension = filename.split('.cypher', 1)[0]
    if len(file_extension.split('.', 1)) != 1:
        file_extension = '.' + file_extension.split('.', 1)[1]
    else:
        file_extension = ''
    M_bloc = []
    C_cut = utils.read_file(filename)
    for i in range(0,len(C_cut)):
        C_cut_int = int_from_bytes(C_cut[i])
        m_i = decryption(C_cut_int)
        M_bloc.append(m_i)
    message_dechiffre = M_bloc[0]
    for i in range(1,len(M_bloc)):
        M_bloc_bytes = int_to_bytes(M_bloc[i])
        message_dechiffre = message_dechiffre<<(len(M_bloc_bytes)*8) ^ M_bloc[i]
    message_dechiffre_bytes = int_to_bytes(message_dechiffre)
    ######################<Generate a file>#########################
    utils.write_clair_file(message_dechiffre_bytes.decode("utf-8"),file_extension)
    #################################################################


def CBC_encry(init_vec):
    filename = utils.get_filename()
    cypher_file = filename + '_CBC' + '.cypher'
    # Fonction de coupage
    M_cut = []
    M_cut = utils.read_file(filename)
    
    # Liste des blocs chiffres
    C_bloc = []
    M_cut_int = int_from_bytes(M_cut[0])
    c_0 = encryption(M_cut_int ^ init_vec)
    C_bloc.append(c_0)
    for i in range(1,len(M_cut)):
        M_cut_int = int_from_bytes(M_cut[i])
        c_i = encryption(M_cut_int ^ C_bloc[i-1])
        C_bloc.append(c_i)
    # Print tous les éléments #
    message_chiffre = C_bloc[0]
    for i in range(1,len(C_bloc)):
        C_bloc_bytes = int_to_bytes(C_bloc[i])
        message_chiffre = message_chiffre<<(len(C_bloc_bytes)*8) ^ C_bloc[i]
        #print(C_bloc_bytes)
    message_chiffre_bytes = int_to_bytes(message_chiffre)
    ######################<Generate a file>#########################
    utils.write_cypher_file(cypher_file,int_to_bytes(message_chiffre))
    #################################################################


def CBC_decry(init_vec):
    filename = utils.get_filename()
    print("File to Decrypt:", filename)

    # Grabbing original file extension
    file_extension = filename.split('.cypher', 1)[0]
    if len(file_extension.split('.', 1)) != 1:
        file_extension = '.' + file_extension.split('.', 1)[1]
    else:
        file_extension = ''

    M_bloc = []
    C_cut = utils.read_file(filename)
    C_cut_int = int_from_bytes(C_cut[0])
    m_0 = decryption(C_cut_int) ^ init_vec
    M_bloc.append(m_0)
    for i in range(1,len(C_cut)):
        C_cut_int = int_from_bytes(C_cut[i])
        m_i = decryption(C_cut_int) ^ int_from_bytes(C_cut[i-1])
        M_bloc.append(m_i)
    message_dechiffre = M_bloc[0]
    for i in range(1,len(M_bloc)):
        M_bloc_bytes = int_to_bytes(M_bloc[i])
        message_dechiffre = message_dechiffre<<(len(M_bloc_bytes)*8) ^ M_bloc[i]
    message_dechiffre_bytes = int_to_bytes(message_dechiffre)
    print(message_dechiffre_bytes)
    ######################<Generate a file>#########################
    utils.write_clair_file(message_dechiffre_bytes.decode("utf-8"),file_extension)
    #################################################################


# ECB_encry()
# ECB_decry()
# CBC_encry(init_vec)
# CBC_decry(init_vec)



def Camellia_message():
    Message = input("Type the word to encrypt\n")
    res = ''.join(format(ord(i), 'b') for i in Message)
    res = int(res)
    print("Original message in hex = ", hex(res))
    ###################################################
    list_message = []
    res_bytes = int_to_bytes(res)
    list_message = [res_bytes[i:i+16] for i in range(0, len(res_bytes), 16)]
    cypher_text = []
    s = ''
    encrypted = []
    for i in range(0,len(list_message)):
        cypher = Camellia.int_from_bytes(list_message[i])
        encrypted.append(Camellia.encryption(cypher))
        cypher_text.append(str(Camellia.encryption(cypher)))

    ###################################################
    print('encryption Message = ', s.join(cypher_text))
    decrypted = []
    for i in range(0,len(encrypted)):
        clair = Camellia.decryption(encrypted[i])
        decrypted.append('0x%x'%(clair))
    
    decrypted_int = "0x"
    for i in decrypted:
        decrypted_int = decrypted_int + i[2:]
 
    
    
    print('decryption Message = ',decrypted_int)
    #print('decryption Message = ', decrypted, type(decrypted[0]))
    print("\n\n\n")