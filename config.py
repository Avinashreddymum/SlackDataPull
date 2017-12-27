class defaults:
    host = 'localhost'
    username = 'root'
    password = 'redhat'
    database = 'storage_report'


    realtime_truncate_query = "TRUNCATE {}_realtime"

    slack_create_table_daily = "CREATE TABLE `{}_daily` ( " + \
        "`timestamp` DATE NOT NULL, `menu` VARCHAR(20) NOT NULL, `group_name` VARCHAR(10) NOT NULL , `hostname` VARCHAR(20) NOT NULL ," + \
        "`status` VARCHAR(20) NOT NULL , `SVMs_available` VARCHAR(20) NOT NULL , " + \
        "`SVMs_provisioned` DOUBLE NOT NULL , `capacity_physical` DOUBLE NOT NULL, " + \
        "`capacity_available` DOUBLE NOT NULL , `IOPS_available` DOUBLE NOT NULL, "  + \
        "`LUNsize_provisioned` DOUBLE NOT NULL , `IOPS_provisioned` DOUBLE NOT NULL ) " + \
        " ENGINE = InnoDB COMMENT = 'daily slack chasis table'; "

    slack_create_table_realtime = "CREATE TABLE `{}_realtime` ( " + \
        "`menu` VARCHAR(20) NOT NULL, `group_name` VARCHAR(10) NOT NULL , `hostname` VARCHAR(20) NOT NULL ," + \
        "`status` VARCHAR(20) NOT NULL , `SVMs_available` VARCHAR(20) NOT NULL , " + \
        "`SVMs_provisioned` DOUBLE NOT NULL , `capacity_physical` DOUBLE NOT NULL, " + \
        "`capacity_available` DOUBLE NOT NULL , `IOPS_available` DOUBLE NOT NULL, "  + \
        "`LUNsize_provisioned` DOUBLE NOT NULL , `IOPS_provisioned` DOUBLE NOT NULL ) " + \
        " ENGINE = InnoDB COMMENT = 'daily slack chasis table'; "

    daily_slack_insert_query = "INSERT INTO `{}_daily` (`timestamp`, `menu`, `group_name`, `hostname`, `status`," + \
         "`SVMs_available`, `SVMs_provisioned`, `capacity_physical`, `capacity_available`, `IOPS_available`," + \
         "`LUNsize_provisioned`, `IOPS_provisioned`) VALUES (CURDATE(), %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "

    realtime_slack_insert_query = "INSERT INTO `{}_realtime` (`menu`, `group_name`, `hostname`, `status`," + \
         "`SVMs_available`, `SVMs_provisioned`, `capacity_physical`, `capacity_available`, `IOPS_available`," + \
         "`LUNsize_provisioned`, `IOPS_provisioned`) VALUES ( %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "




_flavour_dict = { "oracle-se2" : 'oracle-se2',
                 "oracle-se2-windows" : 'oracle-se2',
                 "oracle-se2-rhel" : 'oracle-se2',
                 "oracle-ee2" : 'oracle-ee2',
                 "oracle-ee2-windows" : 'oracle-ee2',
                 "oracle-ee2-rhel" : 'oracle-ee2',
                 }


def get_flavor(string):
    try:
        if string.__contains__('('):
            string = string[:string.index('(')]

        value = _flavour_dict[string.lower()]
        if not value == '':
            return value
    except Exception as e:
        # print(e)
        pass

    return string


def get_query(hostname, kw_query, default_query):
    try:
        query = ''
        loc = hostname.lower()[:3]
        if (loc == 'kw1'):
            query = kw_query
        elif (loc == 'hh3' or loc == 'lo8'):
            query = default_query.format("hh3")
        else:
            query = default_query.format(loc)
    except Exception as e:
        # print(e)
        pass

    return query




def get_realtime_slack_truncate_query(hostname):
    return get_query(hostname, defaults.realtime_slack_truncate_query.format("kw1"), defaults.realtime_slack_truncate_query)


def get_daily_slack_insert_query(hostname):
    return get_query(hostname, defaults.daily_slack_insert_query.format("kw1"), defaults.daily_slack_insert_query)


def get_realtime_slack_insert_query(hostname):
    return get_query(hostname, defaults.realtime_slack_insert_query.format("kw1"), defaults.realtime_slack_insert_query)
