# Linux

## 一、命令基础

### 1. 通用格式

```bash
command [-options] [parameter]
```

- command：命令本体，即命令本身
- options：可选选项，控制命令的行为细节
- parameter：可选参数，控制命令的指向目标

### 2. ls

```bash
ls [-a -l -h] [linux路径]
```

平铺显示当前工作目录内容

- `ls ~/workspaces/codes`: 显示这个路径下的所有内容
- `-a`: all，包括隐藏内容
- `-l`：以列表形式竖向展示，并展示更多信息
- `-h`：以更加人性化的方式展示文件的大小单位

### 3. mkdir

```bash
mkdir -p linux路径
```

- -p：一次性创建多个层级的目录

### 4. touch, cat, more

- `touch linux路径`：创建文件
- `cat linux路径`：查看文件内容
- `more linux路径`：查看文件内容，可翻页查看

### 5. cp, mv, rm

#### （1）cp

```bash
cp [-r] 参数1 参数2
```

- -r：可选，用于复制文件夹，表示迭代
- 参数1：被复制的文件
- 参数2：要复制去的地方

#### （2）mv

```bash
mv 参数1 参数2
```

- 参数1：被移动的文件或文件夹
- 参数2：要移动去的地方，如果目标不存在，则进行改名，确保目标存在

#### （3）rm

```bash
rm [-r -f] 参数1 参数2 ....参数n
```

- -r：用于删除文件夹
- -f：强制删除，force
- 参数1，参数2....参数n，要删除的文件或文件夹

### 6. which, find

#### （1）which

前面学习的linux命令，**它们的本体是一个个二进制可执行程序**，和windows中的.exe文件是一样的意思，可以通过which命令来查找命令的程序文件存放在哪里

```bash
which 要查找的命令
```

例如

```bash
[haojie@localhost ~]$ which cd
/usr/bin/cd
[haojie@localhost ~]$ which python
/usr/bin/python
```

#### （2）find

- 查找文件名

```bash
find 起始路径 -name "被查找文件名"
```

- 按照文件大小查找

```bash
# +，-表示大于和小于
# n表示大小数字
# kMG表示大小单位，k表示kb，M表示MB，G表示GB
find 起始路径 -size +|-n[kMG]
```

例如

```
find / size -10k # 查找小于10k的文件
find / size +20M # 查找大于20M的文件
```

### 7. grep, wc, 管道符

#### （1）grep

从文件中通过关键字过滤文件行 

```bash
grep [-n] 关键字 文件路径
```

- -n：在结果中显示匹配的行号
- 关键字：要过滤的关键字
- 文件路径：要过滤的文件路径，**可作为内容输入端口**

```bash
[haojie@localhost ~]$ grep "Haojie" test.txt
Haojie Shu is a python developer who works in DataGrand.
```

#### （2）wc

统计文件的行数，单词数等

```
wc [-c -m -l -w] 文件路径
```

- -c：统计bytes数量
- -m：统计字符数量
- -l：统计行数
- -w：统计单词数量

```bash
[haojie@localhost ~]$ wc test.txt 
  2  20 110 test.txt  # 2表示行数，20表示单词数，110表示字节数
```

#### （3）管道符(｜)

管道符｜作用：将管道符左边命令的结果，作为右边命令的输入

<img src="./assets/image-20230522095234080.png" alt="image-20230522095234080" style="zoom:70%;" />

任意只要能输出结果的都可以用管道符，管道符右边也可以用`wc`。例如可以通过下面的命令来统计路径下子文件的个数

```bash
[haojie@localhost ~]$ ls -l ~/workspace | wc -l
      10
```

此外任意的输出都可以使用`grep`来做过滤

```bash
[haojie@localhost ~]$ docker stack services idps-product-metal | grep predict
qtufjz1qkgl6   idps-product-metal_chapter_locating_predict             replicated   1/1        dockerhub.datagrand.com/idps/chapter_locating:release_ci_20221117_3ce18f3
nf4brcv01fxp   idps-product-metal_diff_extract_predict                 replicated   1/1        dockerhub.datagrand.com/idps/diff_extract:release_ci_20221117_360dd4d
```

### 8. echo, tail, 重定向符

#### （1）echo

输出制定内容，和print的功能类似

```bash
echo 要输出的内容
```

例如

```bash
echo Hello World. # 打印Hello World.
```

#### （2）反引号(``)

被反引号包围的内容，会被作为命令执行

```bash
echo pwd # 打印Hello World.
echo `pwd` # 打印/Users/shuhaojie
```

#### （3）重定向符(>,>>)

- `>`：将左边命令的结果，覆盖写入到符号右侧的文件中
- `>>`：将左边命令的结果，追加写入到符号右侧的文件中

```bash
echo "Hello World" > hello.txt # 覆盖
echo "Hello World" >> hello.txt # 追加
ls > hello.txt # 将ls的内容覆盖写入到文件中
```

#### （4）tail

查看文件尾部的内容，追踪文件的最新修改

```bash
# -f: 持续跟踪
# -num: 查看尾部多少行, 不指定默认10行
tail [-f -num] linux路径
```

### 9. vi编辑器

命令模式快捷键

```bash
0: 移动光标到当前行的开头
$(shift+4): 移动光标到当前行的结尾
yy: 复制当前行
p: 粘贴复制的内容
u: 撤销修改
gg: 跳到首行
G: 跳到尾行
```

底线模式快捷键

```
:set nu
```

## 二、linux用户

### 1. root用户

- `su`: switch user，切换用户。不仅仅可以切换到root用户，也可以切换到其他用户。

### 2. 用户和用户组

一个用户可以在多个组，一个组可以有多个用户

#### （1）用户组

```bash
groupadd 用户组 # 创建用户组
```

#### （2）用户

- 创建用户

```bash
# -g 表示加入哪个用户组，不指定的话，会自动加入同名用户组
# -d 创建home路径
useradd [-g -d]用户名
```

- 删除用户

```bash
# -r 删除home路径
userdel [-r] 用户名
```

- 查看用户

```bash
# 不指定表示查看自己
id [用户名]
```

- 修改用户所在组

```
usermod -aG 用户组 用户名
```

### 3. 权限













