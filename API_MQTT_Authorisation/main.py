import authentication as auth
import resources as res

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

# @app.before_request
# def initial():
#     res.init()

jwt=JWTManager(app)

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in auth.BLACKLIST

@jwt.expired_token_loader
def expired_token_callback():
    return jsonify({'status':'401',
        'message': 'The token has expired',
        'error': 'token_expired'
    })


@jwt.invalid_token_loader
def invalid_token_callback(error):  # we have to keep the argument here, since it's passed in by the caller internally
    return jsonify({
        'message': 'Signature verification failed.',
        'error': 'invalid_token',
        'status':'401'
    })


@jwt.unauthorized_loader
def missing_token_callback(error):
    return jsonify({
        "description": "Request does not contain an access token.",
        'error': 'authorization_required',
        'status':'401'
    })


@jwt.needs_fresh_token_loader
def token_not_fresh_callback():
    return jsonify({
        "description": "The token is not fresh.",
        'error': 'fresh_token_required',
        'status':'401'
    })


@jwt.revoked_token_loader
def revoked_token_callback():
    return jsonify({
        "description": "The token has been revoked.",
        'error': 'token_revoked',
        'status':'401'
    })

api.add_resource(res.Welcome,'/welcome')
api.add_resource(res.Signup,'/signup')
api.add_resource(res.Deregister,'/deregister/<string:username>')
api.add_resource(res.viewdetails,'/get/details/<string:name>')
api.add_resource(res.forgot_password,'/forgot_password')
api.add_resource(res.Check,'/check')
api.add_resource(res.Add_Router_User,'/router/add')
api.add_resource(res.Remove_Router_User,'/router/remove')
api.add_resource(res.get_router_details,'/router/details')
api.add_resource(res.send_commands,'/router/update')
api.add_resource(auth.UserLogin,'/login')
api.add_resource(auth.TokenRefresh,'/refresh')
api.add_resource(auth.UserLogout,'/logout')
api.add_resource(auth.KillToken,'/killtoken')

app.run(port=8080,host='0.0.0.0',debug=True)
