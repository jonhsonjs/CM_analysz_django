# -*- coding:utf-8 -*-
from restful.common.timeseries import do_query
import datetime
import sys

now = datetime.datetime.now()
one_Day_Ago = now - datetime.timedelta(days=1)  # 前一天

#能量池的变化量
def getUsedrate(query,from_time,to_time,sqParam1,sqParam2):
  responseList = do_query(query, from_time, to_time)
  entityNames = []
  h = []
  for response in responseList:
      if response.timeSeries:
          for ts in response.timeSeries:
            metadata = ts.metadata
            entityName = metadata.attributes['entityName']
            if str(entityName).endswith("group"):
                entityNames.append(entityName)
  for entityName in entityNames:
      row = []
      tempqy = "SELECT "+ sqParam1+","+sqParam2+" WHERE entityName =\""+entityName+"\"AND category = YARN_POOL"
      row.append(entityName)
      responseList = do_query(tempqy, from_time, to_time)
      temp = -1
      flag = 0
      for response in responseList:
          if response.timeSeries:
              for ts in response.timeSeries:
                Value = ts.data[len(ts.data) - 1]
                resultValue = Value.value
                if sqParam1 == "fair_share_mb":
                    resultValue = '%.1f'%((float)(resultValue)/1024)
                    row.append(str(resultValue)+"G")
                else:
                    row.append('%.2f'%(float)(Value.value))
                used_rate = 0
                if temp!=-1:
                    if Value.value!=0:
                        used_rate = '%.2f'%((float)(temp)/(float)(Value.value))
                        used_rate = int((float)(used_rate) * 100)
                    row.append(used_rate)
                if temp == -1:
                    temp = Value.value
                elif Value.value*0.8 <= temp:
                    flag = 1
      if flag == 0:
          row = []
      if len(row) != 0:
        h.append(row)
  result = sorted(h, reverse=True)
  return result


def do_get_vocre_site():
    vcore_info = []
    vocre_site = getUsedrate("SELECT max_share_vcores WHERE category = YARN_POOL", one_Day_Ago, now, "fair_share_vcores",
                           "max_share_vcores")
    for site in vocre_site:
            vcore_info.append({
                    'entityName': site[0],
                    'fair_share_vcores': site[1],
                    'max_share_vcores': site[2],
                    'used_rate/%': site[3]
                }
            )
    return vcore_info


def do_get_memory_site():
    memory_info = []
    memory_site = getUsedrate("SELECT max_share_mb WHERE category = YARN_POOL", one_Day_Ago, now, "fair_share_mb",
                              "max_share_mb")
    for site in memory_site:
        memory_info.append({
            'entityName': site[0],
            'fair_share_mb': site[1],
            'max_share_mb': site[2],
            'used_rate/%': site[3]
            }
        )
    return memory_info

def main(argv):
    t = do_get_vocre_site()
    y = do_get_memory_site()
    print t, y


if __name__ == '__main__':
    sys.exit(main(sys.argv))