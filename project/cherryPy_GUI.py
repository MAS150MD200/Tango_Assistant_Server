__author__ = 'Antonio'

import cherrypy
from jinja2 import Environment, FileSystemLoader
import os, os.path
import time
import graphiteParser
import grafana_dashboard_API
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

    # @cherrypy.expose
    # def grafana_create_dashboard_API(self, metricRadio=None):
    #
    #     #DEBUG
    #     # print(metricRadio)
    #     grafana_API_call_status,  grafana_new_dashboard_url = grafana_dashboard_API.createDashboard(metricRadio)
    #
    #     time.sleep(1)
    #
    #     tmpl = env.get_template('index_grafana.html')
    #     return tmpl.render(new_graph_url=grafana_new_dashboard_url)

    @cherrypy.expose
    def scripted_dashboard(self, metricRadio=None):
        tmpl = env.get_template('index_grafana_scripted_dashboard.html')
        return tmpl.render(new_graph_url=metricRadio)







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

    # http://127.0.0.1:8080/GSE/
    # cherrypy.quickstart(Root(),'/', conf)
    cherrypy.quickstart(Root(),'/', conf)

