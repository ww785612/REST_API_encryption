#!/usr/bin/env python
from flask import Flask, request, jsonify
import rsa


def genRSAKeyPair():
    (pubKey,privKey) = rsa.newkeys(512)
    with open("publicKey.pem","w+") as pubKeyFile:
        pubKeyFile.write(pubKey.save_pkcs1(format='PEM'))
    with open("privateKey.pem","w+") as privKeyFile:
        privKeyFile.write(privKey.save_pkcs1(format='PEM'))

def loadPublicKey():
    with open("publicKey.pem","rb") as pubKeyFile:
        rawKey = pubKeyFile.read()
        pubKey = rsa.PublicKey.load_pkcs1(rawKey)
    return pubKey

def loadPrivateKey():
    with open("privateKey.pem","rb") as privKeyFile:
        rawKey = privKeyFile.read()
        privKey = rsa.PrivateKey.load_pkcs1(rawKey)
    return privKey

    
app = Flask(__name__) # create an instance of the Flask class

tasks = [
    {
        'id': 1,
        'title': u'Buy groceries',
        'description': u'Milk, Cheese, Pizza, Fruit, Tylenol',
        'done':False
    },
    {
          'id': 2,
          'title': u'Learn Python',
          'description': u'Need to find a good Python tutorial on the web',
          'done': False
    }
]

@app.route('/tasks', methods=['GET','POST'])
def get_tasks():
    if (request.method == 'GET'):
        return jsonify({'tasks': tasks})
    elif (request.method == 'POST'):
        data = request.data
        print data
        return 'POST'

if __name__ == '__main__':
    app.run(host='0.0.0.0')
