# socket开发

```go
// 网络 + Go开发网络功能 net库...
// 协议分层模型 OSI
// TCP/UDP

// 开发什么：服务端 客户端
// 如何开发

TCP: // 服务端
    1. 创建监听
	2. for
		a. 接收客户端连接
		b. go 处理客户端业务
			// 规则1：读/写顺序、次数
            // 规则2：数据格式
			获取数据(读数据)
			响应数据(写数据)
	4. 关闭监听

TCP： // 客户端
	1. 连接服务
	2. 处理业务
		a. 获取数据
		b. 响应数据
	3. 关闭连接
```

## net包基础

```go
package main

import (
	"fmt"
	"net"
)

func main() {
	fmt.Println(net.JoinHostPort("127.0.0.1", "9999"))
	fmt.Println(net.LookupAddr("127.0.0.1"))
	fmt.Println(net.LookupHost("www.qq.com")) // 通过域名找地址

	// ip => IP类型
	// 字符串 ipv4 点分十进制
	// ipv6 ::
	var ip net.IP = net.ParseIP("8.8.8.8")
	fmt.Println(ip) // ParseIP给定错误IP格式 返回nil
	ip = net.ParseIP("x")
	fmt.Println(ip == nil) // true

	// ip段 cidr格式
	ip, ipnet, err := net.ParseCIDR("192.168.0.0/24")
	fmt.Println(ip)
	fmt.Println(ipnet)
	fmt.Println(err)

	// Contains 判断一个IP是否在一个IP段中
	fmt.Println(ipnet.Contains(net.ParseIP("192.168.0.1")))
	fmt.Println(ipnet.Contains(net.ParseIP("192.168.1.1")))

	// Addrs 网络地址
	fmt.Println("addrs:")
	addrs, err := net.InterfaceAddrs()
	for k, v := range addrs {
		fmt.Println(k, v.Network(), v.String())
	}

	// Interfaces 网卡地址
	fmt.Println("interfaces:")
	intfs, err := net.Interfaces()
	for k, v := range intfs {
		fmt.Println(k,
			v.Name,
			v.MTU,
			v.Flags,
			v.HardwareAddr.String(),
		)
		fmt.Println(v.Addrs())
		fmt.Println(v.MulticastAddrs())
	}
}
```

## server.go

```go
// 使用channel来获取终止信号
package main

import (
	"log"
	"net"
)

func main() {
	addr := "127.0.0.1:8888"

	listener, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatal(err)
	}
	interrupt := make(chan int, 1)
	go func() {
		// interrupt写入终止信号
	}()
END:
	for {
		select {
		case <-interrupt:
			break END
		default:
		}

	}

	listener.Close()
}
```

```go
// 服务端处理流程 只需要填handle处理逻辑函数
package main

import (
	"fmt"
	"log"
	"net"
	"time"
)

func handle(conn net.Conn) {
	defer conn.Close()
	// 处理逻辑
	// 对于每一个server 外面的逻辑都是一样的 只有handle处理逻辑不一样
	// fmt.Println("local addr:", conn.LocalAddr())
	fmt.Println("client connectd:", conn.RemoteAddr())
	fmt.Fprintf(conn, time.Now().Format("2006-01-02 15:04:05"))
}

func main() {
	addr := "127.0.0.1:8888"

	listener, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("listen: ", listener.Addr())
	defer listener.Close()

END:
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("error access: %s", err)
			break END
		}
		go handle(conn)
	}
}
```

## client.go

```go
package main

import (
	"fmt"
	"log"
	"net"
)

func main() {
	addr := "127.0.0.1:8888"
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close() // 关闭连接

	// 处理业务(交换数据)
	buffer := make([]byte, 1024)
	n, err := conn.Read(buffer)
	if err != nil {
		panic(err)
	}
	fmt.Println(string(buffer[:n]))
}
```

## 聊天服务器/tcp

