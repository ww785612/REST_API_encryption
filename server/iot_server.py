from flask import Flask, request
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import json
import copy
from flaskext.mysql import MySQL

mysql = MySQL()

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

def auth(u,p):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from creds where username = %s and password = %s", [u,p])
    data = cursor.fetchone()
    if data is None:
        return False
    else:
        return True
#enddef

def db_to_json():
    output = dict()
    tableNames = ["device", "deviceSummary", "deniedDataRequest", "grantedDataRequest", "pendingDataRequest", "requester", "dataSource"]
    columnNames = [["ID","dataSize","location","name","srcID","type"],
    ["ID","accessDuration","deviceID"],
    ["ID", "accessEndDate", "accessStartDate", "deviceSummaryID", "requesterID"],
    ["ID", "accessEndDate", "accessStartDate", "deviceSummaryID", "requesterID"],
    ["ID", "accessEndDate", "accessStartDate", "deviceSummaryID", "requesterID"],
    ["ID", "name", "publicKey"],
    ["name", "srcID"]]

    t_length = len(tableNames)
    cursor = mysql.connect().cursor()
    for i in range(0,t_length):
        t = tableNames[i]
        cursor.execute("SELECT * FROM "+ t)
        data = cursor.fetchall()
        output[t] = []
        for r in data:
            one_col = dict()
            c_length = len(columnNames[i])
            for j in range(0,c_length):
                one_col[columnNames[i][j]] = r[j]
            output[t].append(one_col)

    return json.dumps(output)
#enddef

def handle_order(t_name, r_id, policy):
    cnx = mysql.connect()
    cursor = cnx.cursor()
    print "t_name: "+t_name
    print "r_id: "+str(r_id)
    print "policy: "+policy
    cursor.execute("SELECT * FROM "+t_name+" WHERE ID = "+str(r_id))
    data = cursor.fetchone()
    if not data:
        return "wrong enforcement. no such request exists"
    if policy == "accept":
        cursor.execute("INSERT INTO grantedDataRequest SELECT * FROM "+t_name+" WHERE ID = "+str(r_id))
    else:
        cursor.execute("INSERT INTO deniedDataRequest SELECT * FROM "+t_name+" WHERE ID = "+str(r_id))
    
    cursor.execute("DELETE FROM "+t_name+" WHERE ID = "+str(r_id))
    cnx.commit()
    
    return "enforcement success"
#enddef


app = Flask(__name__) # create an instance of the Flask class

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Sagar'
app.config['MYSQL_DATABASE_DB'] = 'iot_server'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)

@app.route('/')
def hello():
    return 'hello world!'

@app.route('/pk', methods=['GET','POST'])
def give_pk():
    with open("/home/ubuntu/server/server/hb_keys/publicKey.pem", "r") as pubKeyFile:
        rawKey = pubKeyFile.read()

    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        username = temp['username']
        password = temp['password']
        if auth(username, password) is True:
            return rawKey
        else:
            return "authentication failed"

    return "invalid method"


@app.route('/notify', methods=['GET','POST'])
def tell():
    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        username = temp['username']
        password = temp['password']
        if auth(username, password) is True:
            return db_to_json()
        else:
            return "authentication failed"

    return "invalid method"
#enddef

@app.route('/actions', methods=['GET','POST'])
def listen():
    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        username = temp['username']
        password = temp['password']
        if auth(username,password) is True:
            print "log in successful"
            policy = temp['action']
            r_id = temp['request_id']
            prior = temp['type']
            return handle_order(prior, r_id, policy)
        else:
            return "authentication failed"
            
    return "invalid method"
#enddef

@app.route('/dmp', methods=['GET','POST'])
def receive_message():
    if (request.method == 'POST'):
        data = request.data
        message = json.loads(data)
        return parser(message['type'], message['payload'])

    return "invalid method"
#enddef

if __name__ == '__main__':
    app.run()
    #app.run(host='0.0.0.0', ssl_context=('cert/cert.pem','cert/key.pem'))
