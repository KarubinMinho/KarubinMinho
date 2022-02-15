#!/usr/bin/env bash
#
# refer: https://docs.docker.com/engine/install/centos/

docker_repo() {
    URL=https://download.docker.com/linux/centos/docker-ce.repo
    REPO_PATH=/etc/yum.repos.d/docker-ce.repo
    /usr/bin/curl -s $URL -o $REPO_PATH
    sed -i '/^baseurl=/s/download.docker.com/mirrors.aliyun.com\/docker-ce/' $REPO_PATH
}

uninstall_old_versions() {
    yum -y remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine > /dev/null 2>&1
}

install_docker_engine() {
    yum -y install docker-ce docker-ce-cli containerd.io
    systemctl start docker
    systemctl enable docker
}

main() {
    docker_repo
    uninstall_old_versions
    install_docker_engine
}

main
