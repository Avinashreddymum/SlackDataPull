import config
import MySQLdb as mdb
from config import defaults

locs = ["hh3", "sy1", "ff1", "os5", "fd2", "va1", "sg2", "kw1"]


def truncate_all_tables():

    con = mdb.connect(host=defaults.host, user=defaults.username, passwd=defaults.password, db=defaults.database)

    with con:
        cur = con.cursor()

        for row in locs:
            try:
                cur.execute("truncate {}_daily".format(row))
                cur.execute("truncate {}_realtime".format(row))
            except Exception as e:
                print("row is not truncated" + str(row))
                print(e)


def drop_all_tables():

    con = mdb.connect(host=defaults.host, user=defaults.username, passwd=defaults.password, db=defaults.database)

    with con:
        cur = con.cursor()

        for row in locs:
            try:
                cur.execute("drop table {}_daily".format(row))
                cur.execute("drop table {}_realtime".format(row))
            except Exception as e:
                print("row is not truncated" + str(row))
                print(e)
# truncate()



def create_all_slack_tables():
    con = mdb.connect(host=defaults.host, user=defaults.username, passwd=defaults.password, db=defaults.database)

    with con:
        cur = con.cursor()
        for row in locs:
            try:
                cur.execute(get_slack_daily_create_query(row).format(row))
                cur.execute(get_slack_realtime_create_query(row).format(row))
            except Exception as e:
                print("table not created" + str(row))
                print(e)



def get_slack_realtime_create_query(hostname):
    return config.get_query(hostname, config.defaults.slack_create_table_realtime, config.defaults.slack_create_table_realtime)


def get_slack_daily_create_query(hostname):
    return config.get_query(hostname, config.defaults.slack_create_table_daily, config.defaults.slack_create_table_daily)

#create_tables
#drop_all_tables()
create_all_slack_tables()

print("process completed!")


