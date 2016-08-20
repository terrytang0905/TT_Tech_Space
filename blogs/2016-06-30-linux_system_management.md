---
layout: post
category : guide
tags : [development,os]
title: Linux System Management Guide
---

#### A.常用的shell命令

    uname -a 查看内核版本/
    lsb_release -a 查看OS版本
    ls -al 显示所有文件的属性
    pwd 显示当前路径
    cd - 返回上一次目录 cd ~ 返回主目录
    date s 设置时间、日期
    cal 显示日历 cal 2006
    bc 计算器具
    man & info 帮助手册
    locale 显示当前字体 locale -a 所有可用字体 /etc/sysconfig/i18n设置文件
    LANG=en 使用英文字体
    sync 将数据同步写入硬盘
    shutdown -h now & half & poweroff 关机
    reboot 重启
    startx & init 5 进入图形介面
    /work & ?work 向上、下查找文档内容
    chgrp 改变档案群组 chgrp testing install.log
    chown 改变所属人/组 chown root:root install.log /chown -R couchbase:couchbase couchbase
    chmod 改变文件属性 chmod 777 install.log read=4 write=2 execute=1
    cp 复制 cp filename
    rm 删除文件
    rm -rf filename 强制删除文件夹及文件
    rename 字符串1 字符串2 文件名
    rmdir 删除文件夹
    mv 移动 mv 123.txt 222.txt 重命名
    mkdir 创建文件夹
    touch 创建文件 更新当前时间
    cat 由第一行开始显示 cat |more 分页
    nl 在内容前加行号
    more & less 一面一面翻动
    head -n filename 显示第N行内容
    tail -n filename 显示后N行内容
    od 显示非纯文档
    whereis 查找命令
    locate 查找
    find 查找 find / -name "***.***"
    which 查看工具
    ln 硬链接
    ln -s 软件链接
    sudo clock —hctosys 设置系统时间

    whoami 显示当前用户 who 所有用户
    gcc -v 查看GCC版本
    chattr +i filename 禁止删除 chattr -i filename 取消禁止
    lsattr 显示隐藏档属性
    updatedb 更新资料库

    alias 显示当前所有的命令别名
    alias lm="ls -al" 命令别名
    unalias lm 取消命令别名
    type 类似which
    bash 进入子程序

    PS1='[\u@\h \w \A #\#]\$ ' 提示字元的設定
    read [-pt] variable -----------读取键盘输入的变量
    參數：-p ：後面可以接提示字元
         -t ：後面可以接等待的seconds

    declare 声明 shell 变量
    set 设置SHELL
    ulimit -a 显示所有限制资料
    ulimit -n 显示打开文件上限
    ls /tmp/yang && echo "exist" || echo "not exist"
    意思是說，當 ls /tmp/yang 執行後，若正確，就執行echo "exist" ,若有問題，就執行echo "not exist"
    last | grep 'root' 搜索有root的一行,加[-v]反向搜索
    cat /etc/passwd | sort 排序显示
    cat /etc/passwd | wc 显示『行、字数、字节数』正规表示法

    ifconfig 显示或设置网络设备
    service network {start/stop/restart/reload/status}
    ifdown eth0 关闭网卡
    ifup eth0 开启网卡
    netstat 显示网络状态
    netstat -tulnp------>找出目前系統上已在監聽的網路連線及其PID
    netstat –nat -----查询Active Internet Connection
    service iptables start/stop 开启/关闭防火墙

    开启：service iptables start
    关闭：service iptables stop

    clear 清屏
    history 历史记录 !55 执行第55个指令
    stty 设置终端 stty -a
    fdisk /mbr 删除GRUB
    at 僅進行一次的Schedule Task
    crontab 循環執行的例行性命令 [e]编辑,[l]显示,[r]删除任务

_grep_

    grep [-acinv] '搜尋正则表达式字串' filename
    參數說明：-a ：將 binary 檔案以 text 檔案的方式搜尋資料
             -c ：計算找到 '搜尋字串' 的次數
             -i ：忽略大小寫的不同，所以大小寫視為相同
             -n ：順便輸出行號
             -v ：反向選擇，亦即顯示出沒有 '搜尋字串' 內容的那一行！
    grep -n 'the' 123.txt 搜索the字符 -----------搜尋特定字串
    grep -n 't[ea]st' 123.txt 搜索test或taste两个字符---------利用 [] 來搜尋集合字元
    grep -n '[^g]oo' 123.txt 搜索前面不为g的oo-----------向選擇 [^]
    grep -n '[0-9]' 123.txt 搜索有0-9的数字
    grep -n '^the' 123.txt 搜索以the为行首-----------行首搜索^
    grep -n '^[^a-zA-Z]' 123.txt 搜索不以英文字母开头
    grep -n '[a-z]$' 123.txt 搜索以a-z结尾的行---------- 行尾搜索$
    grep -n 'g..d' 123.txt 搜索开头g结尾d字符----------任意一個字元 .
    grep -n 'ooo*' 123.txt 搜索至少有两个oo的字符---------重複字元 *
    sed 文本流编辑器 利用脚本命令来处理文本文件
    awd 模式扫描和处理语言
    nl 123.txt | sed '2,5d' 删除第二到第五行的内容
    diff 比较文件的差异
    cmp 比较两个文件是否有差异
    patch 修补文件
    pr 要打印的文件格式化

_vi一般用法:_

    一般模式 编辑模式 指令模式
    h 左 a,i,r,o,A,I,R,O :w 保存
    j 下 进入编辑模式 :w! 强制保存
    k 上 dd 删除光标当前行 :q! 不保存离开
    l 右 ndd 删除n行 :wq! 保存后离开
    0 移动到行首 yy 复制当前行 :e! 还原原始档
    $ 移动到行尾 nyy 复制n行 :w filename 另存为
    H 屏幕最上 p,P 粘贴 :set nu 设置行号
    M 屏幕中央 u 撤消 :set nonu 取消行号
    L 屏幕最下 [Ctrl]+r 重做上一个动作 ZZ 保存离开
    [shift] + G 档案最后一行
    [ctrl]+z 暂停退出 :set nohlsearch 永久地关闭高亮显示
    /work 向下搜索 :sp 同时打开两个文档
    ?work 向上搜索 [Ctrl]+w 两个文档设换
    gg 移动到档案第一行 :nohlsearch 暂时关闭高亮显示

