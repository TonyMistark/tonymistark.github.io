---
layout: post
title:  "Django之Model继承介绍"
date:   2016-12-25 22:32:40 +0800
categories: jekyll update
---

### Django中的Model继承

Django中的model继承和Python中的类继承非常相似, 只不过你要选择具体的实现方式：
让父 model 拥有独立的数据库；还是让父 model 只包含基本的公共信息，而这些信息
只能由子 model 呈现。

#### Django中有三种继承关系：

1.通常，你只是想用父model来保存那些你不想在子 model 中重复录入的信息。父类是不
使用的也就是不生成单独的数据表,这种情况下使用抽象基类继承Abstract base classes。

2.如果你想从现有的Model继承并让每个Model都有自己的数据表，那么使用多重表继承
Multi-table inheritance。

3.最后，如果你只想在 model 中修改 Python-level 级的行为，而不涉及字段改变。
代理 model (Proxy models) 适用于这种场合。

* Abstract base classes

如果你想把某些公共信息添加到很多 model 中，抽象基类就显得非常有用。你编写完基类
之后，在 Meta 内嵌类中设置 abstract=True ，该类就不能创建任何数据表。然而如果
将它做为其他 model 的基类，那么该类的字段就会被添加到子类中。抽象基类和子类如果
含有同名字段，就会导致错误(Django 将抛出异常)。

```
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
 
    class Meta:
        abstract = True
 
class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
```

sql结果

```
CREATE TABLE "myapp_student" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "age" integer unsigned NOT NULL,
    "home_group" varchar(5) NOT NULL
)
```

只为Student model 生成了数据表，而CommonInfo不能做为普通的Django model使用，
因为它是一个抽象基类。他即不生成数据表，也没有manager，更不能直接被实例化和保存。

对很多应用来说，这种继承方式正是你想要的。它提供一种在 Python 语言层级上提取公
共信息的方式，但在数据库层级上，每个子类仍然只创建一个数据表，在JPA中称作
TABLE_PER_CLASS。这种方式下，每张表都包含具体类和继承树上所有父类的字段。因为
多个表中有重复字段，从整个继承树上来说，字段是冗余的。

* Meta继承

创建抽象基类的时候，Django会将你在基类中所声明的有效的 Meta 内嵌类做为一个属性。
如果子类没有声明它自己的 Meta 内嵌类，它就会继承父类的 Meta 。子类的Meta也可以
直接继承父类的 Meta 内嵌类，对其进行扩展。例如：

```
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    class Meta:
        abstract = True
        ordering = ['name']
 
class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
    class Meta(CommonInfo.Meta):
        db_table = 'student_info'
```

sqlall结果：

```
CREATE TABLE "student_info" (
    "id" integer NOT NULL PRIMARY KEY,
    "name" varchar(100) NOT NULL,
    "age" integer unsigned NOT NULL,
    "home_group" varchar(5) NOT NULL
)
```
按照我们指定的名称student_info生成了table。

继承时，Django 会对基类的 Meta 内嵌类做一个调整：在安装 Meta 属性之前，
Django会设置abstract=False。 这意味着抽象基类的子类不会自动变成抽象类。当然，
你可以让一个抽象类继承另一个抽象基类，不过每次都要显式地设置 abstract=True 。

对于抽象基类而言，有些属性放在Meta内嵌类里面是没有意义的。例如，包含 db_table 
将意味着所有的子类(是指那些没有指定自己的 Meta 内嵌类的子类)都使用同一张数据表，
一般来说，这并不是我们想要的。

谨慎使用 related_name (Be careful with related_name)
如果你在 ForeignKey 或 ManyToManyField 字段上使用related_name属性，你必须
总是为该字段指定一个唯一的反向名称。但在抽象基类上这样做就会引发一个很严重的问
题。因为 Django 会将基类字段添加到每个子类当中，而每个子类的字段属性值都完全相同
(这里面就包括 related_name)。注：这样使用ForeignKey或ManyToManyField反向指
定时就无法确定是指向哪个子类了。



