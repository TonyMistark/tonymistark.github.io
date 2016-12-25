### Django中的Model继承

Django中的model继承和Python中的类继承非常相似, 只不过你要选择具体的实现方式：
让父 model 拥有独立的数据库；还是让父 model 只包含基本的公共信息，而这些信息
只能由子 model 呈现。

#### Django中有三种继承关系：

1.通常，你只是想用父 model 来保存那些你不想在子 model 中重复录入的信息。父类是不使用的也就是不生成单独的数据表，这种情况下使用抽象基类继承 Abstract base classes。

2.如果你想从现有的Model继承并让每个Model都有自己的数据表，那么使用多重表继承Multi-table inheritance。

3.最后，如果你只想在 model 中修改 Python-level 级的行为，而不涉及字段改变。 代理 model (Proxy models) 适用于这种场合。

* Abstract base classes

如果你想把某些公共信息添加到很多 model 中，抽象基类就显得非常有用。你编写完基类之后，在 Meta 内嵌类中设置 abstract=True ，该类就不能创建任何数据表。然而如果将它做为其他 model 的基类，那么该类的字段就会被添加到子类中。抽象基类和子类如果含有同名字段，就会导致错误(Django 将抛出异常)。

```
class CommonInfo(models.Model):
    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
 
    class Meta:
        abstract = True
 
class Student(CommonInfo):
    home_group = models.CharField(max_length=5)
```