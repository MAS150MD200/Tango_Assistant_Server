__author__ = 'Antonio'

import cherrypy
from jinja2 import Environment, FileSystemLoader
import os, os.path
from pprint import pprint as pp

env = Environment(loader=FileSystemLoader('templates'))
DATA = """memcache.us0101mmb003.memcached.account_to_email.memcached_ops.hits
memcache.us0101mmb002.memcached.account_to_email.memcached_ops.evictions
memcache.us0101mmb003.memcached.account_to_email.memcached_ops.evictions
memcache.us0101mmb004.memcached.account_to_email.memcached_ops.misses
memcache.us0101mmb001.memcached.account_to_email.memcached_ops.evictions
memcache.us0101mmb002.memcached.account_to_email.memcached_ops.misses
memcache.us0101mmb004.memcached.account_to_email.memcached_ops.evictions
memcache.us0101mmb001.memcached.account_to_email.memcached_ops.hits
memcache.us0101mmb001.memcached.account_to_email.memcached_ops.misses
memcache.us0101mmb002.memcached.account_to_email.memcached_ops.hits
memcache.us0101mmb004.memcached.account_to_email.memcached_ops.hits
memcache.us0101mmb003.memcached.account_to_email.memcached_ops.misses"""




class Root:
    @cherrypy.expose
    def index(self):
        tmpl = env.get_template('index_3.html')

        metrics_list = sorted(DATA.split("\n"))

        return tmpl.render(metrics=metrics_list)

cherrypy.config.update({'server.socket_host': '0.0.0.0',
                         'server.socket_port': 8080,
                        })


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