_帐号管理_

    /etc/passwd 系统帐号信息
    /etc/shadow 帐号密码信息 经MD5 32位加密
    在密码栏前面加『 * 』『 ! 』禁止使用某帐号
    /etc/group 系统群组信息
    /etc/gshadow
    newgrp 改变登陆组
    useradd & adduser 建立新用户 ---------> useradd -m test 自动建立用户的登入目录
    useradd -m -g pgroup test --------->指定所属级
    /etc/default/useradd 相关设定
    /etc/login.defs UID/GID 有關的設定
    passwd 更改密码 -----------> passwd test
    usermod 修改用户帐号
    userdel 删除帐号 ----------->userdel -r test
    chsh 更换登陆系统时使用的SHELL [-l]显示可用的SHELL;[-s]修改自己的SHELL
    chfn 改变finger指令显示的信息
    finger 查找并显示用户信息
    id 显示用户的ID -----------> id test
    groupadd 添加组
    groupmod 与usermod类似
    groupdel 删除组
    su - test 更改用户 su - 进入root,且使用root的环境变量
    sudo 以其他身份来执行指令 –u username /-k kill /-e edit file
    visudo 编辑/etc/sudoers 加入一行『 test ALL=(ALL) ALL 』
    %wheel ALL = (ALL) ALL 系统里所有wheel群组的用户都可用sudo
    %wheel ALL = (ALL) NOPASSWD: ALL wheel群组所有用户都不用密码NOPASSWD
    User_Alias ADMPW = vbird, dmtsai, vbird1, vbird3 加入ADMPW组
    ADMPW ALL = NOPASSWD: !/usr/bin/passwd, /usr/bin/passwd [A-Za-z]*, \
    !/usr/bin/passwd root 可以更改使用者密码,但不能更改root密码 (在指令前面加入 ! 代表不可)
    PAM (Pluggable Authentication Modules, 嵌入式模組)
    who & w 看谁在线
    last 最近登陆主机的信息
    lastlog 最近登入的時間 读取 /var/log/lastlog
    talk 与其他用户交谈
    write 发送信息 write test [ctrl]+d 发送
    mesg 设置终端机的写入权限 mesg n 禁止接收 mesg y
    wall 向所有用户发送信息 wall this is q test
    mail 写mail
    /etc/default/useradd 家目录默认设置

_其他_

    1.Error: /bin/sh^M: bad interpreter: No such file or directory.
    Solution:dos2unix (The software is used to convert file to unix format)

#### B.Linux环境变量设置

  1.总结背景

    > 在linux系统下，如果你下载并安装了应用程序，很有可能在键入它的名称时出现“command not found”的提示内容。如果每次都到安装目标文件夹内，找到可执行文件来进行操作就太繁琐了。这涉及到环境变量PATH的设置问题，而PATH的设置也是在linux下定制环境变量的一个组成部分。
    > Linux是一个多用户的操作系统。每个用户登录系统后，都会有一个专用的运行环境。通常每个用户默认的环境都是相同的，这个默认环境实际上就是一组环境变量的定义。用户可以对自己的运行环境进行定制，其方法就是修改相应的系统环境变量。

  2、设置环境变量
    
    > 环境变量是和Shell紧密相关的，用户登录系统后就启动了一个Shell。对于Linux来说一般是bash，但也可以重新设定或切换到其它的Shell（使用chsh命令）。
    > 根据发行版本的情况，bash有两个基本的系统级配置文件：/etc/bashrc和/etc/profile。这些配置文件包含两组不同的变量：shell变量和环境变量。前者只是在特定的shell中固定（如bash），后者在不同shell中固定。很明显，shell变量是局部的，而环境变量是全局的。环境变量是通过Shell命令来设置的，设置好的环境变量又可以被所有当前用户所运行的程序所使用。对于bash这个Shell程序来说，可以通过变量名来访问相应的环境变量，通过export来设置环境变量。

    > 按变量的生存周期来划分，Linux变量可分为两类：
    > a.永久的：需要修改配置文件，变量永久生效。
    > b.临时的：使用export命令行声明即可，变量在关闭shell时失效。
    > 注：Linux的环境变量名称一般使用大写字母

c.使用命令echo显示环境变量
本例使用echo显示常见的变量HOME
$ echo $HOME
/home/kevin
d.设置一个新的环境变量
$ export MYNAME=”my name is kevin”
$ echo $ MYNAME
my name is Kevin
e.修改已存在的环境变量
接上个示例
$ MYNAME=”change name to jack”
$ echo $MYNAME
change name to jack
f.使用env命令显示所有的环境变量
$ env
HOSTNAME=localhost.localdomain
SHELL=/bin/bash
TERM=xterm
HISTSIZE=1000
SSH_CLIENT=192.168.136.151 1740 22
QTDIR=/usr/lib/qt-3.1
SSH_TTY=/dev/pts/0
……
g.使用set命令显示所有本地定义的Shell变量
$ set  asd
BASH=/bin/bash
BASH_ENV=/root/.bashrc
……

f.使用unset命令来清除环境变量
$ export TEMP_KEVIN=”kevin”     #增加一个环境变量TEMP_KEVIN
$ env | grep TEMP_KEVIN          #查看环境变量TEMP_KEVIN是否生效（存在即生效）
TEMP_KEVIN=kevin #证明环境变量TEMP_KEVIN已经存在
$ unset TEMP_KEVIN            #删除环境变量TEMP_KEVIN
$ env | grep TEMP_KEVIN       #查看环境变量TEMP_KEVIN是否被删除，没有输出显示，证明TEMP_KEVIN被清除了。

g.使用readonly命令设置只读变量
注：如果使用了readonly命令的话，变量就不可以被修改或清除了。
$ export TEMP_KEVIN ="kevin"      #增加一个环境变量TEMP_KEVIN
$ readonly TEMP_KEVIN                  #将环境变量TEMP_KEVIN设为只读
$ env | grep TEMP_KEVIN          #查看环境变量TEMP_KEVIN是否生效
TEMP_KEVIN=kevin        #证明环境变量TEMP_KEVIN已经存在
$ unset TEMP_KEVIN          #会提示此变量只读不能被删除
-bash: unset: TEMP_KEVIN: cannot unset: readonly variable
$ TEMP_KEVIN ="tom"        #修改变量值为tom会提示此变量只读不能被修改
-bash: TEMP_KEVIN: readonly variable

