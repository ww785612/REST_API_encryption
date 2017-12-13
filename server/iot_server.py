from flask import Flask, request
from Crypto.Cipher import AES
from Crypto.PublicKey import RSA
import json
import copy
from flaskext.mysql import MySQL

mysql = MySQL()

with open("/home/ubuntu/server/server/db/db.json", "r") as json_data:
    json_db = json.load(json_data)
    json_data.close()

def parser(m):
    mtype = m['type']

    if mtype == 1:
        step_one(m['payload'])
    elif mtype == 2: #emulating publisher-messenger protocol
        step_two(m['payload'])
    elif mtype == 4:
        step_four(m['payload'])
    elif mtype == 5:
        step_five(m['payload'])
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
    columnNames = ["dataSource", "deniedDataRequest", "device", "deviceSummary", "grantedDataRequest", "pendingDataRequest", "requester"]
    rowNames = [["name", "src_ID"],["ID", "accessEndDate", "accessStartDate", "deviceSummaryID", "requesterID"]]

    cursor = mysql.connect().cursor()
    for c in columnNames:
        cursor.execute("SELECT * FROM "+ c)
        data = cursor.fetchall()
        output[c] = data

    return json.dumps(output)
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

@app.route('/notify', methods=['GET','POST'])
def tell():
    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        print temp
        username = temp['username']
        password = temp['password']
        if auth(username, password) is True:
            print "log in successful"
            return db_to_json()
            #return json.dumps(json_db)
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
            for i in json_db[temp["type"]]:
                if i["ID"] == r_id:
                    item = i
            new_one = copy.deepcopy(item)
            if policy == "accept":
                json_db["grantedDataRequest"].append(new_one)
                json_db[temp["type"]].remove(item)
            else:
                json_db["deniedDataRequest"].append(new_one)
                json_db[temp["type"]].remove(item)
            with open("db.json", "w") as jsonFile:
                json.dump(json_db, jsonFile)
                jsonFile.close()
        else:
            return "authentication failed"
            
    return "invalid method"
#enddef

@app.route('/dmp', methods=['GET','POST'])
def receive_message():
    if (request.method == 'POST'):
        data = request.data
        print data
        return "success"

    return "invalid method"
#enddef

if __name__ == '__main__':
    app.run()
    #app.run(host='0.0.0.0')
