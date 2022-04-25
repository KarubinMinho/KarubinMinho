#!/bin/bash
#
#

name="xx"                                       # remote docker repository name
namespace="namespace"                           # namespace
version=$(date +%Y%m%d%H%M)                     # version
docker_repo="registry.cn-hangzhou.aliyuncs.com" # remote docker repository address
jenkins_name="jenkins_project_name"             # local jenkins project name
host_port=8080                                  # host port
container_port=8080                             # container port

build_image() {
    # build image
    build_path="/var/lib/jenkins/workspace/$jenkins_name/"
    cd $build_path || exit
    docker build -t "$namespace/$name:$version" .
}

push_image() {
    # push to remote repository
    app_id=$(docker images | awk '{if($2 == v && $1 == n)print $3}' v="$version", n="$namespace/$name")

    repo="$docker_repo/$namespace/$name:$version"
    docker tag "$app_id" "$repo"
    docker push "$repo"
}

deploy_image() {
    target=$1
    ansible "$target" -m shell -a "./workspace/module_run.sh $version $namespace $host_port $container_port"
}

main() {
    build_image
    push_image
    deploy_image "$1"
}

main "$1"