```go
// chatServer
1. 谁先说：客户端先说 服务端先读
2. 每次说话说多少内容 读取数据时读多少数据
	网络开发中的粘包处理
	方式1：
		5个字节：数据长度
		size + content // 先读取5个字节 => size 再读取一次
	方式2：
		每次数据都是以\n结尾
		带缓冲区IO
		发送数据主动添加\n
		读取数据读取到\n
3. 通话结束条件
	客户端发送内容为 bye 结束

// 聊天室
需要保存所有客户端连接
并发 -> 需要使用锁
```

### server

```go
package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"net"
	"os"
	"strconv"
	"strings"
)

const (
	sizeBufferLength = 5
	bye              = ""
)

func read(conn net.Conn) (string, error) {
	sizeBuffer := make([]byte, sizeBufferLength)
	n, err := conn.Read(sizeBuffer)
	if err != nil || n != sizeBufferLength {
		return "", fmt.Errorf("size error")
	}
	size, err := strconv.Atoi(string(sizeBuffer))
	if err != nil {
		return "", err
	}

	contextBuffer := make([]byte, size)
	n, err = conn.Read(contextBuffer)
	if err != nil && n != size {
		return "", fmt.Errorf("content length error")
	}

	return string(contextBuffer), nil
}

func write(conn net.Conn, txt string) error {
	// 先写长度
	size := len(txt)
	// 检查长度
	if size >= int(math.Pow10(sizeBufferLength)) {
		return fmt.Errorf("error write log size")
	}

	formatter := fmt.Sprintf("%%0%dd", sizeBufferLength)
	n, err := fmt.Fprintf(conn, formatter, size)
	if err != nil || n != sizeBufferLength {
		return fmt.Errorf("error write size")
	}

	// 再写内容
	n, err = fmt.Fprintf(conn, txt)
	if err != nil || n != size {
		return fmt.Errorf("error write content")
	}

	return nil
}

func input(prompt string) string {
	fmt.Print(prompt)
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	return strings.TrimSpace(scanner.Text())
}

func handle(conn net.Conn) {
	defer conn.Close()
	fmt.Println("客户端连接:", conn.RemoteAddr())
	for {
		txt, err := read(conn)
		if err != nil {
			fmt.Println("读取客户端数据错误:", err)
			break
		}
		fmt.Println("客户端说:", txt)
		if txt == bye {
			fmt.Println("客户端关闭连接")
			break
		}

		// 服务端回消息
		// 从控制台读取(1行)数据并回复
		txt = input("回复消息:")
		// 发送消息
		err = write(conn, txt)
		if err != nil {
			fmt.Println("发送给客户端数据错误:", err)
			break
		}
	}
}

func main() {
	addr := "127.0.0.1:8888"

	listener, err := net.Listen("tcp", addr)
	if err != nil {
		log.Fatal(err)
	}
	fmt.Println("Listen:", listener.Addr())
	defer listener.Close()

END:
	for {
		conn, err := listener.Accept()
		if err != nil {
			log.Printf("error access: %s", err)
			break END
		}
		go handle(conn)
	}
}
```

### client

```go
package main

import (
	"bufio"
	"fmt"
	"log"
	"math"
	"net"
	"os"
	"strconv"
	"strings"
)

const (
	sizeBufferLength = 5
	bye              = ""
)

func read(conn net.Conn) (string, error) {
	sizeBuffer := make([]byte, sizeBufferLength)
	n, err := conn.Read(sizeBuffer)
	if err != nil || n != sizeBufferLength {
		return "", fmt.Errorf("size error")
	}
	size, err := strconv.Atoi(string(sizeBuffer))
	if err != nil {
		return "", err
	}

	contextBuffer := make([]byte, size)
	n, err = conn.Read(contextBuffer)
	if err != nil && n != size {
		return "", fmt.Errorf("content length error")
	}

	return string(contextBuffer), nil
}

func write(conn net.Conn, txt string) error {
	// 先写长度
	size := len(txt)
	// 检查长度
	if size >= int(math.Pow10(sizeBufferLength)) {
		return fmt.Errorf("error write log size")
	}

	formatter := fmt.Sprintf("%%0%dd", sizeBufferLength)
	n, err := fmt.Fprintf(conn, formatter, size)
	if err != nil || n != sizeBufferLength {
		return fmt.Errorf("error write size")
	}

	// 再写内容
	n, err = fmt.Fprintf(conn, txt)
	if err != nil || n != size {
		return fmt.Errorf("error write content")
	}

	return nil
}

func input(prompt string) string {
	fmt.Print(prompt)
	scanner := bufio.NewScanner(os.Stdin)
	scanner.Scan()
	return strings.TrimSpace(scanner.Text())
}

func main() {
	addr := "127.0.0.1:8888"
	conn, err := net.Dial("tcp", addr)
	if err != nil {
		log.Fatal(err)
	}
	defer conn.Close() // 关闭连接

	for {
		txt := input("发送内容:")
		err := write(conn, txt)
		if err != nil {
			fmt.Println("发送消息到服务端失败", err)
			break
		}
		if txt == bye {
			break
		}
		txt, err = read(conn)
		if err != nil {
			fmt.Println("读取服务端消息失败", err)
			break
		}
		fmt.Println("服务端回复消息:", txt)
	}
}
```

