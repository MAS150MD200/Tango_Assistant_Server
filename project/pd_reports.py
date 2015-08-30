__author__ = 'Antonio'

import requests
import re
import name_resolver_se
# import arrow
# from datetime import datetime
from pprint import pprint as pp

"""
curl -H "Content-type: application/json" -H "Authorization: Token token=VCRX6FPqypcrDqw1DGP3" -X GET -G \
    --data-urlencode "since=2015-08-16" \
    --data-urlencode "until=2015-08-19" \
    --data-urlencode "sort_by=created_on" \
    --data-urlencode "limit=300" \
    --data-urlencode "offset=0" \
    --data-urlencode "fields=incident_number,status,created_on,html_url,last_status_change_by,last_status_change_on,trigger_summary_data" \
    "https://tango.pagerduty.com/api/v1/incidents"
"""


def get_incidents(time_since, time_until):

    # TODO:
    # simple time parse:
    # pass


    URL = "https://tango.pagerduty.com/api/v1/incidents"
    TOKEN = "VCRX6FPqypcrDqw1DGP3"
    HEADERS = {'Content-type': 'application/json',
           'Authorization': 'Token token={0}'.format(TOKEN)}

    PAYLOAD = {'since': time_since,  # '2015-08-16T09:55:30Z'
           'until': time_until,  # '2015-08-17T09:55:30Z'
           'sort_by': 'created_on',
           'limit': 100,    #max
           'offset': 0,
           'fields': 'incident_number,incident_key,status,created_on,html_url,last_status_change_by,last_status_change_on,trigger_summary_data'}

    r = requests.get(URL, headers=HEADERS, params=PAYLOAD)
    # debug.
    # pp(r.json())
    return r.json()


