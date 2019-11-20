import os, django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")
django.setup()

from django.core.mail import send_mail
from kops.kapi import *
from celery.task import task
from kops.models import *
import datetime

topics_monitor_email_templete = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Consul Token</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style>
      td.left{{padding-right: 20px; text-align: right;}}
      td{{ line-height: 30px;}}
    </style>
  </head>
  <body style="margin: 0; padding: 0;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;margin:0 auto;">
      <tr>
        <td colspan="2" style="background-color:#922E58;text-align:center;text-align: center;">
          <span style="line-height: 60px; font-size: 22px;color: #ffffff;">Kafka消费堆积报警</span><br>
        </td>
      </tr>
      <tr>
        <td width="150" class="left"> Topic名称 </td>
        <td width="450">{topic}</td>
      </tr>
      <tr>
        <td width="150" class="left"> GroupID </td>
        <td width="450">{group}</td>
      </tr>
      <tr>
        <td width="150" class="left"> 消费集群 </td>
        <td width="450">{cluster}</td>
      </tr>
      <tr>
        <td width="150" class="left"> 报警阈值 </td>
        <td width="450">{value}</td>
      </tr>'''

topics_monitor_email_templete_end = '''
  <tr style="height: 50px">
        <td colspan="2" style="background-color:#922E58;text-align:center;color: #fff;"></td>
       </tr>
      </table>
  </body>
</html>'''

topics_monitor_normal_email = '''
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
  <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    <title>Consul Token</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
    <style>
      td.left{{padding-right: 20px; text-align: right;}}
      td{{ line-height: 30px;}}
    </style>
  </head>
  <body style="margin: 0; padding: 0;">
    <table align="center" border="0" cellpadding="0" cellspacing="0" width="600" style="border-collapse: collapse;margin:0 auto;">
      <tr>
        <td colspan="2" style="background-color:#922E58;text-align:center;text-align: center;">
          <span style="line-height: 60px; font-size: 22px;color: #ffffff;">Kafka消费堆积报警恢复</span><br>
        </td>
      </tr>
      <tr>
        <td width="150" class="left"> Topic名称 </td>
        <td width="450">{topic}</td>
      </tr>
      <tr>
        <td width="150" class="left"> GroupID </td>
        <td width="450">{group}</td>
      </tr>
      <tr>
        <td width="150" class="left"> 消费集群 </td>
        <td width="450">{cluster}</td>
      </tr>
      <tr>
        <td width="150" class="left"> 报警阈值 </td>
        <td width="450">{value}</td>
      </tr>'''

topics_monitor_normal_email_end = '''
      <tr style="height: 50px">
        <td colspan="2" style="background-color:#922E58;text-align:center;color: #fff;"></td>
       </tr>
      </table>
  </body>
</html>'''




configs = dict()

configs['email.from'] = "qazdeep@163.com"
configs['auth_user'] = "qazdeep@163.com"
configs['auth_password'] = "1532105342qazwsx"


@task
def get_consume_monitor():
    log.info('Start get topic consume monitor')

    query_set = topics_monitor.objects.filter(status=1)
    print(query_set)
    for i in query_set:
        try:
            cluster = i.topics.cluster
            topic = i.topics.topic_name
            partition = i.topics.partition
            group = i.group.consumer_group_name
            value = i.value
            time = datetime.datetime.now()
            total_lag = fetch_offset(consumer_group=group, topic_name=topic, partitions=partition)
            print("******",total_lag)
            if not total_lag:
                print("1111")
                continue
            else:
                print("1111")
                if total_lag['total_lag']:
                    print("3333")
                    if total_lag['total_lag'] > value:
                        i.is_monitor_status = 1
                        # 报警
                        cc_list = i.cc_list.split(',')
                        lag_temp = topics_monitor_email_templete
                        lag_temp += '''
                                    <tr>
                                    <td width="150" class="left">''' + "当前lag" + '''</td>
                                    <td width="450">''' + str(total_lag['total_lag']) + '''</td>
                                    </tr>
                                    <tr>
                                    <td width="150" class="left">''' + "报警时间" + '''</td>
                                    <td width="450">''' + str(time) + '''</td>
                                    </tr>'''
                        email_tmp = lag_temp.format(topic=topic, group=group, cluster=cluster, value=i.value)
                        email_template = email_tmp + topics_monitor_email_templete_end.format(topic=topic,
                                                                                              cluster=cluster)
                        i.save()
                        send_mail('【kafka】Topic消费堆积报警', '', configs['email.from'], cc_list,
                                  auth_user=configs['auth_user'],
                                  auth_password=configs['auth_password'],
                                  html_message=email_template)

                    else:
                        if i.is_monitor_status:
                            print("7777")
                            i.is_monitor_status = 0
                            # 恢复
                            cc_list = i.cc_list.split(',')
                            i.save()
                            lag_temp = topics_monitor_normal_email.format(topic=topic, group=group, cluster=cluster,
                                                                          value=i.value)
                            lag_temp += '''
                                                   <tr>
                                                     <td width="150" class="left">''' + "当前lag" + '''</td>
                                                     <td width="450">''' + str(total_lag['total_lag']) + '''</td>
                                                   </tr>
                                                   <tr>
                                        <td width="150" class="left">''' + "当前恢复时间" + '''</td>
                                        <td width="450">''' + str(time) + '''</td>
                                        </tr>'''
                            email_tmp = lag_temp + topics_monitor_normal_email_end.format(topic=topic, cluster=cluster)
                            send_mail('【kafka】Topic消费堆积报警恢复', '', configs['email.from'], cc_list,
                                      auth_user=configs['auth_user'],
                                      auth_password=configs['auth_password'],
                                      html_message=email_tmp)
                        else:
                            pass

        except:
            log.error('id:%s topic: %s, group: %s monitor error!' % (i.id, i.topics.topic_name, i.group))
            log.error(traceback.format_exc())
            continue


if __name__ == '__main__':
    # send_mail('【kafka】Topic消费堆积报警恢复', '',configs['email.from'], ["1532105342@qq.com"],
    #           auth_user=configs['auth_user'],
    #           auth_password=configs['auth_password'],
    #           html_message=topics_monitor_normal_email + topics_monitor_normal_email_end)
    get_consume_monitor()
