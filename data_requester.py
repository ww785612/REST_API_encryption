# importing the requests library
# cloud IP address 35.167.25.135
from flask import Flask, request, jsonify
import requests
import json
import rsa
import bson
import os
import base64

from requests.adapters import HTTPAdapter
from requests.packages.urllib3.poolmanager import PoolManager

def genRSAKeyPair():
    (pubKey,privKey) = rsa.newkeys(512)
    with open("data_requester_public_key.pem","w+") as pubKeyFile:
        pubKeyFile.write(pubKey.save_pkcs1(format='PEM'))
    with open("data_requester_private_key.pem","w+") as privKeyFile:
        privKeyFile.write(privKey.save_pkcs1(format='PEM'))

def loadPublicKey():
    with open("data_requester_public_key.pem","rb") as pubKeyFile:
        rawKey = pubKeyFile.read()
        pubKey = rsa.PublicKey.load_pkcs1(rawKey)
    return pubKey

def loadPrivateKey():
    with open("data_requester_private_key.pem","rb") as privKeyFile:
        rawKey = privKeyFile.read()
        privKey = rsa.PrivateKey.load_pkcs1(rawKey)
    return privKey

def loadOwnerPublicKey():
    with open("owner_public_key.pem","rb") as pubKeyFile:
        rawKey = pubKeyFile.read()
        pubKey = rsa.PublicKey.load_pkcs1(rawKey)
    return pubKey

def loadOwnerPrivateKey():
    with open("owner_private_key.pem","rb") as privKeyFile:
        rawKey = privKeyFile.read()
        privKey = rsa.PrivateKey.load_pkcs1(rawKey)
    return privKey

def getOwnerSignature():
    pubKey = loadPublicKey()
    sPubKey = pubKey.save_pkcs1(format='PEM')
    ownerPrivateKey = loadOwnerPrivateKey()
    signature = rsa.sign(sPubKey, privKey, 'SHA-1')
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
  # defining the api-endpoint 
  API_ENDPOINT = url
  # binaryMsgPkt = bson.dumps(data)
  # data to be sent to api
  # data = {key:value}
  certFile = 'owner_server_https.pem'
  kwargs = dict(verify = certFile) if os.path.exists(certFile) else{}
  # sending post request and saving response as response object
  r = requests.post(url = API_ENDPOINT, data = msgPkt, **kwargs)

def send_msg2():
  pubKey = loadPublicKey()
  privKey = loadPrivateKey()
  metadata = {
    'deviceSummary ID':1,
    'access start date':'12/5/2017',
    'access end date':'12/5/2017'
  }

  duration = {
    'start':'12/5/2017',
    'end':'12/5/2017'
  }

  RT = {
  'name':'Anti-intruder app',
  'request ID':4,
  'metadata':metadata,
  'duration':duration,
  'requester public key':base64.encodestring(pubKey.save_pkcs1(format='PEM')).decode()
  }

  msg2 = {'RT':RT,
          'type':2}
  jsonMsgPkt = json.dumps(msg2)
  owner_server_post('https://35.167.25.135:5000/dmp', jsonMsgPkt)
  # post('http://192.168.71.128:5000/tasks',jsonMsgPkt)
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

# genRSAKeyPair()
send_msg2()

# jasonMsg1 = json.dumps({'msg1':msg1})

# cryptedMsg1 = rsa.encrypt(jasonMsg1, pubKey)
# print(cryptedMsg1)

# fileFormatePublicKey = pubKey.save_pkcs1(format='PEM')
# data = {'public key':fileFormatePublicKey}
# post('http://192.168.116.131:5000/tasks', data)
# get('http://192.168.116.131:5000/tasks')
