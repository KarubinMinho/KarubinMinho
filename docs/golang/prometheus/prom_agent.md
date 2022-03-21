# Prometheus配置管理

```bash
cmdb web prometheus配置

promagentd:
​ API：
​  注册
​  心跳
​  配置获取

​ Agentd:
​  注册： 周期性 1h
​  心跳： 周期性 1m
​  获取配置： 周期性 15m(会有延迟)

Q: 如何减少获取配置延迟？
A: 间隔缩短至1min 但是这个时候配置不一定改变 需要检测配置是否变化 不变化则不用更新  定义：version/update_at字段 比较复杂的可以实现在心跳接口 发生变更再调用获取配置接口更新配置

更新prometheus.yml
kill -HUP $(pidof prometheus)
```

## logrus日志库

[logrus](https://pkg.go.dev/github.com/sirupsen/logrus)

```go
package main

import (
 log "github.com/sirupsen/logrus"
 "gopkg.in/natefinch/lumberjack.v2"
)

func main() {
 // handler, err := os.Create("logs/run.log")
 // if err != nil {
 //  log.Fatal(err)
 // }
 handler := &lumberjack.Logger{
  Filename:   "logs/run.log",
  MaxSize:    1, // Megabytes
  MaxBackups: 7,
  LocalTime:  true,
  Compress:   true,
 }
 defer handler.Close()

 log.SetLevel(log.DebugLevel) // 默认info级别
 log.SetFormatter(&log.TextFormatter{})
 // log.SetFormatter(&log.JSONFormatter{}) // json格式

 log.SetReportCaller(true) // 打印在哪个文件 哪一行输出的日志消息
 log.SetOutput(handler)

 for i := 0; i <= 10000; i++ {
  log.WithFields(log.Fields{
   "test":  "1",
   "test2": 2,
  }).Error("error")
  log.Warn("warning")
  log.Info("info")
  log.Debug("debug")
 }
}
```

## lumberjack日志切割库

[lumberjack](https://pkg.go.dev/gopkg.in/natefinch/lumberjack.v2)

## viper配置解析库

[viper](https://pkg.go.dev/github.com/spf13/viper)

```yaml
---
web:
  addr: 0.0.0.0:9999
  auth:
    user: Minho
    password: 123@456

mysql:
  host: 127.0.0.2
  port: 3307
  user: golang
  password: test@123
  db: cmdb
```

```go
package main

import (
 "fmt"
 "log"

 "github.com/spf13/viper"
)

type webConfig struct {
 Addr string
 Auth struct {
  User     string
  Password string
 }
}

type mysqlConfig struct {
 // 标签指定字段映射
 Addr string `mapstructure:"host"`
 Port int
}

type Config struct {
 Web   webConfig
 MySQL mysqlConfig
}

func main() {
 // 开启功能：从环境变量读取配置
 // 优先级：环境变量 > 配置文件 > 默认值
 viper.AutomaticEnv()
 // 设置环境变量以 prefix_ 开头才能读取到配置
 viper.SetEnvPrefix("testviper") // testviper_web.addr

 // 设置默认值
 // 没有配置文件 或者 配置文件没有配置相关的值 => 使用默认值
 viper.SetDefault("web.addr", ":10000")
 viper.SetDefault("mysql.host", "127.0.0.1")
 viper.SetDefault("mysql.port", 3306)
 viper.SetDefault("mysql.user", "root")
 viper.SetDefault("mysql.password", "")

 viper.SetConfigName("config")
 viper.SetConfigType("yaml")

 // 增加多个查找目录 
 viper.AddConfigPath("./etc/")
 viper.AddConfigPath(".")
    // 如何固定一个配置文件
    // viper.SetConfigFile(xx.yml)

 if err := viper.ReadInConfig(); err != nil {
  if _, ok := err.(viper.ConfigFileNotFoundError); ok {
   log.Println("config not found, use default")
  } else {
   log.Fatal(err)
  }
 }

 fmt.Println(viper.GetString("web.addr"))
 fmt.Println(viper.GetString("web.auth.user"))
 fmt.Println(viper.GetString("web.auth.password"))
 fmt.Println(viper.GetString("mysql.host"))
 fmt.Println(viper.GetString("mysql.port"))

 fmt.Println("=========")

 var config Config
 err := viper.Unmarshal(&config)
 fmt.Println(err)
 fmt.Printf("%#v\n", config)
 fmt.Println(config.MySQL.Addr)
 fmt.Println(config.MySQL.Port)
}
```

## req客户端请求库

[req](https://pkg.go.dev/github.com/imroc/req)

```go
package main

import (
 "crypto/tls"
 "fmt"
 "net/http"

 "github.com/imroc/req"
)

func main() {
 req.Debug = true
 client := &http.Client{
  Transport: &http.Transport{
   TLSClientConfig: &tls.Config{
    InsecureSkipVerify: true,
   },
  },
 }

 request := req.New()
 // 心跳
 // {uuid: "xx"}
 response, err := request.Post("https://localhost:8888/v1/agent/heartbeat", req.Param{
  "uuid": "xxxx",
 }, req.Header{"x-token": "820923a1a2dad74e8d279c48b8a1160c"}, client)

 if err == nil {
  rt := make(map[string]interface{})
  response.ToJSON(&rt)
  fmt.Println(rt)
 }
}
```