```go
// sockst实现http服务器

/*
	Listen
	for {
		client Accept
		go handleClient(client)
	}

	handleClient(client):
		读取客户端数据 解析 => Request
		找URL和处理器的关系 => Request.URL => handler => 多路复用器 => 用于处理url和handler的关系
		给客户端响应 => w => Client
		关闭客户端连接
	
	多路复用器 =>
		注册url => handler
		程序执行过程中通过 url 查找 handler
	
	// 第二个参数就是多路复用器
	多路复用器： http.ListenAndServe(addr, nil)
	
	默认多路复用器：
		请求的url => 查找注册url => 找最长匹配的
		/static/ 1
		/static/www/ 2
		
		请求url /static/www/a.txt 匹配第二个
		请求url /static/www 匹配第一个 没有斜杠
		
	go其他框架 =>
		重新定义多路复用器
		提供一些封装函数
		
	gin => httprouter => 重新定义了多路复用器 => url handler查找关系 radixtree算法
		对json封装
*/
```

# web开发

```go
// 客户端 服务端
// HTTP协议
// 如何开发：服务端 客户端 net.http包

// 框架 beego/gin

// 图解TCP/IP 图解HTTP

C/S => Client + Server
B/S => Browser + Server

WEB API = 第三方使用者 使用目标不是浏览器 需要自己去调用
		  组装HTTP请求 发送给服务端 解析HTTP响应

客户端 <-HTTP-> 服务端
HTTP协议：超文本传输协议
	HTTP 1.1/1.0/2.0 => 3.0

请求和响应的文本格式
请求都是从客户端发起的(请求/应答)
HTTP Request
	\r\n分的多行文本数据
	1: 请求行 Method URL Protocol/Version
		Method: GET POST DELETE ...
		URL: 标识不同的服务
			 针对web开发 需要定义URL和URL处理逻辑
	2: 请求头 多行 Key: Value
		Host: 指定请求访问的主机名
		浏览器信息：UserAgent
		Referer: 表示发出请求的原始URL
		会话信息：Cookie
		Content-Type:请求编码方式
		...
	[空行]
	3. 请求体 可能没有 如果有内容 有一定的格式
		常用编码方式：
			application/x-www-from-urlencoded
				key=value&key=value
			multipart/form-data
				上传文件
			application/json
			application/xml

HTTP Response
	1. 响应行
		协议 响应状态码 响应状态码文本描述
	2. 响应头
		key: value
		Content-Type: 响应格式
		Set-Cookie: 设置会话
	[空行]
	3. 响应体
		text/html
		application/json

// 重点
url -> http.Handler 处理器
	ServerHTTP(http.ResponseWrite, *http.Request)
匹配URL -> 交给handler处理

// 客户端向服务器提交数据：
	url?key=value&key=value

	request body:
		application/x-www-from-urlencoded
		multipart/form-data
		application/json	

// http包提供了HTTP服务器和客户端的开发接口 内置web服务器
// 针对web服务端开发流程为：
	- 定义处理器/处理器函数
        - 接收用户数据
		- 返回信息
	- 启动web服务器
```

