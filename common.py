import config
import hashlib
import time


def authenticate(uid, ip, x_auth_token):
    if config.debugging:
        print("WARNING: DEBUGGING MODE IS ON!")
        return True
    connection = config.database.cursor(dictionary=True)
    connection.execute("SELECT * FROM "+config.gatewaytable+" WHERE uid = "+str(uid)+";")
    results = connection.fetchall()
    if len(results) < 1:
        print("No Matching UID")
        return False
    for result in results:
        # Try to match source IP
        if result['ip'] == ip:
            print("IP Match")
            # Try to match x-auth-token hashed with unix time (for the last 10 seconds)
            unixtime = int(time.time())
            for i in range(unixtime-config.token_timeout, unixtime+config.token_timeout):
                print("Trying: "+str(hashlib.sha512(result['x-auth-base']+str(i)).hexdigest()).upper()+" vs "+str(x_auth_token))
                if str(hashlib.sha512(result['x-auth-base']+str(i)).hexdigest()).upper() == str(x_auth_token):
                    print("MATCH FOUND!")
                    return True
    print("Not authorized")
    return False


def psk_lookup(uid, psk):
    connection = config.database.cursor(dictionary=True)
    connection.execute("SELECT * FROM "+config.devicetable+" WHERE token = '"+str(psk)+"' AND uid = "+str(uid)+";")
    return connection.fetchall()


def dev_lookup(uid, id):
    connection = config.database.cursor(dictionary=True)
    connection.execute("SELECT * FROM "+config.devicetable+" WHERE id = " + str(id) + " AND uid = " + str(uid) + ";")
    return connection.fetchall()


def update_mac(id, mac):
    connection = config.database.cursor(dictionary=True)
    connection.execute("UPDATE "+config.devicetable+" SET macadd = '"+mac+"' WHERE id = "+str(id)+";")
    config.database.commit()
    return True


def update_ip(uid, old_ip, ip):
    connection = config.database.cursor(dictionary=True)
    connection.execute("UPDATE "+config.gatewaytable+" SET ip = "+ip+" WHERE uid = "+uid+" AND ip = "+old_ip+";")
    config.database.commit()
    return True
