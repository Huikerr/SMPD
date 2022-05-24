# <div style="text-align: center;font-size:28pt"><font face="黑体">屏幕监测平台（SMPD）</font></div>

<div style="font-size:14pt">&emsp;&emsp;该平台为实现屏幕检测小项目,基本需求就是摄像头对准一排屏幕，后台获取屏幕信息，并对每个屏幕标定区域，然后进行检测，如果有某一台屏幕坏了，就提醒工作人员进行处理。</div>

## 一、技术栈
`python==3.8`，`django==3.2.6`，`opencv-python==4.5.5.64`,`AILabel`

登入账户：root
登入密码：123456789

## 二、项目生成

###  <font face="宋体体" style="font-size:16pt">1、创建虚拟环境</font>

```shell
conda create -n SMPD python=3.8 # 创建虚拟环境
conda activate SMPD # 激活环境
conda deactivate # 退出环境
```

### 2 安装相关依赖包

```shell
pip install Django==3.2.6
pip install drf-yasg==1.20.0
pip install djangorestframework==3.12.4
pip install opencv-python==4.5.5.64

```

### 3 生成工程文件

```shell
django-admin startproject application # 创建工程
mkdir apps
python ../manage.py startapp smpd
python manage.py makemigrations
python manage.py migrate
```

## 三、文件结构


## 四、关键代码结构

## 五、项目打包

### 5.1 环境搭建

```shell
# pyinstaller可以帮助我们打包解析项目文件，并生成相对应的配置
pip install pyinstaller
# 生成.spec文件
pyi-makespec -D manage.py
```

生成文件``manage.spec``

```python
# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='manage',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='manage',
)
```

### 5.3 生成exe可执行文件

```
pyinstaller manage.spec
```

### 六、项目部署

windows使用gunicorn，以下是在linux下操作的

### 6.1 安装uWSGI

```shell
sudo pip3 install uwsgi==2.0.18 -i https://pypi.douban.com/simple/ # 安装
sudo pip3 freeze | grep -i 'uwsgi' # 查看是否安装
```

### 6.2 配置uWSGI

```shell
touch uwsgi.ini # 在与settings同一目录下创建uwsgi.ini文件
# 配置uwsgi.ini文件
[uwsgi] # 文件以[uwsgi]开头
# socket=192.168.1.112:8000 套接字方式的IP地址：端口号 此模式需要有nginx
http=192.168.1.112:8000 # Http通信方式的IP地址：端口号
chdir=/home/jetson/Desktop/EVMS
wsgi-file=applications/wsgi.py
process=2
threads=2
pidfile=uwsgi.pid
daemonize=uwsgi.log
master=True
uwsgi --ini uwsgi.ini # 启动
uwsgi --stop uwsgi.pid # 停下
ps aux | grep 'uwsgi' # 查看是否启动
```

### 6.3 添加uWSGI到开机自启

```shell
cd /etc/init.d	# 终端进入Linux启动文件夹
# 在/etc/init.d/ 文件夹下创建一个shell脚本名为 uwsgi.sh 添加如下内容 ：
#!/bin/bash -e
/usr/bin/uwsgi --ini /data/wwwroot/traffic_scheduling/web/uwsgi.ini
chmod 755 uwsgi.sh	# 修改uwsgi.sh的文件权限
update-rc.d uwsgi.sh defaults 99	# 添加到开机自动启动
```

![image-20220517150756296](https://cdn.jsdelivr.net/gh/Huikerr/ImageBed/typora/image-20220517150756296.png)

![image-20220517150851301](https://cdn.jsdelivr.net/gh/Huikerr/ImageBed/typora/image-20220517150851301.png)

> ``uWSGI``常见问题汇总
>
> 1.启动失败：端口被占用
>
> ​	原因：有其他进程占用``uWSGI``启动的端口;
>
> ​	解决方案：可执行``sudo lsof -i: port``查询出具体进程；杀掉进程后，重新启动``uWSGI``
>
> 2、停止失败：``stop``无法关闭``uWSGI``
>
> ​	原因：重复启动``uWSGI``，导致``pid``文件中进程号失准
>
> ​	解决方案：``ps``出``uWSGI``进程，手动``kill``掉

### 6.4 Nginx安装

> 什么是``Nginx``：
>
> ``Nginx``是轻量级的高性能``Web``服务器，提供了诸如``HTTP``代理和反向代理、负载均衡等一系列重要特性
>
> C语言编写，执行效率高，
>
> ``nginx``作用
>
> ​	-负载均衡，多台服务器轮流处理请求
>
> ​	-反向代理
>
> 原理：
>
> ​	-客户端请求``nginx``，再由``nginx``请求转发``uWSGI``运行的``django``

## 模板

### 传统的MVC

![image-20220518100951800](https://cdn.jsdelivr.net/gh/Huikerr/ImageBed/typora/image-20220518100951800.png)

![image-20220518101037956](https://cdn.jsdelivr.net/gh/Huikerr/ImageBed/typora/image-20220518101037956.png)

![image-20220518101200485](https://cdn.jsdelivr.net/gh/Huikerr/ImageBed/typora/image-20220518101200485.png)

![image-20220518101241160](https://cdn.jsdelivr.net/gh/Huikerr/ImageBed/typora/image-20220518101241160.png)

![image-20220518101316894](https://cdn.jsdelivr.net/gh/Huikerr/ImageBed/typora/image-20220518101316894.png)

![image-20220518101733976](https://cdn.jsdelivr.net/gh/Huikerr/ImageBed/typora/image-20220518101733976.png)



## 小命令

```shell
#	如果你不知道 Django 源码在你系统的哪个位置，运行以下命令：
python -c "import django; print(django.__path__)"

```



## 参考文献

[1]:https://www.djangoproject.com/	"django官网"
[2]:http://ailabel.com.cn/public/ailabel/api/index.html#1	"AILabel"
[3]:https://blog.csdn.net/weixin_45543571/article/details/115705967	"关于在django框架中在admin页面下添加自定义按钮并实现功能"