## 静态web服务器

```go
package main

import "net/http"

func main() {
	addr := ":8888"
	// 需要定义请求的URL URL映射的目录
	// http.Handle("/static/", http.FileServer(http.Dir("./www")))
	http.Handle("/static/", http.StripPrefix(
		"/static/",
		http.FileServer(http.Dir("./www")),
	)) // 不用再自己创建static目录
	http.ListenAndServe(addr, nil)

	// http://addr:port/static/+path
	// ./www/+static+path
}
```

## 显示time的页面

### 处理器

```go
URL: /time
功能：显示当前的时间

/time => handler(处理器) => 响应当前时间

实现Handler接口
type TimeHandler struct {}

func (t *TimeHandler) ServeHttp(http.ResponseWrite, *http.Request)

http.Handle("/time", &TimeHandler{})
```

### 处理器函数

```go
// 处理器函数
timeHandler = func(http.ResponseWriter, *http.Request)
http.HandleFunc("/time2", timeHandler)
```

```go
package main

import (
	"fmt"
	"net/http"
	"time"
)

type TimeHandler struct {
}

func (h *TimeHandler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
	fmt.Println("time Handler")
	// r => request => 对HTTP请求封装
	// w =>
	fmt.Fprint(w, time.Now().Format("2006-01-02 15:04:05"))
}

func timeHandler(w http.ResponseWriter, r *http.Request) {
	fmt.Fprintf(w, "t2: %s", time.Now().Format("2006-01-02 15:04:05"))
}

func main() {
	http.Handle("/time", &TimeHandler{})
	http.HandleFunc("/time2", timeHandler)
	http.ListenAndServe(":9999", nil)
}
```

## request解析

```go
package main

import (
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"os"
)

func main() {
	addr := ":9999"
	http.HandleFunc("/header/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Println("Method:", r.Method)
		fmt.Println("URL:", r.URL)
		fmt.Println("Proto:", r.Proto)
		fmt.Println("Host:", r.Host)
		// fmt.Println(r.Header) 请求头 key: value
		for k, v := range r.Header {
			fmt.Println(k, v)
		}
	})

	http.HandleFunc("/queryparams/", func(w http.ResponseWriter, r *http.Request) {
		// queryparams -> r.Form
		r.ParseForm() // 需要先解析提交数据
		fmt.Println(r.Form)
		fmt.Println(r.Form.Get("a"))
		fmt.Println(r.Form.Get("b"))
		fmt.Println(r.Form.Get("c"))
		fmt.Println(r.Form.Get("d") == "") // true
		fmt.Println(r.Form["a"])           // 多个重复key值 Form.Get只能获取第一个
		fmt.Println(r.Form["d"])           // nil切片
	})

	http.HandleFunc("/queryparams2/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Println(r.FormValue("a")) // 自动ParseForm 同样只获取第一个值
		fmt.Println(r.FormValue("b"))
		fmt.Println(r.FormValue("c"))
	})

	http.HandleFunc("/form/", func(w http.ResponseWriter, r *http.Request) {
		r.ParseForm()
		fmt.Println(r.PostForm)
		fmt.Println(r.Form) // Form会包含PostForm中的数据以及queryparams的数据
	})

	http.HandleFunc("/form2/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Println(r.PostFormValue("a"))
		fmt.Println(r.PostFormValue("b"))
		fmt.Println(r.PostFormValue("c"))
	})

	http.HandleFunc("/form-data/", func(w http.ResponseWriter, r *http.Request) {
		// 上传文件
		r.ParseMultipartForm(10 * 1024 * 1024) // 参数 MaxMemory
		fmt.Println(r.MultipartForm.File)
		fmt.Println(r.MultipartForm.Value)
		for k, v := range r.MultipartForm.File {
			fmt.Println("file ", k)
			for idx, file := range v {
				fmt.Println(idx, file.Filename, file.Filename, file.Size)
				if f, err := file.Open(); err == nil {
					defer f.Close()
					io.Copy(os.Stdout, f)
					fmt.Println()
				}
			}
		}

		// f, fh, err := FormFile("a")
		// fmt.Println(fh.Filename. fh.Header, fh.Size)
		// io.Copy(os.Stdout, f)
	})

	http.HandleFunc("/body/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Println(r.Header.Get("Content-Type"))
		// io.Copy(os.Stdout, r.Body)
		req := map[string]string{}
		decoder := json.NewDecoder(r.Body)
		err := decoder.Decode(&req)
		fmt.Println(err, req)
		fmt.Println()
	})

	http.ListenAndServe(addr, nil)
}
```

