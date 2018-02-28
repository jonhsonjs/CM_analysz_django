# -*- coding:utf-8 -*-
import collections
import logging

import sys

from restful.business.cluster_site import do_get_dfs_capacity_email
from restful.util.chart_util import two_bar_charts, get_linear_model
from restful.util.unit_converter import check_digital_storage_without_unit

from cm_api.endpoints.services import BaseApiResource, ROAttr, call, SERVICES_PATH
from restful.common.api_client import ApiClient
from restful.common.timeseries import do_query_rollup
from restful.util.date_util import get_last_n_week_from, get_now, get_n_day_ago_from, \
    zone_conversion, get_last_n_month_from, get_last_n_quarter_from, Quarter, get_n_hour_ago_from

LOG = logging.getLogger(__name__)

class HDFSInfo(ApiClient):
    """

    """

    def get_service(self, name, cluster_name="default"):
        """
        Lookup a service by name
        @param resource_root: The root Resource object.
        @param name: Service name
        @param cluster_name: Cluster name 
        @return: An ApiService object
        """
        return self._get_service("%s/%s" % (SERVICES_PATH % (cluster_name,), name))

    def get_service_yesterday(self, name, cluster_name="default"):
        return self._get_service_yesterday("%s/%s" % (SERVICES_PATH % (cluster_name,), name))

    def get_service_today(self, name, cluster_name="default"):
        return self._get_service_today("%s/%s" % (SERVICES_PATH % (cluster_name,), name))

    def _get_service(self, path):
        params = {
            'from': get_n_hour_ago_from(n=1),
            'to': get_now()
        }
        return call(method=self._api.get, path=path, ret_type=ApiTest2, ret_is_list=True, params=params)

    def _get_service_today(self, path):
        params = {
            'from': get_n_day_ago_from(n=0),
            'to': get_n_day_ago_from(n=-1)
        }
        print params
        return call(method=self._api.get, path=path, ret_type=ApiTest2, ret_is_list=True, params=params)

    def _get_service_yesterday(self, path):
        params = {
            'from': get_n_day_ago_from(n=1),
            'to': get_n_day_ago_from(n=0)
        }
        print params
        return call(method=self._api.get, path=path, ret_type=ApiTest2, ret_is_list=True, params=params)

    def get_top_user(self):
        """
        Lookup a service by name
        @param resource_root: The root Resource object.
        @param name: Service name
        @param cluster_name: Cluster name 
        @return: An ApiService object
        """
        return self.get_service("hdfs/reports/hdfsUsageReport", "cluster")

    def get_top_user_today(self):
        return self.get_service_today("hdfs/reports/hdfsUsageReport", "cluster")

    def get_top_user_yesterday(self):
        return self.get_service_yesterday("hdfs/reports/hdfsUsageReport", "cluster")

class ApiTest2(BaseApiResource):
    _ATTRIBUTES = {
        'date': ROAttr(),
        'user': ROAttr(),
        'size': ROAttr(),
        'rawSize': ROAttr(),
        'numFiles': ROAttr(),
    }


def _do_get_hdfs_used(from_time, to_time=get_now(), granularity='WEEKLY'):
    return do_query_rollup("select dfs_capacity_used, dfs_capacity  where  entityName=hdfs:nn-idc", from_time, to_time,
                           granularity)


def do_get_hdfs_used_weekly(pic=''):
    responses = _do_get_hdfs_used(get_last_n_week_from(), get_now(), 'WEEKLY')
    capacity = []
    labels = []
    color = ['r', 'g', 'b']
    file_path = './hdfs_weekly.png'
    for response in responses:
        if response.timeSeries:
            for ts in response.timeSeries:
                bar_labels = []
                hdfs_used_values = []
                metadata = ts.metadata
                unit = metadata.unitNumerators[0]
                for data in ts.data:
                    bar_labels.append(zone_conversion(data.timestamp))
                    hdfs_used_values.append(check_digital_storage_without_unit(data.value, unit, 'bytes'))
                capacity.append(hdfs_used_values)
                labels = bar_labels
        if not pic:
            two_bar_charts(labels[-4::], capacity[-4::], color, file_path)
        list, remaining = ring_table_clo(capacity[0], labels)
        metadata = [u'日期', u'已用容量(T)', u'上周容量(T)', u'增量(T)', u'周增长率(%)']
        return list[-4::][::-1], "%.1f" % (remaining * 7), metadata


def ring_table_clo(capacity, labels):
    list_ring = []
    last_value = 1
    incre_list = []
    for i, value in enumerate(capacity):
        value_unit = check_digital_storage_without_unit(value, 'bytes', 'TB')
        last_value_unit = check_digital_storage_without_unit(last_value, 'bytes', 'TB')
        delta = value_unit - last_value_unit
        if last_value_unit == 0:
            list_ring.append({'col_1': labels[i], 'col_2': value_unit,
                              'col_3': last_value_unit, 'col_4': '%.1f' % delta, 'col_5': 0})
        else:
            list_ring.append({'col_1': labels[i], 'col_2': value_unit,
                              'col_3': last_value_unit, 'col_4': '%.1f' % delta,
                              'col_5': '%.1f' % (delta / last_value_unit * 100)})
        last_value = value
        incre_list.append(delta)

    maxsize = 0
    for size in incre_list[-4::]:
        maxsize = max(size, maxsize)

    message_capacity = do_get_dfs_capacity_email()
    dfs_total = message_capacity['dfs_capacity']
    x_parameters = []
    y_parameters = []
    for i, val in enumerate(capacity):
        value = check_digital_storage_without_unit(val, 'bytes', 'TB')
        x_parameters.append([value])
    for i in range(len(x_parameters)):
        y_parameters.append(i)

    predictions = get_linear_model(x_parameters, y_parameters, dfs_total * 0.7)
    days_remaining = predictions['predicted_value'] - len(y_parameters)
    return list_ring, days_remaining[0]


