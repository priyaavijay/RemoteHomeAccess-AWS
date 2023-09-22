import authentication as auth
import resources as res
import json

import flask
from flask import jsonify
from flask_restful import Api
from flask_jwt_extended import JWTManager


app = flask.Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'asdfghjkl'
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS']=['access','refresh']
app.config['JWT_ACCESS_TOKEN_EXPIRES']=False
api = Api(app)

#@app.before_request
#def initial():
#    res.init()

jwt=JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in auth.BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    response=jsonify({'status':401,
        'message': 'The token has expired',
        'error': 'token_expired'
    })
    response.status_code=401
    return response

@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    print("Signature")
    response=jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token',
        'status':'401'
    })
    response.status_code=401
    return response

@jwt.unauthorized_loader
def missing_token_callback(error):
    response= jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required',
        'status':'401'
    })
    response.status_code=401
    return response


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    response=jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required',
        'status':'401'
    })
    response.status_code=401
    return response


@jwt.revoked_token_loader
def revoked_token_callback():
    response=jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked',
        'status':'401'
    })
    response.status_code=401
    return reponse

api.add_resource(res.Welcome,'/welcome')
api.add_resource(auth.UserLogin,'/login')
api.add_resource(res.Signup,'/signup')
api.add_resource(res.Deregister,'/deregister/<string:username>')

api.add_resource(res.viewdetails,'/get/details/<string:name>')
api.add_resource(res.forgot_password,'/forgot_password')

api.add_resource(res.Check,'/check')

api.add_resource(res.Add_Router_User,'/router/add')
api.add_resource(res.Remove_Router_User,'/router/remove')
api.add_resource(res.user_add,'/user/add')
api.add_resource(res.remove_user,'/user/remove')
api.add_resource(res.remove_user_group,'/user/remove/group')
api.add_resource(res.get_router_details,'/router/details')
api.add_resource(res.send_commands,'/router/update')

api.add_resource(auth.TokenRefresh,'/refresh')
api.add_resource(auth.UserLogout,'/logout')
api.add_resource(auth.KillToken,'/killtoken')

app.run(port=80,host='0.0.0.0',debug=True)
