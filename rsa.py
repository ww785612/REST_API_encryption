import rsa

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

genRSAKeyPair()
pubKey = loadPublicKey()
privKey = loadPrivateKey()

message = "hello"
cryptedPkt = rsa.encrypt(message, pubKey)
print(cryptedPkt)
decryptedMsg = rsa.decrypt(cryptedPkt, privKey)
print(decryptedMsg)

signature = rsa.sign(message, privKey, 'SHA-1')
verificationResult = rsa.verify(message, signature, pubKey) # should be true
if(verificationResult):
    print("verification success")
else:
    print("verification failed")