h.设置环境变量的三种方法

env 列出所有环境变量
export 设置或显示环境变量
export PATH="$PATH":/sbin 添加/sbin入PATH路
name=yang 设定变量
unset name 取消变量
myname="$name its me" & myname='$name its me' 单引号时$name失去变量内容
ciw=/etc/sysconfig/network-scripts/ 设置路径
echo $PATH 显示PATH路径
echo $name 显示变量的内容
echo $RANDOM 显示随意产生的数
echo $PATH | cut -d ':' -f 5 以:为分隔符,读取第5段内容
export | cut -c 10-20 读取第10到20个字节的内容

 a). 在/etc/profile文件中添加变量(对所有用户永久生效)
用VI在文件/etc/profile文件中增加变量，该变量将会对Linux下所有用户有效，并且是“永久的”。
# vi /etc/profile
unset i
unset pathmunge

JAVA_HOME=/home/download/jdk1.6.0_27
export JAVA_HOME
ANT_HOME=/home/download/apache-ant-1.8.2
export ANT_HOME
PATH=$JAVA_HOME/bin:$ANT_HOME/bin:$PATH
export PATH
CLASSPATH=.:$JAVA_HOME/lib:$JAVA_HOME/jre/lib
export CLASSPATH
#. /etc/profile 修改立即生效
注：修改文件后要想马上生效还要运行# source /etc/profile不然只能在下次重启此用户时生效。
 b). 在用户目录下的 /home/user/.bashrc or /root/.bashrc/ or /home/user/.bash_profile 文件中增加变量(对单一用户永久生效)
用VI在用户目录下的.bash_profile文件中增加变量，改变量仅会对当前用户有效,是“永久的”。
例如：编辑guok用户目录（/home/guok）下的.bash_profile
$ vi /home/guok/.bash_profile
添加如下内容：
export CLASSPATH=./JAVA_HOME/lib;$JAVA_HOME/jre/lib
注：修改文件后要想马上生效还要运行$ source /home/guok/.bash_profile不然只能在下次重进此用户时生效。
 c). 直接运行export命令定义变量(只对当前shell（BASH）session有效)
在shell的命令行下直接使用[export变量名=变量值]定义变量，该变量只在当前的shell（BASH）或其子shell（BASH）下是有效的，shell关闭了，变量也就失效了，再打开新shell时就没有这个变量，需要使用的话还需要重新定义

3. source命令用法

source FileName
作用:在当前bash环境下读取并执行FileName中的命令。
注：该命令通常用命令“.”来替代。
如：source .bash_rc 与 . .bash_rc 是等效的。

source命令(从 C Shell 而来)是bash shell的内置命令。
点命令，就是个点符号，(从Bourne Shell而来)是source的另一名称。
同样的，当前脚本中配置的变量也将作为脚本的环境，source(或点)命令通常用于重新执行刚修改的初始化文档，如 .bash_profile 和 .profile 等等。例如，假如在登录后对 .bash_profile 中的 EDITER 和TERM 变量做了修改，则能够用source命令重新执行 .bash_profile 中的命令而不用注销并重新登录。
比如您在一个脚本里export $KKK=111 ,假如您用./a.sh执行该脚本，执行完毕后，您运行 echo $KKK,发现没有值，假如您用source来执行 ，然后再echo,就会发现KKK=111。因为调用./a.sh来执行shell是在一个子shell里运行的，所以执行后，结构并没有反应到父shell里，但是
source不同点命令，就是在本shell中执行的，所以能够看到结果


##### Linux安装命令：

./configure 检查系统信息
./configure --help | more 帮助信息
make clean 清除之前留下的文件
make 编译
make install 安装
alternatives --install /usr/bin/java java /home/software/JDK/bin/java 300

rpm
rpm -q ----->查询是否安装 rpm -ql ------>查询该套件所有的目录
rpm -qi ----->查询套件的说明资料 rpm -qc[d] ----->设定档与说明档
rpm -ivh ---->安装 rpm -V -------->查看套件有否更动过
rpm -e ------>删除 rpm -Uvh ------->升级安装
--nodeps ----->强行安装 --test ----->测试安装

Linux应用创建快捷方式
/usr/bin/mongo
touch /usr/bin/eclipse
chmod 755 /usr/bin/eclipse
gedit /usr/bin/eclipse

添加应用初始化service
/etc/init.d/XXX


