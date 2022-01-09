# 自定义简易WEB框架

## 纯手写WEB框架

### HTTP协议

```python
# HTTP协议
网络协议：
HTTP协议        数据传输是明文
HTTPS协议       数据传输是密文
websocket协议   数据传输是密文

四大特性：
  1. 基于请求响应
  2. 基于TCP、IP作用于应用层之上的协议
  3. 无状态
  4. 短/无链接

数据格式：
  请求首行
  请求头
  \r\n\r\n
  请求体

响应状态码：
  1xx
  2xx    200
  3xx
  4xx    403  404
  5xx    500
  
```

### 简单WEB实现

- **socket实现简单请求-响应**

  ```python
  import socket
  
  server = socket.socket()  # TCP 三次握手四次挥手
  server.bind(('127.0.0.1', 8080))  # IP协议 以太网协议 arp协议...
  server.listen(5)  # 池
  
  # 请求相关的所有信息
  """
  b'GET / HTTP/1.1\r\n
  Host: 127.0.0.1:8080\r\n
  Connection: keep-alive\r\n
  Cache-Control: max-age=0\r\n
  Upgrade-Insecure-Requests: 1\r\n
  User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n
  Sec-Fetch-Site: none\r\n
  Sec-Fetch-Mode: navigate\r\n
  Sec-Fetch-User: ?1\r\n
  Sec-Fetch-Dest: document\r\nA
  ccept-Encoding: gzip, deflate, br\r\n
  Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6\r\n\r\n'
  """
  
  while True:
      conn, client = server.accept()
      data = conn.recv(1024)
      print(data)  
      # 简单加HTTP头之后再返回 浏览器便可以访问该socket服务端
      conn.send(b'HTTP/1.1 200 OK\r\n\r\nhello world')
      conn.close()
      
  ```

- **增加路径判断功能**

  ```python
  # 需求：1. 在上面基础上 如何做到后缀的不同返回不同的内容
  # 解决：拿到用户输入的 路径 做判断
  
  while True:
      conn, client = server.accept()
      data = conn.recv(1024)
      # print(data)                 # bytes
      data = data.decode('utf-8')  # 得到字符串
      # 获取字符串中特定内容 => 正则 or 字符串有规律可以使用：切割
      conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
      current_path = data.split()[1]  # 获取路径信息
      if current_path == '/index':
          conn.send(b'index.html')
      elif current_path == '/login':
          conn.send(b'login.html')
      else:
          conn.send(b'hello web')
      conn.close()
  
  # 需求 2. 返回html页面
  # 解决：修改返回数据代码 直接rb模式读取html文件并返回
  if current_path == '/index':
      with open(r'temp/index.html', 'rb') as f:
          conn.send(f.read())
  elif current_path == '/login':
      with open(r'temp/login.html', 'rb') as f:
          conn.send(f.read())
  else:
      with open(r'temp/index.html', 'rb') as f:
          conn.send(f.read())
  
  # 上面代码不足之处：
    1. 代码重复 重复造轮子  -- 服务端所有人都要重复写
    2. 手动处理http格式的请求数据 并且只能拿到url后缀 需要拿其他数据怎么办?  -- 数据格式一样 处理的代码其实也大致一样 重复写
    3. 路径处理需要一直使用if..else字据 维护性差
    4. 并发的问题 
  ```

### 借助wsgiref参考实现

**缺点**

- 没有写服务端代码 
- 没有写请求头处理代码 
- 可以专注业务逻辑的实现

```python
from wsgiref.simple_server import make_server

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
    if current_path == '/index':
        return [b'index']
    elif current_path == '/login':
        return [b'login']
    return [b'404 Page not found']

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
```

- **对url处理进行封装 优化if..else语句**
```python
from wsgiref.simple_server import make_server

def index(env):
    return 'index'

def login(env):
    return 'login'

def error(env):
    return '404 page not found'

# url与函数的对应关系
# 为什么是函数：组织处理该url访问的业务逻辑代码 不再是简单的一句return
urls = [
    ('/index', index),
    ('/login', login),
]

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

```

### 模块化

**全部文件放在同一个目录 后期会混乱 难以维护**

