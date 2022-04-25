import socket


server = socket.socket()  # TCP 三次握手四次挥手
server.bind(('127.0.0.1', 8080))  # IP协议 以太网协议 arp协议...
server.listen(5)  # 池


""" respuest data:
b'GET / HTTP/1.1\r\n
Host: 127.0.0.1:8080\r\n
Connection: keep-alive\r\n
Cache-Control: max-age=0\r\n
Upgrade-Insecure-Requests: 1\r\n
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.146 Safari/537.36\r\nAccept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9\r\n
Sec-Fetch-Site: none\r\n
Sec-Fetch-Mode: navigate\r\n
Sec-Fetch-User: ?1\r\n
Sec-Fetch-Dest: document\r\nA
ccept-Encoding: gzip, deflate, br\r\n
Accept-Language: zh-CN,zh-TW;q=0.9,zh;q=0.8,en-US;q=0.7,en;q=0.6\r\n\r\n'

"""

while True:
    conn, client = server.accept()
    data = conn.recv(1024)
    # print(data)                 # bytes
    data = data.decode('utf-8')  # 得到字符串
    # 获取字符串中特定内容 => 正则 or 字符串有规律可以使用：切割
    conn.send(b'HTTP/1.1 200 OK\r\n\r\n')
    current_path = data.split()[1]  # 获取路径信息
    if current_path == '/index':
        with open(r'templates/index.html', 'rb') as f:
            conn.send(f.read())
    elif current_path == '/login':
        with open(r'templates/login.html', 'rb') as f:
            conn.send(f.read())
    else:
        conn.send(b'hello web')
    conn.close()


# 如何做到后缀的不同返回不同的内容
# 拿到用户输入的 路径 做判断


