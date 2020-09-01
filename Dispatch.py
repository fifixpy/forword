#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 文件名：server.py

import socket  # 导入 socket 模块
import xml.sax
class IpHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.ip = ""
        self.port = ""
        self.ips = []
        self.ports = []

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "addr":
            print("*****addr*****")
            title = attributes["title"]
            print("Title:", title)

    # 元素结束事件处理
    def endElement(self, tag):
        if self.CurrentData == "ip":
            print("ip:", self.ip)
            self.ips.append(self.ip)
        elif self.CurrentData == "port":
            print("port:", self.port)
            self.ports.append(int(self.port))
        self.CurrentData = ""

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "ip":
            self.ip = content
        elif self.CurrentData == "port":
            self.port = content


class dispatch:
    def __init__(self, clients):
        self.receiver = None
        self.clientList = clients


    def listenDis(self):
        self.receiver = socket.socket()  # 创建 socket 对象
        host = socket.gethostname()  # 获取本地主机名
        port = 12345  # 设置端口
        self.receiver.bind((host, port))  # 绑定端口
        self.receiver.listen(5)  # 等待客户端连接
        while True:
            c, addr = self.receiver.accept()  # 建立客户端连接
            tmsg = c.recv(1024)
            c.close()  # 关闭连接
            for client in self.clientList:
                ts = socket.socket()
                ts.connect((client[0], client[1]))
                ts.send(tmsg)
                ts.close()

class Udpdispatch:
    def __init__(self, clients):
        self.receiver = None
        self.clientList = clients


    def listenDis(self):
        self.receiver = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)  # 创建 socket 对象
        host = socket.gethostname()  # 获取本地主机名
        port = 12345  # 设置端口
        self.receiver.bind((host, port))  # 绑定端口
        self.receiver.listen(5)  # 等待客户端连接
        while True:
            tmsg = self.receiver.recvfrom(1024)
            for client in self.clientList:
                ts = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
                ts.sendto(tmsg, client)
                ts.close()


if __name__ == '__main__':
    # 创建一个 XMLReader
    parser = xml.sax.make_parser()
    # turn off namepsaces
    parser.setFeature(xml.sax.handler.feature_namespaces, 0)

    # 重写 ContextHandler
    Handler = IpHandler()
    parser.setContentHandler(Handler)
    parser.parse("aaa.xml")
    cls = []
    for i in range(len(Handler.ips)):
        cls.append((Handler.ips[i], Handler.ports[i]))
    dis = dispatch(cls)
    dis.listenDis()

