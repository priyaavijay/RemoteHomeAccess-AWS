#importing libraries
import sqlite3
database_name='Details.db'
database_name_status="Status.db"
database_name_command="Command.db"
#creating necessary tables
def creating_table():
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    create_table_USERS="CREATE TABLE IF NOT EXISTS USERS (ID INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,USERNAME text,PASSWORD text,NAME text,EMAIL text)"
    create_table_ADMIN='CREATE TABLE IF NOT EXISTS [ADMIN] ([ID] INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,[USERNAME] TEXT,[ADMIN] TEXT  NOT NULL,FOREIGN KEY(USERNAME) REFERENCES USERS(USERNAME))'
    create_table_ROUTER_MAPPING='CREATE TABLE IF NOT EXISTS [ROUTER_MAPPING] ([ID] INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,[USERNAME] TEXT NOT NULL,[ROUTER_ID] INTEGER  NOT NULL,FOREIGN KEY(USERNAME) REFERENCES USERS(USERNAME))'
    create_table_USER_ADMIN_MAPPING='CREATE TABLE IF NOT EXISTS [USER_ADMIN_MAPPING] ([ID] INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,[USERNAME] TEXT NOT NULL,[ADMIN] TEXT,[ROUTER_ID] TEXT,[GROUP_ID] TEXT,[CONTROL] TEXT)'
    create_table_USER_ADMIN_KEY='CREATE TABLE IF NOT EXISTS [ADMIN_KEY] ([ID] INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,ADMINKEY text)'
    create_table_ROUTER_PASSWORD='CREATE TABLE IF NOT EXISTS [ROUTER_PASSWORD]([ID] INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,ROUTER_ID TEXT,PASSWORD TEXT)'
    cursor.execute(create_table_USERS)
    cursor.execute(create_table_ADMIN)
    cursor.execute(create_table_ROUTER_MAPPING)
    cursor.execute(create_table_USER_ADMIN_MAPPING)
    cursor.execute(create_table_USER_ADMIN_KEY)
    cursor.execute(create_table_ROUTER_PASSWORD)
    connection.commit()
    connection.close()

#deleting all tables
def deleting_table():
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    for i in {'USERS','ADMIN','ROUTER_MAPPING','ROUTER','USER_ADMIN_MAPPING'}:
        query='DROP TABLE '+i
        cursor.execute(query)
    connection.commit()
    connection.close()

#Start_USERS
#Table to store the username password email and name
#Case Non Sensitive
def insert_into_USERS(username,password,name,email):
    username=str(username).upper()
    password=str(password).upper()
    name=str(name).upper()
    email=str(email).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    insert_query = "INSERT INTO USERS (USERNAME,PASSWORD,NAME,EMAIL) VALUES (?,?,?,?)"
    cursor.execute(insert_query,(username,password,name,email))
    connection.commit()
    connection.close()

def content_USERS():
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query='SELECT * FROM users'
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def get_USERS(username):
    username=str(username).upper()
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT * FROM USERS WHERE USERNAME = '" + str(username) +"'"
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def get_USERS_id(id):
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT USERNAME FROM USERS WHERE ID = '" + str(id) +"'"
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    if(len(list_users)!=0):
        return(list_users[0])
    else:
        return 0

def del_user_USERS(username):
    username=str(username).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="DELETE FROM USERS WHERE USERNAME = '" + str(username) +"'"
    cursor.execute(query)
    connection.commit()
    connection.close()

def forgot_password(username,email,new_password):
    username=str(username).upper()
    email=str(email).upper()
    new_password=str(new_password).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    list_users=list()
    query="SELECT PASSWORD FROM USERS WHERE USERNAME = '"+str(username)+"' AND EMAIL = '"+str(email)+"'"
    for row in cursor.execute(query):
        list_users.append(row)
    if(len(list_users)==0):
        return 0
    query="UPDATE USERS SET PASSWORD = '"+new_password+"' WHERE USERNAME='"+str(username)+"' AND EMAIL = '"+str(email)+"'"
    cursor.execute(query)
    connection.commit()
    connection.close()
    return 1

#End_USERS

