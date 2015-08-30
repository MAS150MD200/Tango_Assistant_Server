__author__ = 'Antonio'

import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import re
import random

# CONSTANT VARIABLES.
USERNAME = "atsvetkov"
PASSWORD = "password"
# URL = "http://confluence.tango.corp/display/EN/Tango+Infrastructure+Naming+Convention"
# URL = "http://grafana.tangome.gbl/TAS/static/TangoInfrastructureNamingConventionEngineeringTango.htm"
URL = "http://127.0.0.1:8080/TAS/static/TangoInfrastructureNamingConventionEngineeringTango.htm"

"""
CUSTOM TAGS:

__regions<
>regions__

__sites<
>sites__

__environments<
>environments__

__clusters<
>clusters__

__serviceTypesApplication<
>serviceTypesApplication__

__serviceTypesMongo<
>serviceTypesMongo__

__serviceTypesHornetQMessageBroker<
>serviceTypesHornetQMessageBroker__

__serviceTypesElasticSearch<
>serviceTypesElasticSearch__

__cacheServiceTypesMemcachedRedis1<
>cacheServiceTypesMemcachedRedis1__

__cacheServiceTypesMemcachedRedis2<
>cacheServiceTypesMemcachedRedis2__

__serviceTypesDatabase<
>serviceTypesDatabase__
"""

def getContent(url, username, password):
    """
    TODO:
    check for exit code - response.status

    :param url:
    :param username:
    :param password:
    :return:
    """

    response = requests.get(url, auth=(username, password))
    return response.text


def htmlTableToDict(html_table):

    soup = BeautifulSoup(html_table, "html.parser")

    results = {}
    for row in soup.find_all('tr'):
        aux = row.find_all('td')
        try:
            # results[aux[0].text] = aux[1].text
            # to prevent duplicate keys.
            results[aux[0].text + str(random.randrange(100, 999))] = aux[1].text
        except Exception:
            pass

    # DEBUG.
    # pp(results)
    return results


def create_conventions_dict(html_content):

    convention_dict = {}
    soup = BeautifulSoup(html_content, "html.parser")

    # use my custom tag "__\w+<" to find all such tags.
    content_custom_tags = soup.find_all('span', string=re.compile("__\w+<"))

    for content_custom_tag in content_custom_tags:
        # find table just after my custom tag.
        table_content_bs4 = content_custom_tag.find_next('table')
        table_content_str = str(table_content_bs4)

        convention_dict[content_custom_tag.get_text()] = htmlTableToDict(table_content_str)

    # DEBUG.
    # pp(convention_dict)

    return convention_dict


def resolve_server_name(server_name):

    html_content = getContent(URL, USERNAME, PASSWORD)
    convention_dict = create_conventions_dict(html_content)

    server_name = str(server_name).strip()

    if re.search("^[a-z]{2}\d{4}$", server_name):
        server_name = server_name + "."*6
    elif re.search("^[a-z]+$", server_name):
        server_name = "."*6 + server_name + "."*3
    elif re.search("^[a-z]{2}\d{4}[a-z]+$", server_name):
        server_name = server_name + "."*3
    elif re.search("^[a-z]{3,5}\d{3}$", server_name):
        server_name = "."*6 + server_name
    elif re.search("^[a-z]{2}\d{4}[a-z]{3,5}\d{3}$", server_name):
        server_name = server_name
    else:
        server_name = "."*12

    host_name_dict = {"6Host Number" : server_name[-3:],
               "1Region" : server_name[:2],
               "2Site" : server_name[:4],
               "3Environment" : server_name[:6],
               "4Cluster" : server_name[:7],
               "5Service Type" : server_name[7:-3]
               }

    host_name_dict_result = {}

    for k1,v1 in host_name_dict.items():
        host_name_dict_result[k1] = []
        for k2, v2 in convention_dict.items():
            for k3,v3 in v2.items():
                if v1 == k3[:-3]:                   # remove random number.
                    # debug.
                    # print(k1, v1, k3, v3)
                    host_name_dict_result[k1].append(v3)
                elif (server_name[6] + v1) == k3[:-3]:   # (server_name[6] + v1) workaround for Service Types.
                    # debug.
                    # print(k1, v1, k3, v3)
                    host_name_dict_result[k1].append(v3)
        if not host_name_dict_result[k1]:
            host_name_dict_result[k1] = ["..."]

    host_name_dict_result["6Host Number"] = [server_name[-3:]]

    # DEBUG.
    # pp(host_name_dict_result)

    return(host_name_dict_result)


def main():

    test_name = "us0101bnq001"
    result = resolve_server_name(test_name)
    pp(result)


if __name__ == "__main__":
    main()