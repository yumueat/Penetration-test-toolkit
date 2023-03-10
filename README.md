# 项目介绍

这个项目中包含了一些渗透测试工作中会用到的工具：包括但不限于：

+ 社会工程学字典生成器

# 社会工程学字典生成器

## 版本

+ 1.0.0 初始版本
+ 1.0.1 优化信息显示
+ 1.0.2 支持指定输出字典名和路径
+ 1.0.3 支持不同模式（生日拆分模式，混编模式）
+ 1.0.5 增加异常处理
+ 1.0.6 优化代码结构
+ 1.0.7 修改功能性bug
+ 1.0.8 修改输出颜色

## 使用方法

```
用法: SocialEngineeringDictionaryGenerator.py [-h] [-v] [-g] [-on OUTPUTNAME] [-op OUTPUTPATH] [-m MODE] [-l LEVEL]

Social Engineering Dictionary Generator

options:
  -h, --help            显示帮助信息

  -v, --version         显示版本信息
  -g, --generate        生成密码字典
  -on OUTPUTNAME, --outputname OUTPUTNAME
                        指定输出字典文件名
  -op OUTPUTPATH, --outputpath OUTPUTPATH
                        指定输出字典路径
  -m MODE, --mode MODE  指定模式，详见文档
  -l LEVEL, --level LEVEL
                        指定生日拆分粒度，详见文档
```

### 模式

```
1 生日拆分模式，正常情况下是把生日作为一个组合进行排列组合，比如19991003，但是实际上很多人在密码中并不一定会这样写生日，可能会写为991003或者1003（只写年或者只写月和日），这时就可以使用生日拆分模式，具体拆分方式见下面的粒度文档
2 混编模式，正常情况下是对同一个信息的不同值依次进行排列组合，比如名字叫king 动物有cat 和 dog ，正常情况下是king和cat先进行排列组合，然后king和dog进行排列组合，密码中不会出现cat 和 dog的组合，使用混编模式后，就会对同一个信息的不同值进行排列组合，在这个例子中就会出现kingcatdog的组合
3 混编 + 生日拆分模式
不指定就是默认，默认就是上面说的正常情况
```

### 生日拆分粒度

```
不指定就是默认（所谓的默认是在生日拆分模式下的默认，也就是说mode需要指定为1或者3，不指定mode为生日拆分模式的时候生日不会拆分，输入1996-10-03就是19961003），默认情况举例如下输入1996-10-03将会被拆分为
100396
109603
031096
039610
961003
960310
19961003
19960310
10199603
10031996
03199610
03101996
当然，考虑到基本的拆分可能有些情况不能覆盖，我还提供了更高粒度的拆分
1 在默认的情况下加上单个的年月日 如 在上面例子的基础上加上 1996 10 03 
2 在默认的情况下加上只对月日进行排列 如 在上面例子的基础上加上 1003 0310
```

### 举例

一般的情况

![image-20230308123755990](C:\Users\yumu\AppData\Roaming\Typora\typora-user-images\image-20230308123755990.png)

全部参数加上

![image-20230308124123870](C:\Users\yumu\AppData\Roaming\Typora\typora-user-images\image-20230308124123870.png)

## 使用贴士

+ 如果希望排列组合的生日里面没有0，那就在写的时候不要写0，如1996-09-03就可以写成1996-9-3
+ 有些密码要求大小写字母都要有，如果希望列出有大写字母存在的情况，那就在输入的时候就写大写字母(希望哪个字母是大写的就在输入的时候把哪个字母大写)，比如Password或PASSWORD
+ 有些密码要求要有特殊字符（数字同理），如果希望列出有特殊字符的情况，可以在最后的关键字那里加
+ 总之就是要灵活的利用这些功能