#Start_ADMIN
#Store if the user is just a normal one or a ADMIN
#Start_ADMIN
#Store if the user is just a normal one or a ADMIN
def insert_into_ADMIN(username,admin):
    username=str(username).upper()
    admin=str(admin).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    insert_query = "INSERT INTO ADMIN (USERNAME,ADMIN) VALUES (?,?)"
    cursor.execute(insert_query,(username,admin))
    connection.commit()
    connection.close()

def content_ADMIN():
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query='SELECT * FROM ADMIN'
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def del_user_ADMIN(username):
    username=str(username).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="DELETE FROM ADMIN WHERE USERNAME = '" + str(username) +"'"
    cursor.execute(query)
    connection.commit()
    connection.close()

def get_ADMIN_STATUS(username):
    username=str(username).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT ADMIN FROM ADMIN WHERE USERNAME = '" + str(username) +"'"
    list_users=list()
    for row in cursor.execute(query):
        list_users.append(row[0])
    connection.commit()
    connection.close()
    if(len(list_users)==0):
        return 0
    else:
        return list_users[0]

##END ADMIN
#Admin_Table

#ROUTER_MAPPING START

def insert_into_ROUTER_MAPPING(username,router_id):
    username=str(username).upper()
    router_id=str(router_id).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    insert_query = "INSERT INTO ROUTER_MAPPING(USERNAME,ROUTER_ID) VALUES (?,?)"
    cursor.execute(insert_query,(username,router_id))
    connection.commit()
    connection.close()

def content_ROUTER_MAPPING():
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query='SELECT * FROM ROUTER_MAPPING'
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def del_user_ROUTER_MAPPING_2(username,router_id):
    username=str(username).upper()
    router_id=str(router_id).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="DELETE FROM ROUTER_MAPPING WHERE USERNAME = '" + str(username) +"' AND ROUTER_ID='"+str(router_id)+"'"
    cursor.execute(query)
    connection.commit()
    connection.close()

def find_ROUTER_MAPPING_2(username,router_id):
    username=str(username).upper()
    router_id=str(router_id).upper()
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT * FROM ROUTER_MAPPING WHERE USERNAME = '" + str(username) +"' AND ROUTER_ID='"+str(router_id)+"'"
    for row in cursor.execute(query):
        list_users.append(row)
    if(len(list_users)==0):
        return 0
    else:
        return len(list_users)
    connection.commit()
    connection.close()

def del_user_ROUTER_MAPPING(username):
    username=str(username).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="DELETE FROM ROUTER_MAPPING WHERE USERNAME = '" + str(username) +"'"
    cursor.execute(query)
    connection.commit()
    connection.close()

def get_ROUTER_MAPPING(username):
    username=str(username).upper()
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT * FROM ROUTER_MAPPING WHERE USERNAME = '" + str(username) +"'"
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

#END Router Mapping
#Router_Mapping Tablw

#ADMIN MAPPING START
def insert_into_USER_ADMIN_MAPPING(admin,username,router_id,group_id,control):
    admin=str(admin).upper()
    username=str(username).upper()
    router_id=str(router_id).upper()
    group_id=str(group_id).upper()
    control=str(control).upper()
    x=find_in_ADMIN_MAPPING(admin,username,router_id,group_id)
    if(x==0):
        connection=sqlite3.connect(database_name)
        cursor=connection.cursor()
        insert_query='INSERT INTO USER_ADMIN_MAPPING (ADMIN,USERNAME,ROUTER_ID,GROUP_ID,CONTROL) VALUES(?,?,?,?,?)'
        cursor.execute(insert_query,(admin,username,router_id,group_id,control))
        cursor.close()
        connection.commit()
        connection.close()
    else:
        connection=sqlite3.connect(database_name)
        cursor=connection.cursor()
        update_query="UPDATE USER_ADMIN_MAPPING SET CONTROL='"+control+"'WHERE ADMIN='"+str(admin)+"'AND USERNAME='"+str(username)+"'AND ROUTER_ID='"+str(router_id)+"'AND GROUP_ID='"+str(group_id)+"'"
        cursor.execute(update_query)
        cursor.close()
        connection.commit()
        connection.close()

