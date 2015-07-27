on grafana server:
name_resolver_se.py
URL = "http://grafana.tangome.gbl/TAS/static/TangoInfrastructureNamingConventionEngineeringTango.htm"

graphiteParser.py
FILE_NAME = "../all_data_column.txt"


[root@us0101amo099 graphite_search_engine]# cat get_data.sh
echo {1..8} | xargs -n1 -P0 | xargs -P0 -I'{}' curl -o ./amo'{}'.json http://us0101amo00'{}'/metrics/index.json
cat amo[1-8].json | tr "," "\n" | tr -d '"' | tr -d " " | tr -d "[" | tr -d "]" > amo1-8.json
