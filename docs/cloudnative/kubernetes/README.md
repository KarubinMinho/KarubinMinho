# ⭐ Kubernetes

[![kubernetes readme](https://img.shields.io/badge/Kubernetes-README-356DE3)](https://kubernetes.io/zh/docs/home/)

[![kubernetes](./icons/kubernetes.svg)](https://kubernetes.io/)

`container evolution`

![container_evolution](./icons/container_evolution.svg)

## 容器编排

- Ansible/Saltstack **传统应用**编排工具
- Docker
  - docker compose(docker单机编排)
  - docker swarm(docker主机加入docker swarm资源池)
  - docker machine(完成docker主机加入docker swarm资源池的先决条件/预处理工具)
- Mesos(IDC OS) + marathon(面向容器编排的框架)
- kubernetes(Borg)
  - 自动装箱(基于依赖 自动完成容器部署 不影响其可用性)
  - 自我修复
  - 水平扩展
  - 服务发现和负载均衡
  - 自动发布和回滚
  - 密钥和配置管理
  - 存储编排
  - 任务批量处理运行

概念: `DevOps` `MicroServices` `Blockchain`

- CI: 持续集成
- CD: 持续交互 Delivery
- CD: 持续部署 Deployment

## k8s架构概述

- 集群
  - 有中心节点的集群架构系统(抽象各主机资源 统一对外提供计算)
  - master/nodes(workers)

![kubernetes-cluster](./icons/kubernetes-cluster.png)