def find_in_ADMIN_MAPPING(admin,username,router_id,group_id):
    admin=str(admin).upper()
    username=str(username).upper()
    router_id=str(router_id).upper()
    group_id=str(group_id).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT ADMIN,USERNAME,ROUTER_ID,GROUP_ID FROM USER_ADMIN_MAPPING WHERE ADMIN='"+str(admin)+"'AND USERNAME='"+str(username)+"'AND ROUTER_ID='"+str(router_id)+"'AND GROUP_ID='"+str(group_id)+"'"
    list_users=list()
    for row in cursor.execute(query):
        list_users.append(row)
    cursor.close()
    connection.commit()
    connection.close()
    if(len(list_users)==0):
        return 0
    else:
        return len(list_users)

def find_in_ADMIN_MAPPING_2(admin,username):
    admin=str(admin).upper()
    username=str(username).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT ADMIN,USERNAME,ROUTER_ID,GROUP_ID FROM USER_ADMIN_MAPPING WHERE ADMIN='"+str(admin)+"'AND USERNAME='"+str(username)+"'"
    list_users=list()
    for row in cursor.execute(query):
        list_users.append(row)
    cursor.close()
    connection.commit()
    connection.close()
    if(len(list_users)==0):
        return 0
    else:
        return len(list_users)

def user_dev(username):
    username=str(username).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT ROUTER_ID,GROUP_ID FROM USER_ADMIN_MAPPING WHERE USERNAME='"+str(username)+"'"
    list_users=list()
    for row in cursor.execute(query):
        list_users.append(row)
    cursor.close()
    connection.commit()
    connection.close()
    if(len(list_users)==0):
        return 0
    else:
        return (list_users)

def del_ADMIN(admin):
    admin=str(admin).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="DELETE FROM USER_ADMIN_MAPPING WHERE ADMIN='"+str(admin)+"'"
    cursor.execute(query)
    cursor.close()
    connection.commit()
    connection.close()

def del_USERNAME(username):
    username=str(username).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="DELETE FROM USER_ADMIN_MAPPING WHERE USERNAME='"+str(username)+"'"
    cursor.execute(query)
    cursor.close()
    connection.commit()
    connection.close()

def get_ADMIN_MAPPING(admin):
    admin=str(admin).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT USERNAME FROM USER_ADMIN_MAPPING WHERE ADMIN='"+str(admin)+"'"
    list_users=list()
    for row in cursor.execute(query):
        list_users.append(row)
    cursor.close()
    connection.commit()
    connection.close()
    if(len(list_users)==0):
        return 0
    else:
        return (list_users)

def get_USERS_MAPPING(username):
    username=str(username).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT ADMIN FROM USER_ADMIN_MAPPING WHERE USERNAME='"+str(username)+"'"
    list_users=list()
    for row in cursor.execute(query):
        list_users.append(row)
    cursor.close()
    connection.commit()
    connection.close()
    if(len(list_users)==0):
        return 0
    else:
        return (list_users)

def get_USERS_status(username,router_id,group_id):
    username=str(username).upper()
    router_id=str(router_id).upper()
    group_id=str(group_id).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT CONTROL FROM USER_ADMIN_MAPPING WHERE USERNAME='"+str(username)+"'AND ROUTER_ID='"+str(router_id)+"'AND GROUP_ID='"+str(group_id)+"'"
    list_users=list()
    for row in cursor.execute(query):
        list_users.append(row)
    if(len(list_users)==0):
        return 0
    else:
        return list_users[0][0]

def del_ADMIN_USERNAME(admin,username):
    admin=str(admin).upper()
    username=str(username).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="DELETE FROM USER_ADMIN_MAPPING WHERE USERNAME='"+str(username)+"'AND ADMIN='"+str(admin)+"'"
    cursor.execute(query)
    cursor.close()
    connection.commit()
    connection.close()

