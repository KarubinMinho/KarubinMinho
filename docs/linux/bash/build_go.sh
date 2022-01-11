#!/usr/bin/env bash

GOBIN=$(which go)
OS=$("$GOBIN" env GOOS)

build() {
    "$GOBIN" build -o ./bin/"$1" ./main.go
    "$GOBIN" env -u GOOS
}

build_linux() {
    if [[ "$OS" != "linux" ]]; then
        "$GOBIN" env -w GOOS=linux
    fi
    build "$1"
}

build_windows() {
    if [[ "$OS" != "windows" ]]; then
        "$GOBIN" env -w GOOS=windows
    fi
    build "$1"
}

main() {
    "$GOBIN" env -w GO111MODULE=on
    "$GOBIN" env -w GOPROXY=https://goproxy.cn,direct

    if [[ $# == 1 ]]; then
        build_linux "${1%%.*}"
    elif [[ $# == 2 ]]; then
        build_linux "$1"
        build_windows "$2"
    else
        echo "Usage: ./$0 [linux_bin] [windows_bin]"
    fi
}

main "$@"
