__author__ = 'atsvetkov'

from sqlalchemy import *
import datetime
from pprint import pprint as pp
import config

DB_CONN_DICT = config.DB_CONN_DICT


def get_result_proxy(db_conn_dict=DB_CONN_DICT, appname=None):
    # appname - is not used in this function.

    db = create_engine('mysql://{0[USER]}:{0[PASSWORD]}@{0[DB_HOST_TUNNEL]}/{0[DB_NAME]}'.format(db_conn_dict),
                       echo=True)

    metadata = MetaData()
    metadata.bind = db

    ver_hist_table = Table(DB_CONN_DICT["TABLE_NAME"], metadata, autoload=True)

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


def result_proxy_to_list(result_proxy = None):
    result_list = []
    for row in result_proxy:
        result_list.append([row.APPLICATION_NAME,
                            row.SERVER_NAME,
                            row.VERSION,
                            row.MAX_TIMESTAMP])

    # DEBUG.
    # pp(result_list)

    return result_list


def qa_tool_get_result(appname=None):
    """
    MAIN FUNCTION.

    :param appname:
    :return:
    """

    # TODO: add comments to this function.

    # get raw result object:
    result_proxy = get_result_proxy(appname="abregistrar")

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

    return result_proxy_list, appnames


def main():
    result_proxy_list, appnames = qa_tool_get_result(appname="facilitator")
    pp(appnames)
    pp(result_proxy_list)

if __name__ == "__main__":
    main()


