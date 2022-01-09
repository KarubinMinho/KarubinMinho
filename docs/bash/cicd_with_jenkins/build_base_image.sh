#!/usr/bin/env bash

namespace="basic"                                     # namespace
registory_address="registry.cn-hangzhou.aliyuncs.com" # docker repository address
jenkins_build_path="/var/lib/jenkins/workspace"       # jenkins build path
jenkins_project_name="BasicImages"                    # jenkins project name

log() {
    date=$(date +"%F %T")
    echo "[$date] $*"
}

build_image() {
    tag=$1
    path=$2
    log docker build -t "$tag" "$path"
    docker build -t "$tag" "$path"
}

push_image() {
    name=$1
    log docker push "$name"
    docker push "$name"
}

main() {
    cd "$jenkins_build_path/$jenkins_project_name" || exit
    # 可能更改的不止一个目录
    change_path=$(
        git diff --name-only HEAD HEAD~ | 
        awk -F'/' '{print $1}' | 
        sort | 
        uniq)
    log "##### change path: $change_path"

    for path in $change_path; do
        prefix=${path%%_*}
        repository_name=$(echo "${path}" | tr '[:upper:]' '[:lower:]')

        # build && push
        # cd "$path" || exit
        build_image "${registory_address}/${namespace}/${repository_name}" "$path"

        # push other address if has special prefix
        if [[ $prefix != "us" ]]; then
            push_image "${registory_address}/${namespace}/${repository_name}"
        else
            registory_address="registry-vpc.us-west-1.aliyuncs.com"
            push_image "${registory_address}/${namespace}/${repository_name}"
        fi
    done
}

main