#### C.解压命令：

    *.Z compress 程式壓縮的檔案；
    *.bz2 bzip2 程式壓縮的檔案；
    *.gz gzip 程式壓縮的檔案；
    *.tar tar 程式打包的資料，並沒有壓縮過；
    *.tar.gz tar 程式打包的檔案，其中並且經過 gzip 的壓縮
    compress filename 压缩文件 加[-d]解压 uncompress
    gzip filename 压缩 加[-d]解压 zcat 123.gz 查看压缩文件内容
    bzip2 -z filename 压缩 加[-d]解压 bzcat filename.bz2 查看压缩文件内容
    tar xvfz myfile.tar.bz2
    x 是解压
    v 是复杂输出
    f 是指定文件
    z gz格式
    tar -cvf /home/123.tar /etc 打包，不压缩
    tar -xvf 123.tar 解开包
    tar -zxvf /home/123.tar.gz 以gzip解压
    tar zxvf a.tgz -C ./test
    tar -jxvf /home/123.tar.bz2 以bzip2解压
    tar -ztvf /tmp/etc.tar.gz 查看tar内容
    cpio -covB > [file|device] 份份
    cpio -icduv < [file|device] 还原

    Example：
    把/usr目录并包括它的子目录在内的全部文件做一备份，备份文件名为usr.tar
    tar cvf usr.tar /home
    把/usr 目录内的全部文件做一备份并进行压缩，备份文件名usr.tar.gz
    tar czvf usr.tar.gz /usr
    压缩一组文件，文件的后缀为tar.gz
    #tar cvf back.tar /back/
    #gzip -q back.tar
    or
    #tar cvfz back.tar.gz /back/
    释放一个后缀为tar.gz的文件。
    #tar zxvf back.tar.gz
    #gzip back.tar.gz
    #tar xvf back.tar

    1.以.a为扩展名的文件:
    #tar xv file.a
    2.以.z为扩展名的文件:
    #uncompress file.Z
    3.以.gz为扩展名的文件:
    #gunzip file.gz
    4.以.bz2为扩展名的文件:
    #bunzip2 file.bz2
    5.以.tar.Z为扩展名的文件:
    #tar xvZf file.tar.Z
    或 #compress -dc file.tar.Z | tar xvf -
    6.以.tar.gz/.tgz为扩展名的文件:
    #tar xvzf file.tar.gz
    或 gzip -dc file.tar.gz | tar xvf -
    7.以.tar.bz2为扩展名的文件:
    #tar xvIf file.tar.bz2
    或 bzip2 -dc file.tar.bz2 | xvf -
    8.以.cpio.gz/.cgz为扩展名的文件:
    #gzip -dc file.cgz | cpio -div
    9.以.cpio/cpio为扩展名的文件:
    #cpio -div file.cpio
    或cpio -divc file.cpio
    10.以.rpm为扩展名的文件安装:
    #rpm -i file.rpm
    11.以.rpm为扩展名的文件解压缩：
    #rpm2cpio file.rpm | cpio -div
    12.以.deb为扩展名的文件安装：
    #dpkg -i file.deb
    13.以.deb为扩展名的文件解压缩:
    #dpkg-deb --fsys-tarfile file.deb | tar xvf - ar p
    file.deb data.tar.gz | tar xvzf -
    14.以.zip为扩展名的文件:
    #unzip file.zip
    在linux下解压Winzip格式的文件
    　　要是装了jdk的话，可以用jar命令；还可以使用unzip命令。
    直接解压.tar.gz文件
    　　xxxx.tar.gz文件使用tar带zxvf参数，可以一次解压开。XXXX为文件名。 例如：
    $tar zxvf xxxx.tar.gz 各种压缩文件的解压（安装方法）

    文件扩展名 解压
    .a ar xv file.a
    .Z uncompress file.Z
    .gz gunzip file.gz
    .bz2 bunzip2 file.bz2
    .tar.Z tar xvZf file.tar.Z
    compress -dc file.tar.Z | tar xvf -
    .tar.gz/.tgz tar xvzf file.tar.gz
    gzip -dc file.tar.gz | tar xvf -
    .tar.bz2 tar xvIf file.tar.bz2
    bzip2 -dc file.tar.bz2 | xvf -
    .cpio.gz/.cgz gzip -dc file.cgz | cpio -div
    .cpio/cpio cpio -div file.cpio
    cpio -divc file.cpio
    .rpm/install rpm -i file.rpm
    .rpm/extract rpm2cpio file.rpm | cpio -div
    .deb/install dpkg -i file.deb
    .deb/exrtact dpkg-deb --fsys-tarfile file.deb | tar xvf -
    ar p file.deb data.tar.gz | tar xvzf -
    .zip unzip file.zip
    bzip2 -d myfile.tar.bz2 | tar xvf

    gzip
    gzip[选项]要压缩（或解压缩）的文件名
    -c将输出写到标准输出上，并保留原有文件。
    -d将压缩文件压缩。
    -l对每个压缩文件，显示下列字段：压缩文件的大小，未压缩文件的大小、压缩比、未压缩文件的名字
    -r递归式地查找指定目录并压缩或压缩其中的所有文件。
    -t测试压缩文件是正完整。
    -v对每一个压缩和解压缩的文件，显示其文件名和压缩比。
    -num-用指定的数字调整压缩的速度。


#### D.Linux磁盘文件管理

quota 显示磁盘已使用的空间与限制
quota -guvs ----->秀出目前 root 自己的 quota 限制值
quota -vu 查询
quotacheck 检查磁盘的使用空间与限制 quotacheck -avug ----->將所有的在 /etc/mtab 內，含有 quota 支援的 partition 進行掃瞄
[-m] 强制扫描
quota一定要是独立的分区,要有quota.user和quota.group两件文件,在/etc/fstab添加一句:
/dev/hda3 /home ext3 defaults,usrquota,grpquota 1 2
chmod 600 quota* 设置完成,重启生效
edquota 编辑用户或群组的quota [u]用户,[g]群组,[p]复制,[t]设置宽限期限
edquota -a yang edquota -p yang -u young ----->复制
quotaon 开启磁盘空间限制 quotaon -auvg -------->啟動所有的具有 quota 的 filesystem
quotaoff 关闭磁盘空间限制 quotaoff -a -------->關閉了 quota 的限制
repquota -av 查閱系統內所有的具有 quota 的 filesystem 的限值狀態

Quota 從開始準備 filesystem 的支援到整個設定結束的主要的步驟大概是：
1、設定 partition 的 filesystem 支援 quota 參數：
由於 quota 必須要讓 partition 上面的 filesystem 支援才行，一般來說， 支援度最好的是 ext2/ext3 ，
其他的 filesystem 類型鳥哥我是沒有試過啦！ 啟動 filesystem 支援 quota 最簡單就是編輯 /etc/fstab ，
使得準備要開放的 quota 磁碟可以支援 quota 囉；
2、建立 quota 記錄檔：
剛剛前面講過，整個 quota 進行磁碟限制值記錄的檔案是 aquota.user/aquota.group，
要建立這兩個檔案就必須要先利用 quotacheck 掃瞄才行喔！
3、編輯 quota 限制值資料：
再來就是使用 edquota 來編輯每個使用者或群組的可使用空間囉；
4、重新掃瞄與啟動 quota ：
設定好 quota 之後，建議可以再進行一次 quotacheck ，然後再以 quotaon 來啟動吧！

Disk 查询
df -h 显示分区空间(数据块大小)
df -i 显示index分区空间
du 显示目录或文件的大小
du -h //显示文件夹及文件大小
du -sh  // -s指定目录下不显示子目录或文件大小
du -sh * // 指定目录下文件或目录大小

fdisk 分区设置 fdisk -l /dev/hda 显示硬盘分区状态
mkfs 建立各种文件系统 mkfs -t ext3 /dev/ram15
fsck 检查和修复LINUX档案
Disk setting

/etc/fstab
ls -l /dev/disk/by-uuid/
blkid /dev/sdb2

mke2fs 格式化 mkfs -t ext3
dd if=/etc/passwd of=/tmp/passwd.bak 备份

