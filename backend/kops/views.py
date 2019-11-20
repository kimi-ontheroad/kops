from django.contrib.auth.models import User
from django.core import serializers
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.views import View
from .kapi import *
from .kconfig import per_partition, broker_list
from django.core import serializers
from django.contrib import auth
from .models import *
import logging
import json
import uuid

log = logging.getLogger('django')


class LoginView(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        if not data['username']:
            return JsonResponse({"message": "username is not blank", "code": 302})
        if not data['password']:
            return JsonResponse({"message": "password is not blank", "code": 302})
        existed_user = User.objects.filter(username=data['username'])
        _data = dict(kafkaid=uuid.uuid1(), code=200, expires_in="3600")
        if not existed_user:
            User.objects.create(**data).save()
            return JsonResponse(_data)
        else:
            if existed_user.first().password == data['password']:
                return JsonResponse(_data)
            else:
                return JsonResponse({"message": "password is not correct", "code": 302})


class TopicView(View):
    def get(self, request, *args, **kwargs):
        """
        topic_name__icontains=None, create_user__icontains=None
        """

        try:
            condition = Q()
            condition.connector = "AND"
            [condition.children.append((i[0], int(i[1])))
             if i[0] == 'id' else condition.children.append((i[0] + "__icontains", i[1]))
             for i in request.GET.items() if i[1]]
        except Exception as e:
            return JsonResponse({'error': traceback.format_exc()})
        notos_query = topics.objects.filter(condition)
        data = serializers.serialize("json", notos_query)
        json_data = json.loads(data)
        return JsonResponse(json_data, safe=False)

    def post(self, request, *args, **kwargs):
        '''
        创建topic
        body：{
        "topic_name":"test",
        "size_per_log":"test",
        "cluster":"test",
        "peak_volume":"test",
        "create_user":"test",
        "service_name":"test",
        "machine_number":"test",
        "machine_ip":"test",
        "kafka_client":"test",
        "describe":"test"
        }

        计算值：{

        "partition":"test",
        "brokers":"test",}
        '''
        # 创建topic

        data = json.loads(request.body)
        try:
            log = float(data.get('size_per_log', 0))
            peak_volume = float(data.get('peak_volume', 0))
            data['partition'] = int(log * peak_volume / (per_partition * 1000))
            data['partition'] = data['partition'] if data['partition'] > 0 else 1
            data['brokers'] = ",".join(broker_list)
            topic_name = data.get("topic_name", None)
            is_existed = topics.objects.filter(topic_name=topic_name)
            if not is_existed:
                ret = create_topics(topic_name, data['partition'], 1)
                if ret:
                    del data['is_update']
                    data['peak_volume'] = peak_volume
                    data['size_per_log'] = log
                    data['machine_number'] = int(data['machine_number'])
                    data['kafka_client'] = ",".join(data['kafka_client'])
                    del data['id']
                    topics.objects.create(**data).save()
                    return JsonResponse({'message': 'create topic success', 'code': 200})
                else:
                    return JsonResponse({'message': 'create topic fail', 'code': 302})
            else:
                _is = topics.objects.filter(topic_name=topic_name)
                if not _is:
                    _is.create(**data)
                return JsonResponse({'message': 'topic existed', 'code': 302})
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({'message': 'system error', 'code': 302})

    def delete(self, request):
        """
        删除topicname
        :param request:
        :param topic_name:
        :return:
        """
        topic_name = (request.path.split('/'))[3]
        is_topic = topics.objects.filter(topic_name=topic_name)
        if is_topic:
            ret = delete_topics(topic_name)
            if ret:
                topics.objects.filter(topic_name=topic_name).delete()
                return JsonResponse({'message': "Topic delete success", "code": 200})
            else:
                return JsonResponse({'message': "Topic delete fail", "code": 302})
        else:
            return JsonResponse({'message': "Topic not existed，delete fail", "code": 302})

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)
        topic_id = int(request.path.split('/')[3])
        try:
            del data['is_update']
            del data['index']
            data['kafka_client'] = ",".join(data['kafka_client'])
            topics.objects.filter(id=topic_id).update(**data)
            return JsonResponse({'message': 'update success', "code": 200})
        except Exception:
            return JsonResponse({'message': 'update variable fail', "code": 302})


