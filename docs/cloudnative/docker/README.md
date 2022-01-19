# 🐳 Docker

[![docker readme](https://img.shields.io/badge/Docker-README-00A6ED)](https://docs.docker.com/)

[![docker](./icons/docker-icon.svg)](https://www.docker.com/)

## 主机级虚拟化

[Type1和Type2虚拟机管理程序区别](https://virtual.51cto.com/art/201904/594481.htm)

### Type1

```bash
Type1虚拟机管理程序直接在主机的物理硬件上运行 它被称为裸机虚拟机管理程序
它不必预先加载底层操作系统 通过直接访问底层硬件而无需其他软件(例如操作系统和设备驱动程序)
```

- VMware ESXi
- Microsoft Hyper-V服务器
- 开源KVM
- ...

### Type2

```bash
Type2虚拟机管理程序通常安装在现有操作系统之上 它称为托管虚拟机管理程序
因为它依赖于主机预先安装的操作系统来管理对CPU/内存/存储和网络资源的调用
```

- VMware Fusion
- Oracle VM VirtualBox
- 用于x86的Oracle VM Server
- Oracle Solaris Zones
- Parallels
- VMware Workstation
- ...

## 容器级虚拟化

### Namespace

[man-namespaces](https://man7.org/linux/man-pages/man7/namespaces.7.html)
[namespaces API](https://lwn.net/Articles/531381/)

```bash
clone()   # Creating a child in a new namespace

setns()   # Joining an existing namespace

unshare() # Leaving a namespace
```

Linux Namespaces
| namespace | 系统调用参数 | 隔离内容 | 内核版本 |
| -----| ---- | ---- | ---- |
| UTS | CLONE_NEWUTS | 主机名和域名 | 2.6.19 |
| IPC | CLONE_NEWIPC | 信号量/消息队列/共享内存 | 2.6.19 |
| PID | CLONE_NEWPID | 进程编号 | 2.6.24 |
| Network | CLONE_NEWNET | 网络设备/网络栈/端口等 | 2.6.29 |
| Mount | CLONE_NEWNS | 挂载点(文件系统) | 2.4.19 |
| User | CLONE_NEWUSER | 用户和用户组 | 3.8 |

### Control Groups

[man-cgroups](https://man7.org/linux/man-pages/man7/cgroups.7.html)
[linux资源管理之cgroups简介](https://tech.meituan.com/2015/03/31/cgroups.html)

```bash
cgroups是Linux内核提供的一种可以限制单个进程或者多个进程所使用资源的机制 可以对cpu/内存等资源实现精细化的控制

cgroups 的全称是control groups 
cgroups为每种可以控制的资源定义了一个子系统 典型的子系统介绍如下
```

- blkio 块设备IO
- cpu CPU
- cpuacct CPU资源使用报告
- cpuset 多处理器平台上的CPU集合(按核/按比例)
- devices 设备访问
- freezer 挂起或恢复任务
- memory 内存用量及报告
- perf_event 对cgroup中的任务进行统一性能测试
- net_cls cgroup中的任务创建的数据报文的类别标识符

### LXC

[whats-a-linux-container](https://www.redhat.com/zh/topics/containers/whats-a-linux-container)

- LinuX Container
  - lxc-create(创建namespace)
  - template(拉取所需发行版的仓库相关包进行安装)

### 容器编排

- machine + swarm + docker compose(单机编排)
- mesos + marathon
- kubernetes(k8s)

## Docker

```bash
# docker 容器引擎的发展
# LXC -> libcontainer -> runC
-> libcontainer(docker研发的容器引擎 替换LXC) 
-> runC(容器运行时环境标准 Docker将RunC捐赠给OCI作为OCI容器运行时标准的参考实现)
```

[docker/containerd/runC分别是什么](https://os.51cto.com/art/202110/687502.htm)

### OCI

[![Open Container Initiative](./icons/opencontainers-icon.svg)](https://opencontainers.org/)

Open Container Initiative

- 由Linux基金会主导于2015年6月创立
- 旨在围绕容器格式和运行时制定一个开放的工业化标准
- contains two specifications
  - the Runtime Specification (runtime-spec) 运行时标准(规范)
  - the Image Specification (image-spec) 镜像格式标准(规范)
- The Runtime Specification outlines how to run a "filesystem bundle" that is unpacked on disk
- At a high-level an OCI implementation would download an OCI Image then unpack that image into an OCI Runtime filesystem bundle

### runC

[runC](https://github.com/opencontainers/runc)

- OCF: Open Container Format
- runC: runc is a CLI tool for spawning and running containers on Linux according to the OCI specification

### docker architecture

[![docker architecture](./icons/architecture.svg)](https://docs.docker.com/get-started/overview/#docker-architecture)

```bash
Client -> Daemon(REST API, over UNIX sockets or a network interface)
Registry -> Host(https/http)

Registry: 仓库名(repo name) + 标签(tag) 唯一标识一个镜像
-> nginx:1.14.0
-> nginx:latest(default 最新版)

Images: An image is a read-only template with instructions for creating a Docker container
Images：静态的 不会运行
Containers：动态 有生命周期 类似命令
  /bin/ls
    - ls /etc
    - ls /var

Moby
docker-ee # 企业版
docker-ce # 社区版
```

### docker objects

[docker objects](https://docs.docker.com/get-started/overview/#docker-objects)

- images
- containers
- networks
- volumes
- plugins
- other objects

#### Images

- An image is a read-only template with instructions for creating a Docker container
- Often, an image is based on another image, with some additional customization
- You might create your own images or you might only use those created by others and published in a registry

#### Containers

- A container is a runnable instance of an image
- You can create/start/stop/move or delete a container using the Docker API or CLI
- You can connect a container to one or more networks, attach storage to it, or even create a new image based on its current state

### docker install

[Install Docker Engine](https://docs.docker.com/engine/install/)
[阿里云Mirrors docker-ce](https://mirrors.aliyun.com/docker-ce/)

#### docker-ce.repo

```bash
[docker-ce-stable]
name=Docker CE Stable - $basearch
baseurl=https://download.docker.com/linux/centos/$releasever/$basearch/stable
# baseurl=https://mirrors.aliyun.com/docker-ce/linux/centos/$releasever/$basearch/stable
enabled=1
gpgcheck=1
gpgkey=https://download.docker.com/linux/centos/gpg
```

#### 镜像加速

- docker cn
- [阿里云官方镜像加速](https://help.aliyun.com/document_detail/60750.html)
- 中国科技大学

```json
# 配置文件
/etc/docker/daemon.json

# 更换镜像下载仓库链接
{
    "registry-mirrors": ["系统分配前缀.mirror.aliyuncs.com "]
}
```

### docker cli

[docekr-reference](https://docs.docker.com/reference/)

```bash
docker --help

# docker event state 涉及部分常用命令
```

### docker event state

[![docker event state](./icons/docker-event-state.jpg)](https://docs.docker.com/engine/reference/commandline/events/)

### docker image

```bash
Docker镜像含有启动容器所需的文件系统及其内容 因此 其用于创建并启动docker容器
```

#### docker image layer

![分层构建](./icons/docker-base-image.png)

- 采用分层构建机制 最底层为bootfs 其它为rootfs
  - bootfs: 用于`系统引导`的文件系统 包括`bootloader`和`kernel` 容器启动完成后会被卸载以节约内存资源
  - rootfs: 位于bootfs之上 表现为docker容器的根文件系统
    - 传统模式中 系统启动时 内核挂载rootfs时会首先将其挂载为`只读`模式(自检) 完整性自检完成后将其重新挂载为读写模式
    - docker中 rootfs由内核挂载为`只读`模式 而后通过`联合挂载`技术额外挂载一个`可写`层
- docker image layer
  - 位与下层的镜像成为父镜像(parent image) 最底层的称为基础镜像(base image)
  - 最上层的为`可读写`层 其下的均为`只读`层

![docker image layer](./icons/docker-image-layer.png)

#### aufs

- Advanced Mult-Layered Unification Filesystem 高级多层统一文件系统
- 用于为Linux文件系统实现`联合挂载`
- aufs是之前UnionFS的重新实现 2006年由Junjiro Okajima开发
- Docekr最初使用aufs作为容器文件系统层 它目前仍作为存储后端之一来支持
- aufs的竞争产品是overlayfs 后者自从3.18版本开始被合并到Linux内核
- docker的分层镜像 除aufs之外 docker还支持btrfs/devicemapper/vfs等
  - Ubuntu系统下 docekr默认Ubuntu的aufs 而在CentOS7上 用的是devicemapper(新版默认使用overlay2)

#### docekr registry

```bash
启动容器时 docker daemon 会试图从本地获取相关的镜像 本地镜像不存在时 其将从Registry中下载该镜像并保存到本地
```

- Registry用于保存docker镜像 包括镜像的层次结构和元数据
- 用户可以自建Registry 也可以使用官方的Docker Hub
- 分类
  - Sponsor Registry: 第三方的registry 供客户和Docker社区使用(捐赠者)
  - Mirror Registry: 第三方的registry 只让客户使用(云)
  - Vendor Registry: 由发布Docker镜像的供应商提供的registry(redhat)
  - Private Registry: 通过设有防火墙和额外安全层的私有实体提供的registry(自建)

![docker registry](./icons/docker-registry.png)

#### registry(repository and index)

- Repository
  - 由某特定的docker镜像的`所有迭代版本`组成的镜像仓库
  - 一个Registry中可以存在多个Repository
    - Repository可分为`顶层仓库`和`用户仓库`
    - 用户仓库名称格式为`用户名/仓库名` => `ilolicon/nginx`
  - 每个仓库可以包含多个Tag(标签) 每个标签对应一个镜像
- Index
  - 维护用户账户/镜像的校验以及公共命名空间的信息
  - 相当于为Registry提供一个完成用户认证等功能的检索接口
  
#### docker hub

[docker-hub](https://docs.docker.com/docker-hub/)

Docker Hub provides the following major features:

- [Repositories](https://docs.docker.com/docker-hub/repos/): Push and pull container images
- [Teams & Organizations](https://docs.docker.com/docker-hub/orgs/): Manage access to private repositories of container images
- [Docker Official Images](https://docs.docker.com/docker-hub/official_images/): Pull and use high-quality container images provided by Docker
- [Docker Verified Publisher Images](https://docs.docker.com/docker-hub/publish/): Pull and use high- quality container images provided by external vendors
- [Builds](https://docs.docker.com/docker-hub/builds/): Automatically build container images from GitHub and Bitbucket and push them to Docker Hub
- [Webhooks](https://docs.docker.com/docker-hub/webhooks/): Trigger actions after a successful push to a repository to integrate Docker Hub with other services

#### docker pull

[pull-commandline](https://docs.docker.com/engine/reference/commandline/pull/)
[quay.io](https://quay.io/)

```bash
docker pull <registry>[:port]/[<namespace>/]<name>:<tag>

# e.g:
# registry: quay.io
# port: 443(没指定 默认)
# namespace: coreos
# name: flannel(repostory名称)
# tag: v0.15.1-arm64 指定版本
docker pull quay.io/coreos/flannel:v0.15.1-arm64
```

| Namespace | Examples(<namespace/name>) |
|-----|-----|
| organization | redhat/kubernetes google/kubernetes |
| login(user name) | alice/application ilolicon/application |
| role | devel/database test/database prod/database |

#### 镜像的相关操作

![docker image create](./icons/docker-image-create.png)

- 镜像的生成途径
  - [Dockerfile](https://docs.docker.com/engine/reference/builder/)
  - [基于容器制作](https://docs.docker.com/engine/reference/commandline/commit/)
  - Docekr Hub automated builds(仍是基于Dockerfile)

- 另一种镜像分发方式
  - [docker-save](https://docs.docker.com/engine/reference/commandline/save/)
  - [docker-load](https://docs.docker.com/engine/reference/commandline/load/)

### 容器虚拟化网络

#### 容器虚拟化网络概述

[容器虚拟化网络](https://www.cnblogs.com/hukey/p/14062579.html)

```bash
OVS: Open VSwitch
SDN
Overlay Network(叠加网络)

# docker默认的三种网络
[root@master ~]# docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
78fa953ed316   bridge    bridge    local # 桥接 默认NAT桥
8ec55273feb2   host      host      local # 让容器直接使用宿主机的网络名称空间
9081fe29a218   none      null      local # 只有lo接口 没有其他网卡

[root@master ~]# yum -y install bridge-utils
[root@master ~]# brctl show
```

![Four network container archetypes](./icons/four-network-container-archetypes.png)

[docker-docs:network overview](https://docs.docker.com/network/)

- Closed Container
- Bridged Container(NAT桥接网络 默认)
- Joined Container(联盟式容器网络 相对隔离 只是共享同一个网络名称空间)
- Open Container(开放式容器网络 共享宿主机网络名称空间)

#### Bridged Containers

```bash
# Bridged Containers可以为docker run命令使用
# "--hostname HOSTNAME" 选项为容器指定主机名
docker run --rm --net bridge --hostname cloudnative.ilolicon.com busybox:latest hostname

# "--dns DNS_SERVER_IP" 选项能够为容器指定所使用的dns服务器地址
docker run --rm --dns 8.8.8.8 --dns 8.8.4.4 busybox:latest nslookup docker.com

# "--add-host HOSTNAME:IP" 选项能够为容器指定本地主机名解析项
docker run --rm --dns 172.16.0.1 --add-host "docker.com:172.16.0.100" busybox:latest cat /etc/hosts
```

##### Opening Inbound Communication / Expose

```bash
-p选项的使用格式

# 将指定的容器端口<containerPort> 映射至主机所有地址的一个动态端口
-p <containerPort>

# 将指定的容器端口<containerPort> 映射至指定的主机端口<hostPort>
-p <hostPort>:<containerPort>

# 将指定的容器端口<containerPort> 映射至主机指定<ip>的动态端口
-p <ip>::<containerPort>

# 将指定的容器端口<containerPort> 映射至主机指定<ip>的端口<hostPort>
-p <ip>:<hostPort>:<containerPort>

"动态端口" 指随机端口 具体的映射结果可使用docker port命令查看

Expose端口 还可以参考 -P 选项：暴露容器内部已指定的端口
```

#### Joined Container

- 联盟式容器是指使用某个已存在容器的网络接口的容器 接口被联盟内的各容器共享使用(NTS Network IPC)
- 联盟式容器彼此间虽然共享同一个网络名称空间 但其它内部名称空间如: User/Mount等还是隔离的
- 联盟式容器彼此间存在端口冲突的可能性 使用此种模式的网络模型情况
  - 多个容器上的程序需要程序loopback接口互相通信
  - 对某已存的容器的网络属性进行监控

```bash
# 创建一个监听于2222端口的http服务容器
docker run --name t1 -it --rm busybox
/ # ifconfig

# 创建一个联盟式容器(--network指定使用t1的网络名称空间) 并查看其监听的端口
docker run --name t2 -it --rm --network container:t1 busybox
/ # ifconfig
```

#### Open Container

```bash
# --network 指定 host
# 直接使用宿主机的网络名称空间 无需再Expose端口
docker run --rm -it --network host busybox
```

#### Closed Container

```bash
docker run --rm -it --network none busybox
```

#### 自定义docker0桥的网络信息

```json
// 编辑 /etc/docker/daemon.json 配置文件

{
    "bip": "192.168.1.5/24",
    "fixed-cidr": "10.20.0.0/16",
    "fixed-cidr-v6": "2001:db8::/64",
    "mtu": "1500",
    "default-gateway": "10.20.1.1",
    "default-gateway-v6": "2001:db8:abcd::89",
    "dns": ["10.20.1.2","10.20.1.3"]
}

// 核心选项为bip 即bridge ip之意 
// 用于指定docker0桥自身的IP地址 其他选项可以通过此地址计算得出
```

#### 使用TCP套接字

```json
// dockerd守护进程的C/S 其默认仅监听Unix Socket格式的地址 /var/run/docker.sock
// 如果使用TCP套接字 需要修改 /etc/docekr/daemon.json 配置文件
// 也可向dockerd直接传递 "-H|--host"选项

{
    "hosts": ["tcp://0.0.0.0:2375", "unix:///var/run/docker.sock"]
}
```

```bash
# dockerd使用TCP监听0.0.0.0:2375之后 客户端可以远程执行CLI
docker -H x.x.x.x:2375 image ls
docker -H x.x.x.x:2375 ps -a
```

#### 创建自定义网络

```bash
# 创建自定义网络
docker network create -d bridge --subnet "172.26.0.0/16" --gateway "172.26.0.1" mybr0

# 使用自定义网络
[root@master ~]# docker run -it --rm --name t1 --network mybr0 busybox
/ # ifconfig
eth0      Link encap:Ethernet  HWaddr 02:42:AC:1A:00:02  
          inet addr:172.26.0.2  Bcast:172.26.255.255  Mask:255.255.0.0
```

### docker存储卷

#### Why Data Volumes(存储卷)

```bash
Docker镜像由多个"只读层"叠加而成 
启动容器时 Docker会加载只读镜像层并在镜像栈顶部添加一个"读写层"

如果运行中的容器修改了现有的一个已经存在的文件
那该文件将会从读写层下面的只读层复制到读写层 该文件的只读版本"仍然存在"
只是已经被读写层中该文件的副本所隐藏 此即"写时复制(COW)"机制
```

![file-visible](./icons/files-visible-to-a-container.png)

- 关闭并重启容器 其数据不受影响 但删除Docker容器 则其更改将会全部丢失
- 存在的问题
  - 存储于联合文件系统中 不易于宿主机访问(效率低)
  - 容器间数据共享不便
  - 删除容器其数据会丢失
- 解决方案: "**卷**(volume)"
  - **卷**是容器上的一个或多个**目录** 此类目录可绕过联合文件系统 与宿主机上的某目录**绑定(关联)**
  - Volume于容器初始化之时即会创建 由base image提供的卷中的数据会于此期间完成复制
  - Volume的初衷是独立于容器的生命周期实现数据持久化 因此删除容器之时既不会删除卷 也不会对哪怕未被引用的卷做垃圾回收操作(加选项可以)

![volume](./icons/volume.png)

- 卷为docker提供了独立于容器的数据管理机制
  - 可以把**镜像**想象成静态文件 -> 例如 **程序**; 把卷类比为动态内容 -> 例如 **数据**; 于是 镜像可以重用 而卷可以共享
  - 卷实现了**程序(镜像)** 和 **数据(卷)** 分离 以及 **程序(镜像)** 和 **制作镜像的主机** 分离; 用户制作镜像时无需再考虑镜像运行的容器所在的主机的环境

![volume2](./icons/volume2.png)

#### Data volumes

```bash
Docekr有两种类型的卷 每种类型都在容器中存在一个挂载点 但在其宿主机上的位置有所不同
```

- Bind mount volume(绑定挂在卷)
  - a volume that points to a user-specified location on the host file system
- Docker-managed volume(Docker管理卷)
  - the Docker daemon creates managed volumes in a portion of the host's file system that's owned by Docker

![data-volume](./icons/data-volumes.png)

```bash
# 在容器中使用Volumes
# 为docker run命令使用-v选项即可使用Volume

# Docker-managed volume
docker run -it --name t1 -v /data busybox
docker inspect -f {{.Mounts}} t1

# Bind-mount Volume
docker run -it -v HOSTDIR:VOLUMEDIR --name t2 bustbox
docker inspect -f {{.Mount}} t2
```

#### Sharing volumes

```bash
# There are tow ways to share volumes between containers

# 多个容器的卷使用同一个主机目录
docker run -it --name t1 -v /docker/volumes/v1:/data busybox
docker run -it --name t2 -v /docker/volumes/v1:/data busybox

# 复制使用其他容器的卷 为docker run命令使用 --volumes-from 选项
docker run -it --name t3 -v /docker/volumes/v1:/data busybox
docker run -it --name t4 --volumes-from t3 busybox

# 如果有多个容器需要共享网络名称空间(UTS Network IPC) 以及需要共享存储卷
# 可以 事先创建一个 基础容器 其他的容器都加入该容器的网络名称空间(Joined Container) 并且复制该容器使用的卷(--volumes-from)
docker run --name infracon -it -v /data/infracon/volume:/data busybox
docker run --name nginx --network container:infracon --volumes-from infracon -it nginx
docker run ... --network container:infracon --volumes-from infracon ...
```
