import socketserver
import logging
import threading


FORMAT = "%(asctime)s %(threadName)s %(thread)d %(message)s"
logging.basicConfig(level=20, format=FORMAT, datefmt='%F %T')


class EchoHandler(socketserver.BaseRequestHandler):
    clients = {}
    lock = threading.Lock()

    def setup(self) -> None:
        # setup 资源申请 变量配置
        super().setup()
        self.event = threading.Event()
        # self.lock = threading.Lock()
        with self.lock:
            self.clients[self.client_address] = self.request

    def finish(self) -> None:
        # finally中执行 不管是否异常 都会执行 主要做清理工作
        super().finish()
        self.event.set()
        with self.lock:
            self.clients.pop(self.client_address)

    def handle(self) -> None:
        while True:
            data = self.request.recv(1024)
            if not data or data == b'quit':
                break
            msg = "### {} ###".format(data.decode()).encode()
            with self.lock:
                print(self.lock, id(self.lock))
                for sock in self.clients.values():
                    sock.send(msg)


server = socketserver.ThreadingTCPServer(('127.0.0.1', 9999), EchoHandler)
server.daemon_threads = True  # 设置每个handle线程为daemon线程 否则OSError
threading.Thread(target=server.serve_forever, name='serve_forever').start()
while True:
    cmd = input('>>>')
    if cmd == 'quit':
        server.server_close()
        server.shutdown()   # Stops the serve_forever loop. 否则直接退出会有OSError
        break
    print(threading.enumerate())

print("=====END=====")
