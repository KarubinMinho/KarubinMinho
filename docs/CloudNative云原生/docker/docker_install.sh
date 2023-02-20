#!/usr/bin/env bash
#
# refer: https://docs.docker.com/engine/install/centos/
# refer: https://docs.docker.com/engine/install/ubuntu/

centos_docker_repo() {
    local URL=https://download.docker.com/linux/centos/docker-ce.repo
    local REPO_PATH=/etc/yum.repos.d/docker-ce.repo
    /usr/bin/curl -s $URL -o $REPO_PATH
    sed -i '/^baseurl=/s/download.docker.com/mirrors.aliyun.com\/docker-ce/' $REPO_PATH
}

ubuntu_docker_repo() {
    sudo apt-get update
    sudo apt-get install -y ca-certificates curl gnupg lsb-release
    sudo mkdir -p /etc/apt/keyrings
    sudo rm -f /etc/apt/keyrings/docker.gpg
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
    echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
}

centos_uninstall_old_versions() {
    yum -y remove docker \
                  docker-client \
                  docker-client-latest \
                  docker-common \
                  docker-latest \
                  docker-latest-logrotate \
                  docker-logrotate \
                  docker-engine > /dev/null 2>&1
}

ubuntu_uninstall_old_versions() {
    sudo apt-get remove -y docker docker-engine docker.io containerd runc
}

centos_install_docker_engine() {
    yum -y install docker-ce docker-ce-cli containerd.io
    systemctl start docker
    systemctl enable docker
}

ubuntu_install_docker_engine() {
    sudo chmod a+r /etc/apt/keyrings/docker.gpg
    sudo apt-get update
    local VERSION_STRING=5:20.10.23~3-0~ubuntu-jammy
    sudo apt-get install -y docker-ce=$VERSION_STRING docker-ce-cli=$VERSION_STRING containerd.io docker-compose-plugin
}

# https://docs.docker.com/compose/install/other/
install_docker_compose() {
    local VERSION=v2.15.1
    local ARCH
    ARCH=$(uname -a | awk '{print $(NF-1)}')
    curl -SL https://github.com/docker/compose/releases/download/$VERSION/docker-compose-linux-"$ARCH" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
}

main() {
    if uname -a | grep -qw Ubuntu; then
        ubuntu_docker_repo
        ubuntu_uninstall_old_versions
        ubuntu_install_docker_engine
    else
        centos_docker_repo
        centos_uninstall_old_versions
        centos_install_docker_engine
    fi
    install_docker_compose
}

main