class ConsumerGroupView(View):
    def get(self, request, *args, **kwargs):
        """
        topic_name__icontains=None, consumer_user__icontains=None
        """

        try:
            condition = Q()
            condition.connector = "AND"
            [condition.children.append((i[0], int(i[1])))
             if i[0] == 'consumer_topic' else
             condition.children.append((i[0], i[1]))
             for i in request.GET.items() if i[1]]
        except Exception as e:
            return JsonResponse({'error': traceback.format_exc()})
        notos_query = consumers.objects.filter(condition)
        data = serializers.serialize("json", notos_query)
        json_data = json.loads(data)
        return JsonResponse(json_data, safe=False)

    def post(self, request, *args, **kwargs):
        '''
        创建comsumer
        {
            "consumer_group_name":"test1",
            "consumer_client":"test",
            "consumer_describe":"test",
            "consumer_topic":1,
            "consumer_cluster":"test",
            "consumer_user":"test",
            "consumer_broker_list":"test"
            }
        '''
        data = json.loads(request.body)
        try:
            consumer_group_name = data.get('consumer_group_name', None)
            is_comsumer = consumers.objects.filter(consumer_group_name=consumer_group_name)
            consumer_topic = data.get('consumer_topic', None)
            if not is_comsumer:
                data['consumer_topic'] = topics.objects.get(id=consumer_topic)
                del data['topic_name']
                del data['topic_id']
                is_comsumer.create(**data)
                return JsonResponse({'message': 'create comsumer success', 'code': 200})
            else:
                if is_comsumer.first().consumer_topic.id == int(consumer_topic):
                    return JsonResponse({'message': 'the same topic is not allow the same consume group ', "code": 302})
                else:
                    data['consumer_topic'] = topics.objects.get(id=consumer_topic)
                    del data['topic_name']
                    del data['topic_id']
                    is_comsumer.create(**data)
                    return JsonResponse({'message': 'create comsumer success', 'code': 200})
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({'message': 'system error', "code": 302})

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        consumers_name = (request.path.split('/'))[3]
        partition = int(data.get('partition', 0))
        topic_name = data.get('topic_name')
        print(partition)
        if not partition:
            return JsonResponse({'message': 'partition  is zero', "code": 302})
        data_temp = fetch_offset(consumer_group=consumers_name, topic_name=topic_name, partitions=partition)
        if not data_temp:
            return JsonResponse({'message': '暂时无数据', "code": 302})
        data_temp['code'] = 200
        return JsonResponse(data_temp)

    def delete(self, request, *args, **kwargs):
        consumer_id = int(request.path.split('/')[3])
        is_consumer = consumers.objects.filter(id=consumer_id)
        if is_consumer:
            is_consumer.delete()
            return JsonResponse({'message': 'delete comsumer success', 'code': 200})
        else:
            return JsonResponse({'message': 'comsumer is not existed', "code": 302})

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)
        id = int(request.path.split('/')[3])
        try:
            is_comsumer = consumers.objects.filter(id=id)
            if is_comsumer:
                consumer_topic = data.get('consumer_topic', None)
                data['consumer_topic'] = topics.objects.get(id=consumer_topic)
                del data['topic_name']
                del data['topic_id']
                is_comsumer.update(**data)
                return JsonResponse({'message': 'update comsumer success', 'code': 200})
            else:
                return JsonResponse({'message': 'comsumer not existed', "code": 302})
        except Exception as e:
            print(traceback.format_exc())
            return JsonResponse({'message': 'system error', "code": 302})


class TopicMonitorView(View):
    def get(self, request, *args, **kwargs):
        """
        topic_name__icontains=None, create_user__icontains=None
        """

        try:
            condition = Q()
            condition.connector = "AND"
            [condition.children.append((i[0], int(i[1])))
             if i[0] == 'topics' else condition.children.append((i[0] + "__consumer_group_name__icontains", i[1])) if i[
                                                                                                                          0] == "group" else
            condition.children.append((i[0], i[1]))
             for i in request.GET.items() if i[1]]
            print(condition)
        except Exception as e:
            return JsonResponse({'error': traceback.format_exc()})
        notos_query = list(topics_monitor.objects.filter(condition).values("id",
                                                                           "topics__topic_name",
                                                                           "group__id",
                                                                           "group__consumer_group_name",
                                                                           "cc_list",
                                                                           "value",
                                                                           "creator",
                                                                           "status"))
        json_data = dict(data=notos_query, code=200)
        return JsonResponse(json_data, safe=False)

    def post(self, request, *args, **kwargs):

        data = json.loads(request.body)
        try:
            topic = data.get('topics', None)
            group = data.get('group', None)
            is_topics_monitor = topics_monitor.objects.filter(topics__id=int(topic),
                                                              group__consumer_group_name=group)
            if not is_topics_monitor:
                data['group'] = consumers.objects.filter(consumer_group_name=data['group']).first()
                data['topics'] = topics.objects.filter(id=int(data['topics'])).first()
                del data['is_update']
                data['is_monitor_status'] = 0
                is_topics_monitor.create(**data)
                return JsonResponse({'message': 'TopicMonitor create success', "code": 200})
            else:
                return JsonResponse({'message': 'TopicMonitor existed ', "code": 302})
        except Exception:
            print(traceback.format_exc())
            return JsonResponse({'message': 'system error ', "code": 302})

    def delete(self, request):

        id = (request.path.split('/'))[3]
        is_topic = topics_monitor.objects.filter(id=id)
        if is_topic:
            is_topic.delete()
            return JsonResponse({'message': "Topic delete success", "code": 200})
        else:
            return JsonResponse({'message': "Topic not existed，delete fail", "code": 302})

    def patch(self, request, *args, **kwargs):
        data = json.loads(request.body)
        monitor_id = int(request.path.split('/')[3])
        is_monitor_id = topics_monitor.objects.filter(id=monitor_id)
        if not is_monitor_id:
            return JsonResponse({'message': 'monitor id is not exist', "code": 302})
        try:
            data['group'] = consumers.objects.filter(consumer_group_name=data['group']).first()
            data['topics'] = topics.objects.filter(id=int(data['topics'])).first()
            del data['is_update']
            is_monitor_id.update(**data)
            return JsonResponse({'message': 'monitor update success', "code": 200})
        except Exception:
            return JsonResponse({'message': 'monitor update variable fail', "code": 302})

    def put(self, request, *args, **kwargs):
        data = json.loads(request.body)
        monitor_id = int(request.path.split('/')[3])
        is_monitor_id = topics_monitor.objects.filter(id=monitor_id)
        if not is_monitor_id:
            return JsonResponse({'message': 'monitor id is not exist', "code": 302})
        is_monitor_id.update(**data)
        return JsonResponse({'message': 'monitor update success', "code": 200})

