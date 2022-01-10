#!/usr/bin/env bash

docker run -d --name="grafana-image-renderer" \
-p 8081:8081 \
--restart=always \
grafana/grafana-image-renderer:latest
