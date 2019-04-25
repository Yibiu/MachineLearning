# Learn Python

[TOC]

《Python编程：从入门到实践》

《Python基础教程(第三版)》



## 一：简介

### 1.1 注释

```python
# python 注释
```

### 1.2 用户输入

```python
message = input("This is marked words:")
```





## 二：变量和数据类型

### 2.1 字符串

#### 2.1.1 表述

```python
'...'
"..."
"..." + "..."
```

#### 2.1.2 操作：

```python
len(): 字符串长度
title(): 首字母大写
upper(): 转大写
lower(): 转小写
strip(): 去首尾空格
rstrip(): 去尾部空格
lstrip(): 去首部空格
center(): 两边填充char让字符串居中
find()：查找item第一次出现的位置，未找到返回-1
join(): 使用字符串连接列表digits的元素
split(): 将字符串按char分割成列表
replace(): 替换字符串

isalnum(), isalpha(), isdecimal(), isdigit(), isidentifier(), islower(), isnumeric(), isprintable(), isspace(), istitle(), isupper()
```

#### 2.1.3 字符串转列表

```python
digits = list('hello')
digits = ['h','e','l','l','o']
```

### 2.2 数字

#### 2.2.1 整数

```python
2 + 3 = 5
3 - 2 = 1
2 * 3 = 6
3 / 2 = 1.5
3 ** 2 = 9 (乘方)
2 + 3 * 4 = 14
```

#### 2.2.2 浮点数

带小数点的都称作浮点数，计算结果包含的小数位数可能是不确定的。

```python
0.1 + 0.1 = 0.2
2 * 0.1 = 0.2
0.2 + 0.1 = 0.30000000000000004
```

#### 2.2.3 数字和字符(串)转换

```python
字符(串) = str(数字)
数字 = int(字符串)
```





## 三：列表

### 3.1 列表表达

```python
digits = ['item1', 'item2', 'item3', ..., 'itemN']
digits = [['item1',1], ['item2',2], ...]
```

### 3.2 列表访问

下标访问：

```python
digits[0] = 'item1'
digits[1] = 'item2'
...
digits[-1] = 'itemN'
digits[-2] = 'itemN-1'
...
```

### 3.3 列表操作

#### 3.3.1 修改

```python
digits[0] = 'new_item1'
```

#### 3.3.2 增加

```python
# 尾部增加
digits.append('itemN+1')
# 非尾部插入
digits.insert(0, 'item0')

# 增加多值
digits = digits + ['itemN+1', 'itemN+2', 'itemN+3']
digits.extend(['itemN+1', 'itemN+2', 'itemN+3'])
```

#### 3.3.3 删除

```python
del digits[0]
# 尾部pop
get_item = digits.pop()
# 非尾部pop
get_item = digits.pop(0)

# 值删除(只删除第一个出现的值)
digits.remove('item1')
```

#### 3.3.4 杂项

```python
# 列表清空
digits.clear()

# 列表复制
digits_copy = digits.copy()

# 计算出现次数
digits.count('item1')

# 第一次出现的索引
id = digits.index('itemN')

# 列表相加
[1, 2, 3] + [4, 5, 6] = [1, 2, 3, 4, 5, 6]

# 列表乘法
'python' * 3 = 'pythonpythonpython'
[40] * 5 = [40, 40, 40, 40, 40]
[None] * 3 = [None, None, None]
```

### 3.4 列表组织

#### 3.4.1 永久排序

```python
# 永久排序(改变原本列表)
digits.sort()
digits.sort(reverse=True)
```

#### 3.4.2 临时排序

```python
# 临时排序(不改变原本列表，生成排序列表)
sorted(digits)
sorted(digits, reverse=True)
```

#### 3.4.3 列表反转

```python
digits.reverse()
```

#### 3.4.4 列表长度

```python
len(digits)
```





## 四：操作列表

### 4.1 遍历列表

```python
for digit in digits:
	print(digit)
    ...
```

### 4.2 数值列表

```python
# range左闭右开：1，2，3，4
for value in range(1,5):
	print(value)
	...
    
# range 转列表
digits = list(range(1,5))

# 统计操作
min(digits)
max(digits)
sum(digits)
```

### 4.3 列表推断

```python
digits = [vaule**2 for value in range(1,5)]
```

### 4.4 列表截取

#### 4.4.1 切片

切片范围表述与range相同：左闭右开。