def del_ADMIN_USERNAME_GROUP(admin,username,router_id,group_id):
    admin=str(admin).upper()
    username=str(username).upper()
    group_id=str(group_id).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="DELETE FROM USER_ADMIN_MAPPING WHERE USERNAME='"+str(username)+"'AND ADMIN='"+str(admin)+"'AND GROUP_ID='"+str(group_id)+"'AND ROUTER_ID='"+str(router_id)+"'"
    cursor.execute(query)
    cursor.close()
    connection.commit()
    connection.close()
##ADMIN END

#ADMIN_KEY Start
def insert_into_ADMIN_KEY(adminkey):
    adminkey=str(adminkey).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    insert_query = "INSERT INTO ADMIN_KEY(ADMINKEY) VALUES (?)"
    if(len(get_ADMIN_KEY(adminkey))):
        {}
    else:
        cursor.execute(insert_query,(adminkey,))
        connection.commit()
        connection.close()

def content_ADMIN_KEY():
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query='SELECT * FROM ADMIN_KEY'
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def get_ADMIN_KEY(adminkey):
    adminkey=str(adminkey).upper()
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT * FROM ADMIN_KEY WHERE ADMINKEY = '" + str(adminkey) +"'"
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def del_ADMIN_KEY(adminkey):
    adminkey=str(adminkey).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="DELETE FROM ADMIN_KEY WHERE ADMINKEY = '" + str(adminkey) +"'"
    cursor.execute(query)
    connection.commit()
    connection.close()
#ADMIN_KEY END

#ROUTER_PASSWORD Start
def get_ROUTER_PASSWORD(router_id):
    router_id=str(router_id).upper()
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT PASSWORD FROM ROUTER_PASSWORD WHERE ROUTER_ID = '" + str(router_id) +"'"
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def content_ROUTER_PASSWORD():
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT * FROM ROUTER_PASSWORD"
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def insert_into_ROUTER_PASSWORD(router_id,password):
    router_id=str(router_id).upper()
    password=str(password).upper()
    x=len(get_ROUTER_PASSWORD(router_id))
    if(x==0):
        connection=sqlite3.connect(database_name)
        cursor=connection.cursor()
        insert_query = "INSERT INTO ROUTER_PASSWORD(ROUTER_ID,PASSWORD) VALUES (?,?)"
        cursor.execute(insert_query,(router_id,password))
        connection.commit()
        connection.close()
    else:
        connection=sqlite3.connect(database_name)
        cursor=connection.cursor()
        update_query="UPDATE ROUTER_PASSWORD SET PASSWORD='"+str(password)+"' WHERE ROUTER_ID='"+str(router_id)+"'"
        cursor.execute(update_query)
        connection.commit()
        connection.close()
#ROUTER_PASSWORD End

#ROUTER Start
def insert_into_ROUTER(router_id,devices,state):
    router_id=str(router_id).upper()
    devices=str(devices).upper()
    state=str(state).upper()
    x=find_router_devices(router_id,devices)
    if(x==0):
        connection=sqlite3.connect(database_name)
        cursor=connection.cursor()
        insert_query = "INSERT INTO ROUTER(ROUTER_ID,DEVICES,STATE) VALUES (?,?,?)"
        cursor.execute(insert_query,(router_id,devices,state))
        connection.commit()
        connection.close()
    else:
        connection=sqlite3.connect(database_name)
        cursor=connection.cursor()
        insert_query = "UPDATE ROUTER SET STATE='"+str(state)+"' WHERE ROUTER_ID = '" + str(router_id) +"' AND DEVICES ='"+str(devices)+"'"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()

def content_ROUTER():
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query='SELECT * FROM ROUTER'
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def get_ROUTER(ROUTER_ID):
    ROUTER_ID=str(ROUTER_ID).upper()
    list_users=list()
    connection=sqlite3.connect(database_name_status)
    cursor=connection.cursor()
    query="SELECT ROUTER_ID,GROUP_ID,DEVICES,STATE FROM ROUTER WHERE ROUTER_ID = '" + str(ROUTER_ID) +"'"
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def get_ROUTER_GROUP(ROUTER_ID,GROUP_ID):
    ROUTER_ID=str(ROUTER_ID).upper()
    list_users=list()
    connection=sqlite3.connect(database_name_status)
    cursor=connection.cursor()
    query="SELECT ROUTER_ID,GROUP_ID,DEVICES,STATE FROM ROUTER WHERE ROUTER_ID = '" + str(ROUTER_ID) +"'AND GROUP_ID='"+str(GROUP_ID)+"'"
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def del_user_ROUTER(username):
    username=str(username).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="DELETE FROM ROUTER WHERE USERNAME = '" + str(username) +"'"
    cursor.execute(query)
    connection.commit()
    connection.close()

