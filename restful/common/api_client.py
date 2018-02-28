#!/usr/bin/env python
#
# Customize these constants for your Cloudera Manager.
#
import logging

import sys
from cm_api.api_client import ApiResource, ApiException

#
# CM_HOST = '10.214.128.31'
# CM_USER = 'admin'
# CM_PASSWD = 'admin'
# CM_USE_TLS = False
# VERSION = 13
from cm_api.http_client import HttpClient
from cm_api.resource import Resource

CM_HOST = '***'
CM_USER = '***'
CM_PASSWD = '***'
VERSION = 13
CM_USE_TLS = False

LOG = logging.getLogger(__name__)


class ApiClient(object):
    """

    """

    def __init__(self):
        self._api = ApiResource(CM_HOST, username=CM_USER, password=CM_PASSWD, use_tls=CM_USE_TLS, version=VERSION)

def main(argv):
    test = ApiClient()


    protocol = "http"
    server_port = 7180
    base_url = "%s://%s:%s" % \
        (protocol, CM_HOST, server_port)

    client = HttpClient(base_url, exc_class=ApiException,
                        ssl_context=None)
    client.set_basic_auth(CM_USER, CM_PASSWD, "Cloudera Manager")
    client.set_headers({"Content-Type": "application/json"})

    test1 = Resource(client,)

    params= {
        'startTime': 1495702493388,
        'endTime': 1495704364740,
        'filters': 'application_id=job_1495442492363_9417',
        'offset': 0,
        'limit': 100,
        'serviceName': 'yarn',
        'histogramAttributes': 'allocated_memory_seconds%2Callocated_vcore_seconds%2Ccpu_milliseconds%2Capplication_duration%2Cfile_bytes_read%2Cfile_bytes_written%2Chdfs_bytes_read%2Chdfs_bytes_written%2Chive_query_string%2Cmb_millis%2Cpool%2Cunused_memory_seconds%2Cunused_vcore_seconds%2Cuser&_=1495704510726'
    }
    test3= test1.get(relpath="/api/v13/cm/log")
    # test3= test1.get(relpath="/cmf/yarn/completedApplications?startTime=1495702493388&endTime=1495704364740&filters=application_id%3Djob_1495442492363_9417&offset=0&limit=100&serviceName=yarn&histogramAttributes=allocated_memory_seconds%2Callocated_vcore_seconds%2Ccpu_milliseconds%2Capplication_duration%2Cfile_bytes_read%2Cfile_bytes_written%2Chdfs_bytes_read%2Chdfs_bytes_written%2Chive_query_string%2Cmb_millis%2Cpool%2Cunused_memory_seconds%2Cunused_vcore_seconds%2Cuser&_=1495704510726")
    # test = client.execute(http_method="GET", path="/cmf/yarn/completedApplications?startTime=1495702493388&endTime=1495704364740&filters=application_id%3Djob_1495442492363_9417&offset=0&limit=100&serviceName=yarn&histogramAttributes=allocated_memory_seconds%2Callocated_vcore_seconds%2Ccpu_milliseconds%2Capplication_duration%2Cfile_bytes_read%2Cfile_bytes_written%2Chdfs_bytes_read%2Chdfs_bytes_written%2Chive_query_string%2Cmb_millis%2Cpool%2Cunused_memory_seconds%2Cunused_vcore_seconds%2Cuser&_=1495704510726", params=params)
    print test3
    pass


#
# The "main" entry
#
if __name__ == '__main__':
    sys.exit(main(sys.argv))