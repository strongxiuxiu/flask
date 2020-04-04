"""

    time : 2020.2.6
    theme : gateway
    author :
                                       _                               _
                                 ____ (_)                             (_)        _
                                (____)(_)__    ___   _   _   _   ____  _   ____ (_)__    ____
                                (_)__ (____)  (___) (_) ( ) (_) (____)(_) (____)(____)  (____)
                                 _(__)(_) (_)(_)_(_)(_)_(_)_(_)( )_(_)(_)( )_( )(_) (_)( )_(_)
                                (____)(_) (_) (___)  (__) (__)  (____)(_) (__)_)(_) (_) (____)
                                                                   (_)                 (_)_(_)
                                                                   (_)                  (___)
"""
import datetime
import uuid
import json
import requests
import os, sys

from gatewayapp import models
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from asm.web_status_code import ResponseCodes
from asm.tool import OrmChange, countX, utc_time_change
from rest_framework.pagination import PageNumberPagination
from rest_framework import serializers
from django.core.cache import cache

"""
    this is all function in gateway ，
    if you want modify the file ,
    you need annotation original code add the reasons why.
    good luck!! 
"""
ak = 'q3UjIhNiBFdKP34eeU3DQMsqrYGsRmy5'
alarm_log_file_path = '/home/WebGUI/AIWebGUI/www/templates'


class StandardResultsSetPagination(PageNumberPagination):
    # 默认每页显示的数据条数
    page_size = 6
    # 获取URL参数中设置的每页显示数据条数
    page_size_query_param = 'page_size'

    # 获取URL参数中传入的页码key
    page_query_param = 'page'

    # 最大支持的每页显示的数据条数
    max_page_size = 20


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AIGateway
        fields = "__all__"


class CameraSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AICamera
        fields = "__all__"


class AlertortSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.AIAlertort
        fields = "__all__"


def initializes_the_function_parameter_function(camera_uuid):
    Querfunc = models.AIFuncDefault.objects.all().values()
    QueryIPara = models.AIParaDefault.objects.all().values()
    func = []
    para = []
    for aif in Querfunc:
        function_uuid = uuid.uuid1()
        func.append(models.AIFunction(function_uuid=function_uuid,
                                      camera_uuid=camera_uuid,
                                      function_code=aif['function_code'],
                                      function_name='初始化',
                                      function_status=0,
                                      modification_state=0))
        for qpa in QueryIPara:
            if aif['func_uuid'] == qpa['func_uuid']:
                para.append(models.AIConfiguration(para_uuid=uuid.uuid1(),
                                                   function_uuid=function_uuid,
                                                   parameter_code=qpa['para_code'],
                                                   parameter_key=qpa['para_key'],
                                                   parameter_value=qpa['para_value'],
                                                   parameter_status=0))
    models.AIFunction.objects.bulk_create(func)
    models.AIConfiguration.objects.bulk_create(para)
    return True


