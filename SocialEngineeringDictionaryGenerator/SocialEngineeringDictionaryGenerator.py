# -*- coding: utf-8 -*-
"""
@author yumu
@version 1.0.8
"""
import argparse

__version__ = "1.0.8"
import time
import os,sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils import *

colorPrinter = ColorPrinter()
def get_parser():
    """
    设置命令行参数
    :return:
    """
    parser = argparse.ArgumentParser(description="Social Engineering Dictionary Generator")
    group = parser.add_argument_group()
    group.add_argument(
        "-v",
        "--version",
        action="store_true",
        help="显示版本信息"
    )
    group.add_argument(
        "-g",
        "--generate",
        action="store_true",
        help="生成密码字典"
    )
    group.add_argument(
        "-on",
        "--outputname",
        action="store",
        help="指定输出字典文件名",
        nargs=1,
    )
    group.add_argument(
        "-op",
        "--outputpath",
        action="store",
        help="指定输出字典路径",
    )
    group.add_argument(
        "-m",
        "--mode",
        action="store",
        help="指定模式，详见文档"
    )
    group.add_argument(
        "-l",
        "--level",
        action="store",
        help="指定生日拆分粒度，详见文档"
    )
    return parser

def show_version():
    """
    显示版本信息
    :return:
    """
    print(colorPrinter.wrong_text("[ 社工字典生成器 ]" + __version__))

def check_whippletree(birthday:list)->bool:
    """
    检查输入的生日是否合法
    :param birthday: 生日列表
    :return:返回输入的生日是否合法
    """
    if birthday[0] == "":
        return True
    for day in birthday:
        if "-" not in day:
            return False
    return True

def get_infomation():
    """
    与用户交互，获取信息
    :return: 以字典的形式返回用户输入的信息
    """
    profile = {}
    print("\r\n[+] 请按照提示输入相关信息")
    print("[+] 如果某一项信息您不想添加，可以直接敲空格跳过，某项信息想输入多组可以用空格分隔\r\n")
    profile["victim_name"] = str(input(">姓名(拼音)")).split(" ")
    profile["nickname"] = str(input(">小名或别名(拼音)")).split(" ")
    birthday = str(input(">生日(请按照年-月-日的格式输入，如：2000-1-1或2000-01-01)")).split(" ")
    while not check_whippletree(birthday):
        print(colorPrinter.wrong_text("[-] 您输入的格式有误，请重新输入"))
        birthday = str(input(">生日(请按照年-月-日的格式输入，如：2000-1-1或2000-01-01)")).split(" ")
    profile["birthday"] = birthday

    profile["relative_name"] = str(input(">亲人姓名(父母公婆儿女七大姑八大姨的都可以写在这里，注意用空格分隔)")).split(" ")
    relative_birthday = str(input(">亲人生日(父母公婆儿女七大姑八大姨的都可以写在这里，注意用空格分隔)")).split(" ")
    while not check_whippletree(relative_birthday):
        print(colorPrinter.wrong_text("[-] 您输入的格式有误，请重新输入"))
        relative_birthday = str(input(">亲人生日(父母公婆儿女七大姑八大姨的都可以写在这里，注意用空格分隔)")).split(" ")
    profile["relative_birthday"] = relative_birthday

    profile["pet"] = input(">宠物的名字 ").split(" ")
    profile["company"] = input(">公司或者学校 ").split(" ")

    profile["words"] = input(">想要添加的关键字 ").split(" ")
    return profile

def mix(list:list):
    """

    :param list:要进行排列组合的列表
    :return:排列组合后的结果
    """
    if len(list) <= 1:
        return list
    res_list = []
    for index in range(len(list)):
        temp_list = list[0:index]+list[index+1:]
        for item in mix(temp_list):
            res_list.append(list[index]+item)
    return res_list

def split_birthday(birthdays,level):
    """

    :param birthdays:生日列表
    :param level: 表示生日拆分粒度，默认是对年月日进行倒序排列，并对年缩写的情况进行排列，
    指定为1时，就是在默认的情况下加上单个的年月日，指定为2时就是在默认的情况下加上只对月日进行排列
    :return:可以直接用于排列组合的生日列表
    """

    res_list = []
    for birthday in birthdays:
        if birthday == "":
            res_list.append(birthday)
            break
        else:

            temp_list = birthday.split("-")
            full_list = temp_list
            full_year_fix_birthday = mix(temp_list)
            for i in temp_list:
                if len(i) == 4:
                    year = i
                    temp_list.remove(year)
                    if level == "2":
                        for i in mix(temp_list):
                            res_list.append(i)
                    temp_list.append(year[-2:])
                    simple_year_fix_birthday = mix(temp_list)
                    for i in simple_year_fix_birthday:
                        res_list.append(i)

            for i in full_year_fix_birthday:
                res_list.append(i)
            if level == "1":
                for i in full_list:
                    res_list.append(i)

    return res_list

