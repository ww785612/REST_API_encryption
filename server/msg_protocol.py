from flask import Flask, request, jsonify
import requests
import json
import os
import Crypto
from Crypto.PublicKey import RSA
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

from flaskext.mysql import MySQL
from database import register_request, register_do, verify_request

class AESCipher(object):
    """
    implementation of this class is based on:
    https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256
    """

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

def loadOwnerPrivateKey():
    privKeyFile = open("/home/ubuntu/server/server/hb_keys/privateKey.pem",'r')
    strPrivKey = privKeyFile.read()
    loadedPrivKey = RSA.importKey(strPrivKey)
    privKeyFile.close()
    return loadedPrivKey

def loadOwnerPrivateKey3():
    privKeyFile = open("/home/ubuntu/server/server/hb_keys/privateKey3.pem",'r')
    strPrivKey = privKeyFile.read()
    loadedPrivKey = RSA.importKey(strPrivKey)
    privKeyFile.close()
    return loadedPrivKey

def loadOwnerPublicKey():
    pubKeyFile = open("/home/ubuntu/server/server/hb_keys/publicKey.pem",'r')
    strPubKey = pubKeyFile.read()
    loadedPubKey =  RSA.importKey(strPubKey)
    pubKeyFile.close()
    return loadedPubKey

def generateKeyPair():
    key = RSA.generate(2048) #generate pub and priv key
    with open("/home/ubuntu/server/server/hb_keys/privateKey.pem",'w') as file:
        file.write(key.exportKey('PEM').decode())
    publickey = key.publickey() # pub key export for exchange
    with open("/home/ubuntu/server/server/hb_keys/publicKey.pem",'w') as file:
        file.write(publickey.exportKey('PEM').decode())


def loadPublicKey(strPubKey):
    loadedPubKey =  RSA.importKey(strPubKey)
    return loadedPubKey


def parser(mysql, data):
    """
    parse message type and run helper function to perform related task

    @param mysql:       a mysql object for MySQL database
    @param data:        message payload
    """

    data = request.data.decode()
    msgPkt = json.loads(data)
    
    
    if(msgPkt['type'] == 1):
        encryptedAESKey = base64.decodestring(msgPkt['AESKey'].encode('utf-8'))
        ownerPrivKey = loadOwnerPrivateKey()
        AESKey = ownerPrivKey.decrypt(encryptedAESKey)
        ownerAESObj = AESCipher('data_owner')
        ownerAESObj.updateKey(AESKey)
        encryptedJsonMsg = msgPkt['payload'].encode('utf-8')
        jsonMsg = ownerAESObj.decrypt(encryptedJsonMsg)
        msg = json.loads(jsonMsg)
        step_one(mysql,msg)
    elif(msgPkt['type'] == 2):
        #verify message with requester's public key
        signatureRTName = msg['signature']
        RT = msg['RT']
        requesterPubKeyStr = base64.decodestring(RT['requesterPublicKey'].encode())
        requesterPubKey = loadPublicKey(requesterPubKeyStr)
        name = RT['name']
        if requesterPubKey.verify(name.encode(), signatureRTName) is False:
            return "verification failed for message 2"
        print(requesterPubKey)
        step_two(mysql, msg)
    elif(msgPkt['type'] == 5):
        #decrypt using K_O3
        encryptedAESKey = base64.decodestring(msgPkt['AESKey'].encode('utf-8'))
        ownerPrivKey = loadOwnerPrivateKey3()
        AESKey = ownerPrivKey.decrypt(encryptedAESKey)
        ownerAESObj = AESCipher('data_owner')
        ownerAESObj.updateKey(AESKey)
        encryptedJsonMsg = msgPkt['payload'].encode('utf-8')
        jsonMsg = ownerAESObj.decrypt(encryptedJsonMsg)
        msg = json.loads(jsonMsg)
        step_five(mysql, msg)
    else:
        return "invalid message type"
#enddef

def step_one(mysql,m):
    """
    function to do tasks for message 1 in Data Management Protocol (DMP)

    @param mysql:   a mysql object for MySQL database
    @param m:       message payload    
    """
    
    owner_sk = loadOwnerPrivateKey()
    if(owner_sk.sign(m['sourcePubKey']) != m['ownerSignedSourcePubKey'])
        return "source key verification failed"
    dot = m['DOT']

    device = dict()
    deviceSummary = dict()
    json = dict()

    device["ID"] = m['metadata']['ID']
    device["dataSize"] = m['metadata']["dataSize"]
    device["location"] = m['device']['location']
    device["name"] =  m['device']['name']
    device["srcID"] = m['DOT']['dataSourceID']
    device["type"] = m['device']['type']
    
    deviceSummary["ID"] = m['metadata']['device_summary_ID']
    deviceSummary["accessDuration"] = m['deviceSummary']['access duration']
    deviceSummary["deviceID"] = device["ID"]

    json["device"] = device
    json["deviceSummary"] = deviceSummary
    
    return register_do(mysql, json)
#enddef

def step_two(mysql,m):
    """
    function to do tasks for message 2 in Messaging Service
    Note: verification happened before this step


    @param mysql:   a mysql object for MySQL database
    @param m:       message payload  
    """

    requester = dict()
    pendingDataRequest = dict()
    json = dict()

    requester["ID"] = m['RT']['requesterID']
    requester["name"] = m['RT']['name']
    requester["publicKey"] = m['RT']['requesterPublicKey']

    pendingDataRequest["ID"] = m['RT']['requestID'] 
    pendingDataRequest["accessEndDate"] = m['RT']['duration']['end']
    pendingDataRequest["accessStartDate"] = m['RT']['duration']['start']
    pendingDataRequest["deviceSummaryID"] = m['RT']['metadata']['deviceSummaryID']
    pendingDataRequest["requesterID"] = requester["ID"]

    json['requester'] = requester
    json['pendingDataRequest'] = pendingDataRequest 

    return register_request(mysql, json)
#enddef

def step_five(mysql,m):
    """
    function to do tasks for message 5 in DMP

    @param mysql:   a mysql object for MySQL database
    @param m:       message payload
    """
    requestID = m['query']['queryID']

    #check if this matches with what I did
    if verify_request(mysql, requestID):
        return "verification success"
    else:
        return "verification failed!"
#enddef