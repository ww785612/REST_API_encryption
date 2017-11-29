# importing the requests library
import requests
import json
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
def post(url, data):
  # defining the api-endpoint 
  API_ENDPOINT = url

  # data to be sent to api
  # data = {key:value}
   
  # sending post request and saving response as response object
  r = requests.post(url = API_ENDPOINT, data = json.dumps(data))
pubKey = loadPublicKey()
fileFormatePublicKey = pubKey.save_pkcs1(format='PEM')
data = {'public key':fileFormatePublicKey}
post('http://192.168.116.131:5000/tasks', data)
get('http://192.168.116.131:5000/tasks')
