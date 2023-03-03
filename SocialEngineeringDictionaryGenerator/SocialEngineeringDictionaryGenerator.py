# -*- coding: utf-8 -*-
"""
@author yumu
"""
import argparse

__version__ = "1.0.0"
__start_time__ = 0
import os.path
import time
from pathlib import Path

def get_parser():
    parser = argparse.ArgumentParser(description="Social Engineering Dictionary Generator")
    group = parser.add_mutually_exclusive_group(required=False)
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
    return parser

def show_version():
    print("\r\n	\033[1;31m[ SEDG ]  " + __version__ + "\033[1;m\r\n")

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

def generate_dictionary():
    global __start_time__
    profile = get_infomation()
    __start_time__ = time.time()
    res_list = []
    # 对生日和名字进行预处理（符合中国人习惯）
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
                                        mix_list.append(birthday)
                                    if relative_name != "":
                                        mix_list.append(relative_name)
                                    if relative_birthday != "":
                                        mix_list.append(relative_birthday)
                                    if company != "":
                                        mix_list.append(company)
                                    if pet != "":
                                        mix_list.append(pet)
                                    if word != "":
                                        mix_list.append(word)
                                    res_list.append(mix(mix_list))

    index = 1
    while(os.path.exists("../result/SocialEngineeringDictionaryGenerator/"+str(index)+".txt")):
        index +=1

    if not os.path.exists("../result/SocialEngineeringDictionaryGenerator/"):
        os.makedirs("../result/SocialEngineeringDictionaryGenerator/")

    length = 0
    filename = str(index)+".txt"
    with open("../result/SocialEngineeringDictionaryGenerator/"+filename,"w") as f:
        for list in res_list:
            length += len(list)
            for password in list:
                f.write(password+"\n")

    print("[+] 文件已经保存到 \033[1;31m" + str(Path.cwd().parent) + "\\result\\SocialEngineeringDictionaryGenerator\\"+filename)
    print("\033[1;m[+] 有 \033[1;31m" + str(length)+"\033[1;m 条")
    print("[+] 用时 \033[1;31m" +str(time.time()-__start_time__) +"\033[1;m 秒")

def main():
    parser = get_parser()
    args = parser.parse_args()
    if args.version:
        show_version()
    elif args.generate:
        generate_dictionary()
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
