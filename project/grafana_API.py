__author__ = 'Antonio'

import requests
import json
import urllib.parse
from pprint import pprint as pp


URL = "http://grafana.tangome.gbl:9200/grafana-dash/dashboard/"
dashboard = "atsvetkov_test"

FULL_URL = urllib.parse.urljoin(URL, dashboard)


# json_new_dashboard = '{"user":"guest","group":"guest","title":"atsvetkov_test","tags":[],"dashboard":"{\"id\":null,\"title\":\"atsvetkov_test\",\"originalTitle\":\"New Dashboard\",\"tags\":[],\"style\":\"dark\",\"timezone\":\"browser\",\"editable\":true,\"hideControls\":false,\"sharedCrosshair\":false,\"rows\":[{\"title\":\"Row1\",\"height\":\"250px\",\"editable\":true,\"collapse\":false,\"panels\":[{\"title\":\"memcached\",\"error\":false,\"span\":12,\"editable\":true,\"type\":\"graph\",\"id\":1,\"datasource\":null,\"renderer\":\"flot\",\"x-axis\":true,\"y-axis\":true,\"y_formats\":[\"short\",\"short\"],\"grid\":{\"leftMax\":null,\"rightMax\":null,\"leftMin\":null,\"rightMin\":null,\"threshold1\":null,\"threshold2\":null,\"threshold1Color\":\"rgba(216, 200, 27, 0.27)\",\"threshold2Color\":\"rgba(234, 112, 112, 0.22)\"},\"lines\":true,\"fill\":0,\"linewidth\":1,\"points\":false,\"pointradius\":5,\"bars\":false,\"stack\":false,\"percentage\":false,\"legend\":{\"show\":true,\"values\":false,\"min\":false,\"max\":false,\"current\":false,\"total\":false,\"avg\":false},\"nullPointMode\":\"connected\",\"steppedLine\":false,\"tooltip\":{\"value_type\":\"cumulative\",\"shared\":false},\"targets\":[{\"target\":\"memcache.us0101mmb003.memcached.account_to_email.memcached_ops.hits\"}],\"aliasColors\":{},\"seriesOverrides\":[],\"links\":[]}]}],\"nav\":[{\"type\":\"timepicker\",\"enable\":true,\"status\":\"Stable\",\"time_options\":[\"5m\",\"15m\",\"1h\",\"6h\",\"12h\",\"24h\",\"2d\",\"7d\",\"30d\"],\"refresh_intervals\":[\"5s\",\"10s\",\"30s\",\"1m\",\"5m\",\"15m\",\"30m\",\"1h\",\"2h\",\"1d\"],\"now\":true,\"collapse\":false,\"notice\":false}],\"time\":{\"from\":\"now-6h\",\"to\":\"now\"},\"templating\":{\"list\":[]},\"annotations\":{\"list\":[]},\"refresh\":false,\"version\":6,\"hideAllLegends\":false}"}'
json_new_dashboard = '{"user":"guest","group":"guest","title":"atsvetkov_test","tags":[],"dashboard":"{\\"id\\":null,\\"title\\":\\"atsvetkov_test\\",\\"originalTitle\\":\\"New Dashboard\\",\\"tags\\":[],\\"style\\":\\"dark\\",\\"timezone\\":\\"browser\\",\\"editable\\":true,\\"hideControls\\":false,\\"sharedCrosshair\\":false,\\"rows\\":[{\\"title\\":\\"Row1\\",\\"height\\":\\"250px\\",\\"editable\\":true,\\"collapse\\":false,\\"panels\\":[{\\"title\\":\\"no title (click here)\\",\\"error\\":false,\\"span\\":12,\\"editable\\":true,\\"type\\":\\"graph\\",\\"id\\":1,\\"datasource\\":null,\\"renderer\\":\\"flot\\",\\"x-axis\\":true,\\"y-axis\\":true,\\"y_formats\\":[\\"short\\",\\"short\\"],\\"grid\\":{\\"leftMax\\":null,\\"rightMax\\":null,\\"leftMin\\":null,\\"rightMin\\":null,\\"threshold1\\":null,\\"threshold2\\":null,\\"threshold1Color\\":\\"rgba(216, 200, 27, 0.27)\\",\\"threshold2Color\\":\\"rgba(234, 112, 112, 0.22)\\"},\\"lines\\":true,\\"fill\\":0,\\"linewidth\\":1,\\"points\\":false,\\"pointradius\\":5,\\"bars\\":false,\\"stack\\":false,\\"percentage\\":false,\\"legend\\":{\\"show\\":true,\\"values\\":false,\\"min\\":false,\\"max\\":false,\\"current\\":false,\\"total\\":false,\\"avg\\":false},\\"nullPointMode\\":\\"connected\\",\\"steppedLine\\":false,\\"tooltip\\":{\\"value_type\\":\\"cumulative\\",\\"shared\\":false},\\"targets\\":[{}],\\"aliasColors\\":{},\\"seriesOverrides\\":[]}]}],\\"nav\\":[{\\"type\\":\\"timepicker\\",\\"enable\\":true,\\"status\\":\\"Stable\\",\\"time_options\\":[\\"5m\\",\\"15m\\",\\"1h\\",\\"6h\\",\\"12h\\",\\"24h\\",\\"2d\\",\\"7d\\",\\"30d\\"],\\"refresh_intervals\\":[\\"5s\\",\\"10s\\",\\"30s\\",\\"1m\\",\\"5m\\",\\"15m\\",\\"30m\\",\\"1h\\",\\"2h\\",\\"1d\\"],\\"now\\":true,\\"collapse\\":false,\\"notice\\":false}],\\"time\\":{\\"from\\":\\"now-6h\\",\\"to\\":\\"now\\"},\\"templating\\":{\\"list\\":[]},\\"annotations\\":{\\"list\\":[]},\\"refresh\\":false,\\"version\\":6,\\"hideAllLegends\\":false}"}'


print(type(json_new_dashboard))
print(type(json_new_dashboard), json_new_dashboard)

json_new_dashboard = json.load(json_new_dashboard)
print(type(json_new_dashboard), json_new_dashboard)

json_new_dashboard = json.dumps(json_new_dashboard)
print(type(json_new_dashboard), json_new_dashboard)





print(FULL_URL)


# headers = {'Content-type': 'application/json; charset=UTF-8'}
# r = requests.put(FULL_URL, data=json_new_dashboard, headers=headers)
#
#
# print("REQUEST:")
# pp(r.request.headers)
#
# print("RESPONSE:")
# pp(r.headers)
# print(r.text)
# print(r.status_code)
# print(r.json())





