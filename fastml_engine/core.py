#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import traceback
import time
import os
from fastml_engine.log import Logger
from fastml_engine.exception.infer_exception import InferException
from fastml_engine.exception.load_exception import LoadException
from fastml_engine.modelservice import BaseService


class ServiceEngine:

    def __init__(self):

        service_path = os.getenv('SERVICE_PATH')
        model_path = os.getenv('MODEL_PATH')
        if service_path and os.path.exists(service_path):
            logger = Logger(log_path=service_path + "/logs").getLogger(__name__)
            logger.info('service_path: %s', service_path)
        else:
            raise LoadException('service_path is none, terminated')
        source_path = service_path + '/src'
        if not os.path.exists(source_path):
            raise LoadException('src dir not exist, terminated')
        try:
            logger.info("starting...")
            init_start_time = time.time()
            sys.path.append(source_path)
            subclasses = load_service('inference', source_path)
            self.instance_dict = {}
            for cls in subclasses:
                instance = cls(service_path, model_path)
                name = instance.endpoint()
                self.instance_dict[name] = instance
            duration = time.time() - init_start_time
            print(self.instance_dict)
            logger.info('finished cost:%s s', duration)
        except Exception as e:
            logger.warn("Failed to start ,please check error log")
            logger.error("errmsg: %s , %s", str(e), traceback.format_exc())
            raise LoadException(message='start error' + str(e))

    def infer(self, data, instance_name):
        return self.get_instance(instance_name).infer(data)

    def health(self, instance_name):
        return self.get_instance(instance_name).health()

    def info(self, instance_name):
        return self.get_instance(instance_name).info()

    def sys_info(self):
        # TODO
        return None

    def get_instance(self, instance_name):
        if instance_name in self.instance_dict:
            return self.instance_dict[instance_name]
        else:
            raise InferException(message=instance_name + ' instance is not define')


def load_service(name, path):
    import inspect
    import importlib
    module = importlib.import_module(name, path)
    classes = [cls[1] for cls in inspect.getmembers(module, inspect.isclass)]
    subclasses = list(filter(lambda c: issubclass(c, BaseService) and len(c.__subclasses__()) == 0, classes))
    return subclasses
