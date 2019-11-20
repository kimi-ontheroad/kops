from django.db import models


# Create your models here.
class topics(models.Model):
    """
    Kafka Topic 列表
    """
    topic_name = models.TextField(null=True, blank=True, verbose_name='Topic名称')
    size_per_log = models.CharField(max_length=100, null=True, blank=True, verbose_name='单条日志大小')
    cluster = models.TextField(null=True, blank=True, verbose_name='所属kafka集群')
    peak_volume = models.BigIntegerField(null=True, verbose_name='QPS')
    create_user = models.CharField(max_length=40, null=True, verbose_name='申请人')
    partition = models.IntegerField(null=True, blank=True)
    brokers = models.TextField(null=True, blank=True, verbose_name='生产broker list')
    service_name = models.TextField(null=True, blank=True, verbose_name='日志所属服务名称')
    machine_number = models.IntegerField(verbose_name='生产机器数量')
    machine_ip = models.TextField(blank=True, null=True, verbose_name='生产机器IP列表')
    kafka_client = models.TextField(blank=True, null=True, verbose_name='生产客户端')
    describe = models.TextField(blank=True, null=True, verbose_name='日志用途描述')


class consumers(models.Model):
    """
    kafka consumer列表
    """
    consumer_group_name = models.TextField(null=True, blank=True, verbose_name='消费group名称')
    consumer_client = models.TextField(null=True, blank=True, verbose_name="消费客户端")
    consumer_describe = models.TextField(null=True, blank=True, verbose_name='日志消费用途描述')
    consumer_topic = models.ForeignKey(to='topics', db_constraint=False, on_delete=models.CASCADE,
                                       verbose_name="消费topic", blank=True, null=True)
    consumer_cluster = models.TextField(null=True, blank=True, verbose_name="所属消费集群")
    consumer_user = models.CharField(max_length=40, verbose_name='group负责人')
    consumer_broker_list = models.TextField(null=True, blank=True, verbose_name='消费broker_list')


#
class topics_monitor(models.Model):
    topics = models.ForeignKey(topics, db_constraint=False, related_name='topics', verbose_name='关联topic',
                               on_delete=models.CASCADE)
    group = models.ForeignKey(consumers, db_constraint=False, related_name='comsumergroup', verbose_name='关联消费group',
                              on_delete=models.CASCADE)
    value = models.IntegerField(verbose_name='报警阀值')
    cc_list = models.CharField(verbose_name='报警接受人', max_length=1000)
    creator = models.CharField(verbose_name='创建人', max_length=50)
    monitor_status = (
        (0, '暂停'),
        (1, '运行')
    )
    status = models.IntegerField(verbose_name='报警状态', choices=monitor_status)
    # 0 未报警   1 正在报警
    is_monitor_status = models.IntegerField(verbose_name='是否正在报警')