```python
slices = digits[0:3]
slices = digits[:3]
slices = digits[0:]
slices = digits[-2:] # 最后两位数
slices = digits[0:10:1]

# 切片赋值
slices = [1, 2, 3, 4, 5]
slices[1:1] = [6, 6, 6]		#slices = [1, 6, 6, 6, 2, 3, 4, 5]
```

#### 4.4.2 复制列表

```python
# copy_one和digits指向同一个列表
copy_one = digits

# copy_two为digits的复制
copy_two = digits[:]
```

### 4.5 元组(固定的列表)

为了区别普通列表，元组采用`()` 替代 `[]`。

```python
tuple1 = (20, 50)
tuple2 = ('item1', 'item2')
```

其操作与列表基本相同，只是不能修改元素值，但可以修改元组变量本身（tuple1和tuple2）。

将列表转化为元组：

```python
tuple1 = tuple(digits)
```





## 五：字典

字典其实就是键值对，即map。

### 5.1 字典表达

```python
maps = {'key1':'value1', 'key2':'value2' }

# 从列表创建字典
digits = [('key1', 'item1'), ('key2', 'item2')]
maps = dict(digits)
```

### 5.2 字典访问

键访问。

```python
maps['key1'] = 'value1'
```

### 5.3 字典操作

#### 5.3.1 增加

```python
maps['key3'] = 'value3'
```

#### 5.3.2 修改 

```python
maps['key1'] = 'new_value'
```

#### 5.3.3 删除

```python
del maps['key1']
```

#### 5.3.4 排序

```python
new_maps = sorted(maps)
```

### 5.4 遍历字典

```python
# key
for key in maps.keys():
	...
for key in maps:
	...
    
# value
for value in maps.values():
	...
    
# key and value
for key,value in maps.items():
	...
```

### 5.5 嵌套

列表可以嵌套字典，字典也可以嵌套列表。

```python
# maps in digits
maps1 = {'key1':'value1', 'key2':'value2'}
maps2 = {'key1':'value1', 'key2':'value2'}
maps3 = {'key1':'value1', 'key2':'value2'}
digits = [maps1, maps2, maps3]

# digits in maps
maps = {'key1':['value1_1', 'value1_2']}

# maps in maps
maps = {
	'maps_key1': {
		'key1':'value1',
		'key2':'value2'
	},
	'maps_key2': {
		'key1':'value1',
		'key2':'value2'
	}
}
```





## 六：控制语句

### 6.1 if语句

#### 6.1.1 条件测试

return `True` or `False `:

```python
value1 > value2
value1 < value2
value1 >= value2
value1 <= value2
value1 == value2
value1 != value2
value1 is value2
value2 is not value2
value in value_list
value not in value_list
```

#### 6.1.2 if表达式

```python
# if
if condition_test：
	do something

# if...else...
if condition_test:
	do something
else:
	do something

# if...elif...else...
if condition_test1:
	do something
elif condition_test2:
	do something
else:
	do something
```

### 6.2 while语句

#### 6.2.1 while表达式

```python
while condition_test:
	do something
```

#### 6.2.2 循环退出

```python
# jump out of while
while condition_test:
	do something
	break
	
# skip loop once
while condition_test:
	do something
	continue
```

### 6.3 for语句

```python
for value in value_list:
	do something
```





## 七：函数

### 7.1 定义

```python
def function_name(param1, param2, *var_params1, **var_params2):
	......
    return ret
```

`*var_params1` 传递任意个数参数，传递形式为列表；

`**var_params2` 传递任意个数参数，传递形式为字典。

### 7.2 值传递和引用传递

一般参数传递按值传递：

```python
实参 -> 形参 -> 实参未变化
```

列表传递时按引用传递：

```python
实参 -> 实参 -> 实参变化
```

### 7.3 函数导入

```python
# 模块导入形式(批量导入)
import module

# 导入时指定模块别名
import module as module_alias

# 函数导入形式
from module import function1, function2
from module import *

# 导入时指定函数别名
from module import function as function_alias
```





## 八：类

### 8.1 定义

```python
class CFather():
	# 构造函数
	def __init__(self, param1, param2):
		# 成员变量定义和初始化
		...
        
	# 成员函数
    def function1(self, param):
		...
```

### 8.2 继承

```python
class CChild(CFather):
	# 构造函数
    def __init__(self, param1, param2):
		super().__init__(param1, param2)
		...
        
	# 重写
    def function1(self, param):
		...

	def function2(self):
		...
```

......





