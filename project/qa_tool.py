__author__ = 'atsvetkov'

from sqlalchemy import *
import datetime
from pprint import pprint as pp
import config

DB_CONN_DICT = config.DB_CONN_DICT


def connect_to_db_table(db_conn_dict=DB_CONN_DICT, db_table=None):
    """
    Perform connection to DB table.

    :param db_conn_dict:
    :param db_table:
    :return:
    """

    db = create_engine('mysql://{0[USER]}:{0[PASSWORD]}@{0[DB_HOST_TUNNEL]}/{0[DB_NAME]}'.format(db_conn_dict),
                       echo=False)

    metadata = MetaData()
    metadata.bind = db

    act_hist_table = Table(DB_CONN_DICT[db_table], metadata, autoload=True)

    return db


def get_result_proxy(db_conn_dict=DB_CONN_DICT):

    # s = select([
    #     ver_hist_table.c.appname.label('APPLICATION_NAME'),
    #     ver_hist_table.c.servername.label('SERVER_NAME'),
    #     ver_hist_table.c.version.label('VERSION'),
    #     func.max(ver_hist_table.c.timestamp).label('MAX_TIMESTAMP')]). \
    #     where(ver_hist_table.c.appname == appname). \
    #     group_by('SERVER_NAME'). \
    #     order_by(asc('APPLICATION_NAME'), desc('VERSION'), asc('SERVER_NAME'))

    # s = select([
    #     ver_hist_table.c.appname.label('APPLICATION_NAME'),
    #     ver_hist_table.c.servername.label('SERVER_NAME'),
    #     ver_hist_table.c.version.label('VERSION'),
    #     func.max(ver_hist_table.c.timestamp).label('MAX_TIMESTAMP')]). \
    #     group_by('SERVER_NAME'). \
    #     order_by(asc('APPLICATION_NAME'), desc(ver_hist_table.c.version * 1), asc('SERVER_NAME'))   # workaround for numeric sorting.

    # DEBUG.
    # print(s)

    # get ResultProxy object:
    # rs = s.execute()

    db = connect_to_db_table(db_table="TABLE_NAME_VERS_HIST")

    # get ResultProxy object:
    rs = db.execute("SELECT\
     t1.appname as APPLICATION_NAME,\
     t1.servername as SERVER_NAME,\
     t1.version as VERSION,\
     t1.timestamp as MAX_TIMESTAMP\
     FROM versionhistory as t1\
     INNER JOIN (SELECT t2.servername, MAX(t2.timestamp) as max_timestamp FROM versionhistory as t2 GROUP BY t2.servername) AS moe\
     ON t1.servername = moe.servername AND t1.timestamp = moe.max_timestamp\
     GROUP BY t1.servername ORDER BY t1.appname, t1.timestamp DESC")

    # DEBUG.
    # for row in rs:
    #     print(dict(row))

    return rs


def result_proxy_to_list(result_proxy=None):
    result_list = []
    for row in result_proxy:
        result_list.append([row.APPLICATION_NAME,
                            row.SERVER_NAME,
                            row.VERSION,
                            str(row.MAX_TIMESTAMP)])

    # DEBUG.
    # pp(result_list)

    return result_list


def get_full_build_name_v3(db_conn_dict=DB_CONN_DICT, appname=None, servername=None, version=None):
    """
    Get full build name from actionhistory table, by appname and version.

    :return:
    """

    db = connect_to_db_table(db_table="TABLE_NAME_ACT_HIST")

    # generate table with max_id column - means final successful deploy for current server:
    # {'max_id': 100709, 'targetapplication': 'facilitator', 'targetserver': 'us0101afc001'}
    max_id_tbl_query = db.execute('select max(ah.id) as max_id, ah.targetapplication, ah.targetserver from actionhistory ah where\
    targetserver = "{1}" and\
    appname = "deploy" and\
    actionname = "deploy" and\
    actionresult = "OK" and\
    actiondata = "puppet_helper deploy {0}"'.format(appname, servername))

    max_id_tbl_query_fetch = max_id_tbl_query.fetchone()
    max_id = max_id_tbl_query_fetch[0] if max_id_tbl_query_fetch else None

    # DEBUG:
    # print("max_id")
    # pp(max_id)

    try:
        full_build_name_query = db.execute('select ah.actiondata from\
        actionhistory ah inner join (select max(id) as max_id from actionhistory where\
        id < {0} and\
        appname = "prestage" and\
        actionname = "getbuild" and\
        actiondata LIKE "%%.{1}-%%" and\
        actionresult = "OK") t_max_id on ah.id = t_max_id.max_id'.format(max_id, version))
    except Exception:
        return "No information in DB"

    full_build_name_query_fetch = full_build_name_query.fetchone()
    full_build_name = full_build_name_query_fetch[0] if full_build_name_query_fetch else None

    # DEBUG:
    # pp(full_build_name)


    return full_build_name


def qa_tool_get_result(appname=None):
    """
    MAIN FUNCTION.

    :param appname:
    :return:
    """

    # TODO: add comments to this function.

    # prepare result list:
    result_proxy_list_w_full_vers = []

    # get raw result object:
    result_proxy = get_result_proxy()

    # convert result_proxy to list:
    result_proxy_list = result_proxy_to_list(result_proxy=result_proxy)
    # DEBUG.
    # pp(result_proxy_list)

    # get app names list from result_proxy_list:
    appnames = [app_list[0] if app_list[0].startswith("database") else " "+app_list[0] for app_list in result_proxy_list]
    appnames = set(appnames)
    appnames = sorted(list(appnames))
    # DEBUG.
    # pp(appnames)

    # filter result_proxy_list if necessary:
    if appname == "empty":
        result_proxy_list = []
    elif appname:
        result_proxy_list_filtered = list(filter(lambda x: x[0] == appname.strip(), result_proxy_list))
        result_proxy_list = result_proxy_list_filtered

        # insert full build name:
        for app_data in result_proxy_list:
            app = app_data[0]
            srv_name = app_data[1]
            short_vers = app_data[2]

            full_vers = get_full_build_name_v3(appname=app, servername=srv_name, version=short_vers)
            # DEBUG:
            # print(full_vers)

            app_data.insert(3, full_vers)
            result_proxy_list_w_full_vers.append(app_data)

    return result_proxy_list_w_full_vers, appnames


def main():

    # full_build_name_dict = get_full_build_name_v3(appname="discovery", servername="us0101adi001", version="181101")
    # pp(full_build_name_dict)

    result_proxy_list, appnames = qa_tool_get_result(appname="discovery")
    pp(appnames)
    pp(result_proxy_list)


if __name__ == "__main__":
    main()