def simple_cycle_generate(profile):
    """
    根据用户输入信息进行排列组合（一般情况）
    :param profile: 用户输入的信息
    :return: 排列组合的结果
    """
    res_list = []
    for name in profile["victim_name"]:
        for nickname in profile["nickname"]:
            for birthday in profile["birthday"]:
                for relative_name in profile["relative_name"]:
                    for relative_birthday in profile["relative_birthday"]:
                        for pet in profile["pet"]:
                            for company in profile["company"]:
                                for word in profile["words"]:
                                    mix_list = []
                                    if name != "":
                                        mix_list.append(name)
                                    if nickname != "":
                                        mix_list.append(nickname)
                                    if birthday != "":
                                        birthday = birthday.replace("-", "")
                                        mix_list.append(birthday)
                                    if relative_name != "":
                                        mix_list.append(relative_name)
                                    if relative_birthday != "":
                                        relative_birthday = relative_birthday.replace("-", "")
                                        mix_list.append(relative_birthday)
                                    if company != "":
                                        mix_list.append(company)
                                    if pet != "":
                                        mix_list.append(pet)
                                    if word != "":
                                        mix_list.append(word)
                                    res_list.append(mix(mix_list))
    return res_list

def mixed_cycle_generate(profile):
    """
    根据用户输入信息进行排列组合（混编情况）
    :param profile: 用户输入的信息
    :return: 排列组合的结果
    """
    res_list = []
    mix_list = []
    for name in profile["victim_name"]:
        if name != "":
            mix_list.append(name)
    for nickname in profile["nickname"]:
        if nickname != "":
            mix_list.append(nickname)
    for birthday in profile["birthday"]:
        if birthday != "":
            birthday = birthday.replace("-", "")
            mix_list.append(birthday)
    for relative_name in profile["relative_name"]:
        if relative_name != "":
            mix_list.append(relative_name)
    for relative_birthday in profile["relative_birthday"]:
        if relative_birthday != "":
            relative_birthday = relative_birthday.replace("-", "")
            mix_list.append(relative_birthday)
    for pet in profile["pet"]:
        if pet != "":
            mix_list.append(pet)
    for company in profile["company"]:
        if company != "":
            mix_list.append(company)
    for word in profile["words"]:
        if word != "":
            mix_list.append(word)
    res_list.append(mix(mix_list))
    return res_list

def generate_dictionary(outputpath,outputname,mode,level):
    """
    生成字典
    :param outputpath: 输出路径
    :param outputname: 输出文件名
    :param mode: 模式
    :param level: 生日拆分粒度
    :return:
    """
    profile = get_infomation()
    start_time = time.time()
    res_list = []
    if level == None:
        level = 0
    if mode == "1":
        profile["birthday"] = split_birthday(profile["birthday"],level)
        profile["relative_birthday"] = split_birthday(profile["relative_birthday"],level)
        res_list = simple_cycle_generate(profile)
    elif mode == "2":
        res_list = mixed_cycle_generate(profile)
    elif mode == "3":
        profile["birthday"] = split_birthday(profile["birthday"],level)
        profile["relative_birthday"] = split_birthday(profile["relative_birthday"],level)
        res_list = mixed_cycle_generate(profile)
    else:
        res_list = simple_cycle_generate(profile)

    index = 1
    default_path = "../result/SocialEngineeringDictionaryGenerator/"

    if outputpath!=None:
        default_path = outputpath
        if default_path[-1] != "/":
            default_path += "/"

    if not os.path.exists(default_path):
        os.makedirs(default_path)

    if outputname==None:
        while(os.path.exists(default_path+str(index)+".txt")):
            index +=1
        full_path = default_path+str(index)+".txt"
    else:
        full_path = default_path+outputname[0]
    length = 0
    try:
        with open(full_path,"w") as f:
            for list in res_list:
                length += len(list)
                for password in list:
                    f.write(password+"\n")
        print("[+] 文件已经保存到 " + colorPrinter.wrong_text(os.path.abspath(full_path)))
        print("[+] 有 " + colorPrinter.wrong_text(str(length))+" 条")
        print("[+] 用时 "+colorPrinter.wrong_text(str(time.time()-start_time)) +" 秒")
    except:
        print(colorPrinter.wrong_text("[-] 文件写入失败，请检查路径和文件名以及是否有写入权限"))

def print_tool_info():
    print("[ yumueat | https://github.com/yumueat]")
    print("[ Social Engineering Dictionary Generator | https://github.com/yumueat/Penetration-test-toolkit]")

def main():
    parser = get_parser()
    args = parser.parse_args()
    print_tool_info()
    if args.version:
        show_version()
    elif args.generate:
        generate_dictionary(args.outputpath,args.outputname,args.mode,args.level)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
