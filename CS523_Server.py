#!/usr/bin/env python
from flask import Flask, request, jsonify


def genRSAKeyPair():
    (pubKey,privKey) = rsa.newkeys(512)
    with open("publicKey.pem","w+") as pubKeyFile:
        pubKeyFile.write(pubKey.save_pkcs1(format='PEM'))
    with open("privateKey.pem","w+") as privKeyFile:
        privKeyFile.write(privKey.save_pkcs1(format='PEM'))

def loadPublicKey()
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

@app.route('/tasks', methods=['GET','POST']) # route() decorator is used to bind a function to a URL. in this case, the function is triggered with URL:http//127.0.0.1:5000/tasks
def get_tasks():
    if (request.method == 'GET'):
        return jsonify({'tasks': tasks}) #returns the message we want to display in the user’s browser.
    elif (request.method == 'POST'):
        data = request.data
        print data
        return 'POST'

if __name__ == '__main__':
    app.run(debug=True)


# request.data Contains the incoming request data as string in case it came with a mimetype Flask does not handle.
# request.args: the key/value pairs in the URL query string
# request.form: the key/value pairs in the body, from a HTML post form, or JavaScript request that is not JSON encoded
# request.files: the files in the body, which Flask keeps separate from form. HTML forms must use enctype=multipart/form-data or files will not be uploaded.
# request.values: combined args and form, preferring args if keys overlap

test the server: curl -H "Content-type: application/json" -X POST http://127.0.0.1:5000/messages -d '{"message":"Hello Data"}'
# When sending data via a POST or PUT request, two common formats (specified via the Content-Type header) are:
#application/json
#application/x-www-form-urlencoded