mount 列出系统所有的分区
mount -t iso9660 /dev/cdrom /mnt/cdrom 挂载光盘
mount -t vfat /dev/fd0 /mnt/floppy 挂载软盘
mount -t vfat -o iocharset=utf8,umask=000 /dev/hda2 /mnt/hda2 挂载fat32分区
mount -t ntfs -o nls=utf8,umask=000 /dev/hda3 /mnt/hda3 挂载ntfs分区
mount -t cifs //<MachineName>/<SharedFolder> /mnt/Shared -o username=  <DomainName>/<username>,password=<password>
mount //10.32.122.151/team /mnt/builds 挂载shared folder分区
mount -t nfs -o rw bajie.lss.emc.com:/nfs/backup_mysql /mnt/bajie/ 挂载NFS分区
umount /mnt/hda3 缷载device
转移disk 绑定的路径
sudo umount /media/Dev
sudo mount /dev/sda2 /home
Linux-NTFS File System Project:http://www.tuxera.com/

#### E.Linux系统调试

& 后台运行程序
Example: tar -zxvf 123.tar.gz & --------->后台运行
Example2: command  >out.file 2>&1 & (1 is stdout. 2 is stderr.)

In a unix shell, if I want to combine stderr and stdout into the stdout stream for further manipulation, I can append the following on the end of my command:
2>&1

jobs观看后台暂停的程序 jobs -l
fg 将后台程序调到前台 fg n ------>n是数字,可以指定进行那个程序
bg 让工作在后台运行
一。& 最经常被用到

   这个用在一个命令的最后，可以把这个命令放到后台执行
二。ctrl + z
     可以将一个正在前台执行的命令放到后台，并且暂停
      ctrl + c
      前台进程的终止
三。jobs
     查看当前有多少在后台运行的命令
四。fg （Foreground）
     将后台中的命令调至前台继续运行
   如果后台中有多个命令，可以用 fg %jobnumber将选中的命令调出，%jobnumber是通过jobs命令查到的后台正在执行的命令的序号(不是pid)
五。bg（Background）
     将一个在后台暂停的命令，变成继续执行
   如果后台中有多个命令，可以用bg %jobnumber将选中的命令调出，%jobnumber是通过jobs命令查到的后台正在执行的命令的序号(不是pid)

ps aux 查看后台程序:
     Example: ps -ef|grep java
     Example2: 查看port:  ps -aux|grep 11311

top 查看后台程序
     Example: top -d 2 每两秒更新一次
     Example: top -d 2 -p10604 观看某个PID
    Example: top -b -n 2 > /tmp/top.txt ----->將 top 的資訊進行 2 次，然後將結果輸出到  /tmp/top.txt
    Example:  top -b -n $sampleNUMs -d $interval  >> $logdir/top.log &

pstree 以树状图显示程序 [A]以 ASCII 來連接, [u]列出PID, [p]列出帐号
kill 结束进程 kill -9 PID [9]强制结束,[15]正常结束,[l]列出可用的kill信号
killall 要刪除某個服務 killall -9 httpd
free 显示内存状态 free -m -------->以M为单位显示
uptime 显示目前系统开机时间
dmesg 显示开机信息 demsg | more
nice 设置优先权 nice -n -5 vi & ----->用 root 給一個 nice 植為 -5 ，用於執行 vi
renice 调整已存在优先权
runlevel 显示目前的runlevel
depmod 分析可载入模块的相依性
lsmod 显示已载入系统的模块
modinfo 显示kernel模块的信息
insmod 载入模块
modprobe 自动处理可载入模块
rmmod 删除模块
chkconfig 检查，设置系统的各种服务 chkconfig --list ----->列出各项服务状态
ntsysv 设置系统的各种服务
cpio 备份文件
ftp

Linux 内存释放
#先看看内存使用状况
[root@node1 ~]# free -m
total used free shared buffers cached
Mem: 8004 6557 1446 0 163 5630
-/+ buffers/cache: 763 7240
Swap: 1983 0 1983
#把内存里的数据暂时写到硬盘里
[root@node1 ~]# sync
#修改 /proc/sys/vm/drop_caches文件
[root@node1 ~]# echo 3 > /proc/sys/vm/drop_caches
[root@node1 ~]# cat /proc/sys/vm/drop_caches
#再看内存
[root@node1 ~]# free -m
total used free shared buffers cached
Mem: 8004 631 7372 0 0 60
-/+ buffers/cache: 570 7433
Swap: 1983 0 1983
终于释放出来了

#### F.Linux网络管理

1）统计80端口连接数
netstat -nat | grep -i "80" | wc -l
2）统计httpd协议连接数
ps -ef | grep httpd | wc -l
3）统计已连接上的，状态为“established'
netstat -na | grep ESTABLISHED | wc -l
4）查出哪个IP地址连接最多，将其封了。
netstat -na | grep ESTABLISHED | awk '{print$5}' | awk -F : '{print$1}' | sort | uniq -c | sort -r +0n
netstat - na | grep SYN | awk '{print$5}' | awk -F : '{print$1}' | sort | uniq -c | sort -r +0n

Linux SSH(Secure Shell) 服务

启动命令：
RedHat and Fedora Core Linux
/sbin/service sshd restart

Suse linux
/etc/rc.d/sshd restart

Debian/Ubuntu
/etc/init.d/sshd restart | service ssh start

Solaris 9 and below
/etc/init.d/sshd stop
/etc/init.d/sshd start

Solaris 10
svcadm disable ssh
svcadm enable ssh

AIX
stopsrc -s sshd
startsrc -s sshd

HP-UX
/sbin/init.d/secsh stop
/sbin/init.d/secsh start

安装启动ssh服务
#rpm -qa |grep ssh 检查是否装了SSH包

没有的话yum install openssh-server

#chkconfig --list sshd 检查SSHD是否在本运行级别下设置为开机启动
#chkconfig --level 2345 sshd on  如果没设置启动就设置下.
#service sshd restart  重新启动
#netstat -antp |grep sshd  看是否启动了22端口.确认下.
#iptables -nL  看看是否放行了22口.
#setup---->防火墙设置   如果没放行就设置放行.


#### X.Linux高级研究

