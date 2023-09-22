#importing libraries
import sqlite3
database_name='Details.db'
from flask_restful import Resource, reqparse
from flask import jsonify
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,
create_refresh_token ,
jwt_refresh_token_required ,
get_jwt_identity,
jwt_required,
get_raw_jwt)
from flask import Flask,jsonify,request,render_template


class User:
    def __init__(self,_id,username,password):
        self.id=_id
        self.username=username
        self.password=password

    @classmethod
    def find_by_username(cls,username):
        connection=sqlite3.connect(database_name)
        cursor=connection.cursor()
        cursor=connection.cursor()
        query='SELECT ID,USERNAME,PASSWORD FROM users WHERE username=?'
        result=cursor.execute(query,(username,))
        row=result.fetchone()
        if row:
            user =cls(*row)
        else:
            user =None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls,_id):
        connection=sqlite3.connect(database_name)
        cursor=connection.cursor()
        cursor=connection.cursor()
        query='SELECT ID,USERNAME,PASSWORD FROM users WHERE id=?'
        result=cursor.execute(query,(_id,))
        row=result.fetchone()
        if row:
            user =cls(*row)
        else:
            user =None
        connection.close()
        return user
from werkzeug.security import safe_str_cmp


class UserLogin(Resource):

    @classmethod
    def post(cls):
        parser=reqparse.RequestParser()
        parser.add_argument('username',type=str,required=True,help="The field cannot be left blank")
        parser.add_argument('password',type=str,required=True,help="The field cannot be left blank")
        data = parser.parse_args()
        data['username']=str(data['username']).upper()
        data['password']=str(data['password']).upper()
        user = User.find_by_username(data['username'])

        # this is what the `authenticate()` function did in security.py
        if user and safe_str_cmp(user.password, data['password']):

            access_token = create_access_token(identity=user.id, fresh=True)
            refresh_token = create_refresh_token(user.id)
            return jsonify({
                'status':"200",
                'access_token': access_token,
                'refresh_token': refresh_token
            })

        response=jsonify({"status":"401","message":"Invalid Credentials!"})
        response.status_code=401
        return response

class UserLogout(Resource):
    @jwt_required
    def get(self):
        jti=get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        response=jsonify({'message':'Logged Out','status':200})
        response.status_code=200
        return response

BLACKLIST = set()

class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user=get_jwt_identity()
        new_token=create_access_token(identity=current_user,fresh=False)
        refresh_token = create_refresh_token(current_user)
        return jsonify({'access_token':new_token,'refresh_token':refresh_token,'status':200})

class KillToken(Resource):
    @jwt_required
    def post(self):
        jti=get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return jsonify({'message':'TokenKilled','status':200})
