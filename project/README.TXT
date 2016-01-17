
# TODO: make jinja templates more pretty.

____________________
# on grafana server(us0101amo099.tangome.gbl):

name_resolver_se.py
URL = "http://grafana.tangome.gbl/TAS/static/TangoInfrastructureNamingConventionEngineeringTango.htm"

graphiteParser.py
FILE_NAME = "../all_data_column.txt"

config.py
    USER:
    PASSWORD:

qa_tool.py
    DB_HOST_TUNNEL -> DB_HOST

boto3_aws.py
    set password - not good
    use credentials:
        profile_name="sre-readonly"

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

work directory: /root/graphite_search_engine

USE SCREEN.

screen -ls
screen -r

ctrl+c

mv ./project ./BACKUP/project_14.10.2015

git clone https://github.com/MAS150MD200/Tango_Assistant_Server.git

mv ./Tango_Assistant_Server/project ./
rm -rf ./Tango_Assistant_Server/


RUN under virtual environment:
cd /root/graphite_search_engine/
source ./venv/bin/activate

cd /root/graphite_search_engine/project
python cherryPy_GUI.py

ctrl-a + d
____________________



____________________
# requirements.txt(13.10.2015)
# pip freeze > /tmp/requirements.txt
# pip install -r /tmp/requirements.txt

beautifulsoup4==4.4.0
CherryPy==3.8.0
Jinja2==2.7.3
MarkupSafe==0.23
pytz==2015.4
requests==2.7.0

____________________


