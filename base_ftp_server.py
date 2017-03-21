#!/usr/bin env
#coding:utf-8
#base_ftp_server.py

import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler,ThrottledDTPHandler
from pyftpdlib.servers import FTPServer
from config_ftp import *

def init_ftp_server():
# 实例化虚拟用户 这是ftp验证首页条件
    authorizer = DummyAuthorizer()
    """
           读权限:
            - "e" = 改变文件目录
            - "l" = 列出文件 (LIST, NLST, STAT, MLSD, MLST, SIZE, MDTM commands)
            - "r" = 从服务器接收文件 (RETR command)

           写权限:
            - "a" = 文件上传 (APPE command)
            - "d" = 删除文件 (DELE, RMD commands)
            - "f" = 文件重命名 (RNFR, RNTO commands)
            - "m" = 创建文件 (MKD command)
            - "w" = 写权限 (STOR, STOU commands)
            - "M" = 文件传输模式 (SITE CHMOD command)
    """
    if enable_anonymous:
    #添加匿名用户
        authorizer.add_anonymous(anonymous)

    #读取配置中用户并授权
    for user in user_list:
        name, passwd, permit, homedir = user
        try:
             authorizer.add_user(name, passwd, homedir, perm=permit)
        except:
             print("配置文件错误请检查是否正确匹配了相应的用户名、密码、权限、路径")
             print(user)

    dtp_handler=ThrottledDTPHandler
    dtp_handler.read_limit=max_download #下载速度
    dtp_handler.write_limit=max_upload  #上传速度
    # FTPHandler实例
    ftp_handler=FTPHandler
    ftp_handler.authorizer = authorizer

    # 是否开启记录
    if enable_logging:
        logging.basicConfig(filename="pyftp.log",level=logging.INFO)


    # 登录时候显示的标题
    ftp_handler.banner=welcom_banner
    ftp_handler.masquerade_address=masquerade_address
    ftp_handler.passive_ports=range(passive_ports[0],passive_ports[1])

    # 监听的ip和端口
    server=FTPServer((ip,port),ftp_handler)


    #  设置最大连接数
    server.max_cons = max_cons
    server.max_cons_per_ip = max_ip

    server.serve_forever()

def ignor_octothorpe(text):
    #通过遍历每一行 返回#号前面的数据
    for i,item in enumerate(text):
        if item=="#":
            return text[:i]
        pass
    return text

def init_user_config():
    f = open("baseftp.ini",encoding='utf-8')
    while 1:
        line = f.readline()
        if len(ignor_octothorpe(line)) > 3:
            user_list.append(line.split())

        if not line:
            break


if __name__ == '__main__':
    # 用于保存授权用户的登录
    user_list = []
    # 从配置文件初始化用户
    init_user_config()
    init_ftp_server()