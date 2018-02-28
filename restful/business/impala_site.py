# -*- coding:utf-8 -*-
import inspect
import logging
import os
import sys
import textwrap

#
# Customize these constants for your Cloudera Manager.
#
from cm_api.endpoints.services import get_service

from restful.business.hive_site import do_get_hive_top_email
from restful.common.api_client import ApiClient
from restful.common.timeseries import do_query
from restful.util.chart_util import pie_charts
from restful.util.date_util import get_last_week_to, get_now, zone_conversion_date_format, get_one_day_ago_from, \
    get_n_day_ago_from, zone_conversion

LOG = logging.getLogger(__name__)

IMPALA_QUERY = "select query_duration from IMPALA_QUERIES where service_name = impala and query_duration >= %s"


class ImpalaInfo(ApiClient):
    """

    """

    def get_top_user_demo(self):
        return get_service(self._api, cluster_name="cluster", name="impala").get_impala_queries(
            start_time=get_n_day_ago_from(n=1), end_time=get_now(), filter_str="")


def do_get_impala_top(from_time=get_last_week_to(), to_time=get_now(), duration=300000.0):
    attrs = ['user', 'database', 'query_duration', 'thread_cpu_time', 'category', 'executing', 'service_name',
             'coordinator_host_id', 'stats_missing', 'statement', 'entityName', 'pool']
    responses = do_query(IMPALA_QUERY % duration, from_time, to_time)
    massage_dfs = []
    for response in responses:
        if response.timeSeries:
            for ts in response.timeSeries:
                metadata = ts.metadata
                line = {}
                if metadata.attributes:
                    for attr in attrs:
                        if attr in metadata.attributes:
                            attr_val = metadata.attributes[attr]
                            if attr == 'query_duration':
                                line['query_duration1'] = int(attr_val)
                                if int(attr_val) > 60 * 60 * 1000:
                                    attr_val = ('%.2f' % (float(attr_val) / 60 / 60 / 1000)) + "h"
                                elif int(attr_val) > 60 * 1000:
                                    attr_val = str(int(attr_val) / 60 / 1000) + "m"  # 分
                                elif int(attr_val) > 1000:
                                    attr_val = str(int(attr_val) / 1000) + "s"  # 秒
                                line[attr] = attr_val
                                continue
                            line[attr] = attr_val
                for data in ts.data:
                    line['time'] = zone_conversion(timestamp=data.timestamp, format=u'YYYY-MM-DD HH:mm:ss')
                massage_dfs.append(line)
    return sorted(massage_dfs, key=lambda t: t['query_duration1'], reverse=True)


def do_get_impala_top_email(from_time=get_last_week_to(), to_time=get_now(), duration=300000.0):
    top_list = do_get_impala_top(from_time=from_time, to_time=to_time, duration=duration)
    return top_list[:10]


# add by yujun
def do_get_impala_top_email_bac(from_time=get_last_week_to(), to_time=get_now(), duration=300000.0):
    top_list = do_get_impala_top(from_time=from_time, to_time=to_time, duration=duration)
    return top_list[:20]


def usage():
    doc = inspect.getmodule(usage).__doc__
    print >> sys.stderr, textwrap.dedent(doc % (sys.argv[0],))


def setup_logging(level):
    logging.basicConfig()
    logging.getLogger().setLevel(level)


def get_job_count(query, from_time, to_time):
    job_count = 0
    responses = do_query(query, from_time, to_time)
    for response in responses:
        if response.timeSeries:
            for ts in response.timeSeries:
                for data in ts.data:
                    job_count += 1
    return job_count


