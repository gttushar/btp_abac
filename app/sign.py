from flask import render_template, redirect, url_for, flash, request, session, abort, get_flashed_messages
from sqlalchemy import func, text, and_
from flask_login import current_user,login_user, logout_user, login_required
from wtforms import StringField
from werkzeug.urls import url_parse
from datetime import datetime

import nacl.utils
from nacl.public import PrivateKey, PublicKey, Box
from nacl.encoding import Base64Encoder
import base64

def create_keys():
    keyfile = open("../private_keys.txt", "w+")
    org_dict = { '1' : 'IIT Kharagpur', '2' : 'IIT Kanpur', '3' : 'Jadavpur University', '4' : 'IIT Bombay' }

    print('DELETE FROM Org;')
    for org_id, org_name in org_dict.items():
        private = PrivateKey.generate()
        public = private.public_key
        privatedb = private.encode(Base64Encoder).decode('utf8')
        publicdb = public.encode(Base64Encoder).decode('utf8')
        print('INSERT INTO Org VALUES(' + org_id + ', \'' + org_name + '\' , \'' + publicdb + '\');')
        keyfile.write(org_id + ':' + org_name + ':' + publicdb + ':' + privatedb + '\n')



def get_private_key(org_name):
    file = open(os.path.join(os.path.dirname(__file__), '../private_keys.txt'), 'r+t')
    for line in file.readlines():
        words = line.split(':')
        if words[1] == org_name:
            return words[3]
    return None
def get_public_key(org_name):
    file = open(os.path.join(os.path.dirname(__file__), '../private_keys.txt'), 'r+t')
    for line in file.readlines():
        words = line.split(':')
        if words[1] == org_name:
            return words[2]
    return None

def base64_to_bytes(key:str) -> bytes: 
    return base64.b64decode(key.encode('utf-8'))

def encrypt_for_user(sender_private:str, receiver_public:str, message:str) -> str: 
    sender_private = PrivateKey(base64_to_bytes(sender_private))
    receiver_public = PublicKey(base64_to_bytes(receiver_public))
    sender_box = Box(sender_private, receiver_public)

    return base64.b64encode(sender_box.encrypt(bytes(message, "utf-8"))).decode('utf-8')

def decrypt_for_user(receiver_private:str, sender_public:str, message:str) -> str: 
    receiver_private = PrivateKey(base64_to_bytes(receiver_private))
    sender_public = PublicKey(base64_to_bytes(sender_public))
    receiver_box = Box(receiver_private, sender_public)

    return receiver_box.decrypt(base64.b64decode(message.encode('utf-8'))).decode('utf-8')

# create_keys()
import os, sys
filename = 'examples/' + sys.argv[1]
filename_signed = filename + '_signed.txt'
filename = filename + '.txt'
example = open(os.path.join(os.path.dirname(__file__), '../' + filename), 'r')
example_signed = open(os.path.join(os.path.dirname(__file__), '../' + filename_signed), 'w')
example_signed.write( \
    encrypt_for_user(get_private_key('IIT Kanpur'), get_public_key('IIT Kharagpur'), example.read()))

print(get_private_key('IIT Kanpur'))
print(get_public_key('IIT Kharagpur'))
print(encrypt_for_user(get_private_key('IIT Kanpur'), get_public_key('IIT Kharagpur'), example.read()))

example.close()
example_signed.close()











# import Crypto
# from Crypto.PublicKey import RSA
# # from Crypto.publickey import RSA
# from Crypto import Random
# import base64

# def rsakeys():  
# 	length=1024  
# 	privatekey = RSA.generate(length, Random.new().read)  
# 	publickey = privatekey.publickey()  
# 	return privatekey, publickey

# def encrypt(rsa_publickey,plain_text):
# 	cipher_text=rsa_publickey.encrypt(plain_text,32)[0]
# 	b64cipher=base64.b64encode(cipher_text)
# 	return b64cipher

# def decrypt(rsa_privatekey,b64cipher):
# 	decoded_ciphertext = base64.b64decode(b64cipher)
# 	plaintext = rsa_privatekey.decrypt(decoded_ciphertext)
# 	return plaintext

# def sign(privatekey,data):
# 	return base64.b64encode(str((privatekey.sign(data,''))[0]).encode())

# def verify(publickey,data,sign):
# 	return publickey.verify(data,(int(base64.b64decode(sign)),))

# privatekey,publickey = rsakeys()
# print(privatekey)
# print(publickey)