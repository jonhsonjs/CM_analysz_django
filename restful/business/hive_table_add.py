# -*- coding:utf-8 -*-
from impala.dbapi import connect
import sys
import datetime


today = datetime.date.today()
today_string = today.strftime('%Y-%m-%d')
one_Day_Ago = (today - datetime.timedelta(days=1)).strftime('%Y-%m-%d')  # 前一天

cmd_table_today = "select * from idc_infrastructure_db.hive_table_info_all_daily where dt='"+today_string+"'"
cmd_table_yesterday = "select * from idc_infrastructure_db.hive_table_info_all_daily where dt='"+one_Day_Ago+"'"
cmd_db_today = "select * from idc_infrastructure_db.hive_db_info_all_daily where dt='"+today_string+"'"
cmd_db_yesterday = "select * from idc_infrastructure_db.hive_db_info_all_daily where dt='"+one_Day_Ago+"'"


def query_hive_table(command):
    print 123
    conn = connect(host='***', port=21050, user='***', password='***', auth_mechanism="PLAIN")
    cur = conn.cursor()
    cur.execute(command)
    rows = cur.fetchall()
    hive_db_name_list = []
    hive_table_info = []
    for row in rows:
        hvie_table_dict = {}
        hive_db_name_list.append(row[0])
        hvie_table_dict[row[1]] = row
        hive_table_info.append(hvie_table_dict)
    return (hive_db_name_list, hive_table_info)


def query_hive_db(command):
    conn = connect(host='***', port=21050, user='***', password='***', auth_mechanism="PLAIN")
    cur = conn.cursor()
    cur.execute(command)
    rows = cur.fetchall()
    hive_db_info = []
    for row in rows:
        hive_db_dict = {}
        hive_db_dict[row[0]] = row
        hive_db_info.append(hive_db_dict)
    return hive_db_info


def get_summer_add_hive_info(info_today, info_yesterday):
    adding_info = []
    add_db_list = []
    add_table_list = []
    db_list_today = list(set(info_today[0]))
    table_dict_today = info_today[1]
    db_list_yesterday = list(set(info_yesterday[0]))
    table_dict_yesterday = info_yesterday[1]
    for today in db_list_today:
        if today not in db_list_yesterday:
            add_db_list.append(today)
    adding_info.append(['database', len(db_list_today), len(db_list_yesterday), len(add_db_list)])
    table_list_today = []
    table_list_yesterday = []
    for table in table_dict_today:
        for key in table:
            table_list_today.append(key)
    for table in table_dict_yesterday:
        for key in table:
            table_list_yesterday.append(key)
    for table in table_list_today:
        if table not in table_list_yesterday:
            add_table_list.append(table)
    adding_info.append(['table', len(table_list_today), len(table_list_yesterday), len(add_table_list)])
    return adding_info


def get_query_db_add(info_today, info_yesterday):
    add_db_info = []
    add_db_list = []
    db_list_today = []
    db_list_yesterday = []
    for info in info_today:
        for key in info:
            db_list_today.append(key)
    for info in info_yesterday:
        for key in info:
            db_list_yesterday.append(key)
    for db in db_list_today:
        if db not in db_list_yesterday:
            add_db_list.append(db)
    for info in info_today:
        for key in info:
            if key in add_db_list:
                add_db_info.append(info.get(key))
    return add_db_info


def get_query_table_add(tupe_today, tupe_yesterday):
    add_table_info = []
    add_table_list = []
    table_list_today = []
    table_list_yesterday = []
    hive_table_info_today = tupe_today[1]
    hive_table_info_yesterday = tupe_yesterday[1]
    for table in hive_table_info_today:
        for key in table:
            table_list_today.append(key)
    for table in hive_table_info_yesterday:
        for key in table:
            table_list_yesterday.append(key)
    for today in table_list_today:
        if today not in table_list_yesterday:
            add_table_list.append(today)
    for info in hive_table_info_today:
        for key in info:
            if key in add_table_list:
                add_table_info.append(info[key])
    return add_table_info

hive_tbl_today = query_hive_table(cmd_table_today)
hive_tbl_yesterday = query_hive_table(cmd_table_yesterday)
hive_db_today = query_hive_db(cmd_db_today)
hive_db_yesterday = query_hive_db(cmd_db_yesterday)


def generate_summer_hive_info():
    hive_summer_info = []
    adding_info = get_summer_add_hive_info(hive_tbl_today, hive_tbl_yesterday)
    for info in adding_info:
        hive_summer_info.append(
            {
                "variety": info[0],
                "todayNum": info[1],
                "yesterdayNum": info[2],
                "adding": info[3]
            }
        )
    return hive_summer_info


def generate_db_info():
    hive_db_info_add = []
    add_db_info = get_query_db_add(hive_db_today, hive_db_yesterday)
    if add_db_info:
        for info in add_db_info:
            hive_db_info_add.append(
                {
                    "db_name": info[0],
                    "db_owner": info[1],
                    "db_location": info[2],
                    "db_createTime": info[3]
                }
            )
    return hive_db_info_add


def generate_table_info():
    hive_table_info_add = []
    hive_tbl_today = query_hive_table(cmd_table_today)
    hive_tbl_yesterday = query_hive_table(cmd_table_yesterday)
    add_table_info = get_query_table_add(hive_tbl_today, hive_tbl_yesterday)
    for add in add_table_info:
        hive_table_info_add.append(
            {
                "db_name": add[0],
                "tbl_name": add[1],
                "tbl_owner": add[2],
                "tbl_location": add[3],
                "uotput_format": add[4]
            }
        )
    return hive_table_info_add


def main(argv):
    t = generate_summer_hive_info()
    # y = generate_table_info()
    z = generate_db_info()

    print t


if __name__ == '__main__':
    sys.exit(main(sys.argv))