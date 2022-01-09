#!/usr/bin/env bash

record_version() {
    date=$(date +"%F %T")
    log="/var/log/${1}.log"
    # clean log
    nums=$(wc -l "$log"  | awk '{print $1}')
    if [[ $nums -gt 10 ]]; then
        n=$((nums - 2 ))
        sed -i "1,${n}d" "$log"
    fi
    version=$(docker ps -a | awk '{if($NF == name) print $2}' name="$1")
    echo "[$date] ${version##*:}" >>"$log"
}

clean() {
    # stop && rm container
    docker stop "$1"
    docker rm "$1"
}

run() {
    # 需要修改docker-run参数 修改该函数即可
    host_port=$1
    container_port=$2
    run_image=$3
    name=$4

    # docker-run
    docker run -p "$host_port":"$container_port"/tcp \
        --name="$name" \
        --sysctl net.core.somaxconn=20480 \
        -d -e APP_ENV="PRODUCTION" \
        -v "/data/log/$name/":/var/log/ \
        --restart=always \
        --label "aliyun.logs.prefix-${name}"="/var/log/${name}.log*" \  # 需要修改前缀
        "$run_image"
}

check_params() {
    if [[ -z $1 ]] || [[ -z $2 ]] || [[ -z $3 ]] || [[ -z $4 ]]; then
        echo "Missing required parameters, Please check"
        exit 1
    fi
}

main() {
    script_name=$(basename "$0")
    name=${script_name%_*}
    version=$1
    namespace=$2
    host_port=$3
    container_port=$4
    check_params "$version" "$namespace" "$host_port" "$container_port"

    docker_repo="registry.cn-hangzhou.aliyuncs.com"
    run_image="$docker_repo/$namespace/$name:$version"

    # record version
    record_version "$name"

    # pull new version
    # 登录自定义docker仓库 此处示例为: 阿里云 [容器镜像服务]
    docker login --username=username -p password "$docker_repo"
    docker pull "$run_image"

    # clean old version
    app_id=$(docker ps -a | awk '{if($NF == name) print $1}' name="$name")
    if [[ -n $app_id ]]; then
        clean "$app_id"
    fi

    # docker-run
    run "$host_port" "$container_port" "$run_image" "$name"
}

# docker system prune -a -f
main "$1" "$2" "$3" "$4"