```python
# 解决：模块化
Projects/
    main.py      # 上面 wsgiref Server的封装
    urls.py      # 专门处理urls与业务函数影关系的模块
    views.py     # 专门编写业务函数处理逻辑的模块
    templates/   # html模板目录
        index.html
        login.html
        404.html
        ...
# main.py
from wsgiref.simple_server import make_server
from urls import urls
from views import *

def run(env, response):
    """
    :param env: 请求相关的所有数据 是一个大字典 wsgiref模块帮你处理好http格式的数据 封装成字典让你更加方便的操作
    :param response: 响应相关的所有数据
    :return: 返回给浏览器的数据
    """
    current_path = env.get('PATH_INFO')
    response('200 OK', [])    # 响应首行 响应头
    func = None
    for url in urls:
        if current_path == url[0]:
            func = url[1]
            break  # 匹配到url 立即结束当前循环
    if func:
        res = func(env)
    else:
        res = error(env)
    return [res.encode('utf-8')]

if __name__ == '__main__':
    server = make_server('127.0.0.1', 8080, run)
    server.serve_forever()  # 启动服务端
        
# urls.py
from views import index, login, xxx

urls = [
    ('/index', index),
    ('/login', login),
    ('/xxx', xxx),
]

# views.py
def index(env):
    return 'index'

def login(env):
    return 'login'

def error(env):
    return '404 page not found'

def xxx(enx):
    with open('templates/xxx.html', encoding='utf-8') as f:
        return f.read()

```

### 总结

```python
# 按照功能不同拆分之后 后续添加功能只需要再urls.py书写对应关系 然后在views.py书写业务逻辑即可

# 路由与视图函数对应关系
../urls.py   

# 视图函数(后端业务逻辑) 备注：视图函数可以是函数 也可以是类 
  - 面向函数式编程 
  - 面向对象式编程
../views.py  

# 专门用来存储html文件
../templates文件夹  
```

## 动静态网页

```python
"""
静态网页：
  页面上的数据是直接写死的 万年不变
  
动态网页：
  数据是实时获取的
  在后端发生的 不在浏览器上 后端直接渲染好html返回给浏览器
  e.g.:
    1. 后端获取当前时间 展示到html网页上
    2. 数据是从数据库中获取的 展示到html页面上

"""

# 动态网页制作
import datetime
def get_time(env):
    current_time = "{:%F %T}".format(datetime.datetime.now())
    # 如何将后端获取到的数据"传递"给前端HTML文件?
    with open('templates/mytime.html', encoding='utf-8') as f:
        data = f.read()
    # 在后端将html页面处理好之后再返回给前端
    data = data.replace('%%time%%', current_time)
    return data

# 将一个字典传递给html文件 并且可以在文件上方便快捷操作字典数据 --> Jinja2
from jinja2 import Template
def get_dict(env):
    user_dic = {'username': 'Minho', 'age': 25, 'password': '!(#@$^*fjashidga'}
    with open('templates/get_dict.html', encoding='utf-8') as f:
        data = f.read()
    tmp = Template(data)
    res = tmp.render(user=user_dic)  # 给get_dict.html传递了一个值 页面上通过变量名user就能够拿到user_dict
    return res

# 后端获取数据库中数据展示到前端页面
import pymysql
def get_user(env):
    # 去数据库中获取数据 传递给html页面(借助模板语法) 发送给浏览器
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='minho',
        password='passwd',
        db='test',
        charset='utf8',
        autocommit=True
    )
    cursor = conn.cursor(cursor=pymysql.cursors.DictCursor)
    sql = 'select * from employees'
    affect_rows = cursor.execute(sql)
    data_list = cursor.fetchall()  # [{}, {}, {}]
    # 将获取到的数据 传递给html文件
    with open('templates/get_data.html', encoding='utf-8') as f:
        data = f.read()
    tmp = Template(data)
    res = tmp.render(emp_list=data_list)
    return res

```

## 模板技术

### Jinja2

```python
pip install jinja2

"""模板语法是在后端起作用的 先在后端渲染好HTML页面 然后返回去浏览器"""

# 模板语法(非常贴近Python语法) 有时候比Python语法更简单
{{ user_list }}
{% for i in user_list %}
{% endfor %}

<!--Jinja2模板语法-->
{{ user }}
{{ user.get('username') }}
{{ user.password }}
{{ user['age'] }}

# Jinja2 循环列表数据
<tbody>
<!--[{}, {}, {}]-->
{% for emp in emp_list %}
<tr>
<td>{{ emp.emp_no }}</td>
<td>{{ emp.birth_date }}</td>
<td>{{ emp.first_name + ' ' + emp.last_name }}</td>
<td>{{ emp.gender }}</td>
<td>{{ emp.hire_date }}</td>
</tr>
{% endfor %}
</tbody>
```

## 自定义简易版本web框架请求流程图

```python
"""
wsgiref模块 作用：
  1. 请求来的时候 解析http格式的数据 封装成大字典 -- envrion
  2. 响应走的时候 给数据打包成符合http格式 再返回给浏览器  -- start_response
"""
```

