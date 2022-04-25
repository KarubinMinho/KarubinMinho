

# Python基础

## 环境安装

推荐 pyenv 安装多独立版本虚拟环境



## 基础语法

- 变量/常量
- 运算符/表达式/语句
- 流程控制

```python
# 位运算符要比算术运算符快
# 对性能很高的场景使用： 加解密、编解码
```



## 内置容器

- 线性结构(有序的)
  - list  - 可变
  - 元组
  - 类字符串
    - str
    - bytes
    - bytearray -  可变
- 非线性结构(无序的)  (\_\_hash\_\_ \_\_eq\_\_  魔术方法)
  - set
  - dict
- 列表解析
- 迭代器/生成器
- 解构

```python
# 需要自定义的数据结构
简单的：链表

复杂的：
tree    # 树 各种树 看各种面试宝典学习
堆
图
```



## 函数

```bash
函数就像水管上的一个个接口 数据就像水管里的水 通过函数之后 对水做一些改变

1. 函数是组织代码的最小单元

2. 作用域

3. 有输入(参数) 有输出(返回值）
```



- 定义函数  **定义时**
  - 参数：可以理解为参数是一种协议 它是函数编写着来规范调用方如何传递数据的一种协议 **规范输入**
    - 参数默认值 (方便调用) 
    - 位置参数/关键字参数
    - keyword only参数/ position only参数
    - 可变参数
      - 可变位置传参
      - 可变关键字传参
  - 返回值：**规范输出** 
    - 有且仅有一个返回值 (一个元组)
    - 默认返回None
    - 返回元组的时候可以省略小括号 自动封装为tuple
      - 返回元组的时候 关联**解构**
  
- 调用函数

  ```python
  def add(x, y)
  	return x + y
  ```

  - 传参

    **按位置传参 可以和 关键字传参混用 但是必须位置参数在前**

    - 位置传参  

      ```python
      add(5, 5)
      ```

    - 关键字传参  **无序关注实参传入顺序**

      ```python
      add(x=3, y=5)  
      add(y=3, y=5)
      ```

    - 参数解构 **调用时**

      - 线性结构 使用单星号* 解构为按位置传参
      - 字典 使用双星号** 解构为关键字传参

  - 获取返回值

- 高阶函数

  ```bash
  当一个函数 它的参数 或者 返回值包含函数的时候 称之为高阶函数
  
  高阶函数和递归函数的区分：
    - 高阶函数：传递 或者 返回函数
    - 递归函数：函数体里调用自身的函数
  ```

  - 函数 和普通变量一样 -- 函数是一等公民

    - 可以当作参数传递

    - 可以当作返回值返回

      

  - 柯里化函数

    ```python
    def add(x, y):
        return x + y
    
    # 下面为add函数的柯里化 变形
    def f(x):
        def g(y):
            return x + y
       	return g
    ```

    

  - partial函数

    ```python
    # 第三方库 对我们传入的函数的参数有个数要求
    
    import functools
    
    functools.partial(add, 3)
    ```

  - 装饰器

    **装饰器也是一个函数 在被装饰函数执行前后做功能 增强 或 修改** 

    **当函数在装饰器之后轻易 可以使用@语法糖**

    **当函数在装饰器之前已经定义 可以用函数的方式使用装饰器**

    ```bash
    # 函数增强方式
    1. 在函数执行前做操作
    2. 在函数执行后做操作
    3. 对函数的参数做一些操作
    4. 对函数的返回值做一些操作
    5. 做一些记录工作
    ```

    - 对函数的一个装饰
    - 输入是函数（传入参数 是函数）
    - 输出也是函数（返回值是函数）

  - 带参数的装饰器

    - 还是一个函数
    - 返回一个装饰器

    ```python
    import logging
    from functools import wraps
    
    
    def logger(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            name = fn.__name__
            print(name)
            print(args)
            print(kwargs)
            ret = fn(*args, **kwargs)
            print(ret)
            return ret
        return wrapper
    
    
    def logger2(write=print):
        def logger(fn):
            @wraps(fn)  # == wraps(fn)(wrapper)
            def wrapper(*args, **kwargs):
                name = fn.__name__
                write(name)
                write(args)
                write(kwargs)
                ret = fn(*args, **kwargs)
                write(ret)
                return ret
            return wrapper
        return logger
    
    
    # add = logger(add)
    @logger2(logging.warning)
    def add(x, y):
        return x + y
    
    
    if __name__ == '__main__':
        add(5, 7)

    ```
    
    

- functools.wraps

  **把传入函数的属性 复制给返回函数的参数**

  - 接受一个函数作为参数
  - 返回一个函数

  ```python
  # 自己实现 functools.wraps的功能
  
  def wraps2(fn):  # 带参数的装饰器
      def wrapper(wrapped):  # 接收一个函数 返回一个函数
          wrapped.__name__ = fn.__name__
          # copy more
          return wrapped
      return wrapper
  
  # 类RPC
  def register(functions, name=None):
      def dec(fn):
          if name:
              functions[name] = fn
          else:
              functions[fn.__name__] = fn
          return fn
      return dec
  
  functions = {}
  
  @register(functions, name='_sum')
  def sums(*args):
      return sum(args)
  
  # nonlocal 关键字使用
  # nonlocal 关键字用于在嵌套函数内部使用变量 其中变量不应属于内部函数
  # 请使用关键字 nonlocal 声明变量不是本地变量
  def register(functions, name=None):
      def dec(fn):
          nonlocal name
          if not name:
              name = fn.__name__
          functions[name] = fn
          return fn
      return dec
  
  functions = {}
  
  
  @register(functions, name='_sum')
  def sums(*args):
      return sum(args)
  ```

