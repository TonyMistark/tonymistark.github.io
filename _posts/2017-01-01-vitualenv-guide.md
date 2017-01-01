---
layout: post
title:  "Python虚拟环境：Vitualenv"
date:   2017-01-01 12:52:40 +0800
categories: python update
---

Virtualenv

使用背景：

如果我们要同时开发多个应用程序，那这些应用程序都会共用一个Python，就是安装在系
统的Python 3。如果应用A需要Python 2.7，而应用B需要Python2.6怎么办？这种情况
下，每个应用可能需要各自拥有一套“独立”的Python运行环境。virtualenv就是用来为
一个应用创建一套“隔离”的Python运行环境。

注释：Virtual + environment ->Virtualenv  即虚拟环境

功能：

1.在没有权限的情况先安装新套件

2.不同应用可以使用不同套件版本

3.套件升级不影响其他应用

安装Virtualenv：

sudo apt-get install python-virtualenv

使用方法：

virtualenv  [要创建的虚拟环境的名称]

注释：例如：virtualenv my_virtual 回车，就会在当前面目录创建一个叫my_virtual
的文件夹，即创建的一个虚拟环境

默认情况下，虚拟环境会依赖系统环境中的site packages,就是说系统中已经安装好的第
三方package也会安装在虚拟环境中，如果不想依赖这些package，那么就加上参数
“---site-packages”来创建虚拟环境即：

virtualenv --no-site-packages [要创建的虚拟环境的名称]

启动虚拟环境：

cd进刚刚创建的my_virtual

cd my_virtual

source ./bin/activate

注意此时命令行多了一个(my_virtual)，my_virtual为虚拟环境的名称，接下来所有的
模块都只会安装到该目录中去。

退出虚拟环境：

deactivate

======我是双分割线========

接下来再来一个更高级的玩具

Virtualenvwrapper

Virtualenwrapper 是Virtual 的扩展，用于方便管理多个虚拟环境

功能：

可以在一个目录下创建多个虚拟环境

新增，删除，复制虚拟环境

切换虚拟环境

安装Virtualenwrapper

注意：virtualenvwrapper是安装在系统中，我一开始还以为是要安装在virtualenv里
面的，这里注意下

sudo easy_install virtualenvwrapper

注释：安装完成还不能使用Virtualenvwrapper,默认virtualenvwrapper安装在
/usr/local/bin 目录下，需要运行virtualenvwrapper.sh文件才行，现在需要先打开
virtualenvwrapper.sh文件，文件路径为：
/usr/local/bin/virtualenvwrapper.sh,（find it，and open it)

打开virtualenvwrapper.sh之后就会看见有环境设置的指导，英文的如下：

# Setup:
#
#  1. Create a directory to hold the virtual environments.
#     (mkdir $HOME/.virtualenvs).
#  2. Add a line like "export WORKON_HOME=$HOME/.virtualenvs"
#     to your .bashrc.
#  3. Add a line like "source /path/to/this/file/virtualenvwrapper.sh"
#     to your .bashrc.
#  4. Run: source ~/.bashrc
#  5. Run: workon
#  6. A list of environments, empty, is printed.
#  7. Run: mkvirtualenv temp
#  8. Run: workon
#  9. This time, the "temp" environment is included.
# 10. Run: workon temp
# 11. The virtual environment is activated.
#

提炼出来就是：

创建一个目录用来存放虚拟环境的文件夹

     mkdir $HOME/.virtualenvs

     2.在~/.bashrc文件中添加行：export WORKON_HOME=$HOME/.virtualenvs

     3.在~/.bashrc文件中添加行：source /path/to/this/file/virtualenvwrapper.sh

     4.运行：source ~/.bashrc

现在：玩具virtualenvwrapper就能跑了

使用命令：

列出虚拟环境列表

workon 或者 lsvirtualenv

新建虚拟环境

mkvirtualenv [要创建的虚拟环境的名称]

启动/切换虚拟环境

workon [虚拟环境的名称]

删除虚拟环境

rmvirtualenv [要删除的虚拟环境的名称]

离开虚拟环境

deactivate