def make_incidents_dict(incidents_list):
    """

    :param incidents_list:
[{'created_on': '2015-08-16T09:55:30Z',
  'html_url': 'https://tango.pagerduty.com/incidents/PU70XB6',
  'incident_key': 'event_source=service;host_name=sg0101asw122692201412130011172030000225;service_desc=Free '
                  'Memory',
  'incident_number': 115940,
  'last_status_change_by': None,
  'last_status_change_on': '2015-08-16T09:57:20Z',
  'status': 'resolved',
  'trigger_summary_data': {'HOSTNAME': 'sg0101asw122692201412130011172030000225',
                           'SERVICEDESC': 'Free Memory',
                           'SERVICESTATE': 'CRITICAL',
                           'pd_nagios_object': 'service',
                           'subject': 'sg0101asw122692201412130011172030000225 '
                                      'Free Memory (CRITICAL)'}},
 {'created_on': '2015-08-16T10:35:41Z',
  'html_url': 'https://tango.pagerduty.com/incidents/PV5SRJ3',
  'incident_key': '/Alert/314108/15935436/4064615',
  'incident_number': 115941,
  'last_status_change_by': None,
  'last_status_change_on': '2015-08-16T10:40:24Z',
  'status': 'resolved',
  'trigger_summary_data': {'client': 'New Relic',
                           'client_url': 'https://rpm.newrelic.com/accounts/314108/incidents/15935436',
                           'description': 'Alert open: Error rate > 5.0% - '
                                          'App: Music-Pix-Labs - Policy: '
                                          'Music-Pix'}},
 {'created_on': '2015-08-16T10:52:25Z',
  'html_url': 'https://tango.pagerduty.com/incidents/PXAIELQ',
  'incident_key': '/Alert/314108/15935624/4064615',
  'incident_number': 115942,
  'last_status_change_by': None,
  'last_status_change_on': '2015-08-16T11:05:35Z',
  'status': 'resolved',
  'trigger_summary_data': {'client': 'New Relic',
                           'client_url': 'https://rpm.newrelic.com/accounts/314108/incidents/15935624',
                           'description': 'Alert open: Error rate > 5.0% - '
                                          'App: Music-Pix-Labs - Policy: '
                                          'Music-Pix'}},


    :return(TUPLE OF (incidents_dict, uniq_incidents_numbers_list)):
{115940: {'created_on': '2015-08-16T09:55:30Z',
          'html_url': 'https://tango.pagerduty.com/incidents/PU70XB6',
          'incident_key': 'event_source=service;host_name=sg0101asw122692201412130011172030000225;service_desc=Free '
                          'Memory',
          'incident_number': 115940,
          'last_status_change_by': None,
          'last_status_change_on': '2015-08-16T09:57:20Z',
          'status': 'resolved',
          'trigger_summary_data': {'HOSTNAME': 'sg0101asw122692201412130011172030000225',
                                   'SERVICEDESC': 'Free Memory',
                                   'SERVICESTATE': 'CRITICAL',
                                   'pd_nagios_object': 'service',
                                   'subject': 'sg0101asw122692201412130011172030000225 '
                                              'Free Memory (CRITICAL)'}},
 115941: {'created_on': '2015-08-16T10:35:41Z',
          'html_url': 'https://tango.pagerduty.com/incidents/PV5SRJ3',
          'incident_key': '/Alert/314108/15935436/4064615',
          'incident_number': 115941,
          'last_status_change_by': None,
          'last_status_change_on': '2015-08-16T10:40:24Z',
          'status': 'resolved',
          'trigger_summary_data': {'client': 'New Relic',
                                   'client_url': 'https://rpm.newrelic.com/accounts/314108/incidents/15935436',
                                   'description': 'Alert open: Error rate '
                                                  '> 5.0% - App: '
                                                  'Music-Pix-Labs - '
                                                  'Policy: Music-Pix'}},
 115942: {'created_on': '2015-08-16T10:52:25Z',
          'html_url': 'https://tango.pagerduty.com/incidents/PXAIELQ',
          'incident_key': '/Alert/314108/15935624/4064615',
          'incident_number': 115942,
          'last_status_change_by': None,
          'last_status_change_on': '2015-08-16T11:05:35Z',
          'status': 'resolved',
          'trigger_summary_data': {'client': 'New Relic',
                                   'client_url': 'https://rpm.newrelic.com/accounts/314108/incidents/15935624',
                                   'description': 'Alert open: Error rate '
                                                  '> 5.0% - App: '
                                                  'Music-Pix-Labs - '
                                                  'Policy: Music-Pix'}},


[[115940], [115948, 115951, 115953], [115954], [115957]]

    """
    incidents_dict = {}
    incidents_group_dict = {}

    for incident in incidents_list:
        # ignore Music-PIX.
        if incident['trigger_summary_data'].get('description'):
            if "Music-Pix" in incident['trigger_summary_data']['description']:
                continue

        # add incident to dictionary.
        incidents_dict[incident['incident_number']] = incident

        # create incidents group dictionary.
        if incident['incident_key'] not in incidents_group_dict:
            incidents_group_dict[incident['incident_key']] = []

        incidents_group_dict[incident['incident_key']].append(incident['incident_number'])

    # extract list of incidents numbers from incidents_group_dict.
    uniq_incidents_numbers_list = []
    [uniq_incidents_numbers_list.append(inc_num_list) for inc_num_list in incidents_group_dict.values()]
    uniq_incidents_numbers_list = sorted(uniq_incidents_numbers_list, key=lambda x: x[0])

    # debug.
    # pp(incidents_dict)
    # pp(uniq_incidents_numbers_list)

    return incidents_dict, uniq_incidents_numbers_list