## response响应

```go
package main

import (
	"fmt"
	"net/http"
)

func main() {
	addr := ":9999"
	http.HandleFunc("/header/", func(w http.ResponseWriter, r *http.Request) {
		// 设置header
		var headers http.Header = w.Header()
		headers.Add("Server", "MihnoNginx")
		headers.Set("xxxx", "xxxx")

		// 设置状态码
		w.WriteHeader(http.StatusCreated)

		fmt.Fprintln(w, "headers")
	})

	http.HandleFunc("/redirect/", func(w http.ResponseWriter, r *http.Request) {
		// 跳转到 /home
		http.Redirect(w, r, "/home/", http.StatusFound)
		// 响应：302
		// -> Location: /home/ 你要跳转到哪儿 /home/
		// -> 重新发起(GET)请求 /home/
	})

	http.HandleFunc("/home/", func(w http.ResponseWriter, r *http.Request) {
		fmt.Fprintln(w, "Home Page")
	})

	http.ListenAndServe(addr, nil)
}
```

## cookie

```go
// Session Cookie
// 会话跟踪

// Http 无状态

// 用户第一次访问生成唯一标识(tid[session id => sid] => 服务端对应存储 => session)
// 告知浏览器你的标识 tid Set-Cookie
// 以后请求时携带tid Cookie tid => 找存储 => 增删改查

// cookie
// 浏览器端存储
// 服务器如何告知浏览器存储某些数据(响应)
// 响应体 Set-Cookie: k=v addr (域名 path 过期时间 httponly isSecure ...)

// 浏览器在请求中会将这些数据携带(请求)
// Cookie: k=v
```

# rpc开发

```go
// grpc
// 服务端 客户端

// rpc/http 区别
从功能上来说没有区别
实现上来说：tcp/udp => 数据(编码方法)
		  不同的编码方式 => 序列化/反序列化的效率 网络传输大小
内/外：
	对内：效率 => rpc/restapi
	对外：规范 => restapi
	
	将内部API => 发布到 => 外网(外网API)

	restapi =>
		功能：restapi/rpc
		权限限制

		网关(可能用的第三方/可能自主开发)
			外部restapi => 转换为内部的 rpc/restapi
				/url => /inner url => nginx location
				接收客户端http请求 => 转码 => 发送请求(http/rpc)到服务端
				接收服务端(http/rpc)详情 => 转码 => 给客户端(http)响应
			权限控制/频率限制/...
```

## server/tcp

```go
package main

import (
	"fmt"
	"log"
	"net"
	"net/rpc"
)

// 计算两个int类型数字的加减乘除

// 请求对象
type Request struct {
	Left  int
	Right int
}

// 响应对象
type Response struct {
	R1 int
	R2 int
	R3 int
	R4 int
}

// 计算对象
type Calc struct {
}

func (c *Calc) Calc(req Request, resp *Response) error {
	if req.Right == 0 {
		return fmt.Errorf("divide zero")
	}
	resp.R1 = req.Left + req.Right
	resp.R2 = req.Left - req.Right
	resp.R3 = req.Left * req.Right
	resp.R4 = req.Left / req.Right

	return nil
}

func main() {
	// tcp rpc
	rpc.Register(&Calc{})
    
    // rpc.HandleHttp() // 使用http协议

	listener, err := net.Listen("tcp", ":9999")
	if err != nil {
		log.Fatal(err)
	}
	defer listener.Close()
    rpc.Accept(listener) // http.Serve(lestener)
}
```

