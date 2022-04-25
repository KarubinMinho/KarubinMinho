```go
// 函数 => 函数也是对象 / 闭包
getUsers(string) []User

// 需求：不修改getUsers函数的前提下 给getUser扩展功能
	缓存功能：
		1. 在执行之前检查缓存(内存)
		2. 在执行之后放入缓存
	计算函数执行时间(执行之后时间-执行之前时间)
		1. 执行之前记录时间
		2. 执行之后记录时间 时间相减

// 新定义函数 包装getUsers函数
getUserWrapper(q string) []User {
    // 记录开始时间
    // 检查cache
    // 有 返回
    // 没有 getUsers() => 放入缓存
    // 返回 当前时间 - 开始时间
}

// 如果有一类函数都有类似的需求 怎么优化？
// 如果这些函数签名一致 动态创建包装函数 将函数作为参数传递
// 类似Python装饰器
func wrapper(callback func) {
    return func() {
        // 函数调用前增强功能
        callback() // 闭包
        // 函数调用之后增强功能
    }
}

func wrapper(callback func(string) []User) {
    return func(q string) []User {
        stratTime := timeNow()
        var users []User
        var ok boollean
        // 检查缓存
        ok, users = cached[q]
        if !ok {
            users = callback(q)
            // 没有缓存 增加缓存
            cached[q] = users
        }
        diff := time.Now().Sub(startTime)
        log.Printf("diff: %d", diff.Unix())
        return users
    }
}

getUsersWrapper := wrapper(getUsers)
```

