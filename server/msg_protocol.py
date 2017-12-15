from Crypto.Cipher import AES
from Crypto.PublicKey import RSA

from flaskext.mysql import MySQL
from database import register_request, register_do, verify_request

def parser(mysql,mtype,mpayload):
    """
    parse message type and run helper function to perform related task

    @param mysql:       a mysql object for MySQL database
    @param mtype:       message type (specified by the Data Management Protocol)
    @param mpayload:    message payload
    """

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
    """
    function to do tasks for message 1 in Data Management Protocol (DMP)

    @param mysql:   a mysql object for MySQL database
    @param m:       message payload    
    """


    #decrypt message with my private key
    with open("/home/ubuntu/server/server/hb_keys/privateKey.pem", "r") as pubKeyFile:
        rawKey = pubKeyFile.read()
    sk = RSA.importKey(rawKey)
    sk.decrypt()
    
    #verify source's pubkey with my public key
    
    #verify DOT with source's pubkey
    return 0
#enddef

def step_two(mysql,m):
    """
    function to do tasks for message 2 in Messaging Service

    @param mysql:   a mysql object for MySQL database
    @param m:       message payload  
    """

    #verify message with requester's public key

    #TODO: compare two keys

    #verify RT and feedback using K_E1
    
    #TODO: see if request fits with existing policy
 
    return 0
#enddef

def step_five(mysql,m):
    """
    function to do tasks for message 5 in DMP

    @param mysql:   a mysql object for MySQL database
    @param m:       message payload
    """

    #decrypt using K_O3

    #TODO: check if this matches with what I did
    if verify_request(mysql, json):
        return True
    else:
        return False
#enddef