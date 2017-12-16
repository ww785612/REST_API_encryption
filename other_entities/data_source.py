# importing the requests library
# cloud IP address 35.167.25.135
from flask import Flask, request, jsonify
import requests
import json
import bson
import base64
import os
import Crypto
from Crypto.PublicKey import RSA
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

class AESCipher(object):

    def __init__(self, clientName): 
        self.bs = 32
        self.clientName = clientName
        self.key = clientName+'_AESKey'
        self.key = hashlib.sha256(self.key.encode()).digest()

    def saveKeyToFile(self):
        #'wb' open file as binary file so we can write the key(hashed bytes) to it
        with open(self.clientName+'_AESKey','wb') as f:
          f.write(self.key)

    def loadKeyfromFile(self):
        #'rb' open file as binary file so we can read the key (hashed bytes) as bytes
        with open(self.clientName+'_AESKey','wb') as f:
          key = f.read()
          return key

    def updateKey(self, newKey):
        self.key = newKey

    def getKey(self):
        return self.key

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

def generateKeyPair():
    key = RSA.generate(2048) #generate pub and priv key
    with open('data_source_private_key.pem','w') as file:
        file.write(key.exportKey('PEM').decode())
    publickey = key.publickey() # pub key export for exchange
    with open('data_source_public_key.pem','w') as file:
        file.write(publickey.exportKey('PEM').decode())

def loadPrivateKey():
    privKeyFile = open('data_source_private_key.pem','r')
    strPrivKey = privKeyFile.read()
    loadedPrivKey = RSA.importKey(strPrivKey)
    privKeyFile.close()
    return loadedPrivKey

def loadPublicKey():
    pubKeyFile = open('data_source_public_key.pem','r')
    strPubKey = pubKeyFile.read()
    loadedPubKey =  RSA.importKey(strPubKey)
    pubKeyFile.close()
    return loadedPubKey

def loadOwnerPrivateKey():
    privKeyFile = open('owner_private_key.pem','r')
    strPrivKey = privKeyFile.read()
    loadedPrivKey = RSA.importKey(strPrivKey)
    privKeyFile.close()
    return loadedPrivKey

def loadOwnerPublicKey():
    pubKeyFile = open('owner_public_key.pem','r')
    strPubKey = pubKeyFile.read()
    loadedPubKey =  RSA.importKey(strPubKey)
    pubKeyFile.close()
    return loadedPubKey

def loadRequesterPublicKey():
    pubKeyFile = open('data_requester_public.pem','r')
    strPubKey = pubKeyFile.read()
    loadedPubKey =  RSA.importKey(strPubKey)
    pubKeyFile.close()
    return loadedPubKey

def getOwnerSignature():
    pubKeyFile = open('data_source_public_key.pem','r')
    strPubKey = pubKeyFile.read()
    pubKeyFile.close()
    ownerPrivateKey = loadOwnerPrivateKey()
    signature = ownerPrivateKey.sign(strPubKey.encode(),32)
    return signature

def get(url):
    # api-endpoint
    URL = url
     
    # sending get request and saving the response as response object
    r = requests.get(url = URL)
     
    # extracting data in json format
    data = r.json()
     
    # printing the output
    print("received:", data)
    return data

#data is a list of dictionaries
def post(url, msgPkt):
  # defining the api-endpoint 
  API_ENDPOINT = url
  # sending post request and saving response as response object
  r = requests.post(url = API_ENDPOINT, data = msgPkt, verify='owner_server_https.pem')
  
def owner_server_post(url, msgPkt):
  print(msgPkt)
  # defining the api-endpoint 
  API_ENDPOINT = url
  # binaryMsgPkt = bson.dumps(data)
  # data to be sent to api
  # data = {key:value}
  certFile = 'owner_server_https.pem'
  kwargs = dict(verify = certFile) if os.path.exists(certFile) else{}
  # sending post request and saving response as response object
  r = requests.post(url = API_ENDPOINT, data = msgPkt, **kwargs)