[Beego源码](https://github.com/beego/beego)

[Beego中文文档](https://beego.me/)

# 主要功能/思想

```go
MVC：分层模型
	C: Controller 控制器 连接
	M: Model 模型 数据库操作
	V: View	视图 模板/页面	
```

# 目录结构

```go
// 可以使用bee工具自动生成(有限制) 也可以自己创建
quickstart
|-- conf
|   `-- app.conf  // 配置文件
|-- controllers  // 控制器
|   `-- default.go
|-- main.go  // 程序启动入口
|-- models  // 模型
|-- routers  // 路由配置 url => controller
|   `-- router.go
|-- static  // 静态资源文件
|   |-- css
|   |-- img
|   `-- js
|-- tests
|   `-- default_test.go
`-- views  // 视图
    `-- index.tpl`

services  // 服务
froms  // request提交数据验证 可以自定义验证方法
```

# 启动服务

```go
// 可以使用bee工具启动
package main

import (
	"github.com/beego/beego/v2/server/web"
)

// 定义控制器 http.Handler
type IndexController struct {
	web.Controller
}

func (c *IndexController) Get() { // ServeHTTP
	// 处理Get请求
	// c.Ctx.WriteString("Hello, Golang") // fmt.Fprint(w, "Hello, Golang")
	// c.Controller.Ctx.WriteString("hellohello")
	c.Data["user"] = map[string]string{"id": "1", "name": "Minho"} // 给模板传递数据
	c.TplName = "index.html"                                       // 显示index.html页面
}

func main() {
	web.Router("/", &IndexController{}) // http.Handle
	web.Run()                           // http.ListenAndServe()
}

>>> go run main.go
```

# 配置

[config模块](https://beego.me/docs/module/config.md)

[参数配置](https://beego.me/docs/mvc/controller/config.md)

# 控制器

[Controller详解](https://beego.me/docs/mvc/controller/controller.md)

## 控制器函数

```go
package main

import (
	"github.com/beego/beego/v2/server/web/context"

	"github.com/beego/beego/v2/server/web"
)

func main() {
	// url -> handler/handlerFunc
    
	// 定义路由函数

	// 指定处理器函数(控制器函数)
	// web.Get/Post/Put/Delete/Head/Options/Patch/Any
	// web.Get()
	web.Get("/", func(ctx *context.Context) {
		ctx.WriteString("get")
	})
	// web.Post()
	web.Post("/", func(ctx *context.Context) {
		ctx.WriteString("post")
	})
	// web.Delete()
	web.Delete("/", func(ctx *context.Context) {
		ctx.WriteString("delete")
	})
	// web.Head()
	web.Head("/", func(ctx *context.Context) {
		ctx.WriteString("Head")
	})

	// 一个path指定多个处理方式
	web.Any("/any/", func(ctx *context.Context) {
		ctx.WriteString("any:" + ctx.Request.Method)
	})

	// 正则路由
	// /regex/1/
	// /regex/2/
	// /regex/3/
	// /regex/ 如何匹配不包含数字 加? 表示这个参数可以没有
	web.Get("/regex/?:id([0-9]+)/", func(ctx *context.Context) {
		ctx.WriteString(ctx.Input.Param(":id"))
	})

	web.Get("/regexint/?:id:int/", func(ctx *context.Context) {
		ctx.WriteString(ctx.Input.Param(":id"))
	})

	web.Get("/regexpath/*", func(ctx *context.Context) {
		// 获取url后面的路径
		ctx.WriteString(ctx.Input.Param(":splat"))
	})

	web.Get("/regexext/*.*", func(ctx *context.Context) {
		// 获取url后面的路径
		// path不会带url前缀
		ctx.WriteString(ctx.Input.Param(":path") + ":" + ctx.Input.Param(":ext"))
	})

	web.Run()
}
```

## 控制器结构体

```go
package main

import (
	"github.com/beego/beego/v2/server/web/context"

	"github.com/beego/beego/v2/server/web"
)

type RestfulController struct {
	web.Controller
}

func (c *RestfulController) Get() {
	c.Ctx.WriteString("get:" + c.Ctx.Input.Param(":id"))
}

type CustomController struct {
	web.Controller
}

func (c *CustomController) Open() {
	c.Ctx.WriteString("open:" + c.Ctx.Request.Method)
}

func (c *CustomController) Update() {
	c.Ctx.WriteString("update:" + c.Ctx.Request.Method)
}

func (c *CustomController) Close() {
	c.Ctx.WriteString("Close:" + c.Ctx.Request.Method)
}

func main() {
	// url -> Controller/ControllerFunc

	// 指定处理器(控制器)
	// /restful/id/
	web.Router("/restful/?:id:int/", &RestfulController{})

	// get -> Get post -> POST 请求方法到controller方法的映射
	// 自定义：get -> Open post,delete -> update 其他请求方式到Close 如何实现？
	// 第三个参数：requestmethod:funcmethod;...
	web.Router("/custom/", &CustomController{}, "get:Open;post,delete:Update;*:Close")

	web.Run()
}
```

## 自动路由

```go
package main

import (
	"github.com/beego/beego/v2/server/web/context"

	"github.com/beego/beego/v2/server/web"
)

type AuthController struct {
	web.Controller
}

// /auth/login/
func (c *AuthController) Login() {
	c.Ctx.WriteString("login")
}

// /auth/logout
func (c *AuthController) Logout() {
	c.Ctx.WriteString("logout")
}

func main() {
	// url -> Controller/ControllerFunc

	// 自动路由
    // 通过反射设置 AuthController -> Login/Logout方法
    // /auth/login => Login
    // /auth/logout => Logout
	// url => controllerName:methodName
	web.AutoRouter(new(AuthController)) // 常用

	// 注解路由
	// 不要用 => 只能在开发模式使用 => 生成go文件

	web.Run()
}
```

## 请求数据解析/处理

```go
package main

import (
	"fmt"

	"github.com/beego/beego/v2/server/web"
)

type RequestController struct {
	web.Controller
}

func (c *RequestController) Index() {
	// c.Ctx.Request => http.Request
	// c.Ctx.Input => Query/Bind header
	// C.Ctx => Cookie
	// Controller => GetXXX Input ParseForm SaveToFile
	// 从上到下 为封装层次
	// 优先使用 封装层次最多的(封装层次越多 提供的特性越多 越简单)

	// 登陆 username password
	fmt.Println("username:", c.GetString("username"))
	fmt.Println("password:", c.GetString("password"))
	c.Ctx.WriteString("index")
}

type LoginForm struct {
	Username string `form:"username"`
	Password string `form:"password"`
}

// 提交数据 解析到对象 类似数据库行记录对应到model对象
func (c *RequestController) Parse() {
	var form LoginForm
	err := c.ParseForm(&form)
	fmt.Printf("%v, %#v\n", err, form)

	c.Ctx.WriteString("parse")
}

func (c *RequestController) Bind() {
	// Scan
	var name string
	var password string
	c.Ctx.Input.Bind(&name, "username")
	c.Ctx.Input.Bind(&password, "password")
	fmt.Println(name, ":", password)
	c.Ctx.WriteString("bind")
}

func (c *RequestController) Json() {
	// 解析json

	// 手动调用CopyBody
	// 自动配置 app.conf //copyrequestbody = true
	body := c.Ctx.Input.CopyBody(1024 * 1024)
	fmt.Println(string(body))
	fmt.Println(string(c.Ctx.Input.RequestBody))
	c.Ctx.WriteString("json")
}

func main() {
	web.AutoRouter(&RequestController{})
	web.Run()
}
```

## 响应数据解析/处理

```go
package main

import "github.com/beego/beego/v2/server/web"

type ResponseController struct {
	web.Controller
}

func (c *ResponseController) Index() {
	// Response ResponseWriter
	// Output => Body Download
	// Ctx => WriteString Redirect
	// controller => TplName + Data
	// controller => Data + ServeJSON/ServeXML
	c.Ctx.Output.Body([]byte("index"))
}

func (c *ResponseController) Download() {
	// 文件下载
	c.Ctx.Output.Download("./go.mod")
}

func (c *ResponseController) Json() {
	// 响应json
	c.Data["json"] = map[string]string{"name": "minho", "addr": "Chengdu"}
	c.ServeJSON()
}

func main() {
	web.AutoRouter(&ResponseController{})
	web.Run()
}
```

# Session

```go
// session
存：登陆成功后存储用户标识
取：访问需要登陆后才能访问的处理逻辑之前 取用户进行验证
销毁：退出登陆的时候

controller:
	SetSession(key, value)
	GetSession(key)
	DelSession(key)
	DestroySession()
	SessionRegernateId()  // 重新生成sessionID

Context.Input.CurSession
GlobalSessions.SessionDestory()
```

# URL构建

```go
// url => Controller
// URL构建 省略代码和模板中的URL

=> 在页面上直接指定Controller.Method
=> 自动推导(查询)
=> URL Controller
=> Redirect

页面： beego urlfor
Go代码中：web.URLFor()

// HTML模板
<form action="{{ urlfor `AuthController.Login` }}" method="POST">

// Go代码
c.Redirect(web.URLFor("HomeController.Index"), http.StatusFound)

```

# Flash消息传递

```go
// 不用

// 通过cookie传递消息
/user/delete => setCookie
flash := web.NewFlush()
	flash.Error("xxx") // k-v对
	flash.Warning("xxx")
	flash.Notice("xxx")
	
	flash.Store(&c.Controller)

/cser/query => getCookie deleteCookie
	flash := web.ReadFromRequest(&c.Controller)
controller.Data["flash"] => 写在Data 可以在模板上获取(.flash)
```

# 模板

# BeegoORM

```go
// ORM: 对象关系映射 Object Relation Mapping
	 关系数据库 <=> 面向对象类
	 表(定义) <=> 结构体(类)
	 名字 <=> 结构体名(类名)
	 列 <=> 属性
	 	列名 <=> 属性名
	 	列类型 <=> 属性类型
// 实例：
	Go对象 <=> 反射 => create table
	表结构  => 结构体

// 数据：
	每行数据 <=> 实例化/类对象
// 数据操作：
	增删改查 <=> 方法(自动转换为SQL 调用数据库执行SQL语句)

// ORM思想 => 实现 beego orm, gorm, ...(工具)
orm => 针对不同数据库实现
优势：
	1. 如果在使用过程中未使用某个数据库特性的SQL 可以实现数据库之间的切换
	2. 可以在不了解SQL的情况下 实现对数据库操作
缺点：
	1. 性能
	2. 只能使用ORM框架提供的基本功能  针对数据库提供的特性功能 ORM未实现的功能 只能使用原生SQL

// 使用
使用包：
	数据库驱动 github.com/go-sql-driver/mysql
	orm库： github.com/beego/beego/v2/client/orm // 使用database/sql并提供orm的增强功能

定义结构：
	表结构 = sql
	可以不定义表结构 => 可以通过orm同步
		创建表				=> 同步
		删除表				=> 不同步
		对于表列修改
			添加列			=> 同步
			修改列			=> 同步
				修改列名	=> 可同步 新增
			    列的属性	=> 可同步(beego不同步)
			删除列			=> 同步

// 需要定义结构体(类)
type User struct {
    Id int64
    Name string
}
需要定义结构体和表的关系
	表关系
		表名 <=> 默认 结构体驼峰式 -> 全小写下划线式
				除首字母外 碰到大写字母加下划线转小写
				User <=> user
				UserDB <=> user_d_b 可能不适合 需要：user_db 需要可定义与表的关系 => 方法
		修饰
			索引 => 方法

	列的关系
		列名 <=> 默认 结构体属性名驼峰式 -> 全小写下划线式
				自定义：通过属性标签修改
		修饰 <=> 属性标签
		标签名：orm

告知ORM管理的结构体(注册)
	orm.RegisterModel

表结构：同步
表数据：增删改查

beego orm模块可以单独使用 或与其他第三方模块结合使用
	单独使用orm对数据库增删改查
	和http/gin包结合对数据库操作
```

## 表结构/属性

```go
// 模型定义
表
	表名
	索引
属性
	属性名
	属性修饰

	标签：
		pk auto column  index/unique
		type
			int	int
			int64	bigint
			string	varchar(255)
					size()
					type() text(longtext)/char
			time.Time *time.Time datetime
		null default description

		针对时间：*time.Time // 使用指针 指针可以为nil
			auto_now
			auto_now_add

		针对小数类型
			digits
			decimals
```

```go
package main

import (
	"log"
	"time"

	"github.com/beego/beego/v2/client/orm"
	_ "github.com/go-sql-driver/mysql"
)

// 用beego orm 要显式设置主键：pk
// id属性需要设置int64 或显示指定pk标签 `orm:"pk"`

/*
标签名：orm 标签值用;分隔
指定主键：pk
自动增长：auto
列名：column(name)
字符串类型：默认varchar(255)
          长度修改 size(length)
		  指定其他类型：type(text)
是否允许为null: 默认不允许 标签：null
默认值：default(value)
注释：description(desc)
唯一键：unique
设置索引：index
浮点数小数位数：digits(10);decimals(2)

// 时间
// 下面两个有关时间的属性 不体现在SQL中 是在ORM执行过程中应用
auto_now // 每次更新的时候 自动设置属性为当前时间
auto_now_add // 当数据创建时 设置为当前时间

type(date) // 修改时间格式
*/
type Account struct {
	// ID 		 string `orm:"pk"`
	ID           int64      `orm:"pk;auto;column(id)"`
	Name         string     `orm:"size(64);unique"`
	Password     string     `orm:"size(1024)"`
	Birthday     *time.Time `orm:"type(date)"`
	Telphone     string
	Email        string
	Addr         string `orm:"index;size(64);default(中国)"` // size太长无法创建索引 或者只能为一部分长度创建索引
	Status       int8   `orm:"default(1);description(状态)"`
	RoleId       int64
	DepartmentId int64
	CreatedAt    *time.Time `orm:"auto_now_add"`
	UpdatedAt    *time.Time `orm:"auto_now"`
	DeletedAt    *time.Time `orm:"null"`
	Description  string     `orm:"type(text)"`
	Sex          bool
	Height       float32 `orm:"digits(10);decimals(2)"`
	Weight       float64
	// A string // 列不存在 添加；存在不会删除
	// B string // 修改A名称 -> B ORM感知不到 会新增字段
	// 修改字段类型 ORM也并不会修改

	// ORM只会改动增加的列 不会去删除也不会去修改
}

// Account 自动映射表名为：account
// 如何自定义表名？设置方法
func (account *Account) TableName() string {
	return "act"
}

// 索引方法
func (account *Account) TableIndex() [][]string {
	return [][]string{
		{"name", "password"},
		{"password", "email"},
	}
}

func main() {
	databaseName := "default"
	driverName := "mysql"
	dsn := "root:123123@tcp(127.0.0.1:3306)/beego_test?charset=utf8mb4&parseTime=true"

	// 注册驱动到orm
	orm.RegisterDriver(driverName, orm.DRMySQL) // 类型名(自定义) 类型(由orm指定 看orm支持哪些)

	// 数据库(连接池) 连接(池)名称 使用的驱动名称(orm驱动类型) 数据库配置信息
	// default 连接池名字 beego会指定多个数据库连接 需要指定一个
	err := orm.RegisterDataBase(databaseName, driverName, dsn)
	if err != nil {
		log.Fatal(err)
	}

	// 定义结构
	// 注册模型
	orm.RegisterModel(&Account{})

	// 使用
	// 表结构同步(库需要提前创建)
	// databaseName 同步数据库
	// force: 如果表存在 则删除
	// verbose： 打印出执行的sql语句
	orm.RunSyncdb(databaseName, true, true)
}
```

## 数据操作

```go
// 基本的增删改查
package main

import (
	"fmt"
	"log"
	"time"

	"github.com/beego/beego/v2/client/orm"
	_ "github.com/go-sql-driver/mysql"
)

type Account struct {
    Id           int64 `orm:"column(i_d)"`
	Name         string
	Password     string
	Birthday     *time.Time
	Telphone     string
	Email        string
	Addr         string
	Status       int8
	DepartmentId int64
	CreatedAt    *time.Time `orm:"auto_now_add"`
	UpdatedAt    *time.Time `orm:"auto_now"`
	DeletedAt    *time.Time `orm:"null"`
	Description  string
	Sex          bool
}

func (account *Account) TableName() string {
	return "act" // 查询也可以映射到其他表
}

func main() {
	// orm.Debug = true // 可以打印orm执行的SQL语句

	databaseName := "default"
	driverName := "mysql"
	dsn := "root:123123@tcp(127.0.0.1:3306)/beego_test?charset=utf8mb4&parseTime=true"

	// 注册驱动到orm
	orm.RegisterDriver(driverName, orm.DRMySQL)
	err := orm.RegisterDataBase(databaseName, driverName, dsn)
	if err != nil {
		log.Fatal(err)
	}

	// 注册模型
	orm.RegisterModel(&Account{})
	// orm.RunSyncdb(databaseName, true, true)

	// 增
	now := time.Now()
	account := Account{
		Name:     "minho",
		Password: "123123",
		Birthday: &now,
		Telphone: "123",
		Email:    "456@qq.com",
	}
	ormer := orm.NewOrm()
	// 插入数据并将数据库自动生成的值回填
	id, err := ormer.Insert(&account) // sql执行完 会把account信息回填 此时包括未显式指定的主键ID
	fmt.Println(id, err, account)

	// id, err = ormer.Insert(&account) // 报错 主键冲突
	// fmt.Println(id, err, account)

	// 删
	// 只会按照主键删除 按其他字段 需要指定第二个属性...
	// num, err := ormer.Delete(&Account{Name: "minho", Email: ""}, "Name", "Email")
	// fmt.Println(num, err)

	// 查
	// 查一个结果
	// 需要按照其他属性查 和删除一样 指定第二 第三个属性
	// 数据库多个值相同 返回第一个值
	accountDetail := &Account{Id: 7}
	err = ormer.Read(accountDetail)
	fmt.Println(err, accountDetail)

	// 改
	accountDetail.Addr = "北京"
	num, err := ormer.Update(accountDetail)
	fmt.Println(num, err)

	// 查询列表
	// QueryTable
	fmt.Println("===============")
	queryset := ormer.QueryTable(new(Account))
	fmt.Println(queryset.Count())

	accounts := make([]Account, 0)
	queryset.All(&accounts)
	fmt.Println(accounts)
}
```

