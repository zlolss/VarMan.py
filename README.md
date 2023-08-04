# VarMan

一个辅助监听变量赋值变化的类，基本用法类似dict类型
 
 
# 应用场景示例

- webapp中开关量的前后台同步，前台需要显示开关状态并且可以控制开关，后台亦然。
- 需要监听变量改变并回调相应方法的情形


# 使用方法

```shell
pip install varman
```

```python
import varman
var = varman.VarMan()
```

## 获取改变值的变量名


```python
var.a = 1
print(var.POPMODIFY(tag = 'tag1'))
var.a = 1
print(var.POPMODIFY(tag = 'tag1'))
var.a = 2
print(var.POPMODIFY(tag = 'tag1'))
var.b = 3
print(var.POPMODIFY(tag = 'tag1'))
print(var.POPMODIFY())
```

    {'a'}
    set()
    {'a'}
    {'b'}
    {'a', 'b'}
    

## 设置回调函数


```python
# 对应变量“c”的回调函数
@var.ONMODIFY('c')
def fun(pre, nxt):
    print(f'pre c:{pre}, next c:{nxt}')  
```


```python
var.c = 1
```

    pre c:None, next c:1
    


```python
var['c'] = 4
```

    pre c:1, next c:4
    


```python
# var中任意变量改变时回调
@var.ONMODIFYANY
def func(varname, pre, nxt):
    print(f'var:{varname}; pre: {pre}, next:{nxt}')
```


```python
var.c = 1
```

    pre c:4, next c:1
    var:c; pre: 4, next:1
    


```python
var.a = 5
```

    var:a; pre: 2, next:5
    


```python
var.dd = []
```

    var:dd; pre: None, next:[]
    


```python
# 只能监听基本变量，或变量的id改变，无法监听list、dict等类型的内部更改
var.dd.append(1)
```


```python
# 移除监听器
var.REMOVELISTENER('c')
var.c = 8
```

    var:c; pre: 1, next:8
    


```python
# 移除对任意变量的监听器
var.REMOVEANYLISTENER()
var.c = 10
```

## 作为iter类型使用(类似dict)


```python
for key in var:
    print(f'{key}:{var[key]}')
```

    a:5
    b:3
    c:10
    dd:[1]
    


```python
# 带前缀“_”的变量将隐式调用，不会自动监听赋值状态，也不会被迭代
# 不允许“__”前缀
var._d = 5
for key in var:
    print(f'{key}:{var[key]}')
```

    a:5
    b:3
    c:10
    dd:[1]
    


```python
print(var._d)
```

    5
    


```python
def fun2(**params):
    print(params)
fun2(**var)
```

    {'a': 5, 'b': 3, 'c': 10, 'dd': [1]}
    


```python
# 实例化的同时添加变量
var2 = varman.VarMan(d = 8, e=10)
print(var2)
```

    {'d': 8, 'e': 10}
    


```python
var2
```




    VarMan({'d': 8, 'e': 10})




# todo?

- 删除变量