- 生成器

  - 不是函数 只是长得像函数

  - yield：让出(暂停)当前栈帧 并且弹出yield后面跟的值

    ```python
    # 做IO操作的时候 用得多一些 
    
    def gen(base=0, max=10):
        while base <= max:
            base += 1
            yield base
    
    if __name__ == '__main__':
        g = gen(0, 5)
        print(type(g))
        for x in g:
        print(x)
    ```

- 作用域
  - 作用域指的是变量的可见性
  - 函数参数的作用域 属于函数
  - **默认参数可变时 一定要小心** add(args=[])



## 面向对象

- 类的定义

  - class 定义类

    ```python
    class Point:
        pass
    ```

    

  - 变量

    - 实例变量

      ```bash
      绑定到实例的变量
      通常在初始化方法中绑定并赋初始值
      实例变量的生命周期 等同于实例生命周期
      ```

    - 类变量

      ```python
      定义在方法之外 生命周期等同于类的生命周期
      此类的所有实例 共享类变量
      ```

    - 私有变量/方法

      **Python中不存在绝对的私有变量**

      ```python
      1. 私有变量 __private_var = xxx
      双下划线开头 但是不以双下划线结尾 通过变量重命名的方式实现私有
      
      2. 保护变量 _protect_var = xxx
      单下划线开头 程序员约定 是约定的保护变量
      ```

      

  - 方法

    ```bash
    方法和函数是非常相似的 甚至可以说 方法就是函数
    ```

    - 实例方法 

      ```python
      第一个参数：self 永远指代实例本身
      自动注入 实例 到 self
      
      def print_v(self):
          print(self.类变量, self.实例变量)
      ```

      - 初始化方法(构造方法)\_\_init\_\_
      - 普通方法
      - 魔术方法 （以双下划线开头 双下划线结尾）

    - 类方法

      ```python
      需要 @classmethod 装饰 
      自动注入 类 到 cls(第一参数命名)
      
      类方法可以访问类变量 但是不能访问实例变量
      
      @classmethod
      def cn(cls):
          print(cls.__name__)
      ```

    - 静态方法

      ```python
      需要 @staticmethod 装饰
      没有自动注入效果
      
      静态方法既不能方法问类变量 也不能访问实例变量
      
      @staticmethod
      def sm():
          pass
      ```

- 实例化

  - 类名(初始化参数列表)
  - self参数不需要传递 自动注入(隐式传递) 
  - 除了self参数会自动注入以外 其他和函数一样

- **封装**

  - **代码的组织方式**
  - 私有变量 私有方法的组织

- **继承**

  - 单继承

  ```python
  class Point:
      def __init__(self, x, y):
          self.x = x
          self.y = y
          
      def print(self):
          print(self.x, self.y)
  
  class Point3D(Point):
      def __init__(self, x, y, z):  # 继承父类方法 并修改、增强
          super().__init__(x, y)        self.z = z
  
      def print(self):  # 方法覆盖 重写
          print(self.x, self.y, self.z)
  
  if __name__ == '__main__':
      point = Point3D(3, 5, 8)
      point.print()
  ```

  - 多继承

    - MRO 方法查找顺序 

      ```python
      class A:
          pas
      A.mro()   
      A.__mro__
      
      * 按照mro 方法查找顺序 查找方法 找到第一个就就返回 
      * MRO通过C3算法得到
      ```
    * 有一些多继承的情况 会导致C3算法失败--Python会抛出异常
      ```
      
    ```
    - 多继承里面 super() 的行为也是难以预测的
    
      ```python
    他是查找 mro() 的上一层
      ```

    - 多继承是**危险**的 尽量避免使用多继承 除了一种场景：Mixin

    - **Mixin**
    
      - Mixin是一种特殊的类 无状态的类 -- 没有实例变量/类变量 没有初始化方法
      * 没有super()调用 不应该有super()
      - 以继承的方式实现组合
    - mixin不需要知道宿主类
        - 宿主类和mixin类通过协议通讯 -- 协议指宿主类具有某些实例变量 或者某些方法

      * 通常不能独立存在 独立使用
    
      ```python
      class HelloWorldMixIn:
          def print(self):
              print(f"hello {self.name}")
      
      class Pet:
          def __init__(self, name):
              self.name = name
      
      # 通过继承的方式 把Mixin的功能赋予了宿主类
      class PrintablePet(HelloWorldMixIn, Pet):
          pass
      
      if __name__ == '__main__':
          pp = PrintablePet('pppp')
          pp.print()
      ```

- **多态**

## 模块化

## 内建函数/标准库

- IO
- 并发
- socket





