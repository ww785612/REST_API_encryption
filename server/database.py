from flaskext.mysql import MySQL

def auth(mysql, u,p):
    cursor = mysql.connect().cursor()
    cursor.execute("SELECT * from creds where username = %s and password = %s", [u,p])
    data = cursor.fetchone()
    if data is None:
        return False
    else:
        return True
#enddef

def db_to_json(mysql):
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

def handle_order(mysql, t_name, r_id, policy):
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