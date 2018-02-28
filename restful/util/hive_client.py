# -*- coding: utf-8 -*-

import pyhs2


class HiveClient:
    def __init__(self, db_host, user, password, port=10000, authMechanism="PLAIN"):
        self.conn = pyhs2.connect(host=db_host,
                                  port=port,
                                  authMechanism=authMechanism,
                                  user=user,
                                  password=password,
                                  )

    def query(self, sql):
        with self.conn.cursor() as cursor:
            cursor.execute(sql)
            return cursor.fetch()

    def close(self):
        self.conn.close()


def main():
    hive_client = HiveClient(db_host='10.214.128.11', port=10003, user='analysis_app_user', password='123456',
                             authMechanism='PLAIN')
    result = hive_client.query('show databases')
    print result
    hive_client.close()


if __name__ == '__main__':
    main()
