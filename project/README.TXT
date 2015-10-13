
# TODO: make jinja templates more pretty.

TEST

____________________
# on grafana server:

name_resolver_se.py
URL = "http://grafana.tangome.gbl/TAS/static/TangoInfrastructureNamingConventionEngineeringTango.htm"

graphiteParser.py
FILE_NAME = "../all_data_column.txt"
____________________


____________________
# collect data for graphite:
[root@us0101amo099 graphite_search_engine]# cat get_data.sh
echo {1..8} | xargs -n1 -P0 | xargs -P0 -I'{}' curl -o ./amo'{}'.json http://us0101amo00'{}'/metrics/index.json
cat amo[1-8].json | tr "," "\n" | tr -d '"' | tr -d " " | tr -d "[" | tr -d "]" > amo1-8.json
____________________


____________________
httpd conf:
[root@us0101amo099 ~]# cat /etc/httpd/conf.d/tango_assistant_server.conf
ProxyPass /TAS http://127.0.0.1:8080/TAS
ProxyPassReverse /TAS http://127.0.0.1:8080/TAS
____________________


____________________
# RUN TAS:
USE SCREEN.

screen -ls
screen -r

git clone https://github.com/MAS150MD200/Tango_Assistant_Server.git


RUN under virtual environment:
cd /root/graphite_search_engine/
source ./venv/bin/activate

cd /root/graphite_search_engine/project
python cherryPy_GUI.py

ctrl-a + d
____________________