这篇文章来源于Quroa的一个问答《What are some time-saving tips that every Linux user should know?》—— Linux用户有哪些应该知道的提高效率的技巧。我觉得挺好的，总结得比较好，把其转过来，并加了一些自己的理解。 首先，我想告诉大家，在Unix/Linux下，最有效率技巧的不是操作图形界面，而是命令行操作，因为命令行意味着自动化。如果你看过《你可能不知道的Shell》以及《28个Unix/Linux的命令行神器》你就会知道Linux有多强大，这个强大完全来自于命令行，于是，就算你不知道怎么去做一个环保主义的程序员，至少他们可以让你少熬点夜，从而有利于你的身体健康和性生活。下面是一个有点长的列表，正如作者所说，你并不需要知道所有的这些东西，但是如果你还在很沉重地在使用Linux的话，这些东西都值得你看一看。 （注：如果你想知道下面涉及到的命令的更多的用法，你一定要man一点。对于一些命令，你可以需要先yum或apt-get来安装一下，如果有什么问题，别忘了Google。如果你要Baidu的话，我仅代表这个地球上所有的生物包括微生物甚至细菌病毒和小强BS你到宇宙毁灭）

基础
学习 Bash 。你可以man bash来看看bash的东西，并不复杂也并不长。你用别的shell也行，但是bash是很强大的并且也是系统默认的。（学习zsh或tsch只会让你在很多情况下受到限制）
学习 vim 。在Linux下，基本没有什么可与之竞争的编译辑器（就算你是一个Emacs或Eclipse的重度用户）。你可以看看《简明vim攻略》和 《Vim的冒险游戏》以及《给程序员的Vim速查卡》还有《把Vim变成一个编程的IDE》等等。
了解 ssh。明白不需要口令的用户认证（通过ssh-agent, ssh-add），学会用ssh翻墙，用scp而不是ftp传文件，等等。你知道吗？scp 远端的时候，你可以按tab键来查看远端的目录和文件（当然，需要无口令的用户认证），这都是bash的功劳。
scp -r root@10.37.10.24:/root/Desktop/linux64 /root/Desktop/ (remote copy between2Linux)

熟悉bash的作业管理，如： &, Ctrl-Z, Ctrl-C, jobs, fg, bg, kill, 等等。当然，你也要知道Ctrl+\（SIGQUIT）和Ctrl+C （SIGINT）的区别。
简单的文件管理 ： ls 和 ls -l (你最好知道 “ls -l” 的每一列的意思), less, head, tail 和 tail -f, ln 和 ln -s (你知道明白hard link和soft link的不同和优缺点), chown, chmod, du (如果你想看看磁盘的大小 du -sk *), df, mount。当然，原作者忘了find命令。
基础的网络管理： ip 或 ifconfig, dig。当然，原作者还忘了如netstat, ping, traceroute, 等
理解正则表达式，还有grep/egrep的各种选项。比如： -o, -A, 和 -B 这些选项是很值得了解的。
学习使用 apt-get 和 yum 来查找和安装软件（前者的经典分发包是Ubuntu，后者的经典分发包是Redhat），我还建议你试着从源码编译安装软件。

开机流程简介
1、載入 BIOS 的硬體資訊，並取得第一個開機裝置的代號；
2、讀取第一個開機裝置的 MBR 的 boot Loader (亦即是 lilo, grub, spfdisk 等等) 的開機資訊；
3、載入 Kernel 作業系統核心資訊， Kernel 開始解壓縮，並且嘗試驅動所有硬體裝置；
4、Kernel 執行 init 程式並取得 run-level 資訊；
5、init 執行 /etc/rc.d/rc.sysinit 檔案；
6、啟動核心的外掛模組 (/etc/modprobe.conf)；
7、init 執行 run-level 的各個批次檔( Scripts )；
8、init 執行 /etc/rc.d/rc.local 檔案；
9、執行 /bin/login 程式，並等待使用者登入；
10、登入之後開始以 Shell 控管主機。
在/etc/rc.d/rc3.d內,以S开头的为开机启动,以K开头的为关闭,接着的数字代表执行顺序
GRUB vga设定
彩度\解析度 640x480 800x600 1024x768 1280x1024 bit
256 769 771 773 775 8 bit
32768 784 787 790 793 15 bit
65536 785 788 791 794 16 bit
16.8M 786 789 792 795 32 bit

日常
在 bash 里，使用 Ctrl-R 而不是上下光标键来查找历史命令。
在 bash里，使用 Ctrl-W 来删除最后一个单词，使用 Ctrl-U 来删除一行。请man bash后查找Readline Key Bindings一节来看看bash的默认热键，比如：Alt-. 把上一次命令的最后一个参数打出来，而Alt-* 则列出你可以输入的命令。
回到上一次的工作目录： cd –  （回到home是 cd ~）
使用 xargs。这是一个很强大的命令。你可以使用-L来限定有多少个命令，也可以用-P来指定并行的进程数。如果你不知道你的命令会变成什么样，你可以使用xargs echo来看看会是什么样。当然， -I{} 也很好用。示例：
find . -name \*.py | xargs grep some_function

cat hosts | xargs -I{} ssh root@{} hostname
pstree -p 可以帮你显示进程树。（读过我的那篇《一个fork的面试题》的人应该都不陌生）
使用 pgrep 和 pkill 来找到或是kill 某个名字的进程。 (-f 选项很有用).
了解可以发给进程的信号。例如：要挂起一个进程，使用 kill -STOP [pid]. 使用 man 7 signal 来查看各种信号，使用kill -l 来查看数字和信号的对应表

