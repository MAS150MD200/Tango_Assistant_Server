__author__ = 'Antonio'

import cherrypy
from jinja2 import Environment, FileSystemLoader
import os, os.path
import graphiteParser
from pprint import pprint as pp


#Global variables.
GRAPHITE_DB = "../all_data_column.txt"
env = Environment(loader=FileSystemLoader('templates'))


class Root:
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index_main.html')
        return tmpl.render()

    @cherrypy.expose
    def result(self, queryParameters=None):
        tmpl = env.get_template('index_content.html')

        #TODO: add chech for several spaces.
        queryParameters_list = queryParameters.strip().split(" ")
        metricsFound = graphiteParser.graphiteFileParser(GRAPHITE_DB, queryParameters_list)

        #pass queryParameters_list to the HTML page template. To prevent clear form after submit.
        return tmpl.render(metrics=metricsFound, params=queryParameters_list)

    @cherrypy.expose
    def grafanaAPI(self, metricRadio=None):

        pp(metricRadio)
        return



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

    #TODO: need to place it to the conf.
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                            })

    cherrypy.quickstart(Root(),'/', conf)

