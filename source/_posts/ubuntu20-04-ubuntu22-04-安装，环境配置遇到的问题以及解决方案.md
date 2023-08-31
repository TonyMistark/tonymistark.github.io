---
layout: layout
title: ubuntu20.04/ubuntu22.04 安装，环境配置遇到的问题以及解决方案
date: 2023-08-29 14:48:08
tags: ubuntu
categories: ubuntu
---
### build a python env on ubuntu20.04
#### fix virtualenvwarpper
(Ubuntu20.04安装virtualenv方法以及安装过程中遇到的问题处理)[https://blog.csdn.net/qq_42296146/article/details/108291436]

问题：bash: /usr/local/bin/virtualenvwrapper.sh: No such file or directory

ubuntu18及以上版本，virtualenvwrapper.sh被安装到了家目录下的.local/bin/中，非原来的/usr/local/bin/中

/usr/share/virtualenvwrapper/virtualenvwrapper.sh 实际安装的位置，只要把这个地址配置到.brashrc之后就可以正常运行了。

```
export WORKON_HOME=$HOME/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3.10
export VIRTUALENVWRAPPER_VIRTUALENV=/usr/bin/virtualenv
source /usr/share/virtualenvwrapper/virtualenvwrapper.sh
```
#### install a local git repo updata

```
$ git clone git@bitbucket.org:ginolegaltech/updata.git
$ cd updata
& python3.10 setup.py install
$ rm -rf build/
$ rm -rf updata.egg-info/
```

##### fix ImportError: cannot import name 'html5lib' from 'pip._vendor' (/home/ice/.virtualenvs/310/lib/python3.10/site-packages/pip/_vendor/__init__.py)

```
curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
```



#### bash 显示当前所在分支

在.bashrc文件追加如下代码

```
function git_branch {
   branch="`git branch 2>/dev/null | grep "^\*" | sed -e "s/^\*\ //"`"
   if [ "${branch}" != "" ];then
       if [ "${branch}" = "(no branch)" ];then
           branch="(`git rev-parse --short HEAD`...)"
       fi
       echo " ($branch)"
   fi
}

export PS1='\u@\h \[\033[01;36m\]\w\[\033[01;32m\]$(git_branch)\[\033[00m\] \$ '
```

#### install virtualbox

https://computingforgeeks.com/install-virtualbox-6-on-ubuntu-linux/

```
# step 1
sudo apt update
sudo apt -y upgrade
sudo reboot

# step 2
#Download
curl https://www.virtualbox.org/download/oracle_vbox_2016.asc | gpg --dearmor > oracle_vbox_2016.gpg
curl https://www.virtualbox.org/download/oracle_vbox.asc | gpg --dearmor > oracle_vbox.gpg
#Install on system
sudo install -o root -g root -m 644 oracle_vbox_2016.gpg /etc/apt/trusted.gpg.d/
sudo install -o root -g root -m 644 oracle_vbox.gpg /etc/apt/trusted.gpg.d/

# step 3
# ubuntu 22.04 
echo "deb [arch=amd64] http://download.virtualbox.org/virtualbox/debian focal contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list

# Ubuntu 20.04/18.04:
echo "deb [arch=amd64] http://download.virtualbox.org/virtualbox/debian $(lsb_release -sc) contrib" | sudo tee /etc/apt/sources.list.d/virtualbox.list

# step 4
sudo apt update
sudo apt install linux-headers-$(uname -r) dkms
sudo apt install virtualbox-6.1
```

virtualbox start error:

```
$ sudo /sbin/vboxconfig 
[sudo] password for rcrozier:           
vboxdrv.sh: Stopping VirtualBox services.
vboxdrv.sh: Starting VirtualBox services.
vboxdrv.sh: You must sign these kernel modules before using VirtualBox:
  vboxdrv vboxnetflt vboxnetadp
See the documenatation for your Linux distribution..
vboxdrv.sh: Building VirtualBox kernel modules.
debconf: DbDriver "config": /var/cache/debconf/config.dat is locked by another process: Resource temporarily unavailable
vboxdrv.sh: Failed to enroll secure boot key..
vboxdrv.sh: failed: modprobe vboxdrv failed. Please use 'dmesg' to find out why.

There were problems setting up VirtualBox.  To re-start the set-up process, run
  /sbin/vboxconfig
as root.  If your system is using EFI Secure Boot you may need to sign the
kernel modules (vboxdrv, vboxnetflt, vboxnetadp, vboxpci) before you can load
them. Please see your Linux system's documentation for more information.
```

搜索了很多解决方案都无法处理，最后还是仔细看了报错信息，这里其实有一个很重要的提示信息`Secure Boot you may need to sign the kernel modules`

最后搜到https://askubuntu.com/questions/900118/vboxdrv-sh-failed-modprobe-vboxdrv-failed-please-use-dmesg-to-find-out-why 这个答案最后的以解决答案：

The above answer probably works fine, but if you want an easier time for it:

I was able to solve it by

booting into the BIOS and going > advanced (f7) > boot > scroll down to "secure boot" > change "Windows EUFI mode" to "other OS"

My virtualbox works perfectly now.

最后对于为为的解决方案就是进入BIOS系统之后，和这个答案每个硬件平台的BIOS版本会有所不同(我的硬件三HUAWEI MateBook X Pro 2022)找到"secure boot"关键词对应的默认直是enable，为改为disable，第一次修改没有其作用，是应推出的时候没有保存，第二次再修改选择save and exit，再进入ubuntu启动virtualbox就可以正常运作了。


最近在ubuntu22.04 安装virtualbox的时候遇到另外还有一个报错：
### vboxdrv.sh: failed: Cannot change group vboxusers for device /dev/vboxdrv.
```
执行：/sbin/vboxconfig
输出如下报错
root@ice:~# /sbin/vboxconfig
vboxdrv.sh: Stopping VirtualBox services.
vboxdrv.sh: Starting VirtualBox services.
vboxdrv.sh: Building VirtualBox kernel modules.
vboxdrv.sh: failed: Cannot change group vboxusers for device /dev/vboxdrv.

There were problems setting up VirtualBox.  To re-start the set-up process, run
  /sbin/vboxconfig
as root.  If your system is using EFI Secure Boot you may need to sign the
kernel modules (vboxdrv, vboxnetflt, vboxnetadp, vboxpci) before you can load
them. Please see your Linux system's documentation for more information.
```
* 创建vboxusers group
```
$ sudo groupadd vboxusers
```
* 把当前user 加入到这个group， 你替换这里的ice
```
$ sudo usermod -a -G vboxusers ice
```
* 检查是否添加成功
```
$ grep vboxusers /etc/group
# 输出为:
# vboxusers:x:1003:ice
```
* 然后运行
```
$ sudo /sbin/vboxconfig
```