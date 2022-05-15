# 屏幕监测平台（SMPD）

## 一、技术栈

``python==3.8``，``django==3.2.6``，``opencv-python==4.5.5.64``,``AILabel``

## 二、项目生成

### 1  创建虚拟环境

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







## 参考文献

[1]:https://www.djangoproject.com/	"django官网"
[2]:http://ailabel.com.cn/public/ailabel/api/index.html#1	"AILabel"



