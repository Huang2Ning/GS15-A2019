# -*-coding:UTF-8 -*
# !/usr/bin/env python

import sys
from tkinter import filedialog, Tk

#########################
#                       #
#       FILE UTILS      #
#                       #
#########################

def wipe_file(file):
    """ Erase file content if it already exists
    :param file: <str>
    :return: file: <str> - wiped file
    """
    with open(file, encoding='utf-8', mode='w') as file_to_wipe:
        file_to_wipe.write("")
    return file

def write_cypher_file(cypher_file, text):
    wipe_file(cypher_file)  # Clean cypher file if it already exist
    with open(cypher_file, mode ='wb') as file:
        file.write(text)
        file.close()
    print("\x1b[6;30;42mCypher successfully created\x1b[0m\n")
    sys.stdout.flush()
    return 0

def write_clair_file(text,file_extension):
    print("----------------------------------SAVING DECRYPTED TEXT-----------------------------------")
    new_file = save_file() + file_extension
    with open(new_file, mode='w') as file:
        file.write(text)
        file.close()
  


def check_file_exist(filename):
    """ Check if a file exists
    :param filename: <str>
    :return: <boolean>
    """
    try:
        with open(filename):
            return True
    except:
        return False


def get_filename():
    """ Open a Tkinter filedialog
    :return: <str> - file path
    """
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    return filedialog.askopenfilename(title = "Select file to Encrypt", filetypes = (("Text Files","*.txt"),("all files","*.*")))

def save_file():
    root = Tk()
    root.withdraw()
    root.attributes("-topmost", True)
    return filedialog.asksaveasfilename(title = "Select file", filetypes = (("Encrypted Files","*.cypher"), ("all files","*.*")))

def get_file_hex(file_name="tests/idea_test.txt"):
    """ Getting the content of a file
    :param: file_name: <str> - file name
    :return: content_as_bytes : <str> - content in hex
    """
    with open(file_name, 'rb') as file_alias:
        content_as_bytes = file_alias.read()

    hex_content = bytes.hex(content_as_bytes)
    return hex_content

def PKCS7_padding(hex_message):
    """ Padding PKCS#7
    k - (input_len mod k) octets all having value k - (input_len mod k)
    :param: hex_message: <str> - hexadecimal message
    :return: hex_message: <str> - padded hexadecimal message
    """
    len_message = len(hex_message)

    for i in range(16 - (len_message % 16)):
        hex_message += format(16 - (len_message % 16), 'x')

    assert len(hex_message) % 16 == 0  # Checking if padding is successful
    return hex_message

def PKCS7_unpadding(hex_message):
    """ Unpadding PKCS#7
    k - (input_len mod k) octets all having value k - (input_len mod k)
    :param hex_message: <str> - padded hexadecimal message
    :return: <str> -  unpadded hexadecimal message
    """
    # Getting last character of the chain
    k = hex_message[-1]

    # Converting it to int
    try:
        k = int(k ,16)
    except:
        print("Conversion Error during the un-padding operation")

    # Removing the pad
    return hex_message[:len(hex_message) - k]





def read_file(path):
    message = []
    with open(path, "rb") as f:
        byte = f.read(16)
        while byte != b"":
            print("length = ", len(byte), byte)
            message.append(byte)
            byte = f.read(16)
    print(message)
    return(message)