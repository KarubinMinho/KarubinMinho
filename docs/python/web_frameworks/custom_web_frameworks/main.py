from wsgiref.simple_server import make_server
from Django.urls import urls
from Django.views import *


def run(env, response):
    """
    :param env: 请求相关的所有数据 是一个大字典 wsgiref模块帮你处理好http格式的数据 封装成字典让你更加方便的操作
    :param response: 响应相关的所有数据
    :return: 返回给浏览器的数据
    """
    # print(env)
    # PATH_INFO: 请求路径信息
    current_path = env.get('PATH_INFO')
    response('200 OK', [])    # 响应首行 响应头
    # 定义一个变量 存储匹配到的函数名
    func = None
    for url in urls:
        if current_path == url[0]:
            # 将url对应的函数名赋值给func
            func = url[1]
            break  # 匹配到url 立即结束当前循环
    # 判断func是否有值
    if func:
        res = func(env)
    else:
        res = error(env)
    return [res.encode('utf-8')]


if __name__ == '__main__':
    """
    会实时监听127.0.0.1:8080地址 只有有客户端请求过来
    都会交给run函数处理(触发run函数的运行: run(environ, start_response)
    并注入2个参数：environ, start_response)
    函数： run()
    类：   类加() -> 实例: 能直接调用 -> 实现：__call__ 魔术方法
    
    e.g. flask启动源码：
         make_server('127.0.0.1', 8080, obj)
         __call__
    """
    server = make_server('127.0.0.1', 8080, run)
    server.serve_forever()  # 启动服务端
