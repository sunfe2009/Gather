#coding=utf-8

import tornado.web
import time
from markdown import Markdown
import re
from tornado.escape import xhtml_escape

html_killer = re.compile('<[^>]*>')
url_replace = re.compile(u' ((?:HTTP|HTTPS|FTP|ED2K|THUNDER|FLASHGETX|http|https|ftp|ed2k|thunder|flashgetx)://[^ ]+) ')
img_replace = re.compile(u' ((?:HTTP|HTTPS|http|https)://[^ \r\n]+(?:.jpg|.jpeg|.gif|.png|.JPG|.JPEG|.GIF|.PNG)[^ ]+) ')

md = Markdown(extensions=['fenced_code','smart_strong','tables'])

class BaseHandler(tornado.web.RequestHandler):

    def __init__(self,*args,**kwargs):
        tornado.web.RequestHandler.__init__(self,*args,**kwargs)
        #方便调用
        self.db = self.application.db

    def get_current_user(self):
        user = self.get_secure_cookie('user')
        if self.db.users.find_one({'username':user}) != None:
            return self.get_secure_cookie('user')
        else:
            self.clear_cookie('user')
            return None

    def get_error_html(self,status_code, **kwargs):
        if status_code==404:
            return self.render_string('404.html')
        else:
            return ''


def time_span(t):
    timecha = int(time.time()) - t
    if timecha < 60:
        return str(timecha)+u'秒前'
    elif timecha < 3600:
        return str(timecha/60)+u'分钟前'
    elif timecha < 86400:
        return str(timecha/3600)+u'小时前'
    elif timecha < 1296000:
        return str(timecha/86400)+u'天前'
    else:
        return time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(t+28800))

def md_convert(txt):
    #滤去html标签
    for x in set(html_killer.findall(txt)):
        txt = txt.replace(x,xhtml_escape(x))

    for x in set(img_replace.findall(txt)):
        txt = txt.replace(x,u'<img alt="%s" src="%s" />' % (x,x))

    for x in set(url_replace.findall(txt)):
        txt = txt.replace(x,u'<a href="%s">%s</a>' % (x,x))

    txt = md.convert(txt)

    return txt


def getvalue(dict,keyname):
    try:
        return dict[keyname]
    except:
        return ''