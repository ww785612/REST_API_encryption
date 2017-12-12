#!/usr/bin/env python
from flask import Flask, request
import json
import rsa
import base64
import copy

with open("db.json", "r") as json_data:
    json_db = json.load(json_data)
    json_data.close()

with open("auth.json", "r") as auth_data:
    auth_db = json.load(auth_data)
    json_data.close()

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
    else:
        return "invalid message type"
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
    return

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

def auth(u,p):
    for i in auth_db["creds"]:
        if i["username"] == u and i["password"] == p:
            return true
    
    return false
#enddef

app = Flask(__name__) # create an instance of the Flask class

@app.route('/')
def hello():
    return 'hello world!'

@app.route('/notify')
def tell():
    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        print temp
        username = temp['username']
        password = temp['password']
        if auth(username, password) is true:
            print "log in successful"
            return json.dumps(json_db)
        else:
            return "authentication failed"

    return "invalid method"
#enddef

@app.route('/actions')
def listen():
    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        username = temp['username']
        password = temp['password']
        if auth(username,password) is true:
            print "log in successful"
            policy = temp['action']
            r_id = temp['request_id']
            for i in json_db[temp["type"]]:
                if i["ID"] == r_id:
                    item = i
            new_one = copy.deepcopy(item)
            if policy == "accept":
                json_db["grantedDataRequest"].append(new_one)
                json_db[temp["type"]].remove(item)
            else:
                json_db["deniedDataRequest"].append(new_one)
                json_db[temp["type"]].remove(item)
            with open("db.json", "w") as jsonFile:
                json.dump(json_db, jsonFile)
                jsonFile.close()
        else:
            return "authentication failed"
            
    return "invalid method"
#enddef

@app.route('/dmp')
def receive_message():
    if (request.method == 'POST'):
        print request.form
        for i in request.form:
            print i

    return "invalid method"
#enddef

if __name__ == '__main__':
    app.run(host='0.0.0.0', ssl_context=('cert.pem','key.pem'))
