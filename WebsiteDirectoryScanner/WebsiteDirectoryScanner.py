# -*- coding: utf-8 -*-
"""
@author yumu
@version 1.0.6
"""
import argparse

__version__ = "1.0.6"
__mode2directory__ = {
    '1': "./directory/DIR.txt"
}

import os, sys
import requests

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

colorPrinter = ColorPrinter()

def scan(url, url_list, directory_list, mode, outputname, outputpath, quite, timeout):
    target_url = []
    if url_list != None:
        for url_file in url_list:
            try:
                with open(url_file, "r") as f:
                    urls = f.readlines()
                for single_url in urls:
                    single_url = single_url.strip()
                    if single_url[-1] == "/":
                        single_url = single_url[:-1]
                    target_url.append(single_url)
            except:
                print(colorPrinter.wrong_text("[-] 指定的url文件读取失败，请检查路径和文件名以及是否有读取权限"))

    target_directory = []
    if directory_list != None:
        try:
            for directory_file in directory_list:
                with open(directory_file, "r") as f:
                    directorys = f.readlines()
                for single_directory in directorys:
                    single_directory = single_directory.strip()
                    if single_directory[0] != "/":
                        single_directory = "/" + single_directory
                    target_directory.append(single_directory)
        except:
            print(colorPrinter.wrong_text("[-] 指定的字典文件读取失败，请检查路径和文件名以及是否有读取权限"))

    if url != None:
        for u in url:
            u = u.strip()
            if u[-1] == "/":
                u = u[:-1]
            target_url.append(u)

    if mode != None:
        for m in mode:
            try:
                with open(__mode2directory__[m], "r") as f:
                    directorys = f.readlines()
                for single_directory in directorys:
                    single_directory = single_directory.strip()
                    if single_directory[0] != "/":
                        single_directory = "/" + single_directory
                    target_directory.append(single_directory)
            except:
                print(colorPrinter.wrong_text("[-] 默认字典读取失败，请检查默认字典是否被移动或无读取权限"))

    if len(target_url) == 0:
        print(colorPrinter.wrong_text("没有要扫描的url"))
        return
    if len(target_directory) == 0:
        print(colorPrinter.wrong_text("没有指定的字典"))
        return
    log_info = []
    if timeout == None:
        timeout = 5
    for u in target_url:
        print(colorPrinter.special_text("正在扫描" + u))
        log_info.append(u + "的扫描结果如下")
        for dir in target_directory:
            try:
                resp = requests.get(u + dir, timeout=int(timeout))
            except:
                continue
            if quite:
                if resp.status_code == 200:
                    print(colorPrinter.info_text(u + dir + "   " + str(resp.status_code)))
                    log_info.append(u + dir + "   " + str(resp.status_code))
            else:
                if resp.status_code == 200:
                    print(colorPrinter.info_text(u + dir + "   " + str(resp.status_code)))
                    log_info.append(u + dir + "   " + str(resp.status_code))
                else:
                    print(colorPrinter.warn_text(u + dir + "   " + str(resp.status_code)))

    index = 1
    default_path = "../result/WebsiteDirectoryScanner/"
    if outputpath != None:
        default_path = outputpath
        if default_path[-1] != "/":
            default_path += "/"

    if not os.path.exists(default_path):
        os.makedirs(default_path)

    if outputname == None:
        while (os.path.exists(default_path + str(index) + ".txt")):
            index += 1
        full_path = default_path + str(index) + ".txt"
    else:
        full_path = default_path + outputname[0]
    try:
        with open(full_path, "w") as f:
            for log in log_info:
                f.write(log + "\n")
        print("[+] 文件已经保存到 " + colorPrinter.wrong_text(os.path.abspath(full_path)))
    except:
        print(colorPrinter.wrong_text("[-] 文件写入失败，请检查路径和文件名以及是否有写入权限"))


def get_parser():
    """
    设置命令行参数
    :return:
    """
    parser = argparse.ArgumentParser(description="Website Directory Scanner")
    group = parser.add_argument_group()
    group.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="显示版本信息"
    )
    group.add_argument(
        "-s",
        "--scan",
        action="store_true",
        help="开始扫描"
    )
    group.add_argument(
        "-u",
        "--url",
        action="store",
        help="指定要扫描的url",
        nargs='*'
    )
    group.add_argument(
        "-l",
        "--list",
        action="store",
        help="指定要扫描的url的列表(文件)",
        nargs='*'
    )
    group.add_argument(
        "-d",
        "--directory",
        action="store",
        help="指定扫描字典",
        nargs='*'
    )
    group.add_argument(
        "-m",
        "--mode",
        action="store",
        help="选择模式（内置字典）",
        nargs='*'
    )
    group.add_argument(
        "-on",
        "--outputname",
        action="store",
        help="指定输出结果文件名",
        nargs=1,
    )
    group.add_argument(
        "-op",
        "--outputpath",
        action="store",
        help="指定输出结果路径",
    )
    group.add_argument(
        "-q",
        "--quite",
        action="store_true",
        help="指定为安静模式，只输出200的url"
    )
    group.add_argument(
        "-to",
        "--timeout",
        action="store",
        help="指定超时时间"
    )
    return parser


def show_version():
    """
    显示版本信息
    :return:
    """
    print(colorPrinter.wrong_text("[ 网站目录扫描器 ]  " + __version__))


def print_tool_info():
    print("[ yumueat | https://github.com/yumueat]")
    print("[ Website Directory Scanner | https://github.com/yumueat/Penetration-test-toolkit]")


def main():
    parser = get_parser()
    args = parser.parse_args()
    print_tool_info()
    if args.version:
        show_version()
    elif args.scan:
        scan(args.url, args.list, args.directory, args.mode, args.outputname, args.outputpath, args.quite, args.timeout)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