def do_get_hdfs_used_monthly(pic=''):
    responses = _do_get_hdfs_used(get_last_n_month_from(), None, 'WEEKLY')
    capacity = []
    labels = []
    color = ['r', 'g', 'b']
    file_path = './hdfs_monthly.png'
    for response in responses:
        if response.timeSeries:
            for ts in response.timeSeries:
                test1 = collections.OrderedDict()
                bar_labels = []
                hdfs_used_values = []
                metadata = ts.metadata
                unit = metadata.unitNumerators[0]
                for data in ts.data:
                    test1[zone_conversion(timestamp=data.timestamp, format=u'YYYY-MM')] = data.value
                for key, value in test1.items():
                    bar_labels.append(key)
                    hdfs_used_values.append(check_digital_storage_without_unit(value, unit, 'bytes'))
                capacity.append(hdfs_used_values[-5::])
                labels = bar_labels[-5::]
        if not pic:
            two_bar_charts(labels[-4::], capacity[-4::], color, file_path)
        list, remaining = ring_table_clo(capacity[0], labels)
        metadata = [u'日期', u'已用容量(T)', u'上月容量(T)', u'增量(T)', u'月增长率(%)']
        return list[-4::][::-1], metadata


def do_get_hdfs_used_quarterly(pic=''):
    days, quarter_from = get_last_n_quarter_from()
    responses = _do_get_hdfs_used(quarter_from, None, 'WEEKLY')
    capacity = []
    labels = []
    color = ['r', 'g', 'b']
    file_path = './hdfs_quarterly.png'
    test = {}
    for i in days:
        test[i] = 0
    for response in responses:
        if response.timeSeries:
            for ts in response.timeSeries:
                test1 = collections.OrderedDict()
                bar_labels = []
                hdfs_used_values = []
                metadata = ts.metadata
                unit = metadata.unitNumerators[0]
                for data in ts.data:
                    time = zone_conversion(timestamp=data.timestamp, format=u'YYYY-MM')
                    if time in test.keys():
                        test1[time] = data.value
                for key, value in test1.items():
                    bar_labels.append(key)
                    hdfs_used_values.append(check_digital_storage_without_unit(value, unit, 'bytes'))
                capacity.append(hdfs_used_values[-5::])
                labels = bar_labels[-5::]
        labels = [Quarter.from_string(text=x).__str__() for x in labels]
        if not pic:
            two_bar_charts(labels[-4::], capacity[-4::], color, file_path)
        list, remaining = ring_table_clo(capacity[0], labels)
        metadata = [u'日期', u'已用容量(T)', u'上季容量(T)', u'增量(T)', u'季度增长率(%)']
        return list[-4::][::-1], metadata


def do_get_top_user():
    hdfs_info = HDFSInfo()
    top_users = hdfs_info.get_top_user()
    top_users_sorted = sorted(top_users, key=lambda t: t.size, reverse=True)
    for top_user in top_users:
        do_print(top_user)
    return massage_top_for_json(top_users_sorted)


def do_get_top_user_adding():
    user_today_list = []
    user_yesterday_list = []
    user_today_dict = {}
    user_yesterday_dict = {}
    add_info = []
    hdfs_info = HDFSInfo()
    top_users_today = hdfs_info.get_top_user_today()
    top_users_yesterday = hdfs_info.get_top_user_yesterday()
    for user in top_users_today:
        user_today_list.append(user.user)
        user_today_dict[user.user] = user.rawSize
    for user in top_users_yesterday:
        user_yesterday_list.append(user.user)
        user_yesterday_dict[user.user] = user.rawSize
    for i in range(len(user_today_list)):
        if user_today_list[i] in user_yesterday_list:
            adding = user_today_dict[user_today_list[i]] - user_yesterday_dict[user_today_list[i]]
        else:
            adding = top_users_today[i].rawSize
        add_info.append(
            {
                'user': user_today_list[i],
                'sizeToday': top_users_today[i].rawSize,
                'sizeYesterday': top_users_yesterday[i].rawSize,
                'adding': adding,
            }
        )
    add_info_sorted = sorted(add_info,  key=lambda k: k['adding'], reverse=True)
    return add_info_sorted


def massage_top_for_json(top_users):
    massage_top = []
    for top_user in top_users:
        massage_top.append(
            {
                'user': top_user.user,
                'size': top_user.size,
                'numFiles': top_user.numFiles,
                'rawSize': top_user.rawSize,
            }
        )
    return massage_top


def do_print(cluster):
    print("<ApiService>")
    print("  user: %s" % cluster.user)
    print("  size: %s" % cluster.size)
    print("  numFiles: %s" % cluster.numFiles)
    if cluster.rawSize:
        print("  rawSize: %s" % cluster.rawSize)


def setup_logging(level):
    logging.basicConfig()
    logging.getLogger().setLevel(level)


def get_median(data):
    data.sort()
    half = len(data) // 2
    return data[half] + data[~half]


def main(argv):
    setup_logging(logging.INFO)
    # Do work
    # t = do_get_hdfs_used_quarterly(pic='123')
    # do_get_hdfs_used_weekly()
    # do_get_hdfs_used_quarterly()
    # t = do_get_top_user()
    t = do_get_top_user_adding()
    print t


#
# The "main" entry
#
if __name__ == '__main__':
    sys.exit(main(sys.argv))
