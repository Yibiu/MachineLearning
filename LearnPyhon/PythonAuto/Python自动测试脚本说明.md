# Python自动测试脚本说明

[TOC]

## 一：环境搭建

### 1.1 编译环境搭建

#### 1.1.1 安装Python3.7

选择Win32版本。

安装完确定环境变量配置成功：

```python
python --version
```

#### 1.1.2 安装依赖库

```python
# 更新pip
python -m pip install --upgrade pip

# 安装prettytable
pip install prettytable

# 安装configparser
pip install configparser

# 安装pyinstaller(打包时使用)
pip install pyinstaller

# 安装其他必要库
# ...
```

安装PyMouse：(https://blog.csdn.net/alex1997222/article/details/80518397)

1. 安装PyWin32(对应Python3.7版本)(https://github.com/mhammond/pywin32)；
2. 安装PyHook

生成可运行脚本打包命令：

```python
pyinstaller -F -p 第三方库路径 脚本名称.py
```

### 1.2 运行环境搭建

使用python打包工具，例如pyinstaller，将写好的脚本打包成exe，可以直接执行，无需配置额外环境。



## 二：脚本目录说明

- src：源码目录
- exe：可执行文件目录
- py_config.ini：脚本运行配置文件
- README：脚本说明文档





NOTE:

如果Python的鼠标操作没有效果则可能是编译软件的编译器问题。需要使用其他编译器重新编译，或者使用按键精灵等脚本工具写脚本。