def send_msg1():
  ownerPubKey = loadOwnerPublicKey()
  device = {
    'name':'Living room camera',
    'type':'Camera',
    'location':'Home'
  }

  deviceSummary = {
  'access duration':'access to realtime data'
  }

  metadata =  { 'device_summary_ID':1,
                'start_data':'12/1/2017',
                'end_data':'12/4/2017'
              }
  DOT = {
          'Data_ID':1,
          'K_O':ownerPubKey.exportKey('PEM').decode(),
          'metadata':metadata,
          'DAT':'http://192.168.116.131:5000/data_object'
        }

  ownerSignedPubKey = getOwnerSignature()

  msg1 =  {
            'DOT':DOT,
            'ownerSignedSourcePubKey':ownerSignedPubKey,
            'device':device,
            'deviceSummary':deviceSummary,
            'sourceName':'Storage Provider'
          }
  jsonMsg1 = json.dumps(msg1)
  encryptedJsonMsg1 = ownerAESObj.encrypt(jsonMsg1)
  encryptedAESKey = ownerPubKey.encrypt(ownerAESObj.getKey(), 32)

  msgPkt =  {
              
              'payload': encryptedJsonMsg1.decode(),
              'AESKey':base64.encodestring(encryptedAESKey[0]).decode(),
              'type':1
            }
  jsonMsgPkt = json.dumps(msgPkt)
  post('http://192.168.71.130:5000/tasks',jsonMsgPkt)
  # owner_server_post('https://35.167.25.135:5000/dmp', jsonMsgPkt)


def send_msg5():
  pubKey = loadPublicKey()
  privKey = loadPrivateKey()
  requesterPubKey = loadRequesterPublicKey()
  ownerPubKey = loadOwnerPublicKey()

  device = {
    'name':'Living room camera',
    'type':'Camera',
    'location':'Home'
  }

  deviceSummary = {
  'access duration':'access to realtime data'
  }

  metadata =  { 'device_summary_ID':1,
                'start_data':'12/1/2017',
                'end_data':'12/4/2017'
              }
  DOT = {
          'Data_ID':1,
          'K_O':ownerPubKey.exportKey('PEM').decode(),
          'metadata':metadata,
          'DAT':'http://192.168.116.131:5000/data_object'
        }

  # the public lkeys are too long to sign
  # signatureK_O = privKey.sign(ownerPubKey.exportKey('PEM'),32)
  # signatureK_R = privKey.sign(requesterPubKey.exportKey('PEM'),32)
  # print(len(ownerPubKey.exportKey('PEM')))
  # print(pubKey.verify(requesterPubKey.exportKey('PEM'), signatureK_R))
  msg5 = {
    'DOT':DOT,
    'sourcePublicKey':pubKey.exportKey('PEM').decode()
  }
  
  jsonMsg5 = json.dumps(msg5)
  encryptedJsonMsg5 = ownerAESObj.encrypt(jsonMsg5)
  encryptedAESKey = ownerPubKey.encrypt(ownerAESObj.getKey(), 32)

  msgPkt =  {
              'payload': encryptedJsonMsg5.decode(),
              'AESKey':base64.encodestring(encryptedAESKey[0]).decode(),
              'type':5
            }

  jsonMsgPkt = json.dumps(msgPkt)
  post('http://192.168.71.130:5000/tasks',jsonMsgPkt)

  # print(jsonMsgPkt)
  # post('http://192.168.71.130:5000/tasks',msg2JsonPkt)
  # owner_server_post('https://35.167.25.135:5000/dmp', jsonMsgPkt)

# app = Flask(__name__) # create an instance of the Flask class

# @app.route('/tasks', methods=['GET','POST'])
# def get_tasks():
#     if (request.method == 'GET'):
#         return jsonify({'tasks': tasks})
#     elif (request.method == 'POST'):
#         data = request.data
#         print data
#         return 'POST'

# if __name__ == '__main__':
#     app.run(host='0.0.0.0')

# generateKeyPair()
ownerAESObj = AESCipher('data_source')
# ownerAESObj.saveKeyToFile()
send_msg5()
# send_msg5()

# jasonMsg1 = json.dumps({'msg1':msg1})

# cryptedMsg1 = rsa.encrypt(jasonMsg1, pubKey)
# print(cryptedMsg1)

# fileFormatePublicKey = pubKey.save_pkcs1(format='PEM')
# data = {'public key':fileFormatePublicKey}
# post('http://192.168.116.131:5000/tasks', data)
# get('http://192.168.116.131:5000/tasks')