## client

```go
package main

import (
	"fmt"
	"log"
	"net/rpc"
)

// 请求对象
type Request struct {
	Left  int
	Right int
}

// 响应对象
type Response struct {
	R1 int
	R2 int
	R3 int
	R4 int
}

func main() {
    // rpc.DialHTTP("tcp", addr) // 连接http rpc
	client, err := rpc.Dial("tcp", "127.0.0.1:9999")
	if err != nil {
		log.Fatal(err)
	}
	defer client.Close()

	req := Request{10, 2}
	resp := Response{}
	err = client.Call("Calc.Calc", req, &resp)
	if err == nil {
		fmt.Println(resp)
	} else {
		fmt.Println(err)
	}
}
```

```go
// jsonrpc
	rpc.Register(&Calc{})

	listener, err := net.Listen("tcp", ":9999")
	if err != nil {
		log.Fatal(err)
	}
	defer listener.Close()
	for {
        conn, err := listener.Accept()
        if err != nil {
            break
        }
        go  jsonrpc.ServeConn(conn)
	}
}

// jsonrpc连接
client, err := jsonrpc.Dial("tcp", addr)
...
```

# 模板技术

```go
// 定义模板
// 由模板引擎 加载模板 通过指定数据 生成最终字符串

// 模板语法 + 使用引擎

// Go Pkg
	text/template
	html/template => 在web开发一定要用html => 字符转义(防止一些安全注入的问题)

package main

import (
	"fmt"
	"html/template"
	"log"
	"os"
)

func main() {
	// url => handler/handlerFunc => 先生成html再返回

	// 定义模板字符串
	// 语法
	// 显示数据 {{ . }} .传递的数据
	txt := `{{  . }}`
	// data := "Minho"
	// data := 1
	// data := true
	// data := []int{1, 2, 3}
	data := map[string]string{"kk": "111"}

	// 创建模板
	tpl := template.New("txtTemplate")

	// 解析模板字符串
	tpl, err := tpl.Parse(txt)
	if err != nil {
		log.Fatal(err)
	}

	// 执行 输出到控制台
	err = tpl.Execute(os.Stdout, data)
	if err != nil {
		fmt.Println(err)
	}
}

// 模板语法参考文档
```

## 综合应用

### 目录结构

```go
// 目录结构
--cmdb
│  go.mod
│  main.go
├─handlers // 处理器函数
│      auth.go
│      user.go
├─routers // 路由注册
│      routers.go
├─utils // 通用utils封装
│      template.go
└─views // html模板文件夹
    ├─auth
    │      login.html
    └─user
            users.html
```

### 文件内容

```go
// main.go
package main

import (
	_ "cmdb/routers"
	"net/http"
)

func main() {
	// 用户登录逻辑
	// url => handler/handlerFunc => 业务逻辑 => Response

	// 定义Handler/HandlerFunc
	// 绑定关系 url <=> handler (路由)

	// 启动服务
	addr := ":9999"
	http.ListenAndServe(addr, nil)
}
```

```go
// routers.go
package routers

import (
	"cmdb/handlers"
	"net/http"
)

func init() {
    // url与处理器函数的映射
	http.HandleFunc("/login/", handlers.LoginHandler)
	http.HandleFunc("/users/", handlers.UserHandlers)
}
```

```go
// handlers function
// auth.go
package handlers

import (
	"cmdb/utils"
	"net/http"
)

func LoginHandler(w http.ResponseWriter, r *http.Request) {
	if r.Method == http.MethodPost {
		// 登陆验证

		// 登陆成功后跳转到其他位置(redirect)
		http.Redirect(w, r, "/users/", http.StatusFound)
		return

	}
	// 打开登陆页面
	utils.ParseTemplate(w, r, []string{"views/auth/login.html"}, "login.html", nil)
}

// user.go
package handlers

import (
	"cmdb/utils"
	"net/http"
)

func UserHandlers(w http.ResponseWriter, r *http.Request) {
	utils.ParseTemplate(w, r, []string{"views/user/users.html"}, "users.html", nil)
}
```

