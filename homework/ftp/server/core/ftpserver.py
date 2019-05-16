#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author: vita
import socket
import json
import os
import re
import configparser
import subprocess
import hashlib
from conf import settings
from utils.print_write_log import print_info


class FtpServer(object):
    MSG_SIZE = 1024
    STATUS_CODE = {
        "100": "login success!",
        "101": "your password is not correct",
        "102": "user not exist",
        "200": "file download starting!",
        "201": "the file you download is not exist!",
        "300": "ready to list dir!",
        "400": "ready to change dir!",
        "401": "dir not exist!",
        "402": "you do not have permission to that dir!",
        "500": "user create success!",
        "501": "user already exist!"
    }

    def __init__(self):
        self.server_socket_obj = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.request_conn_obj = None
        self.client_addr = None
        self.accounts = self.load_accounts()
        self.user_current_dir = None
        self.user_home_dir = None
        self.hash = hashlib.md5()
        self.username = None
        self.left_quota = None

    @staticmethod
    def load_accounts():
        """
        加载用户文件
        :return:
        """
        config_obj = configparser.ConfigParser()
        config_obj.read(settings.ACCOUNT_FILE)
        return config_obj

    def keep_running(self):
        """
        这里是允许多用户登录，但这里没有使用多线程，是通过while True的方式，
        一个用户断开连接，另一个用户才能继续连接
        :return:
        """
        self.server_socket_obj.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.server_socket_obj.bind((settings.FTP_SERVER_HOST, settings.FTP_SERVER_PORT))
        self.server_socket_obj.listen(5)
        while True:
            print("waiting client to connect!")
            self.request_conn_obj, self.client_addr = self.server_socket_obj.accept()
            # self.client_addr是个元组('127.0.0.1','13850')
            print_info("client connect:ip:%s port:%s" % (self.client_addr[0], self.client_addr[1]))
            # try:
            self.handle_client_request()
                # 客户端输入quit退出程序时，服务端的
            # except Exception as e:
            #     print(e)

            print_info("client closed connection!ip:%s port:%s" % (self.client_addr[0], self.client_addr[1]))

    def get_response_from_client(self):
        """
        接收客户端发送的数据
        :return:
        """
        # 客户端发送请求命令时，把数据封装为1024字节，避免粘包问题
        client_request_cmd = self.request_conn_obj.recv(self.MSG_SIZE)

        # 因为客户端是先dumps,然后encode("utf-8")
        client_request_cmd = json.loads(client_request_cmd.decode("utf-8"))
        #         client_request_cmd = {
        #             'action_type': action_type,
        #             'fill':''
        #         }
        return client_request_cmd

    def handle_client_request(self):
        """
        接收用户请求，并处理
        :return:
        """
        while True:
            client_request_cmd = self.get_response_from_client()
            action_type = client_request_cmd["action_type"]
            # 客户端传过来quit退出程序，这里退出接受消息的循环，到达接受其他用户请求的循环层
            if action_type == "quit":
                break

            if hasattr(self, action_type):
                func = getattr(self, action_type)

                func(client_request_cmd)

    def send_certain_size_response(self, response_code, **kwargs):
        """
        发送固定打下的包到客户端，这是处理粘包问题的必备思路
        首先发送一个固定大小的包到对方，对方会按照指定大小接受，如果是文件，数据包中会含有要发送的文件的大小
        后面再发送文件或其他内容，对方只需要知道文件的大小，通过循环，即可接受全部的内容
        :param response_code:
        :param kwargs:
        :return:
        """
        response_data = {
            "fill": "",
            "response_code": response_code,
            "response_msg": self.STATUS_CODE[response_code]
        }

        response_data.update(kwargs)
        bytes_response_data = json.dumps(response_data).encode("utf-8")
        if len(bytes_response_data) < self.MSG_SIZE:
            # 进行数据填充，使得长度为1024字节
            response_data["fill"] = response_data["fill"].zfill(self.MSG_SIZE-len(bytes_response_data))
            bytes_response_data = json.dumps(response_data).encode("utf-8")
        # 这里一定是self.request_conn_obj，不是self.server_socket_obj
        self.request_conn_obj.send(bytes_response_data)

    def create_user(self, client_request_cmd):
        """
        创建新用户，验证用户是否存在，同时在home目录下创建文件夹
        :param client_request_cmd:
        :return:
        """

        new_user_name = client_request_cmd["new_user_name"]
        new_user_password = client_request_cmd["new_user_password"]
        # 用户输入的是G，保存到文件中是B，字节，便于后面比较大小
        # 要转换为str才能保存到ini文件中，由于用户可能输入小数，所以用float
        user_quota = str(float(client_request_cmd["user_quota"].replace("G", ""))*1024*1024*1024)
        # 保存字节到文件中

        self.hash.update(new_user_password.encode())
        # 加密后的密码
        new_user_password = self.hash.hexdigest()
        # 新加的用户，在用户家目录下创建目录
        new_user_home_dir = os.path.join(settings.USER_HOME_DIR, new_user_name)
        if self.accounts.has_section(new_user_name):
            print_info(self.STATUS_CODE["501"])
            self.send_certain_size_response("501")
        else:
            self.accounts.add_section(new_user_name)
            self.accounts.set(new_user_name, "password", new_user_password)
            self.accounts.set(new_user_name, "quota", user_quota)
            self.accounts.set(new_user_name, "left_quota", user_quota)
            self.accounts.write((open(settings.ACCOUNT_FILE, "w")))
            self.send_certain_size_response("500")
            os.mkdir(new_user_home_dir)
            print_info(self.STATUS_CODE["500"])

    def auth(self, client_request_cmd):
        """
        用户登录验证
        :param client_request_cmd:
        :return:
        """
        username = client_request_cmd["username"]
        password = client_request_cmd["password"]
        self.hash.update(password.encode())
        # 加密后的密码
        password = self.hash.hexdigest()
        if username in self.accounts:
            real_password = self.accounts[username]["password"]
            if password == real_password:
                self.user_current_dir = os.path.join(settings.USER_HOME_DIR, username)
                self.user_home_dir = os.path.join(settings.USER_HOME_DIR, username)
                self.username = username
                self.left_quota = int(self.accounts[username]["left_quota"])
                self.send_certain_size_response("100", left_quota=self.left_quota)
                print_info(self.STATUS_CODE["100"])

            else:
                print_info("your password is not correct", "error")
                self.send_certain_size_response("101")
        else:
            print_info("user %s not exist" % username, "error")
            self.send_certain_size_response("102")

    @staticmethod
    def file_md5_value(file_asb_path):
        cmd_obj = subprocess.Popen(
            "certutil -hashfile %s MD5" % file_asb_path,
            shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = cmd_obj.stdout.read()
        # stderr = cmd_obj.stderr.read()
        # print(stdout.decode("gbk"))
        file_md5_value = re.findall("[0-9a-zA-Z]{32}", stdout.decode("gbk"))[0]
        return file_md5_value

    def put(self, client_request_cmd):
        """
        处理文件上传,包含md5验证
        :param client_request_cmd:
        :return:
        """
        file_total_size = client_request_cmd["file_total_size"]

        file_name = client_request_cmd["file_name"]
        # 源文件的md5值
        source_file_md5 = client_request_cmd["file_md5_value"]
        file_abs_path = os.path.join(self.user_current_dir, file_name)
        received_file_size = 0
        f = open(file_abs_path, "wb")
        while received_file_size < file_total_size:
            left_file_size = file_total_size-received_file_size
            if left_file_size < self.MSG_SIZE:
                data = self.request_conn_obj.recv(left_file_size)
                # 这样操作是不可以的len(data)!=left_file_size
                # received_file_size += left_file_size
            else:
                data = self.request_conn_obj.recv(self.MSG_SIZE)
                # received_file_size += self.MSG_SIZE
            received_file_size += len(data)
            f.write(data)

        f.close()
        # 用户的剩余磁盘空间减去文件大小
        self.left_quota -= file_total_size
        self.accounts[self.username]["left_quota"] = str(self.left_quota)
        self.accounts.write((open(settings.ACCOUNT_FILE, "w")))
        file_md5_value = self.file_md5_value(file_abs_path)
        # 验证文件是否和客户端一样
        if file_md5_value == source_file_md5:
            print_info("file is same with client,file received done")
        else:
            print_info("file is not same with client!", "error")


    def get(self, client_request_cmd):
        """
        从服务端下载文件
        :param client_request_cmd:
        :return:
        """
        # 客户端上传的相对路径get a/b/test.txt，相对路径与用户当前所在路径想拼
        file_relative_path = client_request_cmd["file_relative_path"]
        # 绝对路径
        file_abs_path = os.path.join(self.user_current_dir, file_relative_path)
        if os.path.exists(file_abs_path):
            file_total_size = os.path.getsize(file_abs_path)
            # 获取源文件的md5值
            file_md5_value = self.file_md5_value(file_abs_path)
            self.send_certain_size_response("200", file_total_size=file_total_size, file_md5_value=file_md5_value)
            f = open(file_abs_path, "rb")
            for line in f:
                self.request_conn_obj.send(line)
            f.close()
            print_info("file transfer successful!")

        else:
            print_info(self.STATUS_CODE["201"])
            self.send_certain_size_response("201")

    def ls(self, client_request_cmd):
        """
        列出当前目录下的内容
        :param client_request_cmd:
        :return:
        """
        print(self.user_current_dir)
        cmd_obj = subprocess.Popen("dir %s" % self.user_current_dir, shell=True,
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        stdout = cmd_obj.stdout.read()
        stderr = cmd_obj.stderr.read()
        cmd_result = stdout+stderr
        if len(cmd_result) == 0:
            cmd_result = "empty dir".encode("gbk")
        cmd_result_total_size = len(cmd_result)
        self.send_certain_size_response("300", cmd_result_total_size=cmd_result_total_size)
        self.request_conn_obj.sendall(cmd_result)

    def cd(self, client_request_cmd):
        target_path = client_request_cmd["target_path"]
        # E:\PythonProject\python-test\homework\ftp\server\home\vita\test\..\..使用abspath能去掉..
        # 变为E:\PythonProject\python-test\homework\ftp\server\home\vita\test
        dir_abs_path = os.path.abspath(os.path.join(self.user_current_dir, target_path))
        print_info(dir_abs_path)
        if os.path.isdir(dir_abs_path):
            if dir_abs_path.startswith(self.user_home_dir):
                client_terminal_display_dir = dir_abs_path.replace(self.user_home_dir, "")
                self.send_certain_size_response("400", client_terminal_display_dir=client_terminal_display_dir)
                print_info(self.STATUS_CODE["400"])
                self.user_current_dir = dir_abs_path
                print_info("dir change success!")
            else:
                # 输出无权限
                self.send_certain_size_response("402")
                print_info(self.STATUS_CODE["402"])
        else:
            # 输出目录不存在
            self.send_certain_size_response("401")
            print_info(self.STATUS_CODE["401"])
