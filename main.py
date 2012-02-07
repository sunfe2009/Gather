#!/usr/bin/env python
#coding=utf-8

import os.path
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web
import pymongo
from tornado.options import define, options

from common import BaseHandler

define('port', default=8888, help='run on the given port', type=int)
define('mongo_host', default='127.0.0.1', help='mongodb host')
define('mongo_port', default=27017, help='mongodb port')

from auth import AuthSignupHandler,AuthLoginHandler,AuthLogoutHandler
from admin import AdminAddNodeHandler
from post import PostHandler

class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r'/', HomeHandler),
            
            (r'/signup', AuthSignupHandler),
            (r'/login', AuthLoginHandler),
            (r'/logout', AuthLogoutHandler),
            
#            (r'/topics/node(\d+)', NodeViewHandler),
#            (r'/topics/(\d+)', PostViewHandler),∂
#            (r'/tag/(.*?)', TagViewHandler),

            (r'/node/(\d+)/add', PostHandler),
            
            (r'/node/add/(.*)', AdminAddNodeHandler),
        ]
        settings = dict(
            bbs_title=u'精英盒子',
            bbs_title_e=u'Jybox',
            template_path=os.path.join(os.path.dirname(__file__), 'templates'),
            static_path=os.path.join(os.path.dirname(__file__), 'static'),
            xsrf_cookies=True,
            cookie_secret='89f3hneifu29IY(!H@@IUFY#(FCINepifu2iY!HU!(FU@H',
            login_url='/login',
            autoescape=None,
        )
        tornado.web.Application.__init__(self, handlers, **settings)

        self.db = pymongo.Connection(host=options.mongo_host,port=options.mongo_port).bbs

class HomeHandler(BaseHandler):
    def get(self):
        self.render('index.html',db=self.db)
        
if __name__ == '__main__':
    tornado.options.parse_command_line()
    http_server = tornado.httpserver.HTTPServer(Application())
    http_server.listen(options.port)
    tornado.ioloop.IOLoop.instance().start()