def filter_alert_information_function(start_time, time_now):
    # now_time = datetime.datetime.now()
    if start_time or time_now:  # 页面刚刚点击的时候显示的是全部的信息
        start_time = utc_time_change(start_time)
        time_now = utc_time_change(time_now)
        filter_time = (time_now - start_time).days
        if start_time or time_now:
            if filter_time <= 0:  # 小时
                if cache.has_key('hour_alarm_function'):
                    rest_list = json.loads(cache.get('hour_alarm_function'))  # 将功能及其的报警数量全部存储在redis中
                    return rest_list
                else:
                    Queryaip = models.AIFuncDefault.objects.all().values()
                    rest_list = []
                    for qip in Queryaip:
                        function_num = {}
                        function_num['funcname'] = qip['default_function']
                        function_num['func_code'] = qip['function_code']
                        QuerySet = models.AIAlertort.objects.filter(alarm_time__gte=start_time,
                                                                    alarm_time__lte=time_now).all().values()
                        f_num = []
                        for qse in QuerySet:
                            if qse['alarm_code'] == qip['function_code']:
                                f_num.append(1)
                        function_num['num'] = sum(f_num)
                        rest_list.append(function_num)
                    cache.set('hour_alarm_function', json.dumps(rest_list), 24 * 60 * 60)
                    return rest_list
            elif 1 <= filter_time <= 7:
                if cache.has_key('week_alarm_function'):
                    rest_list = json.loads(cache.get('week_alarm_function'))  # 将功能及其的报警数量全部存储在redis中
                    return rest_list
                else:
                    Queryaip = models.AIFuncDefault.objects.all().values()
                    rest_list = []
                    for qip in Queryaip:
                        function_num = {}
                        function_num['funcname'] = qip['default_function']
                        function_num['func_code'] = qip['function_code']
                        QuerySet = models.AIAlertort.objects.filter(alarm_time__gte=start_time,
                                                                    alarm_time__lte=time_now).all().values()
                        f_num = []
                        for qse in QuerySet:
                            if qse['alarm_code'] == qip['function_code']:
                                f_num.append(1)
                        function_num['num'] = sum(f_num)
                        rest_list.append(function_num)
                    cache.set('week_alarm_function', json.dumps(rest_list), 24 * 60 * 60)
                    return rest_list
            else:
                if cache.has_key('month_alarm_function'):
                    rest_list = json.loads(cache.get('month_alarm_function'))  # 将功能及其的报警数量全部存储在redis中
                    cache.set('month_alarm_function', json.dumps(rest_list), 1)
                    return rest_list
                else:
                    Queryaip = models.AIFuncDefault.objects.all().values()
                    rest_list = []
                    for qip in Queryaip:
                        function_num = {}
                        function_num['funcname'] = qip['default_function']
                        function_num['func_code'] = qip['function_code']
                        QuerySet = models.AIAlertort.objects.filter(alarm_time__gte=start_time,
                                                                    alarm_time__lte=time_now).all().values()
                        f_num = []
                        for qse in QuerySet:
                            if qse['alarm_code'] == qip['function_code']:
                                f_num.append(1)
                        function_num['num'] = sum(f_num)
                        rest_list.append(function_num)
                    cache.set('month_alarm_function', json.dumps(rest_list), 24 * 60 * 60)
                    return rest_list
    else:
        if cache.has_key('all_alarm_function'):
            rest_list = json.loads(cache.get('all_alarm_function'))  # 将功能及其的报警数量全部存储在redis中
            # print(rest_list)
            # cache.set('all_alarm_function', json.dumps(rest_list), 20)
            return rest_list
        else:
            Queryaip = models.AIFuncDefault.objects.all().values()
            QuerySet = models.AIAlertort.objects.all().values()
            rest_list = []
            for qip in Queryaip:
                function_num = {}
                function_num['funcname'] = qip['default_function']
                function_num['func_code'] = qip['function_code']
                f_num = []
                for qse in QuerySet:
                    if qse['alarm_code'] == qip['function_code']:
                        f_num.append(1)
                function_num['num'] = sum(f_num)
                rest_list.append(function_num)
            cache.set('all_alarm_function', json.dumps(rest_list), 24 * 60 * 60)
            return rest_list



def map_api_longitde_latitude():
    gateway_place_dict = {}
    camera_place_dict = {}
    gateway_place = []
    camera_place = []
    QuerySet = models.AIGateway.objects.filter(device_status=1).all().values()
    for qys in QuerySet:
        gateway_uuid = qys['gateway_uuid']
        longitude = qys['gateway_longitude']
        latitude = qys['gateway_latitude']
        location = "%s,%s" % (longitude, latitude)
        city_name = send_longitude_latitude_get_cityname(location)
        print(city_name)
        if city_name:
            gateway_place.append(city_name)
            QueryCam = models.AICamera.objects.filter(gateway_uuid=gateway_uuid).all().values()
            for qca in QueryCam:
                # city_name = send_longitude_latitude_get_cityname(location)
                camera_place.append(city_name)
        else:
            break
    gateway_place_all = list(set(gateway_place))
    camera_place_all = list(set(camera_place))
    for gpa in gateway_place_all:
        num = countX(gateway_place, gpa)
        gateway_place_dict[gpa] = num
    for cpa in camera_place_all:
        num = countX(camera_place, cpa)
        camera_place_dict[cpa] = num
    retu_list = {}
    retu_list['gateway'] = gateway_place_dict
    retu_list['camera'] = camera_place_dict
    # retu_list.append(gateway_place_dict)
    # retu_list.append(camera_place_dict)
    return retu_list


def send_longitude_latitude_get_cityname(location):
    try:
        print(location)
        r = requests.get(url='http://api.map.baidu.com/reverse_geocoding/v3/',
                         params={'location': location, 'ak': ak, 'output': 'json',
                                 'coordtype': 'wgs84ll'})
        result = r.json()
        city = result['result']['addressComponent']['city']
        print(city)
        return city
    except:
        print('访问Map api_error')
        return None


