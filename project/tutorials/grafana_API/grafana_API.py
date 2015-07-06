__author__ = 'Antonio'

import requests
import json
import urllib.parse
from pprint import pprint as pp
#json_raw = '{ "user": "guest", "group": "guest", "title": "atsvetkov_test", "tags": [ ], "dashboard": "{\\"id\\":null,\\"title\\":\\"atsvetkov_test\\",\\"originalTitle\\":\\"New Dashboard\\",\\"tags\\":[],\\"style\\":\\"dark\\",\\"timezone\\":\\"browser\\",\\"editable\\":true,\\"hideControls\\":false,\\"sharedCrosshair\\":false,\\"rows\\":[{\\"title\\":\\"Row1\\",\\"height\\":\\"250px\\",\\"editable\\":true,\\"collapse\\":false,\\"panels\\":[{\\"title\\":\\"memcached\\",\\"error\\":false,\\"span\\":12,\\"editable\\":true,\\"type\\":\\"graph\\",\\"id\\":1,\\"datasource\\":null,\\"renderer\\":\\"flot\\",\\"x-axis\\":true,\\"y-axis\\":true,\\"y_formats\\":[\\"short\\",\\"short\\"],\\"grid\\":{\\"leftMax\\":null,\\"rightMax\\":null,\\"leftMin\\":null,\\"rightMin\\":null,\\"threshold1\\":null,\\"threshold2\\":null,\\"threshold1Color\\":\\"rgba(216, 200, 27, 0.27)\\",\\"threshold2Color\\":\\"rgba(234, 112, 112, 0.22)\\"},\\"lines\\":true,\\"fill\\":0,\\"linewidth\\":1,\\"points\\":false,\\"pointradius\\":5,\\"bars\\":false,\\"stack\\":false,\\"percentage\\":false,\\"legend\\":{\\"show\\":true,\\"values\\":false,\\"min\\":false,\\"max\\":false,\\"current\\":false,\\"total\\":false,\\"avg\\":false},\\"nullPointMode\\":\\"connected\\",\\"steppedLine\\":false,\\"tooltip\\":{\\"value_type\\":\\"cumulative\\",\\"shared\\":false},\\"targets\\":[{\\"target\\":\\"memcache.us0101mmb003.memcached.account_to_email.memcached_ops.hits\\"}],\\"aliasColors\\":{},\\"seriesOverrides\\":[],\\"links\\":[]}]}],\\"nav\\":[{\\"type\\":\\"timepicker\\",\\"enable\\":true,\\"status\\":\\"Stable\\",\\"time_options\\":[\\"5m\\",\\"15m\\",\\"1h\\",\\"6h\\",\\"12h\\",\\"24h\\",\\"2d\\",\\"7d\\",\\"30d\\"],\\"refresh_intervals\\":[\\"5s\\",\\"10s\\",\\"30s\\",\\"1m\\",\\"5m\\",\\"15m\\",\\"30m\\",\\"1h\\",\\"2h\\",\\"1d\\"],\\"now\\":true,\\"collapse\\":false,\\"notice\\":false}],\\"time\\":{\\"from\\":\\"now-6h\\",\\"to\\":\\"now\\"},\\"templating\\":{\\"list\\":[]},\\"annotations\\":{\\"list\\":[]},\\"refresh\\":false,\\"version\\":6,\\"hideAllLegends\\":false}"}'


#GLOBAL VARIABLES:
URL = "http://grafana.tangome.gbl:9200/grafana-dash/dashboard/"

