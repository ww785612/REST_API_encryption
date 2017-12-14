def parser(mtype,mpayload):
    if mtype == 1:
        step_one(mpayload)
    elif mtype == 2: #emulating publisher-messenger protocol
        step_two(mpayload)
    elif mtype == 4:
        step_four(mpayload)
    elif mtype == 5:
        step_five(mpayload)
    else:
        return "invalid message type"
#enddef

def step_one(m):
    #decrypt message with my private key
    
    #verify source's pubkey with my public key
    
    #verify DOT with source's pubkey
    return 0
#enddef

def step_two(m):
    #verify message with requester's public key

    #TODO: compare two keys

    #verify RT and feedback using K_E1
    
    #TODO: see if request fits with existing policy
 
    return 0
#enddef

def step_four(m):
    return 0

def step_five(m):
    #decrypt using K_O3

    #TODO: check if this matches with what I did
    
    return 0
#enddef