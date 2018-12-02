#!/usr/bin/env python3.6
# Luke Song, Nick Marcopoli, Andy Shin, Austin Sura
# final project
# webserver.py

import cherrypy, asyncio
from _user_database import _user_database
from _crypto_api import _crypto_api
from users import UserController
from crypto import CryptoController
from reset import ResetController

class optionsController:
    def OPTIONS(self, *args, **kargs):
        return ""

def CORS():
    cherrypy.response.headers["Access-Control-Allow-Origin"] = "*"
    cherrypy.response.headers["Access-Control-Allow-Methods"] = "GET, PUT, POST, DELETE, OPTIONS"
    cherrypy.response.headers["Access-Control-Allow-Credentials"] = "*"

def start_service():
    # Create dispatcher and connect controller
    dispatcher = cherrypy.dispatch.RoutesDispatcher()
    # database files
    udb = _user_database("user_pwd.db", "user_wallet.db")
    crypto = _crypto_api()
    uController = UserController(udb)
    cController = CryptoController(crypto)
    rController = ResetController(udb, crypto)
    # User db controller
    dispatcher.connect('user_get_wallet', '/users/:user', controller=uController,
                        action = 'GET_WALLET', conditions=dict(method=['GET'])
                )
    dispatcher.connect('user_changeID', '/users/change/', controller=uController,
                        action = 'PUT_CHANGE', conditions=dict(method=['PUT'])
                )
    dispatcher.connect('user_check_pwd', '/users/', controller=uController,
                        action = 'PUT_PWD', conditions=dict(method=['PUT'])
                )
    dispatcher.connect('make_new_id', '/users/', controller=uController,
                        action = 'POST_ID', conditions=dict(method=['POST'])
                )
    dispatcher.connect('change_pwd', '/users/:user', controller=uController,
                        action = 'PUT', conditions=dict(method=['PUT'])
                )
    dispatcher.connect('add_asset', '/users/:user', controller=uController,
                        action = 'POST', conditions=dict(method=['POST'])
                )
    dispatcher.connect('delete_user', '/users/change/:user', controller=uController,
                        action = 'PUT_DELETE', conditions=dict(method=['PUT'])
                )
    # Crypto api controller
    dispatcher.connect('get_hottest', '/crypto/', controller=cController,
                        action = 'POST_TOPN', conditions=dict(method=['POST'])
                )
    dispatcher.connect('get_price', '/crypto/', controller=cController,
                        action = 'PUT', conditions=dict(method=['PUT'])
                )
    dispatcher.connect('get_hotcold5', '/crypto/:temp', controller=cController,
                        action = 'GET_TEMP', conditions=dict(method=['GET'])
                )
    dispatcher.connect('what_if', '/crypto/whatif/', controller=cController,
                        action = 'PUT_WHATIF', conditions=dict(method=['PUT'])
                )
    # Reset controller
    dispatcher.connect('reset', '/reset/', controller=rController,
                        action = 'GET', conditions=dict(method=['GET'])
                )

    # Options requests for dispatcher
    dispatcher.connect('user_options', '/users/:user', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                )
    dispatcher.connect('users_all', '/users/', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                )
    dispatcher.connect('users_change', '/users/change/', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                ) 
    dispatcher.connect('users_delete', '/users/change/:user', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                ) 

    dispatcher.connect('crypto_hot_cold', '/crypto/', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                )
    dispatcher.connect('crypto_whatif', '/crypto/whatif/', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                )
    dispatcher.connect('user_reset', '/reset/', controller=optionsController,
                        action = 'OPTIONS', conditions=dict(method=['OPTIONS'])
                )

    
    # Configuration for the server
    conf = { 
            'global' : {
                    'server.socket_host': 'student04.cse.nd.edu',
                    'server.socket_port': 52109, 
                },
            '/' : { 'request.dispatch': dispatcher,
                    'tools.CORS.on': True,
                  } 
           }

    # Update config
    cherrypy.config.update(conf)
    app = cherrypy.tree.mount(None, config=conf)
    cherrypy.quickstart(app)

def fetch_data():
    crypto = _crypto_api()
    crypto.fetch_data()
    print("fetched\n\n")

    

if __name__ == '__main__':
    cherrypy.tools.CORS = cherrypy.Tool('before_finalize', CORS)
    bg = cherrypy.process.plugins.BackgroundTask(60, fetch_data)
    bg.start()
    start_service()