jsonDashboard = """{
    "id": null,
    "title": "atsvetkov_test",
    "originalTitle": "NewDashboard",
    "tags": [],
    "style": "dark",
    "timezone": "browser",
    "editable": true,
    "hideControls": false,
    "sharedCrosshair": false,
    "rows": [
        {
            "title": "Row1",
            "height": "250px",
            "editable": true,
            "collapse": false,
            "panels": [
                {
                    "title": "memcached",
                    "error": false,
                    "span": 12,
                    "editable": true,
                    "type": "graph",
                    "id": 1,
                    "datasource": null,
                    "renderer": "flot",
                    "x-axis": true,
                    "y-axis": true,
                    "y_formats": [
                        "short",
                        "short"
                    ],
                    "grid": {
                        "leftMax": null,
                        "rightMax": null,
                        "leftMin": null,
                        "rightMin": null,
                        "threshold1": null,
                        "threshold2": null,
                        "threshold1Color": "rgba(216,200,27,0.27)",
                        "threshold2Color": "rgba(234,112,112,0.22)"
                    },
                    "lines": true,
                    "fill": 0,
                    "linewidth": 1,
                    "points": false,
                    "pointradius": 5,
                    "bars": false,
                    "stack": false,
                    "percentage": false,
                    "legend": {
                        "show": true,
                        "values": false,
                        "min": false,
                        "max": false,
                        "current": false,
                        "total": false,
                        "avg": false
                    },
                    "nullPointMode": "connected",
                    "steppedLine": false,
                    "tooltip": {
                        "value_type": "cumulative",
                        "shared": false
                    },
                    "targets": [
                        {
                            "target": "memcache.us0101mmb003.memcached.account_to_email.memcached_ops.hits"
                        }
                    ],
                    "aliasColors": {},
                    "seriesOverrides": [],
                    "links": []
                }
            ]
        }
    ],
    "nav": [
        {
            "type": "timepicker",
            "enable": true,
            "status": "Stable",
            "time_options": [
                "5m",
                "15m",
                "1h",
                "6h",
                "12h",
                "24h",
                "2d",
                "7d",
                "30d"
            ],
            "refresh_intervals": [
                "5s",
                "10s",
                "30s",
                "1m",
                "5m",
                "15m",
                "30m",
                "1h",
                "2h",
                "1d"
            ],
            "now": true,
            "collapse": false,
            "notice": false
        }
    ],
    "time": {
        "from": "now-6h",
        "to": "now"
    },
    "templating": {
        "list": []
    },
    "annotations": {
        "list": []
    },
    "refresh": false,
    "version": 6,
    "hideAllLegends": false
}"""


json_main = """{
    "user": "guest",
    "group": "guest",
    "title": "atsvetkov_test",
    "tags": [],
    "dashboard": "jsonDashboard"
}"""


def createDashboard(dashboard_name, metric_name):

    full_url = urllib.parse.urljoin(URL, dashboard_name)

    #JSON str -> DICT.
    json_main_dict = json.loads(json_main)
    #JSON str -> DICT.
    jsonDashboard_dict = json.loads(jsonDashboard)

    #Modify metric in the dashboard dictionary.
    jsonDashboard_dict["rows"][0]["panels"][0]["targets"][0]["target"] = metric_name

    #Change JSON format for Python + Elasticserach API.
    jsonDashboard_str = json.dumps(jsonDashboard_dict)
    jsonDashboard_str = jsonDashboard_str.replace('"', '\"')

    #Insert dashboard dictionary to the json_main_dict.
    json_main_dict["dashboard"] = jsonDashboard_str

    #DICT -> JSON str.
    json_main_modified = json.dumps(json_main_dict)

    #Change JSON format for Python + Elasticserach API.
    json_main_modified = json_main_modified.replace('\\"', '\\\"')
    json_main_modified = json_main_modified.replace(' ', '')
    # print(json_main_modified)


    headers = {'Content-type': 'application/json; charset=utf-8'}
    r = requests.put(full_url, data=json_main_modified, headers=headers)

    #DEBUG
    # print("REQUEST:")
    # pp(r.request.headers)
    #
    # print("RESPONSE:")
    # pp(r.headers)
    # print(r.text)
    # print(r.status_code)
    # print(r.json())

    return r.status_code

def main():
    dashboard = "atsvetkov_test"
    new_dashboard_metric = "memcache.us0101mmb001.memcached.account_to_email.memcached_ops.hits"

    createDashboard(dashboard, new_dashboard_metric)
    pass

if __name__ == "__main__":
    main()



