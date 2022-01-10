#!/bin/bash
#
# refer: https://grafana.com/docs/loki/latest/installation/

VERSION=2.3.0
BASE_PATH=/opt/promtail

mkdir -p $BASE_PATH
cd $BASE_PATH || exit
wget https://raw.githubusercontent.com/grafana/loki/v$VERSION/clients/cmd/promtail/promtail-docker-config.yaml -O $BASE_PATH/promtail-config.yaml

docker run -d \
--name promtail \
--restart always \
-v "$(pwd)":/mnt/config \
-v /data:/data \
grafana/promtail:$VERSION -config.file=/mnt/config/promtail-config.yaml
