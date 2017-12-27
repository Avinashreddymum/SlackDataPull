from slackclient import SlackClient
import time
import MySQLdb as mdb
from config import defaults
import config
from builtins import str

_servers = ("fd2a", "ff1a", "hh3b", "kw1a", "kw1b", "lo8a", "os5a", "os5b", "sg2a", "sg2b", 'sy1a', 'va1a', 'va1b')
_types = {"nfs":"FileStorage Premium", "cluster":"FileStorage Standard", "":"BlockStorage"}
_total_values = {"SVMs available": 4, "SVMs provisioned":5, "physical capacity":6, "available capacity":7, "IOPS available":8, "LUN size":9, "IOPS provisioned":10}


def parse(text):

    content = text.split("\n")

    rows = []

    row = []

    for line in content:
        line = line[:len(line)]

        if line.__contains__("Netapp Cluster"):
            row = []
            rows.append(row)
            hostname = line.strip().split(":")[1].strip()[1:-2]
            loc = hostname[:3]
            group = hostname[3]

            for key, val in _types.items():
                if str(line).__contains__(key):
                    menu = val
                    if key == "":
                        group = "a/b"  # set group a/b for FileStorage Standard
                    break

            row.append(menu)
            row.append(group)
            row.append(hostname)
            row.append("enabled")  # status
            [row.append("0") for i in range(0, 7)]  # append 0.00 rows

        elif line.__contains__("Total"):
            try:
                value = line.split(":")[1].strip()
                for key, val in _total_values.items():
                    if str(line).lower().__contains__(key.lower()) and not value == "":
                        row[val] = value
                        break
            except Exception:
                pass

    return rows


def create_and_populate(rows):

    con = mdb.connect(host=defaults.host, user=defaults.username, passwd=defaults.password, db=defaults.database)

    with con:
        cur = con.cursor()

        for row in rows:
            try:
                cur.execute(config.get_daily_slack_insert_query(row[2]), tuple(row))
            except Exception as e:
                print("row is not inserted" + str(row))
                print(e)


def main():
    slack_token = "API-Token"
    channel_name = 'Channel_Name'
    time_on_last_message = time.time()
    channel_id = ""
    ts = 0.000
    threshmins = 20
    channels_call = SlackClient(slack_token).api_call("channels.list")
    rows = []
    # print(channels_call)
    for channel in channels_call["channels"]:
        if channel["name"] == channel_name:
            channel_id = channel["id"]
            print(channel)

    print(channel_id)
    time_since_last_update = time.time() - time_on_last_message
    print("Waiting for new data....", time.time() - time_on_last_message)
    if time_since_last_update > threshmins * 60:
        pass

    sc = SlackClient(slack_token)

    data = sc.api_call(
        "channels.history",
        channel=channel_id,
        count=500,
    )

    if (data['ok'] == True):
        messages = data['messages']

        for message in reversed(messages):
            # print(message['ts'])
            if float(message['ts']) > ts:
                print("difference=", float(message['ts']) - ts)
                if float(message['ts']) - ts > (threshmins * 60):
                    print("greater diffrrece>reset................")

                time_on_last_message = time.time()

                ts = float(message['ts'])

                rows += parse(message['text'])

    else:
        print("No data returned or error")

    create_and_populate(rows)

    time.sleep(5)  # in Seconds
    print("process completed!")

main()
