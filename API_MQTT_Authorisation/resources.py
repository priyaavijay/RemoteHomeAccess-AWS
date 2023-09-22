import table as table

from flask import Flask,jsonify,request,render_template
from flask_restful import Resource, reqparse,Api
from flask_jwt_extended import JWTManager,jwt_required,get_jwt_identity,get_jwt_claims
from werkzeug.security import safe_str_cmp

def init():
    table.creating_table()
    table.insert_into_ADMIN_KEY("qwerty")
    table.insert_into_ROUTER_PASSWORD("abcd123","1234567")
    table.insert_into_ROUTER_PASSWORD("abcd123","5789")
    table.insert_into_ROUTER_PASSWORD("abcd456","12345")
    table.insert_into_ROUTER("abcd123","Light1","On")
    table.insert_into_ROUTER("abcd123","Light2","Off")
    table.insert_into_ROUTER("abcd456","Fan1","On")
    table.insert_into_ROUTER("abcd456","Fan2","Off")

def return_data(status=200,message=None):
    response=jsonify({"status":status,"message":message})
    response.status_code=status
    return response

def get_username(jwt_id):
    x=table.get_USERS_id(jwt_id)
    if(x==0):
        # response = return_data(401,"Invalid Token")
        # return response
        return 0
    if(len(x)==0):
        # response = return_data(401,"Invalid Token")
        # return response
        return 0
    return ((x[0]))

class Welcome(Resource):
    def get(self):
        return return_data(200,"Welcome to Smart Home")

class Signup(Resource):
    def post(self):
        data=request.get_json()
        if((len(table.get_USERS(data['username'])))):
            return return_data(404,"Details Already Present")
        adminkey=data['adminkey']
        if(adminkey=="None"):
            table.insert_into_ADMIN(data['username'],"User")
            table.insert_into_USERS(data['username'],data['password'],data['name'],data['email'])
            return  return_data(200)
        x=len(table.get_ADMIN_KEY(adminkey))
        if(x):
            table.insert_into_ADMIN(data['username'],"Admin")
        else:
            return return_data(404,"ADMIN_KEY_ERROR")
        table.insert_into_USERS(data['username'],data['password'],data['name'],data['email'])
        return return_data()

class Deregister(Resource):
    def get(self,username):
        x=len(table.get_USERS(username))
        if(x==0):
            return return_data(404,"Username not found")
        table.del_user_USERS(username)
        table.del_user_ADMIN(username)
        return return_data()

class viewdetails(Resource):
    def get(self,name):
        if(name.upper()=='USERS'):
            return return_data(200,table.content_USERS())
        elif(name.upper()=='ADMIN'):
            return return_data(200,table.content_ADMIN())
        elif(name.upper()=='ROUTER_MAPPING'):
            return return_data(200,table.content_ROUTER_MAPPING())
        elif(name.upper()=='ROUTER'):
            return return_data(200,table.content_ROUTER())
        elif(name.upper()=='USER_ADMIN_MAPPING'):
            return return_data(200,table.content_USER_ADMIN_MAPPING())
        elif(name.upper()=='ADMIN_KEY'):
            return return_data(200,table.content_ADMIN_KEY())
        elif(name.upper()=='ROUTER_PASSWORD'):
            return return_data(200,table.content_ROUTER_PASSWORD())
        else:
            return return_data(404,"Error!Wrong Table Name")

class forgot_password(Resource):
    def post(self):
        data=request.get_json()
        x=table.forgot_password(data['username'],data['email'],data['new_password'])
        if(x==0):
            return return_data(401,"Username/E-Mail Mismatch")
        else:
            return return_data(200)

class Check(Resource):
    @jwt_required
    def get(self):
        return return_data(200,get_username(get_jwt_identity()))