def get_ROUTER_2(ROUTER_ID,devices):
    ROUTER_ID=str(ROUTER_ID).upper()
    devices=str(device).upper()
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT STATE FROM ROUTER WHERE ROUTER_ID = '" + str(ROUTER_ID) +"'AND DEVICES='"+str(devices)+"'"
    for row in cursor.execute(query):
        list_users.append(row)
    connection.commit()
    connection.close()
    return list_users

def update_ROUTER(router_id,devices,state):
    router_id=str(router_id).upper()
    devices=str(devices).upper()
    state=str(state).upper()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="UPDATE ROUTER SET STATE = '"+str(state)+"' WHERE ROUTER_ID='"+str(router_id)+"' AND DEVICES = '"+str(devices)+"'"
    cursor.execute(query)
    connection.commit()
    connection.close()

def find_router_devices(router_id,device):
    router_id=str(router_id).upper()
    device=str(device).upper()
    list_users=list()
    connection=sqlite3.connect(database_name)
    cursor=connection.cursor()
    query="SELECT * FROM ROUTER WHERE ROUTER_ID = '" + str(router_id) +"' AND DEVICES ='"+str(device)+"'"
    for row in cursor.execute(query):
        list_users.append(row)
    if (len(list_users)==0):
        return 0
    else:
        return(len(list_users))
    connection.commit()
    connection.close()
    return list_users

#ROUTER End



#####Table Status
import sqlite3
database_name_status="Status.db"
def create_table_status():
    connection=sqlite3.connect(database_name_status)
    cursor=connection.cursor()
    create_table_ROUTER='CREATE TABLE IF NOT EXISTS [ROUTER]([ID] INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,ROUTER_ID TEXT,GROUP_ID TEXT,DEVICES TEXT,STATE TEXT,LAST_UPDATED_TIME DATETIME,CURRENT_TIME_N DATETIME,DIFFERENCE_TIME DATETIME)'
    cursor.execute(create_table_ROUTER)
    connection.commit()
    connection.close()

def insert_into_status(router_id,group_id,devices,state):
    router_id=str(router_id).upper()
    group_id=str(group_id).upper()
    devices=str(devices).upper()
    state=str(state).upper()
    x=status_find_duplicates(router_id,group_id,devices)
    if(x==0):
        connection=sqlite3.connect(database_name_status)
        cursor=connection.cursor()
        insert_query = "INSERT INTO ROUTER(ROUTER_ID,GROUP_ID,DEVICES,STATE) VALUES (?,?,?,?)"
        cursor.execute(insert_query,(router_id,group_id,devices,state))
        insert_query = "UPDATE ROUTER SET LAST_UPDATED_TIME= datetime() WHERE ROUTER_ID = '" + str(router_id) +"'AND GROUP_ID ='"+str(group_id)+"'AND DEVICES ='"+str(devices)+"'"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
    else:
        connection=sqlite3.connect(database_name_status)
        cursor=connection.cursor()
        insert_query = "UPDATE ROUTER SET STATE='"+str(state)+"'WHERE ROUTER_ID ='" + str(router_id) +"' AND GROUP_ID='"+str(group_id)+ "'AND DEVICES ='"+str(devices)+"'"
        cursor.execute(insert_query)
        insert_query = "UPDATE ROUTER SET LAST_UPDATED_TIME= datetime() WHERE ROUTER_ID ='" + str(router_id) +"' AND GROUP_ID='"+str(group_id)+ "'AND DEVICES ='"+str(devices)+"'"
        cursor.execute(insert_query)
        connection.commit()
        connection.close()
    set_current_time()

