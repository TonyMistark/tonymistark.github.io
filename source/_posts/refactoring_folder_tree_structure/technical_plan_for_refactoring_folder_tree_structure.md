---
title: MongoDB 文件夹树结构重构技术方案
categories:
  - refactoring_folder_tree_structure
date: 2025-04-22 00:24:57
tags:
---

# MongoDB 文件夹树结构重构技术方案

## 当前问题分析

当前系统使用嵌套的树形结构存储文件夹关系，导致：
1. 并发修改时需要锁定整个树结构，成为性能瓶颈
2. 大规模数据时查询和修改效率低下
3. 难以实现部分树的加载和更新

## 重构方案：离散化存储

### 1. 数据模型重构

#### 当前模型 (嵌套树)
```python
class RootFolder(Document):
    customer = ReferenceField('Customer')
    tree = DictField()  # 嵌套的树结构
```

#### 新模型 (离散存储)
```python
class Folder(Document):
    customer = ReferenceField('Customer')
    domain = ReferenceField('Domain')
    name = StringField(required=True)
    parent = ReferenceField('self', null=True)  # 自引用，根目录parent为None
    path = StringField()  # 可选，存储完整路径如"/root/folder1"
    is_root = BooleanField(default=False)
    created_at = DateTimeField(default=datetime.utcnow)
    meta = {
        'indexes': [
            'customer',
            'domain',
            'parent',
            'path'
        ]
    }
```

### 2. 迁移方案

#### 迁移脚本
```python
def migrate_tree_to_discrete(customer_id):
    customer = Customer.objects.get(id=customer_id)
    
    for domain in Domain.objects.filter(customer=customer):
        root_folder = RootFolder.objects.get(customer=customer, domain=domain)
        
        # 创建根文件夹
        root = Folder(
            customer=customer,
            domain=domain,
            name='root',
            parent=None,
            path='/',
            is_root=True
        ).save()
        
        # 递归迁移子树
        def migrate_node(node, parent, current_path):
            for name, child in node.items():
                folder_path = f"{current_path}{name}/"
                folder = Folder(
                    customer=customer,
                    domain=domain,
                    name=name,
                    parent=parent,
                    path=folder_path
                ).save()
                
                if isinstance(child, dict):
                    migrate_node(child, folder, folder_path)
        
        migrate_node(root_folder.tree, root, '/')
```

### 3. 并发控制优化

新模型下不再需要全局锁，可以采用：
1. 文档级锁 (只锁定正在修改的文件夹)
2. 乐观并发控制 (使用版本号字段)

```python
class Folder(Document):
    # ... 其他字段同上
    version = IntField(default=1)
    
    def update_folder(self, **kwargs):
        current_version = self.version
        self.update(inc__version=1, **kwargs)
        return self.__class__.objects(
            id=self.id,
            version=current_version
        ).update_one(inc__version=1, **kwargs)
```

### 4. 查询优化

#### 获取子树
```python
def get_subtree(folder_id, depth=None):
    folder = Folder.objects.get(id=folder_id)
    
    # 使用聚合框架查询子树
    pipeline = [
        {"$match": {"_id": folder.id}},
        {
            "$graphLookup": {
                "from": "folder",
                "startWith": "$_id",
                "connectFromField": "_id",
                "connectToField": "parent",
                "as": "children",
                "maxDepth": depth-1 if depth else None
            }
        }
    ]
    
    result = Folder.objects.aggregate(*pipeline)
    return next(result)
```

#### 获取路径
```python
def get_path(folder_id):
    folder = Folder.objects.get(id=folder_id)
    
    if folder.path:
        return folder.path.split('/')
    
    # 如果没有path字段，动态计算
    path = []
    current = folder
    while current:
        path.insert(0, current.name)
        current = current.parent
    return path
```

### 5. 文档模型调整

```python
class Doc(Document):
    # 原有字段
    folder_id = ReferenceField('Folder')  # 改为引用新的Folder模型
    # ... 其他字段
```

### 6. API调整

1. 创建文件夹:
   ```python
   def create_folder(customer_id, domain_id, name, parent_id=None):
       parent = Folder.objects.get(id=parent_id) if parent_id else None
       path = f"{parent.path}{name}/" if parent else f"/{name}/"
       
       folder = Folder(
           customer=customer_id,
           domain=domain_id,
           name=name,
           parent=parent,
           path=path
       ).save()
       return folder
   ```

2. 移动文件夹:
   ```python
   def move_folder(folder_id, new_parent_id):
       folder = Folder.objects.get(id=folder_id)
       new_parent = Folder.objects.get(id=new_parent_id)
       
       # 更新路径
       new_path = f"{new_parent.path}{folder.name}/"
       
       # 更新所有子文件夹路径
       def update_children_paths(parent_folder, old_base, new_base):
           children = Folder.objects(parent=parent_folder)
           for child in children:
               child.path = child.path.replace(old_base, new_base, 1)
               child.save()
               update_children_paths(child, old_base, new_base)
       
       old_path = folder.path
       folder.parent = new_parent
       folder.path = new_path
       folder.save()
       
       update_children_paths(folder, old_path, new_path)
   ```

## 实施步骤

1. **备份数据**: 完整备份当前数据库
2. **开发环境测试**: 在开发环境实现并测试迁移脚本
3. **性能测试**: 对新模型进行并发性能测试
4. **分阶段部署**:
   - 先部署新模型代码，保持双写
   - 运行迁移脚本
   - 验证数据一致性
   - 切换读取到新模型
   - 移除旧模型代码
5. **监控**: 部署后密切监控性能和数据一致性

## 回滚方案

1. 保留旧模型代码和数据
2. 如果出现问题，切换回旧模型
3. 使用备份恢复数据

## 性能预期

1. 并发性能提升: 从全局锁变为文档级操作
2. 查询效率: 简单查询更快，复杂树查询可能需要优化索引
3. 存储空间: 可能略有增加，但换来更好的扩展性

这种重构将使系统能够更好地处理并发操作和大规模数据，同时保持数据一致性。
