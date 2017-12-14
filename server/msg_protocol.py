from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from flaskext.mysql import MySQL

from database import register_request, register_do, verify_request

def parser(mysql,mtype,mpayload):
    if mtype == 1:
        return step_one(mysql,mpayload)
    elif mtype == 2: #emulating publisher-messenger protocol
        return step_two(mysql,mpayload)
    elif mtype == 5:
        return step_five(mysql,mpayload)
    else:
        return "invalid message type"
#enddef

def step_one(mysql,m):
    #decrypt message with my private key
    
    #verify source's pubkey with my public key
    
    #verify DOT with source's pubkey
    return 0
#enddef

def step_two(mysql,m):
    #verify message with requester's public key

    #TODO: compare two keys

    #verify RT and feedback using K_E1
    
    #TODO: see if request fits with existing policy
 
    return 0
#enddef

def step_five(mysql,m):
    #decrypt using K_O3

    #TODO: check if this matches with what I did
    if verify_request(mysql, json):
        return True
    else:
        return False
#enddef
