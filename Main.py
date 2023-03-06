#imports
from Crypto import Random
from Crypto.Cipher import AES
import os
import os.path
from os import listdir
from os.path import isfile, join


class Encryptor:
    def __init__(self, key):
        self.key = key

    #ensure plaintext has same lenght as AES block cipher.
    def pad(self, s):
        return s + b"\0" * (AES.block_size - len(s) % AES.block_size)

    #ecrypt the contents of the file
    def encrypt(self, message, key, key_size=256):
        message = self.pad(message)
        #iv to make sure that two identical plaintext doesnt generate identical ciphertext
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(key, AES.MODE_CBC, iv)
        return iv + cipher.encrypt(message)

    #store file as a .enc format and remove plaintext file
    def encrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            plaintext = fo.read()
        enc = self.encrypt(plaintext, self.key)
        with open(file_name + ".enc", 'wb') as fo:
            fo.write(enc)
        os.remove(file_name)

    #decrypt contents of the file
    def decrypt(self, ciphertext, key):
        iv = ciphertext[:AES.block_size]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        plaintext = cipher.decrypt(ciphertext[AES.block_size:])
        return plaintext.rstrip(b"\0")

    #store decrypted file as its original format and remove .enc file
    def decrypt_file(self, file_name):
        with open(file_name, 'rb') as fo:
            ciphertext = fo.read()
        dec = self.decrypt(ciphertext, self.key)
        with open(file_name[:-4], 'wb') as fo:
            fo.write(dec)
        os.remove(file_name)

#Key hardcoded in the code to decrypt even after killing the program
key = b'[EX\xc8\xd5\xbfI{\xa2$\x05(\xd5\x18\xbf\xc0\x85)\x10nc\x94\x02)j\xdf\xcb\xc4\x94\x9d(\x9e'
enc = Encryptor(key)

if os.path.isfile('data.txt.enc'):
    while True:
        pw = str(input("Enter password: "))
        enc.decrypt_file("data.txt.enc")
        p = ''
        with open("data.txt", "r") as f:
            p = f.readlines()
        if p[0] == pw:
            enc.encrypt_file("data.txt")
            break

    while True:
       
        choice = str(input(
            "1. Press 'E' to encrypt file.\n2. Press 'D' to decrypt file.\n3. Press 'X' to exit.\n"))
        if choice == 'E' or 'e':
            enc.encrypt_file(str(input("Enter path  of the  file to encrypted: ")))
        elif choice == 'D' or 'd':
            enc.decrypt_file(str(input("Enter path of file the to decrypted  : ")))
        elif choice == 'X' or 'x':
            exit()
        else:
            print("Please select a valid option!")

else:
    while True:
        #pw/rwp - password and repeat password 
        pw = str(input("Create a Password(remember this password as it will be used for decryption): "))
        rpw = str(input("Re-enter password: "))
        if pw == rpw:
            break
        else:
            print("Passwords Mismatched!")
    f = open("data.txt", "w+")
    f.write(pw)
    f.close()
    enc.encrypt_file("data.txt")
    print("Please restart the program to complete the setup")
    input()