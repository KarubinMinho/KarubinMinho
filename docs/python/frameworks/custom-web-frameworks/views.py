def index(env):
    return 'index'


def login(env):
    return 'login'


def error(env):
    return '404 page not found'


def xxx(enx):
    with open('templates/xxx.html', encoding='utf-8') as f:
        return f.read()


import datetime
def get_time(env):
    current_time = "{:%F %T}".format(datetime.datetime.now())
    # 如何将后端获取到的数据"传递"给前端HTML文件?
    with open('templates/mytime.html', encoding='utf-8') as f:
        data = f.read()
    # 在后端将html页面处理好之后再返回给前端
    data = data.replace('%%time%%', current_time)
    return data


from jinja2 import Template
def get_dict(env):
    user_dic = {'username': 'Minho', 'age': 25, 'password': '!(#@$^*fjashidga'}
    with open('templates/get_dict.html', encoding='utf-8') as f:
        data = f.read()
    tmp = Template(data)
    res = tmp.render(user=user_dic)  # 给get_dict.html传递了一个值 页面上通过变量名user就能够拿到user_dict
    return res


import pymysql  # 仅测试使用
def get_user(env):
    # 去数据库中获取数据 传递给html页面(借助模板语法) 发送给浏览器
    conn = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        user='user',
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