class Add_Router_User(Resource):
    @jwt_required
    def post(self):
        username=get_username(get_jwt_identity())
        if(username==0):
            response = return_data(401,"Invalid Token")
            return response
        is_admin=table.get_ADMIN_STATUS(username)
        if(is_admin!='ADMIN'):
            return(return_data(200,"Not a Admin!!"))
        data=request.get_json()
        router_id=data['router_id']
        password=data['password']
        x=table.get_ROUTER_PASSWORD(router_id)
        if(len(x)==0):
            return(return_data(200,"Router Not Found"))

        x=table.find_ROUTER_MAPPING_2(username,router_id)

        if(x!=0):
            return(return_data(200,"Username and Router ID Already present"))
        else:
            x=table.get_ROUTER_PASSWORD(router_id)
            # return(jsonify(x[0][0],password))
            if (password!=x[0][0]):
                return(return_data(401,"ROUTER_PASSWORD_Error"))
            table.insert_into_ROUTER_MAPPING(username,router_id)
            return(return_data(200))

class Remove_Router_User(Resource):
    @jwt_required
    def post(self):
        username=get_username(get_jwt_identity())
        if(username==0):
            response = return_data(401,"Invalid Token")
            return response
        is_admin=table.get_ADMIN_STATUS(username)
        if(is_admin!='ADMIN'):
            return(return_data(200,"Not a Admin!!"))
        data=request.get_json()
        router_id=data['router_id']
        x=table.find_ROUTER_MAPPING_2(username,router_id)
        if(x==0):
            return(return_data(401,"Error!Username Router ID pair Error"))
        else:
            table.del_user_ROUTER_MAPPING_2(username,router_id)
            return(return_data())

class get_router_details(Resource):
    @jwt_required
    def post(self):
        username=get_username(get_jwt_identity())
        if(username==0):
            response = return_data(401,"Invalid Token")
            return response
        is_admin=table.get_ADMIN_STATUS(username)
        if(is_admin=='ADMIN'):
            x=table.get_ROUTER_MAPPING(username)
            if(len(x)==0):
                return(return_data(200,"User does not have any Routers"))
            router_list=list()
            for element in x:
                router_list.append(element[2])
            device_list=list()
            for router in router_list:
                single_router=table.get_ROUTER(router)
                for devices in single_router:
                    router_li=devices[0]
                    group_li=devices[1]
                    devices_li=devices[2]
                    status_li=devices[3]
                    device_list.append({"router_id":router_li,"group_id":group_li,"devices_id":devices_li,"status":status_li})
            x=len(device_list)
            if(x!=0):
                return (return_data(200,device_list))
            else:
                return(return_data(200,"No Router/ Devices Connected"))
        else:
            user_table=table.user_dev(username)
            user_router_group_list=list()
            if(user_table==0):
                return(return_data(200,"User does not have any Routers"))
            for element in user_table:
                user_router_group_list.append((element[0],element[1]))
            device_list=list()
            for router,group in user_router_group_list:
                    devices=table.get_ROUTER_GROUP(router,group)
                    print(devices)
                    router_li=devices[0][0]
                    group_li=devices[0][1]
                    devices_li=devices[0][2]
                    status_li=devices[0][3]
                    device_list.append({"router_id":router_li,"group_id":group_li,"devices_id":devices_li,"status":status_li})
            x=len(device_list)
            if(x!=0):
                return (return_data(200,device_list))
            else:
                return(return_data(200,"No Router/ Devices Connected"))
                
class send_commands(Resource):
    @jwt_required
    def post(self):
        username=get_username(get_jwt_identity())
        if(username==0):
            response = return_data(401,"Invalid Token")
            return response
        # print(username)
        is_admin=table.get_ADMIN_STATUS(username)
        data=request.get_json()
        router_id=data['router_id']
        router_id=str(router_id).upper()
        group_id=data['group_id']
        group_id=str(group_id).upper()
        devices1=data['devices']
        devices1=str(devices1).upper()
        state=data['state']
        if(is_admin=='ADMIN'):
            x=table.get_ROUTER_MAPPING(username)
            if(len(x)==0):
                return(return_data(404,"User does not have any tables"))
            router_list=list()
            for element in x:
                router_list.append(element[2])
            if not(router_id in router_list):
                return(return_data(404,"Router Not Found"))
            group_list=list()
            device_list=list()
            single_router=table.get_ROUTER(router_id)
            for group in single_router:
                group_list.append(group[1])
                device_list.append(group[2])
            if(not(group_id in group_list)):
                return(return_data(404,"Group not found in Router"))
            if(not (devices1 in device_list)):
                return(return_data(404,"Device not found in the Router"))
            table.insert_command(router_id,group_id,devices1,state)
            return(return_data())

        else:
            x=table.get_USERS_status(username,router_id,group_id)
            if(x!='USERIO'):
                return(return_data(200,"User does not have credentials"))
            user_table=table.user_dev(username)
            user_group_list=list()
            user_router_list=list()
            user_router_group_list=list()
            for element in user_table:
                user_router_list.append(element[0])
                user_group_list.append(element[1])
                user_router_group_list.append((element[0],element[1]))
            if(not(router_id in user_router_list)):
                return(return_data(200,"User and Router Pair not found"))
            if(not(group_id in user_group_list)):
                return(return_data(200,"User and Group Pair not found"))
            device_list=list()
            for router,group in user_router_group_list:
                    devices=table.get_ROUTER_GROUP(router,group)
                    devices_li=devices[0][2]
                    device_list.append(devices_li)
                    # print(device_list)
            if(not(devices1 in device_list)):
                return(return_data(200,"Device Not Found"))
            table.insert_command(router_id,group_id,devices1,state)
            return(return_data())


