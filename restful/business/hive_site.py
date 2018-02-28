# -*- coding:utf-8 -*-
import inspect
import logging
import sys
import textwrap

#
# Customize these constants for your Cloudera Manager.
#
from cm_api.endpoints import services
from cm_api.endpoints.services import ApiService, get_service

from restful.common.api_client import ApiClient
from restful.common.timeseries import do_query_rollup, do_query
from restful.util.chart_util import pie_charts
from restful.util.date_util import get_last_week_from, get_last_week_to, get_now, zone_conversion_date_format, \
    get_one_day_ago_from, get_n_hour_ago_from, get_n_day_ago_from, round_milli_time, zone_conversion

LOG = logging.getLogger(__name__)

HIVE_QUERY = "select application_duration from YARN_APPLICATIONS where service_name =  \"yarn\" " \
             "and  hive_query_id RLIKE \".*\" and application_duration >= %s"


class HiveInfo(ApiClient):
    """

    """
    def get_top_user_demo(self, from_time, to_time, duration=900):
        filter_str = "hive_query_id RLIKE \".*\" and application_duration >= %s" % duration
        return get_service(self._api, cluster_name="cluster", name="yarn").get_yarn_applications(start_time=from_time, end_time=to_time, filter_str=filter_str)


def do_get_top_user_demo(from_time=get_one_day_ago_from(), to_time=get_now(), duration=900):
    hive_info = HiveInfo()
    top_users = hive_info.get_top_user_demo(from_time=from_time, to_time=to_time, duration=duration)
    massage_dfs = []
    if top_users.applications:
        for i in top_users.applications:
            line = {}
            line['category'] = "YARN_APPLICATION"
            line['service_name'] = "yarn"
            line['pool'] = i.pool
            line['user'] = i.user
            try:
                line['cpu_milliseconds'] = i.attributes['cpu_milliseconds']
            except KeyError:
                line['cpu_milliseconds'] = 0
            line['name'] = i.attributes['hive_query_string']
            line['entityName'] = i.applicationId
            line['time'] = zone_conversion(timestamp=i.startTime, format=u'YYYY-MM-DD HH:mm:ss')
            attr_val = round_milli_time(i.startTime, i.endTime)
            line['application_duration1'] = attr_val
            if int(float(attr_val)) > 60 * 60 * 1000:
                attr_val = ('%.2f' % (float(attr_val) / 60 / 60 / 1000)) + "h"
            elif int(float(attr_val)) > 60 * 1000:
                attr_val = str(int(float(attr_val)) / 60 / 1000) + "m"  # 分
            elif int(float(attr_val)) > 1000:
                attr_val = str(int(float(attr_val)) / 1000) + "s"  # 秒
            line['application_duration'] = attr_val
            massage_dfs.append(line)
    return sorted(massage_dfs, key=lambda t: t['application_duration1'], reverse=True)


def do_get_hive_top(from_time=get_one_day_ago_from(), to_time=get_now(), duration=900000.0):
    attrs = ['user', 'name', 'application_duration', 'entityName', 'pool', 'cpu_milliseconds', 'category',
             'service_name']
    responses = do_query(HIVE_QUERY % duration, from_time, to_time)
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
                            if 'application_duration' == attr:
                                line['application_duration1'] = float(attr_val)
                                if int(float(attr_val)) > 60 * 60 * 1000:
                                    attr_val = ('%.2f' % (float(attr_val) / 60 / 60 / 1000)) + "h"
                                elif int(float(attr_val)) > 60 * 1000:
                                    attr_val = str(int(float(attr_val)) / 60 / 1000) + "m"  # 分
                                elif int(float(attr_val)) > 1000:
                                    attr_val = str(int(float(attr_val)) / 1000) + "s"  # 秒
                            line[attr] = attr_val
                for data in ts.data:
                    line['time'] = zone_conversion(timestamp=data.timestamp, format=u'YYYY-MM-DD HH:mm:ss')
                massage_dfs.append(line)
    return sorted(massage_dfs, key=lambda t: t['application_duration1'], reverse=True)


def do_get_hive_top_email(from_time=get_one_day_ago_from(), to_time=get_now(), duration=900000.0):
    top_list = do_get_top_user_demo(from_time=from_time, to_time=to_time, duration=duration)
    return top_list[:10]

def do_get_hive_top_email_bac(from_time=get_one_day_ago_from(), to_time=get_now(), duration=900000.0):
    top_list = do_get_top_user_demo(from_time=from_time, to_time=to_time, duration=duration)
    return top_list[:40]


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


def get_hive_job_summary(from_time=get_one_day_ago_from(), to_time=get_now()):
    query_5min_count = "select application_duration from YARN_APPLICATIONS where service_name = \"yarn\" and hive_query_id RLIKE \".*\" and application_duration < 300000.0 "
    query_15min_count = "select application_duration from YARN_APPLICATIONS where service_name = \"yarn\" and hive_query_id RLIKE \".*\" and application_duration >= 300000.0 and application_duration < 900000.0 "
    query_30min_count = "select application_duration from YARN_APPLICATIONS where service_name = \"yarn\" and hive_query_id RLIKE \".*\" and application_duration >= 900000.0 and application_duration < 1800000.0"
    query_60min_count = "select application_duration from YARN_APPLICATIONS where service_name = \"yarn\" and hive_query_id RLIKE \".*\" and application_duration >= 1800000.0 and application_duration < 3600000.0"
    query_120min_count = "select application_duration from YARN_APPLICATIONS where service_name = \"yarn\" and hive_query_id RLIKE \".*\" and application_duration >= 3600000.0 and application_duration < 7200000.0 "
    query_120min_plus_count = "select application_duration from YARN_APPLICATIONS where service_name = \"yarn\" and hive_query_id RLIKE \".*\" and application_duration >= 7200000.0 "

    job_5min_count = get_job_count(query_5min_count, from_time, to_time)
    job_15min_count = get_job_count(query_15min_count, from_time, to_time)
    job_30min_count = get_job_count(query_30min_count, from_time, to_time)
    job_60min_count = get_job_count(query_60min_count, from_time, to_time)
    job_120min_count = get_job_count(query_120min_count, from_time, to_time)
    job_120min_plus_count = get_job_count(query_120min_plus_count, from_time, to_time)
    job_total = job_5min_count + job_15min_count + job_30min_count + job_60min_count + job_120min_count + job_120min_plus_count

    types = '1-5m', '5-15m', '15-30m', '30-60m', '60-120m', '>120m'
    x = [job_5min_count, job_15min_count, job_30min_count, job_60min_count, job_120min_count, job_120min_plus_count]

    file_path = "./hive_pie.png"
    pie_charts(x, types, job_total, file_path)


def main(argv):
    setup_logging(logging.INFO)
    # Do work
    t = do_get_top_user_demo()
    print t


#
# The "main" entry
#
if __name__ == '__main__':
    sys.exit(main(sys.argv))