def get_impala_job_summary(from_time=get_one_day_ago_from(), to_time=get_now()):
    query_1min_count = "select  query_duration from IMPALA_QUERIES where serviceName=impala AND (query_state=FINISHED OR query_state=EXCEPTION)  and query_duration <= 60000.0"
    query_5min_count = "select  query_duration from IMPALA_QUERIES where serviceName=impala AND (query_state=FINISHED OR query_state=EXCEPTION)  and query_duration > 60000.0 and query_duration <= 300000.0"
    query_15min_count = "select  query_duration from IMPALA_QUERIES where serviceName=impala AND (query_state=FINISHED OR query_state=EXCEPTION)  and query_duration > 300000.0 and query_duration <= 900000.0"
    query_30min_count = "select  query_duration from IMPALA_QUERIES where serviceName=impala AND (query_state=FINISHED OR query_state=EXCEPTION)  and query_duration > 900000.0 and query_duration <= 1800000.0"
    query_60min_count = "select  query_duration from IMPALA_QUERIES where serviceName=impala AND (query_state=FINISHED OR query_state=EXCEPTION)  and query_duration > 1800000.0 and query_duration <= 3600000.0"
    query_120min_count = "select  query_duration from IMPALA_QUERIES where serviceName=impala AND (query_state=FINISHED OR query_state=EXCEPTION)  and query_duration > 3600000.0 and query_duration <= 7200000.0"
    query_120min_plus_count = "select query_duration from IMPALA_QUERIES where serviceName=impala AND (query_state=FINISHED OR query_state=EXCEPTION)  and query_duration > 7200000.0"

    job_1min_count = get_job_count(query_1min_count, from_time, to_time)
    job_5min_count = get_job_count(query_5min_count, from_time, to_time)
    job_15min_count = get_job_count(query_15min_count, from_time, to_time)
    job_30min_count = get_job_count(query_30min_count, from_time, to_time)
    job_60min_count = get_job_count(query_60min_count, from_time, to_time)
    job_120min_count = get_job_count(query_120min_count, from_time, to_time)
    job_120min_plus_count = get_job_count(query_120min_plus_count, from_time, to_time)
    job_total = job_1min_count + job_5min_count + job_15min_count + job_30min_count + job_60min_count + job_120min_count + job_120min_plus_count
    types = '0-1m', '1-5m', '5-15m', '15-30m', '30-60m', '60-120m', '>120m'
    x = [job_1min_count, job_5min_count, job_15min_count, job_30min_count, job_60min_count, job_120min_count,
         job_120min_plus_count]
    file_path = "./impala_pie.png"
    pie_charts(x, types, job_total, file_path)


def main():
    setup_logging(logging.INFO)
    # Do work
    top_impalas = do_get_impala_top_email()
    top_hives = do_get_hive_top_email()
    user_impala_map = {}
    user_hive_map = {}
    aggregation_map = {}

    # step-1: 根据执行用户聚合
    for top_impala in top_impalas:
        key = top_impala['user']
        if key not in user_impala_map:
            value = [top_impala]
            user_impala_map[key] = value
        else:
            user_impala_map[key].append(top_impala)
    for top_hive in top_hives:
        key = top_hive['user']
        if key not in user_hive_map:
            value = [top_hive]
            user_hive_map[key] = value
        else:
            user_hive_map[key].append(top_hive)

    from metricBA_apps.models import UserGroup
    from metricBA_apps.models import StaffInfo
    queryset = UserGroup.objects.filter(name='admin')
    admins = StaffInfo.objects.all().filter(group=queryset)
    # step-2: 执行用户和员工进行映射
    for user in user_impala_map:
        queryset = UserGroup.objects.filter(name=user)
        staffs = StaffInfo.objects.all().filter(group=queryset)
        if not staffs:
            staffs = admins
        for staff in staffs:
            if staff.name not in aggregation_map:
                value = {
                    'impala': user_impala_map[user],
                    'staff': staff.name,
                    'email': staff.email
                }
                aggregation_map[staff.name] = value
            else:
                value = aggregation_map[staff.name]
                if 'impala' not in value:
                    value['impala'] = [user_impala_map[user]]
                else:
                    value['impala'].append(user_impala_map[user])
    for user in user_hive_map:
        queryset = UserGroup.objects.filter(name=user)
        staffs = StaffInfo.objects.all().filter(group=queryset)
        if not staffs:
            staffs = admins
        for staff in staffs:
            if staff.name not in aggregation_map:
                value = {
                    'hive': user_hive_map[user],
                    'staff': staff.name,
                    'email': staff.email
                }
                aggregation_map[staff.name] = value
            else:
                value = aggregation_map[staff.name]
                if 'hive' not in value:
                    value['hive'] = [user_hive_map[user]]
                else:
                    value['hive'].append(user_hive_map[user])
    for i in aggregation_map:
        print i


#
# The "main" entry
#
if __name__ == '__main__':
    # import django
    #
    # os.environ.setdefault("DJANGO_SETTINGS_MODULE", "metricBA.settings")
    # django.setup()
    # main()
    get_impala_job_summary()
