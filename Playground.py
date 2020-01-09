import Camellia
import MD5
import Diffie_Hellman_sim as dh
import Signature_ElGammal as sig
from colorama import Fore, Back, Style
import binascii
import utils
####################Camellia basic test#############################
# Message = 123456789
# Message = input("please type the original message")
# #print('initial message: ', '0x%x'%Message)
# res = ''.join(format(ord(i), 'b') for i in Message)
# res = int(res)
# print(hex(res))
# encrypted = Camellia.encryption(res)
# #print('encryption Message = ', '0x%x'%(Camellia.encryption(Message)))
# print('encryption Message = ', encrypted)

# print('decryption Message = ', '0x%x'%(Camellia.decryption(encrypted)))


# ####################Camellia encryption mode test#############################
# # init_vec = 0xffffffffffffffffffffffffffffffff
# # Camellia.ECB_encry()
# # Camellia.ECB_decry()


# #######################MD5 basic test###############################
# sum = MD5.md5("hello world")
# print(sum)




#print(Camellia.int_from_bytes(bytes('hello world', encoding="utf8")))

# MD5.md5fic('/home/wenbin/Desktop/test')

# ################Diffie-Hellman simulation test######################
# dh.Diffie_Hellman_sim()


# ################Signature-ElGammal simulation test######################
# sig.Signature_sim()


def interaction():
    state = ""
    exit = False
    while(exit == False):
        print("--1. Encrypt a message with Camellia algo\n")
        print("--2. Encrypt a file with Camellia EBC\n")
        print("--3. Decrypt a file with Camellia EBC\n")
        print("--4. Encrypt a file with Camellia CBC\n")
        print("--5. Decrypt a file with Camellia CBC\n")
        print("--6. Generate a paire of public/private key\n")
        print("--7. Diffie-Hellman simulation\n")
        print("--8. Verification of certification simulation\n")
        print("--9. MD5 message\n")
        print("--10. Sponge function with MD5\n")
        print("--11. Sign the message\n")
        print("--0. Exit")
        state = input('what do you want\n')
        if state == "1":
            Camellia.Camellia_message()
        
        elif state == "2":
            Camellia.ECB_encry()
            print("\n\n\n")

        elif state == "3":
            Camellia.ECB_decry()
            print("\n\n\n")
        
        elif state == "4":
            init_vec = 0xffffffffffffffffffffffffffffffff
            Camellia.CBC_encry(init_vec)
            print("\n\n\n")

        elif state == "5":
            init_vec = 0xffffffffffffffffffffffffffffffff
            Camellia.CBC_decry(init_vec)
            print("\n\n\n")


        elif state == "6":
            print("Generating...\n")
            sig.gen_keys()
            print("\n\n\n")

        elif state == "7":
            dh.Diffie_Hellman_sim()


        elif state == "8":
            sig.Signature_sim()

        elif state == "9":
            Message = input("Type the word to hash\n")
            print(MD5.md5(Message))

        elif state == "10":
            Message = input("Type the word to hash\n")
            print(MD5.eponge(Message))
        elif state == "11":
            sig.sign_message()
        elif state =="0":
            return 0





interaction()

