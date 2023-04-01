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

# 网站目录扫描器

## 版本

+ 1.0.0 初始版本
+ 1.0.1 增加安静模式
+ 1.0.2 补充输出信息
+ 1.0.3 增加指定输出文件名和路径功能
+ 1.0.4 增加异常处理
+ 1.0.5 增加设置超时时间功能
+ 1.0.6 增加了几个内置字典
+ 1.0.7 调整代码结构
+ 1.0.8 增加探测403 3xx的功能

## 使用方法

```
用法: WebsiteDirectoryScanner.py [-h] [-v] [-s] [-u [URL ...]] [-l [LIST ...]] [-d [DIRECTORY ...]] [-m [MODE ...]] [-on OUTPUTNAME] [-op OUTPUTPATH] [-q] [-to TIMEOUT] [-a]

Website Directory Scanner

options:
  -h, --help            show this help message and exit

  -v, --version         显示版本信息
  -s, --scan            开始扫描
  -u [URL ...], --url [URL ...]
                        指定要扫描的url
  -l [LIST ...], --list [LIST ...]
                        指定要扫描的url的列表(文件)
  -d [DIRECTORY ...], --directory [DIRECTORY ...]
                        指定扫描字典
  -m [MODE ...], --mode [MODE ...]
                        选择模式（内置字典）
  -on OUTPUTNAME, --outputname OUTPUTNAME
                        指定输出结果文件名
  -op OUTPUTPATH, --outputpath OUTPUTPATH
                        指定输出结果路径
  -q, --quite           指定为安静模式，只输出200的url（如果指定探测403和3xx，则也会输出403和3xx的信息）
  -to TIMEOUT, --timeout TIMEOUT
                        指定超时时间
  -a, --add             探测403和3xx
```

### 文件格式

字典文件格式要求一行一个，示例如下

```
admin
admin_index
admin_admin
index_admin
GfEditor
index
EditBox
default
manage
```

url文件格式也要求一行一个，示例如下

```
http://127.0.0.1:5000
http://127.0.0.1:5000
http://127.0.0.1:5000
```

### 模式

模式其实就是选择字典，不同模式对应不同字典，字典可以多选，模式与字典的对应关系如下，具体可以直接打开查看

```
1 ASP
2 ASPX
3 DIR
4 JSP
5 MDB
6 PHP
```

### 举例

```
最简单版本，指定一个url，然后用默认的字典进行扫描
python .\WebsiteDirectoryScanner.py -s -u http://127.0.0.1:5000 -m 3
指定多个字典
python .\WebsiteDirectoryScanner.py -s -u http://127.0.0.1:5000 -m 1 2 3
指定一个url文件，然后用默认的字典进行扫描，并指定为安静模式
python .\WebsiteDirectoryScanner.py -s -l ./url.txt -m 3 -q
指定url文件和字典文件，并选择探测403和3xx，并开启安静模式
python .\WebsiteDirectoryScanner.py -s -l ./url.txt -d ./simple_dic.txt -q -a
```

![image-20230328181315859](C:\Users\yumu\AppData\Roaming\Typora\typora-user-images\image-20230328181315859.png)

# 爆破工具包

## Mysql爆破工具

### 版本

+ 1.0.0 初始版本

### 使用方法

```
用法: MysqlBruteForceAttackTool.py [-h] [-v] [-u URL] [-nd NAMEDIRECTORY] [-pd PASSWORDDIRECTORY] [-l LIST] [-q] [-b] [-p PORT]

Mysql Brute Force Attack Tool

optional arguments:
  -h, --help            show this help message and exit

  -v, --version         显示版本信息
  -u URL, --url URL     指定要爆破的主机
  -nd NAMEDIRECTORY, --namedirectory NAMEDIRECTORY
                        指定用户名爆破字典
  -pd PASSWORDDIRECTORY, --passworddirectory PASSWORDDIRECTORY
                        指定密码爆破字典
  -l LIST, --list LIST  指定要爆破的主机列表文件
  -q, --quite           安静模式，只输出成功的结果
  -b, --brute           开始爆破
  -p PORT, --port PORT  指定端口
```

#### 举例

简单爆破一下 `python .\MysqlBruteForceAttackTool.py -b `

如果没有指定端口、主机、用户名和密码字典，则会使用对应的默认值

![image-20230329141609140](C:\Users\yumu\AppData\Roaming\Typora\typora-user-images\image-20230329141609140.png)

全部指定` python .\MysqlBruteForceAttackTool.py -b -u 127.0.0.1 -p 3306 -nd ./simple_user.txt -pd ./simple_dic.txt`

![image-20230329142517745](C:\Users\yumu\AppData\Roaming\Typora\typora-user-images\image-20230329142517745.png)

安静模式 `python .\MysqlBruteForceAttackTool.py -b -q `

![image-20230329142601596](C:\Users\yumu\AppData\Roaming\Typora\typora-user-images\image-20230329142601596.png)

### 使用贴士

+ 如果主机，用户名，密码都指定了多个，那么再爆破的时候会按照主机--用户名--密码的顺序进行爆破，也就是说会先对一个主机进行爆破，然后去爆破其他的主机，在爆破一个主机的时候会先对一个用户名进行爆破，之后才回去爆破其他的用户名。

+ 关于主机和用户名的列表文件以及密码字典文件的格式，在前面的工具中提到过，这里就不再赘述
