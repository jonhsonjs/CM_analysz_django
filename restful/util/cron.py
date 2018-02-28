# -*- coding: utf-8 -*-
import logging

from restful.util.email_util import overall_report, sendmailto_sql_users


def my_scheduled_job():
    logging.basicConfig()
    overall_report()


def my_scheduled_job1():
    logging.basicConfig()
    sendmailto_sql_users()


