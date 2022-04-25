#!/bin/bash
#
# Prometheus Webhook Dingtalk Docker Install

docker run --restart=always \
-d --name "prometheus-webhook-dingtalk" \
-p 127.0.0.1:8060:8060 \
-v "/etc/prometheus-webhook-dingtalk:/etc/prometheus-webhook-dingtalk/" \
timonwong/prometheus-webhook-dingtalk
