#!/usr/bin/env bash
#
# Grafana Docker Install

docker run --restart=always \
-d --name grafana -p 3000:3000 \
-e "GF_SECURITY_ADMIN_PASSWORD=password" \
-v "/mnt/data/grafana/grafana.ini:/usr/share/grafana/conf/defaults.ini" \
-v "/mnt/data/grafana/data/:/var/lib/grafana" \
grafana/grafana
