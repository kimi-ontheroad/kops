from kafka import KafkaConsumer, TopicPartition, KafkaProducer
from kafka.client import KafkaClient
from kafka.admin import KafkaAdminClient, NewTopic, NewPartitions
from kops import kconfig as ksetting
import logging, traceback
import datetime

log = logging.getLogger('django')


def init_client(client_type, **data):
    if client_type == "KafkaClient":
        return KafkaClient(bootstrap_servers=ksetting.broker_list)
    elif client_type == "KafkaAdminClient":
        return KafkaAdminClient(bootstrap_servers=ksetting.broker_list)
    elif client_type == "KafkaConsumer":
        return KafkaConsumer(bootstrap_servers=ksetting.broker_list, group_id=data['consumer_group'])
    elif client_type == "KafkaProducer":
        return KafkaProducer(bootstrap_servers=ksetting.broker_list)


def fetch_topics():
    """
    获取指定集群的Topic列表
    """
    client = init_client("KafkaClient")

    return client.cluster.topics(exclude_internal_topics=True)


def create_topics(topic_name, topic_num_partitions, topic_replication_factor):
    """
    创建Topic
    """

    create_topic_list = []
    admin_client = init_client("KafkaAdminClient")
    print(topic_name)
    print(topic_num_partitions)
    print(topic_replication_factor)
    create_topic_list.append(
        NewTopic(name=topic_name, num_partitions=topic_num_partitions, replication_factor=topic_replication_factor))
    print(create_topic_list)
    try:
        a = admin_client.create_topics(new_topics=create_topic_list, validate_only=False)
        print(a)
        return True
    except Exception:
        print(traceback.format_exc())
        return False


def delete_topics(topics):
    """
    删除Topic
    """
    delete_topic_list = []
    delete_topic_list.append(topics)
    admin_client = init_client("KafkaAdminClient")
    try:
        admin_client.delete_topics(delete_topic_list)
        return True
    except Exception:
        log.error(traceback.format_exc())
        return False


def extend_partitions(topic_name, topic_num_partitions):
    """
    扩容指定Topic的Partition数量
    """

    admin_client = init_client("KafkaAdminClient")
    new_partitions = NewPartitions(total_count=topic_num_partitions, new_assignments=None)
    topic_partitions = {topic_name: new_partitions}
    try:
        admin_client.create_partitions(topic_partitions)
        return True
    except Exception:
        log.error(traceback.format_exc())
        return False


def fetch_offset(consumer_group, topic_name, partitions):
    """
    获取指定分区的最大偏移量
    """
    data = list()
    tp_list = []
    data_dict = dict()
    for partition in range(partitions):
        tp_list.append(TopicPartition(topic_name, partition))
    consumer = init_client("KafkaConsumer", consumer_group=consumer_group)
    try:
        time = datetime.datetime.now()
        end = consumer.end_offsets(tp_list)
        print(end)
        total_lag = 0
        total_end_offsets = 0
        total_commit_offset = 0
        index = 0
        for i in tp_list:
            print("*****", i)
            data_tmp = dict()
            data_tmp['end_offsets'] = end.get(i, 0)
            print("UUUUUUU")
            data_tmp['commit_offset'] = consumer.committed(i)
            print("UUUUUUUU1")
            if not data_tmp['commit_offset']:
                data_tmp['commit_offset'] = 0
            lag = data_tmp['end_offsets'] - (
                data_tmp['commit_offset'] if data_tmp['commit_offset'] else data_tmp['end_offsets'])
            data_tmp['lag'] = lag if lag > 0 else 0
            total_lag += data_tmp['lag']
            total_end_offsets += data_tmp['end_offsets']
            total_commit_offset += data_tmp['commit_offset']
            data_tmp['time'] = time
            data_tmp['partition'] = index
            index += 1
            data.append(data_tmp)
        data.insert(0,{
            "end_offsets": total_end_offsets,
            "commit_offset": total_commit_offset,
            "lag": total_lag,
            "time": time,
            "partition": partitions
        })
        data_dict = dict(data=data, total_lag=total_lag, total_end_offsets=total_end_offsets,
                         total_commit_offset=total_commit_offset)

        return data_dict
    except Exception:
        log.error(traceback.format_exc())
        return data_dict

# def fetch_commit_offset(tp, consumer_group):
#     """
#     获取给定分区的最后一个提交的偏移量
#     """
#     consumer = init_client("KafkaConsumer", consumer_group=consumer_group)
#
#     try:
#         return consumer.committed(tp)
#
#     except Exception:
#         log.error(traceback.format_exc())
#         return False
