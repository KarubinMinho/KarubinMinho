# IPIPTools



## Python版本

```bash
3.6+

```



## PIP依赖

```bash
netaddr==0.8.0

```



## 使用方法



### 导入

```python
>>> from ipiptools import IPIPTools

```



### 实例化

```python
# IPIPTools(country_code)
# country_code: 国家两位代码 大写 
# 参考：ipv4_china_cn.txt 字段
>>> us = IPIPTools('US')
>>> ca = IPIPTools('CA')

```



### 合并网段为CIDR

```python
# 合并对应 country_code 网段为 CIDR 格式
# 下例 us 为上面实例化后的 instance
>>> us.merge2cidr()

```



### 查看合并后的CIDR内容

```python
# 合并后可以直接查看CIDR内容
# return list
>>> us.cidr    

```



### 查看合并后的CIDR数量

```python
# 获取country_code合并后的cidr数量
>>> us.nums
91182

```



### 写文件

```python
# 将对应国家合并后的CIDR写入文件
# 如果dstpath=None 默认写到：./ForeignSet/countr_code.lower().set
>>> IPIPTools(country_code).write2file(dstpath=None)

# e.g. 将us合并后的cidr写入对应文件
>>> us.write2file(r'D:/temp/us.ip')    # 保存到指定文件
>>> or
>>> us.write2file()    # 保存到默认位置

```



### 获取所有2位代码缩写

```python
# 获取所有的 country_code 2位代码缩写
# 可以实例调用 也可以不用实例化 类直接调用
# A-Z 排序
>>> us.get_codes() # IPIPTools.get_codes()
AD 安道尔
AE 阿联酋
AF 阿富汗
AO 安哥拉
...
BB 巴巴多斯
BD 孟加拉
...
ZM 赞比亚
ZW 津巴布韦

```



### 获取统计数量前N的运营商

```python
# 获取统计前10的运营商 仅简单统计在ipv4.txt文件中出现的条数
# 也可以 类直接调用 IPIPTools.getisp(limit=20)
# limit 设置显示前N的运营商
>>> us.get_isp()
26962      chinamobile.com
21381      chinatelecom.com.cn
14642      chinaunicom.com
8246       cmtietong.com
7389       cht.com.tw
3821       edu.cn
3401       fetnet.net
1567       twmbroadband.com
1567       aliyun.com
1078       aptg.com.tw

```



### 获取BANList

```python
# 获取BANList(GOOGLE FACEBOOK TWITTER)
>>> ban = IPIPTools.cidr2ban()  # code: BANList
>>> ban.write2file()  # 将结果保存文件

```



### instance比较

```python
# 比较国家合并后的 CIDR 数量大小
>>> us > ca
True

```



### instance合并

```python
# 合并 已经合并后的2个国家的CIDR
>>> USCA = us + ca

```



### 转换文件内容为IPset_Format

```python
# 将纯IP格式调整为 ipset 需要的格式
# create us hash:net maxelem 1508228
# add us x.x.x.x
# ...
>>> us.set_ipset_format('./IPIP/ForeignSet/us.set')

```



### 直接执行

```python
# 直接执行 会解析合并下面元组的set 
# 默认保存到 项目目录下面的 ForeignSet/code.set 
# 并自动转换格式为 ipset_format
>>> country_codes = ('HK', 'CN', 'SG', 'TW', 'JP', 'KR', 'RU', 'VN', 'AU', 'TH', 'IN', 'CA', 'US', 'EU')

```



## 帮助文档

```python
Help on class IPIPTools in module IPIP.ipiptools:
class IPIPTools(builtins.object)
 |  IPIPTools(code, cidr=None)
 |  
 |  Methods defined here:
 |  
 |  __add__(self, other)
 |  
 |  __eq__(self, other)
 |      Return self==value.
 |  
 |  __ge__(self, other)
 |      Return self>=value.
 |  
 |  __gt__(self, other)
 |      Return self>value.
 |  
 |  __init__(self, code, cidr=None)
 |      Initialize self.  See help(type(self)) for accurate signature.
 |  
 |  __repr__(self)
 |      Return repr(self).
 |  
 |  merge2cidr(self)
 |      :return: list of cidr
 |  
 |  set_ipset_format(self, srcfile)
 |      :param srcfile: file_path that need to be converted
 |      :return: None
 |  
 |  write2file(self, dstpath=None)
 |      :param dstpath: save_path of ipset file
 |      :return: None
 |  
 |  ----------------------------------------------------------------------
 |  Class methods defined here:
 |  
 |  cidr2ban() from builtins.type
 |      :return: list of ban_cidr
 |  
 |  get_codes() from builtins.type
 |      :return: all country iso code
 |  
 |  get_isp(limit=10) from builtins.type
 |      :return: top limit isp
 |  
 |  ----------------------------------------------------------------------
 |  Data descriptors defined here:
 |  
 |  __dict__
 |      dictionary for instance variables (if defined)
 |  
 |  __weakref__
 |      list of weak references to the object (if defined)
 |  
 |  cidr
 |      :return: cidr of self.code
 |  
 |  nums
 |      :return: cidr length of merged
 |  
 |  ----------------------------------------------------------------------
 |  Data and other attributes defined here:
 |  
 |  __hash__ = None
    
```