使用 nohup 或  disown (保持不挂起）       如果你要让某个进程运行在后台。
使用netstat -lntp来看看有侦听在网络某端口的进程。当然，也可以使用 lsof。

查看某一端口的占用情况： lsof -i:端口号

在bash的脚本中，你可以使用 set -x 来debug输出。使用 set -e 来当有错误发生的时候abort执行。考虑使用 set -o pipefail 来限制错误。还可以使用trap来截获信号（如截获ctrl+c）。
在bash 脚本中，subshells (写在圆括号里的) 是一个很方便的方式来组合一些命令。一个常用的例子是临时地到另一个目录中，例如：
# do something in current dir
(cd /some/other/dir; other-command)
# continue in original dir
在 bash 中，注意那里有很多的变量展开。如：检查一个变量是否存在: ${name:?error message}。如果一个bash的脚本需要一个参数，也许就是这样一个表达式 input_file=${1:?usage: $0 input_file}。一个计算表达式： i=$(( (i + 1) % 5 ))。一个序列： {1..10}。 截断一个字符串： ${var%suffix} 和 ${var#prefix}。 示例： if var=foo.pdf, then echo ${var%.pdf}.txt prints “foo.txt”.
通过 <(some command) 可以把某命令当成一个文件。示例：比较一个本地文件和远程文件 /etc/hosts： diff /etc/hosts <(ssh somehost cat /etc/hosts)
了解什么叫 “here documents” ，就是诸如 cat <<EOF 这样的东西。
在 bash中，使用重定向到标准输出和标准错误。如： some-command >logfile 2>&1。另外，要确认某命令没有把某个打开了的文件句柄重定向给标准输入，最佳实践是加上 “</dev/null”，把/dev/null重定向到标准输入。
使用 man ascii 来查看 ASCII 表。
在远端的 ssh 会话里，使用 screen 或 dtach 来保存你的会话。（参看《28个Unix/Linux的命令行神器》）
http://en.flossmanuals.net/gnulinux/index.php
要来debug Web，试试curl 和 curl -I 或是 wget 。我觉得debug Web的利器是firebug，curl和wget是用来抓网页的，呵呵。
把 HTML 转成文本： lynx -dump -stdin
如果你要处理XML，使用 xmlstarlet
对于 Amazon S3， s3cmd 是一个很方便的命令（还有点不成熟）
在 ssh中，知道怎么来使用ssh隧道。通过 -L or -D (还有-R) ，翻墙神器。
Mac: ssh username@server -p port
你还可以对你的ssh 做点优化。比如，.ssh/config 包含着一些配置：避免链接被丢弃，链接新的host时不需要确认，转发认证，以前使用压缩（如果你要使用scp传文件）：
TCPKeepAlive=yes
ServerAliveInterval=15
ServerAliveCountMax=6
StrictHostKeyChecking=no
Compression=yes
ForwardAgent=yes
如果你有输了个命令行，但是你改变注意了，但你又不想删除它，因为你要在历史命令中找到它，但你也不想执行它。那么，你可以按下 Alt-# ，于是这个命令关就被加了一个#字符，于是就被注释掉了。

数据处理

了解 sort 和 uniq 命令 (包括 uniq 的 -u 和 -d 选项).
了解用 cut, paste, 和 join 命令来操作文本文件。很多人忘了在cut前使用join。
如果你知道怎么用sort/uniq来做集合交集、并集、差集能很大地促进你的工作效率。假设有两个文本文件a和b已解被 uniq了，那么，用sort/uniq会是最快的方式，无论这两个文件有多大（sort不会被内存所限，你甚至可以使用-T选项，如果你的/tmp目录很小）
cat a b | sort | uniq > c   # c is a union b 并集
cat a b | sort | uniq -d > c   # c is a intersect b 交集
cat a b b | sort | uniq -u > c   # c is set difference a - b 差集
了解和字符集相关的命令行工具，包括排序和性能。很多的Linux安装程序都会设置LANG 或是其它和字符集相关的环境变量。这些东西可能会让一些命令（如：sort）的执行性能慢N多倍（注：就算是你用UTF-8编码文本文件，你也可以很安全地使用ASCII来对其排序）。如果你想Disable那个i18n 并使用传统的基于byte的排序方法，那就设置export LC_ALL=C （实际上，你可以把其放在 .bashrc）。如果这设置这个变量，你的sort命令很有可能会是错的。
了解 awk 和 sed，并用他们来做一些简单的数据修改操作。例如：求第三列的数字之和： awk ‘{ x += $3 } END { print x }’。这可能会比Python快3倍，并比Python的代码少三倍。
使用 shuf 来打乱一个文件中的行或是选择文件中一个随机的行。
了解sort命令的选项。了解key是什么（-t和-k）。具体说来，你可以使用-k1,1来对第一列排序，-k1来对全行排序。
Stable sort (sort -s) 会很有用。例如：如果你要想对两例排序，先是以第二列，然后再以第一列，那么你可以这样： sort -k1,1 | sort -s -k2,2
我们知道，在bash命令行下，Tab键是用来做目录文件自动完成的事的。但是如果你想输入一个Tab字符（比如：你想在sort -t选项后输入<tab>字符），你可以先按Ctrl-V，然后再按Tab键，就可以输入<tab>字符了。当然，你也可以使用$’\t’。
如果你想查看二进制文件，你可以使用hd命令（在CentOS下是hexdump命令），如果你想编译二进制文件，你可以使用bvi命令（http://bvi.sourceforge.net/ 墙）
另外，对于二进制文件，你可以使用strings（配合grep等）来查看二进制中的文本。
对于文本文件转码，你可以试一下 iconv。或是试试更强的 uconv 命令（这个命令支持更高级的Unicode编码）
如果你要分隔一个大文件，你可以使用split命令（split by size）和csplit命令（split by a pattern）。

系统调试

如果你想知道磁盘、CPU、或网络状态，你可以使用 iostat, netstat, top (或更好的 htop), 还有 dstat 命令。你可以很快地知道你的系统发生了什么事。关于这方面的命令，还有iftop, iotop等（参看《28个Unix/Linux的命令行神器》）
要了解内存的状态，你可以使用free和vmstat命令。具体来说，你需要注意 “cached” 的值，这个值是Linux内核占用的内存。还有free的值。
Java 系统监控有一个小的技巧是，你可以使用kill -3 <pid> 发一个SIGQUIT的信号给JVM，可以把堆栈信息（包括垃圾回收的信息）dump到stderr/logs。
使用 mtr 会比使用 traceroute 要更容易定位一个网络问题。
如果你要找到哪个socket或进程在使用网络带宽，你可以使用 iftop 或 nethogs。
Apache的一个叫 ab 的工具是一个很有用的，用quick-and-dirty的方式来测试网站服务器的性能负载的工作。如果你需要更为复杂的测试，你可以试试 siege。
如果你要抓网络包的话，试试 wireshark 或 tshark。
了解 strace 和 ltrace。这两个命令可以让你查看进程的系统调用，这有助于你分析进程的hang在哪了，怎么crash和failed的。你还可以用其来做性能profile，使用 -c 选项，你可以使用-p选项来attach上任意一个进程。
了解用ldd命令来检查相关的动态链接库。注意：ldd的安全问题
使用gdb来调试一个正在运行的进程或分析core dump文件。参看我写的《GDB中应该知道的几个调试方法》
学会到 /proc 目录中查看信息。这是一个Linux内核运行时记录的整个操作系统的运行统计和信息，比如： /proc/cpuinfo, /proc/xxx/cwd, /proc/xxx/exe, /proc/xxx/fd/, /proc/xxx/smaps.

如果你调试某个东西为什么出错时，sar命令会有用。它可以让你看看 CPU, 内存, 网络, 等的统计信息。
使用 dmesg 来查看一些硬件或驱动程序的信息或问题。
sar 命令行的常用格式： sar [options] [-A] [-o file] t [n]
在命令行中，n 和t 两个参数组合起来定义采样间隔和次数，t为采样间隔，是必须有的参数，n为采样次数，是可选的，默认值是1，-o file表示将命令结果以二进制格式存放在文件中，file 在此处不是关键字，是文件名。options 为命令行选项，sar命令的选项很多，下面只列出常用选项：
-A：所有报告的总和。
-u：CPU利用率
-v：进程、I节点、文件和锁表状态。
-d：硬盘使用报告。
-r：没有使用的内存页面和硬盘块。
-g：串口I/O的情况。
-b：缓冲区使用情况。
-a：文件读写情况。
-c：系统调用情况。
-R：进程的活动情况。
-y：终端设备活动情况。
-w：系统交换活动。

下面将举例说明。
例一：使用命令行 sar -u t n
例如，每5秒采样一次，连续采样5次，观察CPU 的使用情况，并将采样结果以二进制形式存入当前目录下的文件filename中，需键入如下命令：
# sar -u -o filename 5 5
屏幕显示：
Linux 2.6.18-164.el5 (zjm_242_97)       03/28/2011
09:58:17 AM       CPU     %user     %nice   %system   %iowait    %steal     %idle
09:58:22 AM       all      2.25      0.00      1.62      0.33      0.00     95.80
09:58:27 AM       all      2.55      0.00      1.92      0.27      0.00     95.25
09:58:32 AM       all      1.77      0.00      1.30      0.42      0.00     96.50
09:58:37 AM       all      1.65      0.00      0.93      0.33      0.00     97.10
09:58:42 AM       all      1.82      0.00      1.40      0.05      0.00     96.73
Average:          all      2.01      0.00      1.43      0.28      0.00     96.28

在显示内容包括：
%usr：CPU处在用户模式下的时间百分比。
%system：CPU处在系统模式下的时间百分比。
%iowait：CPU等待输入输出完成时间的百分比。
%idle：CPU空闲时间百分比。
在所有的显示中，我们应主要注意%iowait和%idle，%wio的值过高，表示硬盘存在I/O瓶颈， %idle值高，表示CPU较空闲，如果%idle值高但系统响应慢时，有可能是CPU等待分配内存， 此时应加大内存容量。%idle值如果持续低于10，那么系统的CPU处理能力相对较低，表 明系统中最需要解决的资源是CPU。
如果要查看二进制文件filename中的内容，则需键入如下sar命令：#sar -u -f filename
可见，sar命令即可以实时采样，又可以对以往的采样结果进行查询。

例二：使用命行sar -v t n
例如，每5秒采样一次，连续采样5次，观察核心表的状态，需键入如下命令：
# sar -v 5 5
屏幕显示：
Linux 2.6.18-164.el5 (zjm_242_97)       03/28/2011

10:00:04 AM dentunusd   file-sz  inode-sz  super-sz %super-sz  dquot-sz %dquot-sz  rtsig-sz %rtsig-sz
10:00:09 AM    380230      4080    393279         0      0.00         0      0.00         0      0.00
10:00:14 AM    380214      3570    393152         0      0.00         0      0.00         0      0.00
10:00:19 AM    380183      3570    393167         0      0.00         0      0.00         0      0.00
10:00:24 AM    380164      3060    393050         0      0.00         0      0.00         0      0.00
10:00:29 AM    380176      3570    393148         0      0.00         0      0.00         0      0.00
Average:       380193      3570    393159         0      0.00         0      0.00         0      0.00

显示内容包括：
inode-sz：目前核心中正在使用或分配的i节点表的表项数，由核心参数 MAX-INODE控制。
file-sz： 目前核心中正在使用或分配的文件表的表项数，由核心参数MAX-FILE控 制。
super-sz：溢出出现的次数。
rrqm/s:   每秒进行 merge 的读操作数目.即 delta(rmerge)/s
wrqm/s:  每秒进行 merge 的写操作数目.即 delta(wmerge)/s
r/s:           每秒完成的读 I/O 设备次数.即 delta(rio)/s
w/s:         每秒完成的写 I/O 设备次数.即 delta(wio)/s
rsec/s:    每秒读扇区数.即 delta(rsect)/s
wsec/s:  每秒写扇区数.即 delta(wsect)/s
rkB/s:      每秒读K字节数.是 rsect/s 的一半,因为每扇区大小为512字节.(需要计算)
wkB/s:    每秒写K字节数.是 wsect/s 的一半.(需要计算)
avgrq-sz: 平均每次设备I/O操作的数据大小 (扇区).delta(rsect+wsect)/delta(rio+wio)
avgqu-sz: 平均I/O队列长度.即 delta(aveq)/s/1000 (因为aveq的单位为毫秒).
await:    平均每次设备I/O操作的等待时间 (毫秒).即 delta(ruse+wuse)/delta(rio+wio)
svctm:   平均每次设备I/O操作的服务时间 (毫秒).即 delta(use)/delta(rio+wio)
%util:      一秒中有百分之多少的时间用于 I/O 操作,或者说一秒中有多少时间 I/O 队列是非空的.即 delta(use)/s/1000 (因为use的单位为毫秒)

tps：该设备每秒的传输次数（Indicate the number of transfers per second that were issued to the device.）。“一次传输”意思是“一次I/O请求”。多个逻辑请求可能会被合并为“一次I/O请求”。“一次传输”请求的大小是未知的。

kB_read/s：每秒从设备（drive expressed）读取的数据量；kB_wrtn/s：每秒向设备（drive expressed）写入的数据量；kB_read：读取的总数据量；kB_wrtn：写入的总数量数据量；这些单位都为Kilobytes。