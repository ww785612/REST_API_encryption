from flask import Flask, request
from flaskext.mysql import MySQL
import json

from database import auth, db_to_json, handle_order
from msg_protocol import parser

app = Flask(__name__) # create an instance of the Flask class

#configuation of MySQL
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Sagar'
app.config['MYSQL_DATABASE_DB'] = 'iot_server'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql = MySQL()
mysql.init_app(app)

@app.route('/pk', methods=['GET','POST']) #/pk interface
def give_pk():
    """
    interface that application interacts to retrive the public key
    """
    with open("/home/ubuntu/server/server/hb_keys/publicKey.pem", "r") as pubKeyFile:
        rawKey = pubKeyFile.read()

    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        username = temp['username']
        password = temp['password']
        if auth(mysql, username, password) is True: #check username,password
            return rawKey
        else:
            return "authentication failed"

    return "invalid method"
#enddef

@app.route('/notify', methods=['GET','POST'])
def tell():
    """
    interface that application interacts to receive recent updates
    """
    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        username = temp['username']
        password = temp['password']
        if auth(mysql, username, password) is True: #check username,password
            return db_to_json(mysql)
        else:
            return "authentication failed"

    return "invalid method"
#enddef

@app.route('/actions', methods=['GET','POST'])
def listen():
    """
    interface that application interacts to enforce a policy for each data request
    """

    if (request.method == 'POST'):
        session = request.form
        temp = json.loads(list(session)[0])
        username = temp['username']
        password = temp['password']
        if auth(mysql, username, password) is True:
            print "log in successful"
            policy = temp['action']
            r_id = temp['request_id']
            prior = temp['type']
            return handle_order(mysql, prior, r_id, policy)
        else:
            return "authentication failed"
            
    return "invalid method"
#enddef

@app.route('/dmp', methods=['GET','POST'])
def receive_message():
    """
    interface that data source and data requester uses to send messages
    """

    if (request.method == 'POST'):
        data = request.data
        return parser(mysql, data)

    return "invalid method"
#enddef

if __name__ == '__main__':
    app.run()

    #comment line above and uncomment line below if you run this code with HTTPS and without Apache

    #app.run(host='0.0.0.0', ssl_context=('cert/cert.pem','cert/key.pem'))