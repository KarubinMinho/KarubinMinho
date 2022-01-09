# PYTHON

## 环境安装

### 虚拟环境工具

[虚拟环境工具-pyenv](https://github.com/pyenv/pyenv)

[AutomaticInstaller](https://github.com/pyenv/pyenv-installer)

```Bash
# DependsInsatll
$ yum install -y git curl gcc make patch gdbm-devel openssl-devel sqlite-devel readline-devel zlib-devel bzip2-devel
```

### Pyenv

#### Pyenv 目录

```bahs
~/.pyenv/
```

#### 安装其他Python版本

```bash
# 备注：如果下载太慢 直接去官网下载源码包(.tar.xz) 保存到Pyenv目录的 cache目录(需要新建)下
pyenv install <version> [-vvv]
```

#### 缓存文件

```bash
# ~/.pyenv/cahce  缓存文件 存放目录 需要手动创建
mkdir -p ~/.pyenv/cache && wget https://www.python.org/ftp/python/3.6.12/Python-3.6.12.tar.xz -P  ~/.pyenv/cache
pyenv install 3.6.12 -vvv
```

#### 更换Python版本

  - golbal

    ```bash
    # 全局设置python版本为：3.6.12 不建议使用
    pyenv global 3.6.12  
    ```

  - shell

    ```bash
    # 当前会话：3.6.12 仅对当前会话(shell|session|terminal)有影响   
    pyenv shell 3.6.12  
    ```

  - local  

    ```bash
    # 把目录当成项目 每个项目可以使用不同版本
    # 将Pyehon version绑定目录 子目录同样有效 离开目录失效
    pyenv local 3.6.12
        
    # 这样使用 虽然每个项目(不同目录) 使用了不同版本 但是如果2个项目使用同一个版本 
    # 一个需要装django 1.8 另一个需要django 2.2 就会产生冲突
        
    # 解决方案：使用虚拟环境
    ```

    

#### 虚拟环境

```bash
pyenv virtualenv 3.6.12 virtualenv-3612  # 根据需要的版本 创建一个虚拟环境
cd $project_dir
pyenv local virtualenv-3612  # 为当前项目 设置虚拟环境
```



### PIP配置

[Aliyun源](http://mirrors.aliyun.com/)

```Bash
# Windows配置文件
~/pip/pip.ini

# Linux配置文件
~/.pip/pip.conf

# 内容
[global]
index-url = https://mirrors.aliyun.com/pypi/simple/

[install]
trusted-host=mirrors.aliyun.com
```

## 基础语法

### 字符串

```Bash
# 裸字符 r'str' r前缀
r'\n\tabcd'

# f字符串 插值 格式化字符串

# 续行 \

# 缩进

```

### 语言区别

```bash
# 动静
变量定义 是否需要事先申明类型

# 强弱 强制类型转换
自动转换 不报错     ---- 弱类型
不能做隐式类型转换   ---- 强类型
```

### 运算符

```python
# 除法 python2 都是整除
1/2     # 自然除法 python2 3除法不一样 差异
1//2    # 整除 向下取整

# 取模 取余
5 % 2   4 % 2

# 位运算符
& | ^ << >>
~ 按位取反 包括符号位

# 判断奇数
7 % 2 == 1    # 取余 判断结果是否为1
7 & 1 == 0    # 与运算 位与:按位相乘

0111
0001 &
-------
0001  == 1 

# 移位： <<   >>
<< 左移 == *2 *2 *2 *2 ...
>> 右移 == /2 /2 /2 /2 ...

0111    # 7
1110    # 14 = 7 * 2 | 7 << 1
11100   # 7 << 2 左移2位

# 短路运算
运算符 优化 -- 尽量短路 
- 逻辑运算符返回值不一定是Bool型
- 最频繁使用 决定整个逻辑表达式的值 尽量往前放

```

## 模块

### hashlib

```python
"""
1. 什么是hash
   hash是一类算法 该算法接受传入的内容 经过一系列运算得到一串hash值
   hash值的特点：
     1.1 只要传入的内容一样 得到的hash值必然一样
     1.2 不能跟据hash值反解出传入内容(没有绝对的安全 撞库...)
     1.3 只要使用的hash算法不变 无论传入的内容多大 得到的hash值长度固定


2. hash的用途
   1.2 用于密码密文传输与验证
   1.1 1.3 用于文件完整性校验

hash算法：
  MD5
  sha512
  sha256
"""
```

### 使用

#### 文件完整性

```python
import hashlib

# 得到hash工厂
m = hashlib.md5()
# m = hashlib.sha256()

# update() 传入bytes -> 不断给这个hash工厂运送原材料
"""
多次update的值合到一起 
  好处：内容比较大的情况下 比如校验文件(一行一行读 节约内存)
  缺点：文件内容过大 时间慢 如何解决? -> 解决：取一部分进行校验 不用全部读完
       f = open('file', mode='rb')
       f.seek() 选取几个点取内容 update进去
"""
m.update('hello'.encode('utf-8'))
m.update('world'.encode('utf-8'))

# 获取上面原材料合到一起得到的值
res = m.hexdigest()  # 'helloworld'
print(res)
```

#### 密码加盐

```python
import hashlib

# 密码前后加盐
m = hashlib.md5()
m.update('天王'.encode('utf-8'))
m.update(b'alex3714')
m.update('盖地虎'.encode('utf-8'))
print(m.hexdigest())
# 'ali天王ex37盖地虎14'  # 可以对密码截取 分开加盐

"""
加盐之后 撞库：
  1. 需要知道加的盐内容是什么
  2. 还需要知道你的盐加在了什么位置
"""
```



## 面向对象进阶

[魔术方法参考](https://pyzh.readthedocs.io/en/latest/python-magic-methods-guide.html)

**魔术方法 一般使用要小心 弄不好就会递归**

###  实例化

#### \_\_new\_\_

#### \_\_init\_\_

**初始化方法 构造器 or 构造方法**

```python
# __new__ 作用
# 1. 用在元编程当中 type构造类对象有关 metaclass
# 2. 构造实例

class A:
    def __new__(cls, *args, **kwargs):  # 实例化第一阶段：实例化
        print(cls)     # A类型
        print(args)    # 收集位置传参为元组
        print(kwargs)  # 收集关键字传参为字典
        # return None/return 'abc'
        # return cls(*args, **kwargs) RecursionError 递归异常
        # return object.__new__(cls)
    	return super().__new___(cls)
        # 实例化不能自己做 交给根基类实现 调根基类的__new__方法 
        # 传参cls 根据类型 制造实例
        # 没有绑定效果 永远是 静态方法
    
    def __init__(self):  # 实例化第二阶段：初始化
		pass

t = A()  

# 1. 实例化 => __new__(cls) 制造实例
# 2. 初始化 => __init__(self)

# 实例化伪代码
1. obj =  object.__new__(A)  # obj = instance
2. obj.__init__()  # 该方法不能有返回值 隐式 return None
3. return obj
```

```python
class A:
    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        instance.z = 200  # 建议放到__init__ 初始化方法
        cls.Z = 300  # 直接放到类属性定义 否则每次实例化都会重复覆盖Z属性
        return instance
   
	def __init__(self):
        pass
```

### 可视化

#### \_\_str\_\_ 

实例的字符串表达

```python
class A:
   def __init__(self):
        self.x = x
        self.y = y
        
    # 该实例的字符串表达 string
  	def __str__(self):  
        return "<A {}, {}, {}>".format(self.x, self.y, self(hex(id(self)))
```

#### \_\_repr\_\_ 

实例的非字符串表达

  ```python
class A:
    # 该实例的 非字符串表达形式
    def __repr__(self):
         return 'repr '  
                                         
    __str__ = __repr__  # 常用
          
class B(list):
    pass
  
# print 实例化后的对象 表现不同
# 继承 mro => object.__str__ 基类定义一个即可
print(A(5, 7))  # <__main__.A object at 0x00000xxx> 通用方式表达  
print(B())  # []    human-readable 符号性的表达
  ```

  **作用方法影响**

 print\str\format

  ```python
t = A(5, 7)
  
# str\print\format 直接作用实例 调用__str__ 方法
print(t)
print(str(t))
print('{}'.format(t))
  
# 下面不是直接作用实例 不调用__str__ 转而调用__repr__
print((t,))  # 作用在元组上
print([t])   # 作用在列表上
print(str([t]))
print({t})
  
# result: 直接作用
>>> <A 5, 7, addr=0x1f482195d88>
>>> <A 5, 7, addr=0x1f482195d88>
>>> <A 5, 7, addr=0x1f482195d88>
  
# result: 不是直接作用 间接作用调用__repr__
>>> (<__main__.A object at 0x000001F482195D88>,)
>>> [<__main__.A object at 0x000001F482195D88>]
>>> [<__main__.A object at 0x000001F482195D88>]
>>> {<__main__.A object at 0x000001F482195D88>}
  ```

  ```python
# print\str\format 三个函数
  - 直接作用对象上 调用 对象.__str__  => 尝试调用 __repr__ => object.__repr__  # 先继承(除object) 没有调用self.__repr__
  - 间接作用对象上 调用 对象.__repr__ => object.__repr__
    
repr(对象) => 对象.__repr__ => ...mro... => obj.__repr__
  ```

**Path类 例子**

```python
from pathlib import Path

p1 = Path('/etc/sysconfig/network')
print(p1)    # print直接作用到p1上 __str__
print([p1])  # print作用到列表上   __repr__

# open 拿到的是个Path对象 不是字符串
# 小心 可能会报错 这里不报错时因为：pathlib是Python内建函数 很多都已经能够使用Path实例 (内部会做判断)
with open(p1) as f: 
    pass

# 第三方函数(文件对象 or 路径字符串) -- OK
# 第三方函数(str(p1))  p1.__str__  返回路径字符串 -- OK
# 第三方函数(p1) == 第三方函数(repr(p1))  类型不对 -- Not OK

# 下面结果说明 Path类的 __str__ 和 __repr__ 不一样
>>> '\etc\sysconfig\network'
>>> [WindowsPath('/etc/sysconfig/network')]
```

#### \_\_bytes\_\_

```python
print(bytes(t))  # 报错 没有object兜底
>>> TypeError: cannot convert 'A' object to bytes

class A:
    # 该实例的 非字符串表达形式
    def __repr__(self):
        return 'repr '

    __str__ = __repr__  # 常用

    def __bytes__(self):  # bytes(t)
        return str(self).encode()  
        # str(self) => str(t) => t.__str__

t = A()
print(bytes(t))
>>> b'repr '
```

| 方法          | 意义                                                         |
| ------------- | ------------------------------------------------------------ |
| \_\_str\_\_   | str()\format()\print()函数调用 需要返回对象的字符串表达 <br>如果没有定义 就去调用\__repr__方法返回字符串表达 <br>如果\__repr__没有定义 就直接返回对象的内存地址信息 |
| \_\_repr\_\_  | 内建函数repr()对一个对象获取**字符串**表达 <br>调用\__repr__方法返回字符串表达 如果 \__repr__也没有定义 就直接返回object的定义(显示内存地址信息) |
| \_\_bytes\_\_ | butes()函数调用 返回一个对象的bytes表达 即返回bytes对象      |

### \_\_bool\_\_

```python
class A:
    pass

if A:  # 类对象 默认为真 => if bool(A)
    print('real A')

if A():  # 类实例 默认为真 => if bool(A())
    print('read A()')
    
>>> real A
>>> read A()

class B:
    def __bool__(self):  # self 跟当前实例(B的实例)有关
        return False
        # return bool(self)  递归

print(bool(B))  # B 类对象 type的实例
>>> True  # 类对象 默认为真

t = B()
print(bool(t))
>>> False # t.__bool__()
```

### \_\_len\_\_

```python
# 空容器 等效False 仅Python
  - []
  - ()
  - {}
  - set()
  - ''
  - b''
# 
  - None
  - 0

class B:
    def __len__(self):
        print('enter __len__')
        # return 100 -> True
        # 返回值 >=0; 0 False; >0 非空True
        # True if > 0 else False
        return 0
    
t = B()
print(bool(t))  # bool(t) => t.__bool__ => t.__len__
>>> enter __len__
>>> False

# 类实例 没有__bool__ __len__ 默认为真
# 类对象 默认为真 是type实例
class B:
    pass

bool(B), bool(B())
>>> (True, True)
```

| 方法         | 意义                                                         |
| ------------ | ------------------------------------------------------------ |
| \_\_bool\_\_ | 内建函数bool() 或者对象放在**逻辑表达式**的位置 调用这个函数 返回布尔值<br>没有定义\__bool__() 就找\__len_()返回长度(>=0) 非0为真<br>如果\__len__()也没有定义 那么所有实例都返回真 |

### 运算符重载

**运算符是一种语法糖**

| 运算符                        | 特殊方法                                                     | 含义                                 |
| ----------------------------- | ------------------------------------------------------------ | ------------------------------------ |
| < <= ==<br>> >= !=            | \_\_lt\_\_ \_\_le\_\_ \_\_eq\_\_<br>_\_gt_\_\_ \_\_ge\_\_ \_\_ne\_\_ | 比较运算符                           |
| + - * / <br>% // **<br>divmod | \_\_add\_\_ \_\_sub\_\_ \_\_mul\_\_ \_\_truediv\_\_ <br>\_\_mod\_\_ \_\_floordiv\_\_ \_\_pow\_\_ <br>\_\_divmod\_\_ | 算术运算符 移位 位运算也有对应的方法 |
| += -= *=<br>/= %= //= **=     | \_\_iadd\_\_ \_\_isub\_\_ \_\_imul\_\_<br>\_\_imod\_\_ \_\_ifloordiv\_\_ \_\_ ipow\_\_ | i -- inplace 就地修改                |

```python
# e.g. Path 路径拼接
from pathlib import Path

p1 = Path('/etc/sysconfig/network')
p1 / 'ifcfg-eth0'
'ifcfg-eth1' / p1

# 除法 / 对应着一个除法函数：除法函数重新定义 => 运算发重载
# 比如上面Path类中 / 做的除法运算符重载
#  1 / 2    => instance1.__xxx__(instance2)
# 'a' + 'b' => + 被运算符重载 用来描述字符串拼接 比用函数拼接(concat('a', 'b'))
```

#### \_\_gt\_\_ \_\_lt\_\_ \_\_eq\_\_

**大小比较 使用这三个方法 解决所有比较问题**

```python
class A:
    def __init__(self, x):
        self.x = x

print(sorted([A(5), A(2), A(3)]))  
# 自定义类A 没有实现> or <运算符重载 不支持比较
# 内建类型 Python自己实现 自定义类 需要自己实现内容比较
>>> TypeError: '<' not supported between instances of 'A' and 'A'
  
# 不能比较大小 单可以判断 ==
# == 同类型 比较内容 不知道怎么比较内容 同类型转为比较内存地址是否相同
# 不同类型 直接False
print(1, A(3) == A(5))
print(2, A(3) == A(3))
print(3, 100 == A(3))
>>> 1 False
>>> 2 False
>>> 3 False

class A:
    def __init__(self, x):
        self.x = x
	# 定义__eq__方法 解决 == 是否等于的问题
    def __eq__(self, other):  # 同时实现 != __ne__
        return self.x == other.x
    
    def __gt__(self, other):  # 同时实现 < __lt__
        return self.x > other.x
    
    def __ge__(self, other):  # 同时实现 <= __le__
        return self.x >= other.x
        
    def __repr__(self):
        return "<A {}>".format(self.x)

print(1, A(3) == A(5))  # A(3).__eq__(A(5))
print(2, A(3) == A(3))
print(3, 100 == A(3))  # 涉及反转的算法
>>> False
>>> True
>>> AttributeError: 'int' object has no attribute 'x'	

# 定义__gt__魔术方法之后 再次比较
print(sorted([A(5), A(2), A(3)]))  # A(5).__gt__(A(3))
>>> [<A 2>, <A 3>, <A 5>]    # __repr__方法输出

print(A(5) < A(3))  # 定义__gt__ 同时实现__lt__
>>> False
```

#### \_\_sub\_\_

```python
class Student:
    def __init__(self, name, score):
        self.name = name
        self.score = score

    # 减法运算符重载
    def __sub__(self, other):
        return self.score - other.score
    
    def __repr__(self):
        return "<Student {}: {}>".format(self.name, self.score)

tom = Student('Tom', 90)
jerry = Student('Jerry', 85)
print(tom)
print(tom - jerry)  # tom.__sub__(jerry)
tom -= jerry  # 调用__isub__ 如果没有转而调用tom.__sub__(jerry) +=类似
print(tom)
>>> <Student Tom: 90>  # 刚实例化后 是类对象
>>> 5
>>> 5  # -= 之后 改变了tom类型(不合适)：Student -> int

# 定义__isub__魔术方法解决该问题
# 方法1
def __isub__(self, other):  # inplace 就地修改
    # 重新构建了一个Student实例 内存地址改变
    return Student(self.name, self.score - other.score)

>>> <Student Tom: 90> 2716001388360
>>> <Student Tom: 5> 2716001388744

# 方法2
def __isub__(self, other):  # inplace 就地修改
    # 在self对象上直接修改 还是原来的实例 内存地址不变
    self.score -= other.score
    return self

>>> <Student Tom: 90> 2943212406664
>>> <Student Tom: 5> 2943212406664

# 方法3
def __isub__(self, other):  # inplace 就地修改
    # 比方法1 更通用 要先实现 __sub__
    # 同方法1 内存地址改变
    return Student(self.name, self - other)
```



### \_\_slots\_\_

```python
# 用tuple定义允许绑定的属性名称
# 限制实例的属性
# 使用__slots__要注意 __slots__定义的属性仅对当前类实例起作用 对继承的子类是不起作用的
class Student:
    __slots__ = ('name', 'age') 
    
s = Student()
s.height = 180
>>> AttributeError: 'A' object has no attribute 'height'
```



