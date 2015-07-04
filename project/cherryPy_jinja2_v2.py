__author__ = 'Antonio'

import cherrypy
from jinja2 import Environment, FileSystemLoader
env = Environment(loader=FileSystemLoader('templates'))

class Root:
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index_2.html')
        # return tmpl.render(salutation='Hello', target='World')

        class a:
            pass

        class b:
            pass

        a.href = "a_href"
        a.caption = "a_caption"

        b.href = "b_href"
        b.caption = "b_caption"

        nav_list = [a, b]
        return tmpl.render(navigation=nav_list)

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                         'server.socket_port': 8080,
                        })


if __name__ == '__main__':
    cherrypy.quickstart(Root())

