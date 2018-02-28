# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.translation import ugettext_lazy as _

# Create your models here.


class UserGroup(models.Model):
    """
                           ____________ wanda id A
                           |   
    userGroup: hdfsUser ——— ——————————— wanda id B       one to many
                           |
                            ----------- wanda id C
                            
     
     +--------------------------------------------------------------------------------------+
     |  字段        |     类型       |                        说明                           |
     +--------------------------------------------------------------------------------------+
     |  name        |     String    | 用户组名称(对应的是hdfs集群上的用户),该记录可以通过api添加，|
     
     |              |               | 也可以使用hdfs cm_api 做同步更新入库                     |
     +--------------------------------------------------------------------------------------+
     |  description |     String    |  描述                                                  |
     +---------------------------------------------------------------------------------------+
     |  create_user |     String    |      修改人(用于区分 认为修改还是后台任务更新)             |
     +---------------------------------------------------------------------------------------+
     |  join_date   |     dateTime  |      创建/修改时间                                      |
     +---------------------------------------------------------------------------------------+
     
    """

    name = models.CharField(_('name'), max_length=80, unique=True)
    description = models.TextField(blank=False)
    create_user = models.CharField(_('create_user'), max_length=80, blank=True)
    join_date = models.DateTimeField(_('join_date'), auto_now_add=True)

    class Meta:
        ordering = ('join_date',)


class StaffInfo(models.Model):
    """
    
                            ____________ userGroup1
                           |   
             wanda id A ——— ——————————— userGroup2      one to many   
                           |
                            ----------- userGroup3
      

      +--------------------------------------------------------------------------------------+
      |  字段        |     类型       |                        说明                           |
      +--------------------------------------------------------------------------------------+
      |  name        |     String    | 用户名称(唯一)                                         |
      +--------------------------------------------------------------------------------------+
      |  code        |     String    |  工号                                                  |
      +---------------------------------------------------------------------------------------+
      |  email       |     String    |   邮箱信息(beta1为单邮箱，后面可以做多邮箱，以;分割)        |
      +---------------------------------------------------------------------------------------+
      |  group    |     String    |   外键 group id                                        |
      +---------------------------------------------------------------------------------------+
      |  join_date   |     dateTime  |      创建/修改时间                                      |
      +---------------------------------------------------------------------------------------+

     """

    name = models.CharField(_('name'), max_length=80, blank=False)
    code = models.CharField(_('code'), max_length=80, blank=False)
    email = models.TextField(_('email'), blank=False)

    group = models.ForeignKey(UserGroup, related_name='staffs')

    join_date = models.DateTimeField(_('join_date'), auto_now_add=True)

    class Meta:
        ordering = ('join_date',)
        unique_together = ('name', 'code', 'group')
