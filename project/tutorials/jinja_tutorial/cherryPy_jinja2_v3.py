__author__ = 'Antonio'

import cherrypy
from jinja2 import Environment, FileSystemLoader
import os, os.path
from pprint import pprint as pp

env = Environment(loader=FileSystemLoader('templates'))

class Root:
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index_gse_search.html')
        return tmpl.render()

    @cherrypy.expose
    def result(self, queryParameters=None):
        tmpl = env.get_template('index_gse_result.html')
        queryParameters_list = sorted(queryParameters.split(" "))
        return tmpl.render(params=queryParameters_list)



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

    #need to place it to the conf.
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                            })

    cherrypy.quickstart(Root(),'/', conf)

