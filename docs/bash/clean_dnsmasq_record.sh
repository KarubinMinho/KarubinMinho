#!/usr/bin/env bash

# 匹配需要删除的IP行
SERVER_IPS=(
    x.x.x.1
    x.x.x.2
    x.x.x.3
    x.x.x.n
)

DNSMASQ_PATH=/etc/dnsmasq.d/

# refer: https://unix.stackexchange.com/questions/412868/bash-reverse-an-array
reverse() {
    array=( "$@" )
    local min=0
    local max=$(( ${#array[@]} -1 ))

    while [[ min -lt max ]]; do
        # Swap current first and last elements
        local x="${array[$min]}"
        array[$min]="${array[$max]}"
        array[$max]="$x"

        # Move closer
        (( min++, max-- ))
    done
}

delete_record() {
    local file_path
    local file_number
    local records=( "$@" )
    # shellcheck disable=SC2068
    for line in ${records[@]}; do
        file_path=$(echo "$line" | awk -F: '{print $1}')
        file_number=$(echo "$line" | awk -F: '{print $2}')
        sed -i "${file_number}d" "$file_path"
    done
}

restart_service() {
    # restart dnsmasq
    systemctl restart dnsmasq
}

main() {
    # shellcheck disable=SC2068
    for ip in ${SERVER_IPS[@]}; do
        mapfile -t raw_records < <(grep -w -n -r "$ip" "$DNSMASQ_PATH")
        reverse "${raw_records[@]}"
        delete_record "${array[@]}"
    done

    restart_service
}

main
