import mysql.connector

# Debug mode
debugging = True

# Seconds a token is valid for
token_timeout = 20

# Initialize connection to database
database = mysql.connector.connect(
    host="localhost",
    user="root",
    passwd="password",
    database="telus"
)

# Define various database table name
usertable = "loginInfo"
routertable = "routerTable"
subnettable = "subnetTable"
porttable = "portTable"
devicetable = "deviceTable"
gatewaytable = "gateways"
