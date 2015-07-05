__author__ = 'Antonio'

import requests
import json
from pprint import pprint as pp


URL = "http://grafana.tangome.gbl/api/dashboards/db/"

json_new_dashboard = """ { "dashboard": { "id": null, "title": "Production Overview", "tags": [ "templated" ], "timezone": "browser", "rows": [ { } ] "schemaVersion": 6, "version": 0 }, "overwrite": false }"""
pp(json_new_dashboard)
print(json.dumps(json_new_dashboard))


r = requests.post(URL, data=json.dumps(json_new_dashboard))
print(r.text)
print(r.status_code)
print(r.headers)
print(r.json())