```go
// utils
// template.go 封装通用函数
package utils

import (
	"html/template"
	"net/http"
)

func ParseTemplate(w http.ResponseWriter,
	r *http.Request,
	files []string,
	tplName string,
	data interface{}) {
	tpl, err := template.ParseFiles(files...)
	if err != nil {
		panic(err)
	}
	err = tpl.ExecuteTemplate(w, tplName, data)
	if err != nil {
		panic(err)
	}
}
```

# 爬虫

```go
// goquery库
https://pkg.go.dev/github.com/PuerkitoBio/goquery
```

# embed

```go
// 部署Go程序的时候 配合打包依赖的配置文件等
// 把文件编译到Go二进制程序中去

// 可以和模板文件html结合 把html文件打包到go二进制文件中
```

## 使用文件变量

```go
package main

import (
	_ "embed"
	"fmt"
)

//go:embed version
var version string

//go:embed version
var versionBytes []byte

// 找文件目录 => 当前.go文件同级目录下
// 找对应的embed文件 => 相对当前go文件所在目录 并且不能设置其父目录
func main() {
	fmt.Println("verion: ", version)
	fmt.Println("verion: ", versionBytes)
	fmt.Println("verion: ", string(versionBytes))
}
```

```go
// pkg io/fs 抽象的fs库
```

## 多个文件

```go
package main

import (
	"embed"
	"fmt"
	"io"
	"log"
	"os"
)

// 多个文件
//go:embed version
//go:embed name
//go:embed *.params
//go:embed params
var fs embed.FS

func PrintFile(name string) {
	file, err := fs.Open(name)
	defer file.Close()
	if err != nil {
		log.Fatal(err)
	}
	io.Copy(os.Stdout, file)
	fmt.Println()
}

func main() {
	PrintFile("version")
	PrintFile("name")
	PrintFile("a.params")
	PrintFile("b.params")
	PrintFile("params/a")
	PrintFile("params/b")
}
```

# Go操作数据库

```go
// https://golang.google.cn/pkg/database/sql/

1. 找一个驱动 SQL接口规范 => 驱动实现
	https://pkg.go.dev/github.com/go-sql-driver/mysql

2. 初始化驱动 下划线导入
	github.com/go-sql-driver/mysql

3. 导入database/sql
	对数据库操作 连接池 => 对象池 sync.Pool

4. 连接数据库 Open
	host:port user:password dbName charset=utf8mb4 parseTime=true

5. 测试 Ping

6. 操作(常用)：
	DML Exec
		INSERT/DELETE/UPDATE -> 最后插入ID/受影响行数
	SQL Query
		SELECT -> 查询的结果
```

## 示例

