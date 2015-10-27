__author__ = 'Antonio'

import cherrypy
from jinja2 import Environment, FileSystemLoader
import os, os.path
import time
# import simplejson
import graphiteParser
import name_resolver_se
import pd_reports
import qa_tool
import boto3_aws
import config
from pprint import pprint as pp


# Global variables.
GRAPHITE_DB = "../all_data_column.txt"
env = Environment(loader=FileSystemLoader('templates'))


class Root:
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index_start.html')
        return tmpl.render()


    @cherrypy.expose
    def gse_search(self):
        tmpl = env.get_template('index_gse_search.html')
        return tmpl.render()


    @cherrypy.expose
    def gse_result(self, queryParameters=None):
        tmpl = env.get_template('index_gse_result.html')

        #TODO: add check for ending space.
        queryParameters_list = queryParameters.strip().split(" ")
        metricsFound = graphiteParser.graphiteFileParser(GRAPHITE_DB, queryParameters_list)

        #pass queryParameters_list to the HTML page template. To prevent clear form after submit.
        return tmpl.render(metrics=metricsFound, params=queryParameters_list)


    @cherrypy.expose
    def scripted_dashboard(self, metricsCheckBox=None):

        # in case of checked only one checkbox.
        if isinstance(metricsCheckBox, str):
            metricsCheckBox = [metricsCheckBox]

        metricsCheckBox_joined = ",".join(metricsCheckBox)

        tmpl = env.get_template('index_grafana_scripted_dashboard.html')
        return tmpl.render(metrics=metricsCheckBox_joined)


    @cherrypy.expose
    def name_resolver(self, server_name_form=""):
        tmpl = env.get_template('index_name_resolver.html')

        host_name_dict = {}

        if server_name_form:
            host_name_dict = name_resolver_se.resolve_server_name(server_name_form)

        return tmpl.render(server_name_form_to_tmpl=server_name_form, host_name_dict_to_tmpl=host_name_dict)


    @cherrypy.expose
    def pd_report_generator(self, form_time_since="", form_time_until="", form_timezone=""):
        tmpl = env.get_template('pd_report.html')

        print(form_time_since, form_time_until, form_timezone)

        report_list = []
        if form_time_since and form_time_until:
            report_list = pd_reports.get_report(form_time_since, form_time_until, form_timezone)

        return tmpl.render(form_time_since_to_tmpl=form_time_since,
                           form_time_until_to_tmpl=form_time_until,
                           form_timezon_to_tmpl=form_timezone,
                           report_list_to_tmpl=report_list)


    @cherrypy.expose
    def qa_tool(self, form_appname="empty"):
        tmpl = env.get_template('qa_tool.html')


        result_proxy_list, appnames = qa_tool.qa_tool_get_result(appname=form_appname)
        # DEBUG.
        # pp(appnames)

        selected_app = form_appname
        return tmpl.render(appnames_to_tmpl=appnames,
                           versions_to_tmpl=result_proxy_list,
                           selected_app_to_tmpl=selected_app)

    @cherrypy.expose
    def amazon_statistics(self):
        tmpl = env.get_template('aws_statistics.html')

        # get data:
        t_aws_dict = boto3_aws.get_tango_aws_dict(arg_instance_state='all')

        summary_table, details_tables_dict = boto3_aws.tango_aws_dict_pretty_print(t_aws_dict, arg_aws_region='all', arg_report_type='full')

        # Convert to HTML and add css to summary table:
        summary_table_html = summary_table.get_html_string(attributes={"class": "table table-striped"})

        # Convert to HTML and add css to details table:
        details_tables_dict_html = dict((k, v.get_html_string(attributes={"class": "table table-striped"})) for k, v in details_tables_dict.items())

        # return tmpl.render()
        return tmpl.render(summary_table_html_to_tmpl=summary_table_html,
                           details_tables_dict_html_to_tmpl=details_tables_dict_html)



# RESTful API:
class QAToolREST:

    exposed = True
    @cherrypy.tools.json_out()
    def GET(self, app=None):

        result_proxy_list, appnames = qa_tool.qa_tool_get_result(appname=app)

        # make some changes:
        appnames = list(map(lambda _: _.strip(), appnames))

        if not app:
            return {"appnames": appnames}
        elif app in appnames:
            return {"versions": result_proxy_list}
        else:
            return {"message": "application not found."}


if __name__ == '__main__':


    # global conf:
    cherrypy.config.update({'server.socket_host': '0.0.0.0',
                            'server.socket_port': 8080,
                            })

    # app config:
    conf_tas = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public',
        }
    }

    conf_QAToolREST = {
        '/': {'request.dispatch': cherrypy.dispatch.MethodDispatcher()}
    }

    # app tree mount:
    cherrypy.tree.mount(
        Root(), '/TAS/', conf_tas
    )

    cherrypy.tree.mount(
        QAToolREST(), '/TAS/api/qa_tool/', conf_QAToolREST
    )

    # engine start:
    cherrypy.engine.start()
    cherrypy.engine.block()

    # cherrypy.quickstart(Root(),'/', conf_tas)
    # cherrypy.quickstart(Root(),'/TAS/', conf_tas)

