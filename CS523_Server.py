#!/usr/bin/env python
from flask import Flask, request, json
import rsa


def genRSAKeyPair():
    (pubKey,privKey) = rsa.newkeys(512)
    with open("publicKey.pem","w+") as pubKeyFile:
        pubKeyFile.write(pubKey.save_pkcs1(format='PEM'))
    with open("privateKey.pem","w+") as privKeyFile:
        privKeyFile.write(privKey.save_pkcs1(format='PEM'))
#enddef

def loadPublicKey():
    with open("publicKey.pem","rb") as pubKeyFile:
        rawKey = pubKeyFile.read()
        pubKey = rsa.PublicKey.load_pkcs1(rawKey)
    return pubKey
#enddef

def loadPrivateKey():
    with open("privateKey.pem","rb") as privKeyFile:
        rawKey = privKeyFile.read()
        privKey = rsa.PrivateKey.load_pkcs1(rawKey)
    return privKey
#enddef

def parser(m):
    mtype = m['type']

    if mtype == 1:
        step_one(m['message'])
    elif mtype == 2: #emulating publisher-messenger protocol
        step_two(m['message'])
    elif mtype == 4:
        step_four(m['message'])
    elif mtype == 5:
        step_five(m['message'])
    else:
        print '?'
#enddef

def step_one(m):
    #decrypt message with my private key
    pubKey = loadPublicKey()
    privKey = loadPrivateKey()
    decrypted = privKey.decrypt(m)
    dec_m = json.loads(decrypted)      

    #decrypt source's pubkey with my public key
    src_key_string = pubKey.decrypt(dec_m['K_O'])
    src_key = rsa.PublicKey.load_pkcs1(source_key)
    
    #decrypt DOT with source's pubkey
    dot = src_key.decrypt(dec_m['DOT'])

    #TODO: parse dot

    #TODO: send notification to app

    #TODO: store this DOT (id, owner's pubkey, metadata, DAP) DAP has url, contact info, instructions, physical location
    return 1
#enddef

def step_two(m):
    #decrypt message with requester's public key
    req_key = rsa.PublicKey.load_pkcs1(m['K_R'])
    decrypted = req_key.decrypt(m['request'])
    
    #TODO: compare two keys
    req_key_v = decrypted['K_R']

    #decrypt RT using K_E1
    my_key = rsa.PublicKey.load_pkcs1(decrypted['K_E1'])
    r_and_f = my_key.decrypt(decrypted['RT_and_feedback'])
    RT = req_key.decrypt(r_and_f['RT'])

    #TODO: see if request fits with existing policy
    #TODO: if so, process it
    
    #TODO: if not, ask app


    return 2
#enddef

def step_five(m):
    #decrypt using K_3O
    pubKey = loadPublicKey()
    privKey = loadPrivateKey()
    result = privKey.decrypt(m)

    #check if this matches with what I did
    
    return 5
#enddef

app = Flask(__name__) # create an instance of the Flask class

@app.route('/inner', methods=['POST'])
def listen():
    if (request.method == 'POST'):
        data = request.data
        message = json.loads(data)
#enddef

@app.route('/outer', methods=['POST'])
def receive_message():
    if (request.method == 'POST'):
        data = request.data
        message = json.loads(data)
        print message
        parser(message)
        src_addr = request.remote_addr
        return 'POST'
#enddef

if __name__ == '__main__':
    #TODO: build sql db
    app.run(host='0.0.0.0')
