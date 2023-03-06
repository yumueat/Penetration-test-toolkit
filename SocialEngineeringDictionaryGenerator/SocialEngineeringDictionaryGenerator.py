# -*- coding: utf-8 -*-
"""
@author yumu
@version 1.0.4
"""
import argparse

__version__ = "1.0.4"
import os.path
import time
from pathlib import Path

def get_parser():
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
    print("\r\n	\033[1;31m[ 社工字典生成器 ]  " + __version__ + "\033[1;m\r\n")

def check_whippletree(birthday:list)->bool:
    if birthday[0] == "":
        return True
    for day in birthday:
        if "-" not in day:
            return False
    return True

def get_infomation():
    profile = {}
    print("\r\n[+] 请按照提示输入相关信息")
    print("[+] 如果某一项信息您不想添加，可以直接敲空格跳过，某项信息想输入多组可以用空格分隔\r\n")
    profile["victim_name"] = str(input(">姓名(拼音)").lower()).split(" ")
    profile["nickname"] = str(input(">小名或别名(拼音)").lower()).split(" ")
    birthday = str(input(">生日(请按照年-月-日的格式输入，如：2000-1-1或2000-01-01)")).lower().split(" ")
    while not check_whippletree(birthday):
        print("\n\033[1;31m[-] 您输入的格式有误，请重新输入\033[1;m")
        birthday = str(input(">生日(请按照年-月-日的格式输入，如：2000-1-1或2000-01-01)")).lower().split(" ")
    profile["birthday"] = birthday

    profile["relative_name"] = str(input(">亲人姓名(父母公婆儿女七大姑八大姨的都可以写在这里，注意用空格分隔)").lower()).split(" ")
    relative_birthday = str(input(">亲人生日(父母公婆儿女七大姑八大姨的都可以写在这里，注意用空格分隔)")).lower().split(" ")
    while not check_whippletree(relative_birthday):
        print("\n\033[1;31m[-] 您输入的格式有误，请重新输入\033[1;m")
        relative_birthday = str(input(">亲人生日(父母公婆儿女七大姑八大姨的都可以写在这里，注意用空格分隔)")).lower().split(" ")
    profile["relative_birthday"] = relative_birthday

    profile["pet"] = input(">宠物的名字 ").lower().split(" ")
    profile["company"] = input(">公司或者学校 ").lower().split(" ")

    profile["words"] = input(">想要添加的关键字 ").lower().split(" ")
    return profile

def mix(list:list):
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
    with open(full_path,"w") as f:
        for list in res_list:
            length += len(list)
            for password in list:
                f.write(password+"\n")

    print("[+] 文件已经保存到 \033[1;31m" + os.path.abspath(full_path))
    print("\033[1;m[+] 有 \033[1;31m" + str(length)+"\033[1;m 条")
    print("[+] 用时 \033[1;31m" +str(time.time()-start_time) +"\033[1;m 秒")

def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.version:
        show_version()
    elif args.generate:
        generate_dictionary(args.outputpath,args.outputname,args.mode,args.level)
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