class DelGatewayInfo(object):
    """这是删除网关及其对应的相机及其日志的对象"""

    def __init__(self):
        """
            explain:
                if gateway is True

        """
        self.alarm_uuid = []
        self.whether_del_alarm_log = False

    def __str__(self):
        return "now whether del alarm log is %s" % (self.whether_del_alarm_log)

    def delete_gateway(self, whether_del_alarm_log, gateway_uuid):
        self.whether_del_alarm_log = whether_del_alarm_log
        if self.whether_del_alarm_log:
            for g_id in gateway_uuid:
                camera_id_list, alarm_log_id_list = self.get_gatewayid_return_correlation_id(g_id,
                                                                                             self.whether_del_alarm_log)
                if self.del_alarm_log_method(alarm_log_id_list):
                    return False
                else:
                    if self.del_camera_method(camera_id_list):
                        return False
                    else:
                        if self.del_gateway_method(g_id):
                            return False
            return True
        else:
            for g_id in gateway_uuid:
                camera_id_list, alarm_log_id_list = self.get_gatewayid_return_correlation_id(g_id,
                                                                                             self.whether_del_alarm_log)
                if self.del_camera_method(camera_id_list):
                    return False
                else:
                    if self.del_gateway_method(g_id):
                        return False
            return True

    def delete_camera(self, whether_del_alarm_log, camera_uuid):
        self.whether_del_alarm_log = whether_del_alarm_log
        if self.whether_del_alarm_log:
            for c_id in camera_uuid:
                alarm_log_id_list = self.get_cameraid_return_correlation_id(c_id)
                if self.del_alarm_log_method(alarm_log_id_list):
                    return False
                else:
                    if self.del_camera_method(c_id):
                        return False
            return True
        else:
            for c_id in camera_uuid:
                if self.del_gateway_method(c_id):
                    return False
            return True

    def delete_alarm_log(self, alarm_uuid):
        if self.del_alarm_log_method(alarm_uuid):
            return False
        else:
            return True

    def get_gatewayid_return_correlation_id(self, gateway_id, no_log=True):
        """ send a gateway_id return camera and alarm_log list """
        camera_id_list = []
        alarm_log_id_list = []
        if no_log:
            if gateway_id:
                Query_camera = models.AICamera.filter(gateway_uuid=gateway_id).all().values()
                for c_id in Query_camera:
                    camera_id_list.append(c_id['camera_uuid'])
            return camera_id_list
        else:
            if gateway_id:
                Query_camera = models.AICamera.filter(gateway_uuid=gateway_id).all().values()
                Query_Alertort = models.AIAlertort.filter(gateway_uuid=gateway_id).all().values()
                for c_id in Query_camera:
                    camera_id_list.append(c_id['camera_uuid'])
                for a_id in Query_Alertort:
                    alarm_log_id_list.append(a_id['alertor_uuid'])
            return camera_id_list, alarm_log_id_list

    def get_cameraid_return_correlation_id(self, camera_id):
        """ send a camera_id return alarm log id list """
        alarm_log_id_list = []
        if camera_id:
            Query_Alertort = models.AIAlertort.filter(camera_uuid=camera_id).all().values()
            for a_id in Query_Alertort:
                alarm_log_id_list.append(a_id['alertor_uuid'])
        return alarm_log_id_list

    def del_gateway_method(self, gateway_list):
        if gateway_list:
            error_list = []
            for gateway_id in gateway_list:
                status = models.AIGateway.filter(gateway_uuid=gateway_id).delete()
                if status:
                    pass
                else:
                    error_list.append(gateway_id)
            return error_list
        else:
            return False

    def del_camera_method(self, camera_list):
        if camera_list:
            error_list = []
            for camera_id in camera_list:
                status = models.AICamera.filter(camera_uuid=camera_id).delete()
                if status:
                    pass
                else:
                    error_list.append(camera_id)
            return error_list
        else:
            return False

    def del_alarm_log_method(self, alarm_log_list):
        if alarm_log_list:
            error_list = []
            for alarm_log_id in alarm_log_list:
                q_info = models.AIAlertort.filter(alertor_uuid=alarm_log_id).all().values()
                for i in q_info:
                    dirPath = alarm_log_file_path + i['alarm_picture']
                    if (os.path.exists(dirPath)):
                        os.remove(dirPath)
                        print('移除后test 目录下有文件：%s') % os.listdir(dirPath)
                    else:
                        print("要删除的文件不存在！")
                status = models.AIAlertort.filter(alertor_uuid=alarm_log_id).delete()
                if status:
                    pass
                else:
                    error_list.append(alarm_log_id)
            return error_list
        else:
            return False
