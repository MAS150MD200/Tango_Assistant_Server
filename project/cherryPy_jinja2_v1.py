__author__ = 'Antonio'

import cherrypy
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

class Root:
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index.html')
        return tmpl.render(salutation='Hello', target='World')

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                         'server.socket_port': 8080,
                        })


if __name__ == '__main__':
    cherrypy.quickstart(Root())