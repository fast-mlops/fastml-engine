#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import traceback
import time
from flask import json
import os
from fastml_engine.log import Logger
from fastml_engine.exception.infer_exception import InferException
from fastml_engine.exception.load_exception import LoadException


class ServiceEngine:

    def __init__(self):

        service_path = os.getenv('SERVICE_PATH')
        if service_path and os.path.exists(service_path):
            logger = Logger(log_path=service_path + "/logs").getLogger(__name__)
            logger.info('service_path: %s', service_path)
        else:
            raise LoadException('service_path is none, terminated')
        if not os.path.exists(service_path+'/src'):
            raise LoadException('src dir not exist, terminated')
        if not os.path.exists(service_path + "/conf/endpoint.json"):
            raise LoadException('endpoint.json file not exist, terminated')
        try:
            logger.info("starting...")
            init_start_time = time.time()
            sys.path.append(service_path + "/src")
            self.endpoint_arr = load_endpoint(service_path + "/conf/endpoint.json")
            self.instance_dict = {}
            for endpoint in self.endpoint_arr:
                script_name = endpoint['script_name']
                class_name = endpoint['subclass_name']
                logger.info('instance %s ==> %s', script_name, class_name)
                ext_module = __import__(script_name)
                cls = getattr(ext_module, class_name)
                instance = cls()
                logger.info(dir(ext_module))
                self.instance_dict[script_name] = instance
            duration = time.time() - init_start_time
            logger.info('finished cost:%s s', duration)
        except Exception as e:
            logger.warn("Failed to start ,please check error log")
            logger.error("errmsg: %s , %s", str(e), traceback.format_exc())
            raise LoadException(message='start error' + str(e))

    def invoke(self, data, instance_name):
        if instance_name in self.instance_dict:
            output = self.instance_dict[instance_name].inference(data)
        else:
            raise InferException(message='infer instance is none')
        return output


def load_endpoint(path):
    with open(path, 'r') as load_f:
        arr = json.load(load_f)
    return arr