```go
package main

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

func ddl(db *sql.DB) error {
	// 执行
	rawSql := `
	create table if not exists alarm(
		id bigint primary key auto_increment,
		alarm_time datetime not null,
		content text
	) engine=innodb default charset utf8mb4;
	`
	_, err := db.Exec(rawSql)
	return err
}

func dmlInsert(db *sql.DB) error {
	// dml
	r, err := db.Exec("insert into alarm(alarm_time, content) values('2021-09-03 11:38:10', 'CPU告警')")
	if err != nil {
		return err
	}
	fmt.Println(r.LastInsertId())
	fmt.Println(r.RowsAffected())

	// 拼接SQL 可能会导致SQL注入
	// Go有限制 但是可以绕过
	alartTime, alartContent := time.Now().Format("2006-01-02 15:04:05"), "内存告警"
	sql := "insert into alarm(alarm_time, content) values('" + alartTime + "', '" + alartContent + "');"
	r, err = db.Exec(sql)
	if err != nil {
		return err
	}
	fmt.Println(r.LastInsertId())
	fmt.Println(r.RowsAffected())

	// 预处理方式 (提交参数)
	sql = "insert into alarm(alarm_time, content) values(?, ?)"
	alartContent = "',');delete from user;#"
	r, err = db.Exec(sql, alartTime, alartContent)
	if err != nil {
		log.Fatal(err)
		return err
	}
	fmt.Println(r.LastInsertId())
	fmt.Println(r.RowsAffected())

	return nil
}

func dqlRows(db *sql.DB) error {
	sql := "select id, content from alarm"
	rows, err := db.Query(sql)
	// db.QueryRow() // 查询一行
	if err != nil {
		log.Fatal(err)
	}

	// 关闭rows 告知将连接放入连接池
	defer rows.Close()
	for rows.Next() {
		// ** 扫描查询数据到变量中 变量数量及类型需要与扫描结果中顺序和类型保持一致 => 谨慎使用select *
		var id int64
		var content string
		if err := rows.Scan(&id, &content); err != nil {
			log.Fatal(err)
		} else {
			fmt.Println(id, content)
		}
	}
	return nil
}

func dqlRow(db *sql.DB) error {
	sql := "select id, content, alarm_time from alarm where id = ?"

	var (
		i         int64
		content   string
		alarmTime time.Time
	)
	if err := db.QueryRow(sql, 22).Scan(&i, &content, &alarmTime); err != nil {
		log.Fatal(err)
		return err
	}
	fmt.Println("QueryRow: ", i, content, alarmTime)
	return nil
}

func main() {
	// 打开数据库连接池
	// dsn := "user:password@tcp(host:port)/dbName?charset=utf8mb4&parseTime=true"
	dsn := "root:123123@tcp(127.0.0.1:3306)/chaos?charset=utf8mb4&parseTime=true"
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		log.Fatal(err)
	}

	// 只有在程序退出时关闭
	defer db.Close()

	// 测试数据库连接
	if err := db.Ping(); err != nil {
		log.Fatal(err)
	}

	// fmt.Println("ok")
	// fmt.Println("ddl", ddl(db))
	// dmlInsert(db)

	// 查询
	dqlRows(db)
	dqlRow(db)
}
```

## 事务

```go
// 多个操作要同时成功/同时失败 => 多个操作放在一个事务中
package main

import (
	"database/sql"
	"fmt"
	"log"
	"time"

	_ "github.com/go-sql-driver/mysql"
)

func main() {
	// 打开数据库连接池
	// dsn := "user:password@tcp(host:port)/dbName?charset=utf8mb4&parseTime=true"
	dsn := "root:123123@tcp(127.0.0.1:3306)/chaos?charset=utf8mb4&parseTime=true"
	db, err := sql.Open("mysql", dsn)
	if err != nil {
		log.Fatal(err)
	}

	// 只有在程序退出时关闭
	defer db.Close()
	// 测试数据库连接
	if err := db.Ping(); err != nil {
		log.Fatal(err)
	}

	db.Exec("truncate table alarm;")
	tx, err := db.Begin()
	if err != nil {
		log.Fatal(err)
	}

	sql := "insert into alarm(id, content, alarm_time) values(?, ?, ?)"
	_, err = tx.Exec(sql, 1, "第一条告警", time.Now())
	fmt.Println(err)
	if err == nil {
		_, err = tx.Exec(sql, 2, "第一条告警", time.Now())
		fmt.Println(err)
	}
	if err == nil {
		// 都成功 提交
		tx.Commit()
	} else {
		// 有一个失败 回滚
		tx.Rollback()
	}
}
```

## 获取结构

```go
func main() {
	sql := "select * from user limit 0"
	rows, err := db.Query(sql)
	...
	defer rows.Close()
	columnTypes, _ := rows.ColumnTypes()
	columns, _ := rows.Columns() 
    for i, typ := range columnTypes {
        fmt.Println(i, columns[i], "=====")
        fmt.Println(typ.DatabaseTypeName())
        fmt.Println(typ.Length())
        fmt.Println(typ.Nullable)
        fmt.Println(typ.ScanType())
        fmt.Println(typ.DecimalSize())
    }
}

// 根据获取的结构 可以根据表结构生成对应的结构体
```

## 密码校验

```go
// pkg: crypto/bcrypt
```

