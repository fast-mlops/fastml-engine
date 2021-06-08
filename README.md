### Algorithm Model Service Engine

#### 介绍

fastml-engine. 采用[Gunicorn](https://docs.gunicorn.org/)
Web服务框架搭建,以简化模型推理工程部署的工作内容

#### 功能特性

1. 集成Gunicorn Flask 服务组件,稳定可靠,可用于生产.
2. 统一推理服务接口,支持多种接口请求格式(text/json/octet-stream/form-data)
3. 搭配inference-template使用,支持自定义模型推理代码
4. 支持简便的启动命令

#### 安装
   ```
   pip install fastml-engine
   ```

#### 使用说明
1. 下载 inference-template-python [代码地址](https://github.com/fast-mlops/inference-template-python.git)
2. 启动服务
```shell
   fastml server --help  #查看帮助
   #service_path参数为inference-template-python目录的绝对路径
   fastml server --service-path /home/<service_path> --host 0.0.0.0 --port 5000
   #在未声明service-path参数的情况下，则使用当前命令执行路径
   fastml server --host 0.0.0.0 --port 5000
   #支持定义 model-path参数声明模型存放路径，未声明则默认使用<service-path>/model
   fastml server --service-path /home/<service_path> --model-path /opt/model --host 0.0.0.0 --port 5000
   #快速启动，执行如下命令，采用默认参数
   fastml server
```    
3. 验证服务  
   a)通过浏览器访问健康检查接口 ip:port/health  
   b)查看启动日志,日志目录在代码根路径/logs目录下

#### API接口

|  接口说明   |  URI   | 请求协议  |返回内容  |说明
|  ----  |  ----  | ----  | ----  | ---|
| 健康检查  | /health  | GET | ｛ status:UP｝ |
| 推理接口  | /algo/{endpoint}  | POST | 返回预测结果 |endpoint为BaseService实现类的名称(小写)，如果有多个实现类，则映射多个推理接口 |

> 健康检查接口响应报文

```json
{
  "status": "UP"
}
```

> 推理接口响应报文

```json
{
   "status": true,
   "data": {
      "k": "v"
   },
   "metadata": {
      "duration": 1.65576171875,
      "content_type": "json"
   }
}
```

#### 测试

注意：请求头需要添加Content-Type参数,用来指定请求报文格式

|  Content-Type   |  说明   | 
|  ----  |  ----  | 
| text/plain  | 文本格式  |
| application/json  | json格式  |
| application/octet-stream  | 文件 | 
| multipart/form-data  | form-data格式 |   


#### 日志

运行日志存放在推理引擎根目录logs文件夹下

1. access.log为请求调用日志
2. error-access.log为错误日志
3. app.log为业务日志,使用python logging模块打印