def generate_report_list(incidents_dict, group_incidents):

    # result report list.
    report_list = []

    # get total number of incidents:
    inc_cntr = 0
    for inc in group_incidents:  # element of group_incidents could be a list too.
        if isinstance(inc, list):
            inc_cntr += len(inc)
        else:
            inc_cntr += 1

    # REPORT HEADER:
    report_list.append("Total number of incidents: {0}\n".format(inc_cntr))
    report_list.append("Action items for next shift: None\n")

    # iterate over group_incidents list:
    service_names_dict = {}  # this will act like a cache for service name resolver.
    for num, incident_numbers in enumerate(group_incidents, 1):

        # one if result report item:
        group_incidents_txt = ",".join(map(str, incident_numbers))  # list of inc_num to string with "," as a delimiter.

        # parse details(trigger_summary_data) section:
        trigger_summary_data = incidents_dict[incident_numbers[0]]['trigger_summary_data']
        hostname_txt = ""
        servicename_txt = ""
        for k, v in trigger_summary_data.items():
            if k in ["subject"]:  # alert from nagios.
                description_txt = v
            elif k in ["HOSTNAME"]:  # alert from nagios.
                hostname_txt = v
            elif k in ["description"]:  # alert from NewRelic.
                description_txt = v

                # get ecomm hostname.
                new_relic_host = re.search(r'(ip-\d{1,3}-\d{1,3}-\d{1,3}-\d{1,3})', v)
                hostname_txt = new_relic_host.group(0) if new_relic_host else hostname_txt

                # get ecomm service name.
                ecomm_service = re.search(r'(eCommerce-\w*)', v)
                servicename_txt = ecomm_service.group(0) if ecomm_service else servicename_txt

            # try to resolve hostname.
            # hostname could be like "us0101abs001" or "us0101abs001.tangome.gbl" or "ip-172-16-148-51" or None or something else.
            if hostname_txt:
                # hostname_parts = re.search(r'(\w{2})(\d{4})(\w{1,5})(\d{3}).*', hostname_txt)
                hostname_parts = re.search(r'([a-z]{2})(\d{4})([a-z]{1,5})(\d+).*', hostname_txt)

                if hostname_parts:
                    service_part = hostname_parts.group(3)
                    print(service_part)


                    # try to use cache:
                    if service_part in service_names_dict:
                        servicename_txt = service_names_dict[service_part]
                    # ask resolver:
                    else:
                        try:
                            service_names_dict[service_part] = name_resolver_se.resolve_server_name(service_part)['5Service Type'][0]
                            servicename_txt = service_names_dict[service_part]
                        except Exception:
                            service_names_dict[service_part] = ""

                    # debug.
                    # pp(service_names_dict)
                    # print(servicename_txt)

        # BEGIN PRETTY PRINTING:
        report_list.append("-" * 100)
        report_list.append("{0}) Incident(s) number: {1}".format(num, group_incidents_txt))
        report_list.append("Opened on: {0}".format(incidents_dict[incident_numbers[0]]['created_on']))
        report_list.append("Description: {0}".format(description_txt))

        report_list.append("Host: {0}".format(hostname_txt))
        report_list.append("Service: {0}".format(servicename_txt))

        report_list.append("Status: {0}".format(incidents_dict[incident_numbers[0]]['status']))

        # last_status_change_by = incidents_dict[incident_numbers[0]]['last_status_change_by']['name'] if incidents_dict[incident_numbers[0]]['last_status_change_by'] else 'auto'
        # report_list.append("Last status changed by: {0}".format(last_status_change_by))
        # report_list.append("Last status changed on: {0}".format(incidents_dict[incident_numbers[0]]['last_status_change_on']))
        # report_list.append("Details:")

        report_list.append("PD link: {0}".format(incidents_dict[incident_numbers[0]]['html_url']))

        report_list.append('Details: None')
        report_list.append('Ticket number: None')
        report_list.append('Next actions: None')

    report_list.append("-" * 100)

    return report_list


def get_report(time_since, time_until):
    incidents_obj = get_incidents(time_since, time_until)
    incidents_list = incidents_obj['incidents']
    incidents_dict, group_incidents = make_incidents_dict(incidents_list)
    report_list = generate_report_list(incidents_dict, group_incidents)
    return report_list


def main():

    time_since = '2015-08-26 05:00:00Z'
    time_until = '2015-08-26 18:00:00Z'

    for line in get_report(time_since, time_until):
        print(line)

if __name__ == "__main__":
    main()
