import rsa

def genRSAKeyPair(a,b):
    (pubKey,privKey) = rsa.newkeys(4096)
    with open(a,"w+") as pubKeyFile:
        pubKeyFile.write(pubKey.save_pkcs1(format='PEM'))
    with open(b,"w+") as privKeyFile:
        privKeyFile.write(privKey.save_pkcs1(format='PEM'))


genRSAKeyPair("publicKey.pem","privateKey.pem")
genRSAKeyPair("publicKey2.pem","privateKey2.pem")
genRSAKeyPair("publicKey3.pem","privateKey3.pem")
