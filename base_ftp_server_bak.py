#!/usr/bin env
#base_ftp_server.py

import logging
from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer

# 实例化虚拟用户 这是ftp验证首页条件
authorizer = DummyAuthorizer()
# 为了方便起见 这里文件目录改成了home目录
# 添加用户权限和路径 参数分别是 用户名 密码 用户目录 权限
authorizer.add_user("user", "12345", "E:\python\\bwj", perm="elradfmw")
#添加匿名用户 这个只需要路径就行
authorizer.add_anonymous("E:\python\\bwj")
#初始化ftp句柄
handler = FTPHandler
handler.authorizer = authorizer
#监听ip 和端口 这是本地一个服务器
handler.masquerade_address='127.0.0.1'
handler.passive_ports=range(2000,2333)
server = FTPServer(("0.0.0.0", 21), handler)
# 开始服务
server.serve_forever()