class user_add(Resource):
    @jwt_required
    def post(self):
        username_admin=get_username(get_jwt_identity())
        data=request.get_json()
        username=data['username']
        router_id=data['router_id']
        group_id=data['group_id']
        control=data['control']
        username=str(username).upper()
        router_id=str(router_id).upper()
        group_id=str(group_id).upper()
        control=str(control).upper()
        is_admin=table.get_ADMIN_STATUS(username_admin)
        if(is_admin!='ADMIN'):
            return(return_data(200,"Not a Admin!!"))
        user_present=table.get_ADMIN_STATUS(username)
        if(user_present==0):
            return(return_data(200,"User Not Present"))
        elif(user_present=='ADMIN'):
            return(return_data(200,"The user you have entered is a Admin"))
        admin_router=table.get_ROUTER_MAPPING(username_admin)
        admin_router_list=list()
        for router in admin_router:
            admin_router_list.append(router[2])
        print(admin_router_list)
        if(not(router_id in admin_router_list)):
            return(return_data(200,"The Router Not found in Admin Table"))
        x=table.get_ROUTER_GROUP(router_id,group_id)
        if(len(x)==0):
            return(return_data(200,"The Gateway Group Pair not found"))
        if((control=='USER')|(control=='USERIO')):
            table.insert_into_USER_ADMIN_MAPPING(username_admin,username,router_id,group_id,control)
            return(return_data())
        else:
            return(return_data(200,"Control options not presetnt"))

class remove_user(Resource):
    @jwt_required
    def post(self):
        username_admin=get_username(get_jwt_identity())
        data=request.get_json()
        username=data['username']
        is_admin=table.get_ADMIN_STATUS(username_admin)
        if(is_admin!='ADMIN'):
            return(return_data(200,"Not a Admin!!"))
        x=table.find_in_ADMIN_MAPPING_2(username_admin,username)
        if(x==0):
            return(return_data(200,"User Admin Pair Not found"))
        table.del_ADMIN_USERNAME(username_admin,username)
        return(return_data())

class remove_user_group(Resource):
    @jwt_required
    def post(self):
        username_admin=get_username(get_jwt_identity())
        data=request.get_json()
        username=data['username']
        router_id=data['router_id']
        group_id=data['group_id']
        username=str(username).upper()
        router_id=str(router_id).upper()
        group_id=str(group_id).upper()
        is_admin=table.get_ADMIN_STATUS(username_admin)
        if(is_admin!='ADMIN'):
            return(return_data(200,"Not a Admin!!"))
        x=table.find_in_ADMIN_MAPPING_2(username_admin,username)
        if(x==0):
            return(return_data(200,"User Admin Pair Not found"))
        user_table=table.user_dev(username)
        user_group_list=list()
        user_router_list=list()
        for element in user_table:
            user_router_list.append(element[0])
            user_group_list.append(element[1])
        print(user_router_list)
        if(not(router_id in user_router_list)):
            return(return_data(200,"User and Router Pair not found"))
        if(not(group_id in user_group_list)):
            return(return_data(200,"User and Group Pair not found"))
        table.del_ADMIN_USERNAME_GROUP(username_admin,username,router_id,group_id)
        return(return_data())
