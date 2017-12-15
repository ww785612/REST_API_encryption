import json
from flaskext.mysql import MySQL

def auth(mysql,u,p):
    """
    authenticates user credentials

    @param mysql:   a mysql object for MySQL database
    @param u:       username
    @param p:       password
    """

    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from creds where username = %s and password = %s", [u,p])
    data = cursor.fetchone()
    if data is None:
        return False
    else:
        return True
#enddef

def db_to_json(mysql):
    """
    grabs all entries in database and jsonify the data

    @param mysql:   a mysql object for MySQL database
    """

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
    for i in range(0,t_length): #for each table
        t = tableNames[i]
        cursor.execute("SELECT * FROM "+ t)
        data = cursor.fetchall()
        output[t] = []
        for r in data: #for each column
            one_col = dict()
            c_length = len(columnNames[i])
            for j in range(0,c_length):
                one_col[columnNames[i][j]] = r[j]
            output[t].append(one_col)

    return json.dumps(output)
#enddef

def handle_order(mysql, t_name, r_id, policy):
    """
    enforce policy from Data Owner by moving data request from one table to another

    @param mysql:   a mysql object for MySQL database
    @param t_name:  name of table
    @param r_id:    request ID
    @param policy:  accept/deny
    """

    cnx = mysql.connect()
    cursor = cnx.cursor()
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

def register_do(mysql, json):
    """
    helper function that registers data objects into MySQL DB

    @param mysql:   a mysql object for MySQL database
    @param json:    metadata that contains information for data source and device
    """

    cnx = mysql.connect()
    cursor = cnx.cursor()

    dataSource = json["dataSource"]
    device = json["device"]
    deviceSummary = json["deviceSummary"]

    dataSource_arr = [dataSource["name"], int(dataSource["srcID"])]
    
    device_arr = 
    [int(device["ID"]), 
    int(device["dataSize"]), 
    device["location"], 
    device["name"], 
    int(device["srcID"]), 
    device["type"]]
    
    deviceSummary_arr = 
    [int(deviceSummary["ID"]),
    deviceSummary["accessDuration"],
    int(deviceSummary["deviceID"])]
    
    cursor.execute("INSERT INTO dataSource (name, srcID) VALUES (%s, %d)", dataSource_arr)
    cursor.execute("INSERT INTO device (ID, dataSize, location, name, srcID, type) VALUES (%d, %d, %s, %s, %d, %s)", device_arr)
    cursor.execute("INSERT INTO deviceSummary (ID, accessDuration, deviceID) VALUES (%d, %s, %d)", deviceSummary_arr)
    cnx.commit()
    return "data object registration success"

def register_request(mysql, json):
    """
    helper function that registers data requests into MySQL DB

    @param mysql:   a mysql object for MySQL database
    @param json:    metadata that contains information for data request
    """

    cnx = mysql.connect()
    cursor = cnx.cursor()

    requester = json["requester"]
    pendingDataRequest = json["pendingDataRequest"]

    requester_arr = 
    [int(requester["ID"]),
    requester["name"],
    requester["publicKey"]]

    pendingDataRequest_arr = 
    [int(pendingDataRequest["ID"]),
    pendingDataRequest["accessEndDate"],
    pendingDataRequest["accessStartDate"],
    int(pendingDataRequest["deviceSummaryID"]),
    int(pendingDataRequest["requesterID"])
    ]

    cursor.execute("INSERT INTO requester (ID, name, publicKey) VALUES (%d,%s,%s)", requester_arr)
    cursor.execute("INSERT INTO pendingDataRequest (ID, accessEndDate, accessStartDate, deviceSummaryID, requesterID) VALUES (%d,%s,%s,%d,%d)", pendingDataRequest_arr)

    cnx.commit()

    return "request registration success"

def verify_request(mysql, requestID):
    """
    helper function that verifies granted data requests 

    @param mysql:       a mysql object for MySQL database
    @param requestID:   the request ID that you want to verify    
    """

    cnx = mysql.connect()
    cursor = cnx.cursor()

    cursor.execute("SELECT * FROM grantedDataRequest WHERE ID = %d", [requestID])
    data = cursor.fetchone()
    if data is None:
        return False
    else:
        return True