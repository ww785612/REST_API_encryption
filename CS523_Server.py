#!/usr/bin/env python
from flask import Flask, request
import json
import rsa
import base64

json_db = {}

def genRSAKeyPair():
    (pubKey,privKey) = rsa.newkeys(4096)
    with open("publicKey.pem","w+") as pubKeyFile:
        pubKeyFile.write(pubKey.save_pkcs1(format='PEM'))
    with open("privateKey.pem","w+") as privKeyFile:
        privKeyFile.write(privKey.save_pkcs1(format='PEM'))
#enddef

def loadPublicKey(pubk):
    with open(pubk,"rb") as pubKeyFile:
        rawKey = pubKeyFile.read()
        pubKey = rsa.PublicKey.load_pkcs1(rawKey)
    return pubKey
#enddef

def loadPrivateKey(prik):
    with open(prik,"rb") as privKeyFile:
        rawKey = privKeyFile.read()
        privKey = rsa.PrivateKey.load_pkcs1(rawKey)
    return privKey
#enddef

def parser(m):
    mtype = m['type']

    if mtype == 1:
        step_one(m['payload'])
    elif mtype == 2: #emulating publisher-messenger protocol
        step_two(m['payload'])
    elif mtype == 4:
        step_four(m['payload'])
    elif mtype == 5:
        step_five(m['payload'])
#enddef

def step_one(m):
    #decrypt message with my private key
    pubKey = loadPublicKey("hb_keys/publicKey.pem")
    privKey = loadPrivateKey("hb_keys/privateKey.pem")

    decrypted = rsa.decrypt(base64.decodestring(m),privKey)
    


    #verify source's pubkey with my public key
    K_O = base64.decodestring(decrypted['K_O'])
    sig = base64.decodestring(decrypted['user_signed_source_public_key'])
    rsa.verify(K_O,sig,pubKey)
    
    src_key = rsa.PublicKey.load_pkcs1(K_O)
    
    #verify DOT with source's pubkey
    rsa.verify(decrypted['DOT'],decrypted['DOT_sig'],src_key)

    dot = m["DOT"]
    json_db[m['Data_ID']] = json.loads(dot['metadata'])
#enddef

def step_two(m):
    #verify message with requester's public key
    req_key = rsa.PublicKey.load_pkcs1(m['K_R'])
    try:
        rsa.verify(m['lhs'],m['lhs_hash'],req_key)
    except VerificationError:
        print "request signature does not match"
        return

    #TODO: compare two keys
    if m['lhs']['K_R'] != m['K_R']:
        print "key K_R does not match"
        return

    #verify RT and feedback using K_E1
    
    e_key = rsa.PublicKey.load_pkcs1(m['lhs']['K_E1'])
    try:
        rsa.verify(m['lhs']['RT_and_feedback'],m['hash'])
    except VerificationError:
        print "verification error!"
        return

    RT = req_key.decrypt(r_and_f['lhs']['RT_and_feedback']['RT'])

    #TODO: see if request fits with existing policy
    
    json_db[RT['Request_ID']] = RT
#enddef

def step_five(m):
    #decrypt using K_O3
    pubKey = loadPublicKey("hb_keys/publicKey3.pem")
    privKey = loadPrivateKey("hb_keys/privateKey3.pem")
    result = rsa.decrypt(m,privKey)
    result['DOT'][metadata]

    #TODO: check if this matches with what I did
    
    return 5
#enddef

app = Flask(__name__) # create an instance of the Flask class

@app.route('/notify', methods=['POST'])
def tell():
    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        print temp
        if temp['username'] == 'Aravind' and temp['password'] == 'Sagar':
            print "log in successful"
            return json.dumps(json_db)
#enddef

@app.route('/actions', methods=['POST'])
def listen():
    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        if (temp['username'] == 'Aravind' and temp['password'] == 'Sagar'):
            print "log in successful"
            policy = json.loads(temp['actions'])
            for a in policy:
                
                return json.dumps(json_db)

@app.route('/dmp', methods=['POST'])
def receive_message():
    if (request.method == 'POST'):
        print request
        session = request.form
        print json.dumps(session)
        #print json.loads(list(session)[0])
        #message = json.loads(data)
        #print message
        #parser(message)
        #src_addr = request.remote_addr
        return 'POST'
#enddef

if __name__ == '__main__':
    
    app.run(host='0.0.0.0', ssl_context=('cert.pem','key.pem'))
