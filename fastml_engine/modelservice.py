import sysconfig

import six
import logging
from abc import ABCMeta, abstractmethod

logger = logging.getLogger(__name__)


@six.add_metaclass(ABCMeta)
class BaseService(object):
    """
    推理主类，BaseService，作为推理调用的主方法入口，支持文本字符串、JSON、二进制参数类型(文件、图片)
    方法介绍：
           load_context:上下文初始化方法
           infer:推理主方法
    """

    def __init__(self, service_path, model_path):
        self.service_path = service_path
        self.model_path = model_path
        self.load_context()

    @abstractmethod
    def load_context(self):
        """
        初始化上下文，默认在__init__方法中被调用，需要自定义实现逻辑
        """
        pass

    @abstractmethod
    def infer(self, input_data):
        """
        推理方法，响应推理请求时调用，需要自定义实现逻辑
        """
        output_data = input_data
        return output_data

    def endpoint(self) -> str:
        """
        获取端点，使用类名称作为默认值
        可重写返回自定义端点
        """
        return self.__class__.__name__.lower()

    def health(self):
        """
        健康检查方法
        可重写定义检查逻辑
        """
        return {'status': 'UP'}

    def info(self):
        # 服务详细信息，展示系统信息、进程信息、服务信息
        pythonversion = sysconfig.get_python_version()
        # TODO
        return pythonversion


if __name__ == '__main__':
    print(sysconfig.get_python_version())
