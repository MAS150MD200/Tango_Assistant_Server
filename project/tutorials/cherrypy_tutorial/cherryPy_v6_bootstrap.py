__author__ = 'Antonio'


import os, os.path
import random
import string

import cherrypy

class StringGenerator(object):
   @cherrypy.expose
   def index(self):
       return """<html>
         <head>
           <link href="/static/bootstrap-3.3.5-dist/css/bootstrap.min.css" rel="stylesheet">
           <link href="/static/bootstrap-3.3.5-dist/css/bootstrap-theme.min.css" rel="stylesheet">
         </head>
     <body>
       <form method="get" action="generate">
         <input type="text" value="8" name="length"  />
             <button type="submit" class="btn btn-lg btn-success">Give it now!</button>
       </form>
     </body>
   </html>"""

   @cherrypy.expose
   def generate(self, length=8):
       some_string = ''.join(random.sample(string.hexdigits, int(length)))
       cherrypy.session['mystring'] = some_string
       return some_string

   @cherrypy.expose
   def display(self):
       return cherrypy.session['mystring']

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                            })
    cherrypy.quickstart(StringGenerator(), '/', conf)


