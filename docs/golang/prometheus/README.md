# ⭐ Prometheus

[官网](https://prometheus.io/)

## 安装

[二进制包安装](https://prometheus.io/download/)

```bash
#!/usr/bin/env bash

export VERSION=2.26.0
wget https://github.com/prometheus/prometheus/releases/download/v${VERSION}/prometheus-${VERSION}.linux-amd64.tar.gz
tar -xzvf prometheus-${VERSION}.linux-amd64.tar.gz -C /usr/local/
cd /usr/local/
ln -sv prometheus-${VERSION}.linux-amd64/ prometheus
```

[yum安装](https://packagecloud.io/app/prometheus-rpm/release/search)

```bash
curl -s https://packagecloud.io/install/repositories/prometheus-rpm/release/script.rpm.sh | sudo bash
```

[docker-compose安装](https://github.com/ilolicon/prometheus-compose)

## 基础认证

[BasicAuth](https://prometheus.io/docs/guides/basic-auth/)

```bash
# Web Basic
 user:password
 
# Prometheus scrape:
 - Web Basic
 - Token方法

 Authorization: Token
  - web basic: Basic[空格]base64(user:password)
  - bearer token: Bearer[空格]Token
   格式： token jwttoken(如果有失效日期 需要同步配置文件)
```

## 配置文件

```yaml
# Prometheus.yml
global:
  scrape_interval:     15s # 抓取周期 默认1分钟
  evaluation_interval: 15s # 内置的记录规则/告警规则的评估周期 

# Alertmanager告警配置
alerting:
  alertmanagers:
  - static_configs:
    - targets:
      # - alertmanager:9093

# 规则(告警规则 record规则)
rule_files:  # 载入外部的规则配置
  # - "first_rules.yml"
  # - "second_rules.yml"

# 抓取配置
scrape_configs:  # 采集/刮擦的配置
  - job_name: 'prometheus'
    static_configs:  # 静态配置
    - targets: ['localhost:9090']  # targets 可以是静态配置 也可以是自动发现
    
# 默认使用: http 默认采集路径: /metrics
scheme: http
metrics_path: /metrics
```

## Exporters

### node_exporter

```bash
wget https://github.com/prometheus/node_exporter/releases/download/v1.1.2/node_exporter-1.1.2.linux-amd64.tar.gz

# 或者直接yum安装 配置上面的yum仓库
yum -y install node_exporter
systemctl restart node_exporter

./node_exporter --help  # 查看参数 包括指定收集哪些数据
```

### blackbox_exporter

[黑盒监控](https://www.infoq.cn/article/sxextntuttxduedeagiq)

[网络探测黑盒监控](https://cloud.tencent.com/developer/article/1584310)

```bash
# blackbox_exporter 在执行ICMP时 只发送一个数据包
# 因此 "数据包数量"的等价物基于probe_success度量

# 包数: count_over_time(probe_success[5m])
# 返回数据包数: sum_over_time(probe_success[5m])
# 可用性: avg_over_time(probe_success[5m])
```

### 自定义exporter

[client-libraries](https://prometheus.io/docs/instrumenting/clientlibs/)

[go-application](https://prometheus.io/docs/guides/go-application/)

[client-golang](https://pkg.go.dev/github.com/prometheus/client_golang)

[write-clientlibs](https://prometheus.io/docs/instrumenting/writing_clientlibs/)

[prometheus-doc](https://pkg.go.dev/github.com/prometheus/client_golang/prometheus#section-documentation)

#### 指标类型

- Counter
- Guage
- Histogram
- Summary

#### 标签是否动态

- 固定标签
- 动态标签

#### 开发流程

1. 指定指标
2. 注册指标
3. 启动web服务器(注册promhttp Handler)
4. 指标信息更新

#### 指标信息更新

- 指标信息提供者

1. 事件触发型 如:http请求时更新
2. 事件触发型 如:周期性更新

- Prometheus调用metrics api触发获取

#### 示例

```go
package main

import (
 "bytes"
 "encoding/base64"
 "fmt"
 "math/rand"
 "net/http"
 "strconv"
 "strings"
 "time"

 "github.com/prometheus/client_golang/prometheus"
 "github.com/prometheus/client_golang/prometheus/promhttp"
)

type MemPercentCollector struct {
 desc *prometheus.Desc
}

func NewMemPercentCollector() *MemPercentCollector {
 return &MemPercentCollector{
  prometheus.NewDesc("mem_percent", "Mem Percent", nil, nil),
 }
}

func (c *MemPercentCollector) Describe(ch chan<- *prometheus.Desc) {
 ch <- c.desc
}

func (c *MemPercentCollector) Collect(ch chan<- prometheus.Metric) {
 // 四种类型返回值
 fmt.Println("Mem Percent")
 ch <- prometheus.MustNewConstMetric(c.desc, prometheus.GaugeValue, rand.Float64()*100)
}

var (
 requestTotal = prometheus.NewCounter(prometheus.CounterOpts{
  Namespace:   "dev",
  Subsystem:   "web",
  Name:        "http_request_total",
  Help:        "web server http request total",
  ConstLabels: map[string]string{"env": "dev"},
 })

 syncTaskTotal = prometheus.NewCounterVec(prometheus.CounterOpts{
  Name: "sync_task_total",
  Help: "Sycn data tasl total",
 }, []string{"type"})

 // 访问/metrics触发
 currentTime = prometheus.NewCounterFunc(prometheus.CounterOpts{
  Name: "web_server_current_time",
  Help: "Web Server Current Time",
 }, func() float64 {
  fmt.Println("current time")
  return float64(time.Now().Unix())
 })

 // GaugeVec
 cpuPercent = prometheus.NewGaugeVec(prometheus.GaugeOpts{
  Name: "web_server_cpu_percent",
  Help: "Web Server CPU Percent",
 }, []string{"cpu"})

 delayHistogram = prometheus.NewHistogramVec(prometheus.HistogramOpts{
  Name:    "web_process_delay",
  Help:    "Web Process Dealy",
  Buckets: prometheus.LinearBuckets(2, 2, 5),
 }, []string{"path"})

 delaySummary = prometheus.NewSummaryVec(prometheus.SummaryOpts{
  Name:       "web_process_delay_summary",
  Help:       "Web Process Delay Summary",
  Objectives: map[float64]float64{0.6: 0.05, 0.8: 0.02, 0.9: 0.01, 0.95: 0.005, 1: 0.001},
 }, []string{"path"})
)

// 事件触发 每次访问 / 的时候+1
func IndexHandler(w http.ResponseWriter, r *http.Request) {
 delay := float64(rand.Intn(20))
 delayHistogram.WithLabelValues(r.URL.Path).Observe(delay)
 delaySummary.WithLabelValues(r.URL.Path).Observe(delay)
 rand.Intn(20)
 fmt.Println("IndexHandler")
 requestTotal.Inc()
 fmt.Fprintf(w, "%d", time.Now().Unix())
}

func Auth(handler http.Handler) http.Handler {
 return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
  // 检查前
  authorization := r.Header.Get("Authorization")
  prefix := "Basic "
  // if strings.HasPrefix(authorization, prefix) {
  //  authorization = authorization[len(prefix):]
  // }
  authorization = strings.TrimPrefix(authorization, prefix)
  txt, err := base64.StdEncoding.DecodeString(authorization)
  if err != nil || !bytes.Equal(txt, []byte("minho:123")) {
   // 认证失败
   w.Header().Add("www-authenticate", "Basic")
   w.WriteHeader(401)
   return
  }

  handler.ServeHTTP(w, r)
  // 检查后
 })
}

func main() {
 rand.Seed(time.Now().Unix())

 // 同步任务1 周期性触发
 go func() {
  for range time.Tick(time.Second * 10) {
   fmt.Println("task1")
   syncTaskTotal.WithLabelValues("task1").Inc()
  }
 }()
 // 同步任务2 周期性触发
 go func() {
  for range time.Tick(time.Second * 3) {
   fmt.Println("task2")
   syncTaskTotal.WithLabelValues("task2").Inc()
  }
 }()

 go func() {
  for range time.Tick(time.Second * 10) {
   for i := 0; i < 4; i++ {
    fmt.Println("cpu percent", i)
    cpuPercent.WithLabelValues(strconv.Itoa(i)).Set(rand.Float64() * 100)
   }
  }
 }()

 // 1. 定义指标
 // 2. 注册指标
 prometheus.MustRegister(requestTotal)
 prometheus.MustRegister(syncTaskTotal)
 prometheus.MustRegister(currentTime)
 prometheus.MustRegister(cpuPercent)
 prometheus.MustRegister(delayHistogram)
 prometheus.MustRegister(delaySummary)
 prometheus.MustRegister(NewMemPercentCollector())
 // 3. 注册处理器
 // 4. 启动web服务
 // 5. 更新指标信息
 // fmt.Println(prometheus.LinearBuckets(2, 2, 5))

 addr := ":9999"
 http.Handle("/", Auth(http.HandlerFunc(IndexHandler)))
 http.Handle("/metrics/", Auth(promhttp.Handler()))
 http.ListenAndServe(addr, nil)
}
```

### 内置client_golang

```bash
# 比如：内置在cmdb里面 暴露cmdb的一些指标

# 需要使用框架的两个钩子函数
  - 请求来之前
  - 请求处理过后
  
# Beego
Filter Before
  - 总的请求次数 Counter
  - 每个URL请求次数 Counter
  
Filter After
  - 每个状态码的出现次数 Counter
  - 每次URL请求延迟时间统计 Histogram
```

```go
package filters

import (
 "strconv"
 "time"

 "github.com/beego/beego/v2/server/web/context"

 "github.com/prometheus/client_golang/prometheus"
)

var (
 totalRequest = prometheus.NewCounter(prometheus.CounterOpts{
  Name: "cmdb_request_total",
  Help: "cmdb request total",
 })

 urlRequest = prometheus.NewCounterVec(prometheus.CounterOpts{
  Name: "cmdb_request_url_total",
  Help: "cmdb request url total",
 }, []string{"url"})

 statusCode = prometheus.NewCounterVec(prometheus.CounterOpts{
  Name: "cmdb_status_code",
  Help: "cmdb status code",
 }, []string{"status_code"})

 elapsedTime = prometheus.NewHistogramVec(prometheus.HistogramOpts{
  Name:    "cmdb_url_elapsed_time",
  Help:    "cmdb url elapsed time",
  Buckets: prometheus.LinearBuckets(1, 5, 1),
 }, []string{"url"})
)

func init() {
 prometheus.MustRegister(totalRequest)
 prometheus.MustRegister(urlRequest)
 prometheus.MustRegister(statusCode)
 prometheus.MustRegister(elapsedTime)
}

func BeforeExec(ctx *context.Context) {
 totalRequest.Inc()
 urlRequest.WithLabelValues(ctx.Input.URL()).Inc()
 ctx.Input.SetData("stime", time.Now().Unix())
}

func AfterExec(ctx *context.Context) {
 statusCode.WithLabelValues(strconv.Itoa(ctx.ResponseWriter.Status)).Inc()
 stime := ctx.Input.GetData("stime")
 if stime != nil {
  if st, ok := stime.(int64); ok {
   elapsed := time.Now().Unix() - st
   elapsedTime.WithLabelValues(ctx.Input.URL()).Observe(float64(elapsed))
  }
 }
}
```

## PromQL

Prometheus提供PromQL功能用于时许数据的查询和统计

### 表达式数据类型

- 瞬时向量

```bash
针对每个查询结果集单项中只包含一组时序数据和样本值
```

- 范围向量

```bash
针对每个查询结果集单项中包含多组时许数据和样本值 带时间区间
```

- 标量

```bash
浮点型数据 float64
```

- 字符串

```bash
字符串类型 string
```

### 瞬时向量查询

- 指定指标名称查询

```bash
up
prometheus_http_requests_total
node_boot_time_seconds
node_cpu_percent
node_mem_percent
node_cpu_seconds_total
```

```bash
# 指标名若未prometheus关键字 则必须使用__name__标签指定指标名称进行查询
{ __name__ = "up" }

# 关键字
bool
on
ignoring
without
by
group_left
group_right
```

- 指定指标及标签进行查询

```bash
# 标签比较方法
# = 与字符串匹配
node_cpu_seconds_total{mode="idle"}

# != 与字符串不匹配
node_cpu_seconds_total{mode!="idle"}

# =~ 与正则表达式匹配
node_cpu_seconds_total{mode=~"idle|system"}

# !~ 与正则表达式不匹配
node_cpu_seconds_total{mode!~"idle|system"}
```

### 范围向量查询

在瞬时向量查询表达式后 使用[]指定查询数据时间范围 默认相对当前时间

```bash
# 时间单位
# 秒： s
# 分： m
# 时： h
# 天： d
# 周： w
# 年： y
node_cpu_percent[5m]
```

### 偏移量

修改查询数据偏移时间

```bash
# 5分钟前的cpu使用率
node_cpu_percent offset 5m

# 5分钟前的5分钟内的cpu使用率数据
node_cpu_percent[5m] offset 5m
```

### 子查询

查询给定时间范围及刻度范围向量

```bash
irate(node_cpu_percent[5m])[30m:1m]
```

### 运算

- 算数运算

```bash
# 运算符
+ - * / % ^

# 操作数
- 两个标量
- 一个瞬时向量 一个标量 # 向量中的每个数据 与 标量进行计算的新向量
- 两个瞬时向量 # 将左侧向量中的每个元素与右侧对应的向量元素进行计算组成新的向量
```

- 关系运算

```bash
# 运算符
== != > < >= <=

# 运算结果
0/false 1/true

# 默认情况将过滤出结果为true的数据 若需要计算结果true/false 则需要使用bool关键字
up == 1 # 会过滤掉结果
up == bool 1 # 得到比较的结果

# 操作数
- 两个标量
- 一个瞬时向量 一个标量
- 两个瞬时向量
```

- 逻辑运算

```bash
# 两个操作数都为瞬时向量

# 运算符
and
or
unless
```

- 向量匹配

```bash
# 左操作数与右操作数中相同标签元素数量关系
1：1
1：n或n:n
```

- 集合运算符

```bash
# 运算符
count
stdvar
topk
...
```

### 内置函数

```bash
abs
absent
absent_over_time # 有over_time说明操作数据是范围向量 没有则操作瞬时向量
ceil             # 向上取整
floor
changes
clamp_max        # 设置瞬时向量样本最大值/最小值
clamp_min
day_of_month
delta            # 第一个值和最后一个值的差
idelta           # 适用敏感性较强的时序数据
deriv
exp
rate             # 计算时序数据每秒平均增长率
irate
increase
time
timestamp
resets           # 计算重置次数
round
scalar
vector
<op>_over_time   # 操作范围向量
...
```

### PromQL示例

```bash
# 每台主机CPU在5分钟内的平均使用率
(1-avg(irate(node_cpu_seconds_total{mode="idle"}[5m])) by (instance)) * 100

# node_exporter 没有上报主机名的情况下 使用主机名标签过滤
sum(rate(node_network_receive_bytes_total{device="eth0"}[5m]) * 8 * on(instance) group_left(nodename) node_uname_info{nodename=~"txgz.*"})
```

## HTTPAPI

### 查询

```bash
和web界面发起请求的url一致
```

### 管理员

需命令行参数 `--web.enable-admin-api` 开启

```bash
# 功能
- 快照
- 删除时序  /api/v1/admin/tsdb/delete_series
- 清理磁盘数据

说明：数据并未真正从磁盘删除 后续在压缩时进行清理
```

### 生命周期管理

需命令行参数 `--web.enable-lifecycle` 开启

```bash
# 功能
- 健康状态
- 准备状态
- 重新加载配置 /-/reload # 如果开启一定要注意访问权限
- 退出 /-/quit
```

## 联合模式

```bash
# 联邦集群

联合模式允许Prometheus从另一个Prometheus服务器抓取数据
metrices_path: /federate
```

## 告警管理

### 用途

- 告警分组
- 静默处理
- 抑制处理
- 高可用(配置多个AlertManager)
- 发送处理

### 配置

参考官方文档

### 管理API

```bash
# 功能
- 健康状态
- 准备状态 /-/ready
- 重新加载配置 /-/reload # 如果开启一定要注意访问权限
```

## Alertmanager

[alertmanager](https://prometheus.io/docs/alerting/)