def status_find_duplicates(router_id,group_id,devices):
    router_id=str(router_id).upper()
    group_id=str(group_id).upper()
    devices=str(devices).upper()
    list_users=list()
    connection=sqlite3.connect(database_name_status)
    cursor=connection.cursor()
    query="SELECT * FROM ROUTER WHERE ROUTER_ID = '" + str(router_id) +"'AND GROUP_ID ='"+str(group_id)+"'AND DEVICES ='"+str(devices)+"'"
    for row in cursor.execute(query):
        list_users.append(row)
    if (len(list_users)==0):
        return 0
    else:
        return(len(list_users))
    connection.commit()
    connection.close()
    return list_users



def remove_from_status(router_id,group_id,devices):
    router_id=str(router_id).upper()
    devices=str(devices).upper()
    connection=sqlite3.connect(database_name_status)
    cursor=connection.cursor()
    query="DELETE FROM ROUTER WHERE ROUTER_ID = '" + str(router_id) +"'AND GROUP_ID ='"+str(group_id)+"'AND DEVICES ='"+str(devices)+"'"
    cursor.execute(query)
    connection.commit()
    connection.close()

def set_current_time():
    connection=sqlite3.connect(database_name_status)
    cursor=connection.cursor()
    query="UPDATE ROUTER SET CURRENT_TIME_N=datetime()"
    cursor.execute(query)
    connection.commit()
    connection.close()
    set_difference_time()

def set_difference_time():
    connection=sqlite3.connect(database_name_status)
    cursor=connection.cursor()
    query="UPDATE ROUTER SET DIFFERENCE_TIME=(julianday(CURRENT_TIME_N) - julianday(LAST_UPDATED_TIME)) * 86400.0"
    cursor.execute(query)
    connection.commit()
    connection.close()

def remove_device_status(threshold):
    connection=sqlite3.connect(database_name_status)
    cursor=connection.cursor()
    query="UPDATE ROUTER SET STATE='DISCONNECTED' WHERE DIFFERENCE_TIME >'"+str(threshold)+"'"
    cursor.execute(query)
    connection.commit()
    connection.close()

def status_sort():
    connection=sqlite3.connect(database_name_status)
    cursor=connection.cursor()
    query="SELECT * FROM ROUTER ORDER BY GROUP_ID ASC"
    cursor.execute(query)
    connection.commit()
    connection.close()
##End

##Table Command
def create_table_command():
    connection=sqlite3.connect(database_name_command)
    cursor=connection.cursor()
    create_table_ROUTER='CREATE TABLE IF NOT EXISTS [COMMAND]([ID] INTEGER  PRIMARY KEY AUTOINCREMENT NOT NULL,ROUTER_ID TEXT,GROUP_ID TEXT,DEVICES TEXT,STATE TEXT)'
    cursor.execute(create_table_ROUTER)
    cursor.close()
    connection.commit()
    connection.close()

def insert_command(router_id,group_id,devices_id,state):
    router_id=str(router_id).upper()
    group_id=str(group_id).upper()
    devices_id=str(devices_id).upper()
    state=str(state).upper()
    connection=sqlite3.connect(database_name_command)
    cursor=connection.cursor()
    insert_query='INSERT INTO COMMAND(ROUTER_ID,GROUP_ID,DEVICES,STATE) VALUES(?,?,?,?)'
    cursor.execute(insert_query,(router_id,group_id,devices_id,state))
    cursor.close()
    connection.commit()
    connection.close()

def table_queue():
    connection=sqlite3.connect(database_name_command)
    cursor=connection.cursor()
    queue_querry='SELECT ROUTER_ID,GROUP_ID,DEVICES,STATE FROM COMMAND'
    list_commands=list()
    for row in cursor.execute(queue_querry):
        list_commands.append(row)
    cursor.close()
    connection.commit()
    connection.close()
    message=list_commands
    list_commands_formatted=list()
    for i in message:
        list_commands_formatted.append(i[0]+"/"+i[1]+"/"+i[2]+"/"+i[3])
    connection=sqlite3.connect(database_name_command)
    cursor=connection.cursor()
    clear_query='DELETE FROM COMMAND'
    cursor.execute(clear_query)
    connection.commit()
    connection.close()
    return list_commands_formatted

##End
