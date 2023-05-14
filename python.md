# # Python

## 一、 正则

### 1. 字符

正则表达式是用来匹配**字符串的**。

 `re.search`返回第一个匹配，此外还会返回匹配的字符索引范围。

```python
res = re.search(r'def', 'abcdefghijklmn')
print(res)  # <re.Match object; span=(3, 6), match='def'>, 表示匹配成功, 并且匹配的字符索引范围是(3,6)
print(res[0]) # def
```

#### （1）`.`

`.`：匹配除了换行符`\n`之外的任意字符

```python
re.search(r'...', '_*_') # <re.Match object; span=(0, 3), match='_*_'>
```

#### （2）`\`

转义字符，使后一个字符改变原来的意思。对于一些特殊字符，例如`.`,`\`等在匹配的时候，可以使用转义字符

```python
re.search(r'a\.c', 'a.c') # <re.Match object; span=(0, 3), match='a.c'>
re.search(r'a\\c', 'a\c') # <re.Match object; span=(0, 3), match='a\\c'>
```

####  （3）`[]`

- `[...]`: 匹配字符集，只要出现在[]里的规划内容，都算符合匹配规则
  - `[aeiou]`:匹配aeiou字符
  - `[a-z]`: 匹配小写字母
  - `[A-Z]`:匹配大写字母
  - `[0-9]`: 匹配任何数字

````python
re.match(r'[0-9a-zA-Z_]', 'Z')  # 由于Z出现在[]里，匹配成功
````

- `[^...]`: 出现在[^]里的规划内容，都不符合匹配规则
  - `[^aeiou]`:匹配非aeiou字符
  - `[^a-z]`:匹配非小写字母
  - `[^A-Z]`:匹配非大写字母
  - `[0-9]`: 匹配非数字

```python
re.match(r'[^0-9a-zA-Z_]', 'Z')  # 由于Z出现在[]里，匹配失败
```

### 2. 预定义字符集

#### （1）`\d`

`\d`：匹配一个数字

`\D`: 匹配任何一个非数字

```python
re.search(r'\d\dabc', '.*abc') # 匹配失败
re.search(r'\D\Dabc', '.*abc') # <re.Match object; span=(0, 5), match='.*abc'>
```

#### （2）`\w`

`\w`：匹配一个字母，数字，下划线

`\W`：匹配任何非字母、数字、下划线

```python
re.search(r'\w\wabc', '_1abc') # <re.Match object; span=(0, 5), match='_1abc'>
re.search(r'\W\Wabc', '_1abc') # 匹配失败
```

#### （3）`\s` 

`\s`：匹配空格

`\S`：匹配非空格

```python
re.search(r'a\sc', 'a c') # <re.Match object; span=(0, 3), match='a c'>
re.search(r'abc', 'a c') # 匹配失败
```

### 3. 边界上的匹配

#### （1）`^`

`^`：匹配字符串的起始点

```python
re.search(r'^a', 'abcd')  # <re.Match object; span=(0, 1), match='a'>
```

#### （2）`$`

`$`：匹配字符串的最后面

```python
re.search(r'c$', 'abc') # <re.Match object; span=(2, 3), match='c'>
```

#### （3）`\A`

`\A`：匹配字符串的起始点

```python
re.search(r'\Aa', 'abc')  # <re.Match object; span=(0, 1), match='a'>
```

#### （4）`\Z`

`\Z`：匹配字符串的最后面

```python
re.search(r'c\Z', 'abc')  # <re.Match object; span=(2, 3), match='c'>
```

#### （5）`\B`

`\B`：匹配除了字符串最后面的其他位置

```python
re.search(r'ful\B', 'colorful') # 匹配失败
```

### 4. 数量上的匹配

这几个都是对**前一个字符**进行数量上的匹配

#### （1）`*`

`*`：匹配前一个字符0次或无限次。例如`abc*`可以匹配`abccc`或者`ab`

```python
re.search("Go*d", "Goooooood") # <re.Match object; span=(0, 9), match='Goooooood'>
re.search("G*d", "Goooooood") # <re.Match object; span=(8, 9), match='d'>
```

第一个例子，会将o字母匹配7次

**第二个例子，会将G字母匹配0次**

#### （2）`+`

`+`：匹配前一个字符1次或无限次。例如`abc+`可以匹配`abccc`或者`abc`

```python
re.search("Go+d", "Goooooood") # <re.Match object; span=(0, 9), match='Goooooood'>
re.search("G+d", "Goooooood") # 匹配失败
```

#### （3）`?`

`?`：匹配前一个字符0次或1次。例如`abc+`可以匹配`ab`或者`abc`

```python
re.search(r'abc?', 'ab')  # <re.Match object; span=(0, 2), match='ab'>
re.search(r'abc?d', 'abcd')  # <re.Match object; span=(0, 4), match='abcd'>
```

#### （4）`{n}`

`{n}`：匹配前一个字符n次

```python
re.search("Go{7}d", "Goooooood") # <re.Match object; span=(0, 9), match='Goooooood'>
```

#### （5）`{n,}`

`{n}`：匹配前一个字符n次或n次以上

```python
re.search("Go{2,}d", "Goooooood") # <re.Match object; span=(0, 9), match='Goooooood'>
```

#### （6）`{n, m}`

`{n,m}`：匹配前一个字符n到m次

```python
re.search(r'\d{3}\s+\d{3,8}', '003 2134')  # <re.Match object; span=(0, 8), match='003 2134'>
```

### 5. 逻辑与分组

#### （1）`|`  

`｜`: 左右表达式任意匹配一个。如果`|` 没有出现在`()`中，它的匹配范围是整个表达式。

```python
re.match(r'P|python', 'python')  # <re.Match object; span=(0, 6), match='python'>
re.match(r'P|python', 'Python')  # <re.Match object; span=(0, 1), match='P'>, 因为进行全文匹配
re.match(r'(P|p)ython', 'Python')  # <re.Match object; span=(0, 6), match='Python'>
```

#### （2）`()`

- 以整个括号内的字符为一个单位

```python
re.search('(abc)*d', 'abcabcd') # <re.Match object; span=(0, 7), match='abcabcd'>
re.search('a(123|456)c', 'a456c')  # <re.Match object; span=(0, 5), match='a456c'>
```

- `(?P<name>exp)` : 对分组进行命名

```python
res = re.search('(?P<name>abc){2}d', 'abcabcd')
res[0] # abcabcd
res.group('name')  # 'abc'
```

注意**只需要关注命名的后面部分即可, 前面部分并没有实际意义, 只是用来命名而已**。

- `(?P=name)`：引用别名为`<name>`的分组匹配到的字符串。

```python
re.search('(?P<id1>\d)abc(?P=id1)', '6abc6')  # <re.Match object; span=(0, 5), match='6abc6'>
re.search('(?P<id2>\d)abc(?P=id2)', '2abc6')  # 匹配失败
```

实际案例

```python
import re

s = re.compile(fr'(?P<F_100375>^[一二三四五六七八九十零]+[、\.\s]+.*)', )
c = s.match('一、项目概况')
c.group('F_100375')  # 一、项目概况
```

最后的`.*`匹配任意字符

### 6. 贪婪匹配

正则匹配默认是贪婪匹配，也就是匹配尽可能多的字符

```python
re.match(r'^(\d+)(0*)$', '102300').groups()  # ('102300', '')
```

`\d+`会贪婪匹配，把所有的数字都匹配到，此时后面的`(0*)代表的是0个0。

```python
re.match(r'^(\d+?)(0*)$', '102300').groups()
```

### 7. 字符组合

#### （1）`\d+`

由前面的知识知道，`\d`匹配的是一个数字，`+`：匹配前一个字符1次或无限次。

#### （2）`.*`

bbb

### 8. re.compile

当我们在Python中使用正则表达式时，`re`模块内部会干两件事情：

1. 编译正则表达式，如果正则表达式的字符串本身不合法，会报错；
2. 用编译后的正则表达式去匹配字符串。

如果一个正则表达式要重复使用几千次，出于效率的考虑，我们可以预编译该正则表达式，接下来重复使用时就不需要编译这个步骤了，直接匹配。

```python
import re
re_telephone = re.compile(r'^(\d{3})-(\d{3,8})$')
re_telephone.match('010-12345').groups() # ('010', '12345')
re_telephone.match('010-8086').groups() # ('010', '8086')
```

### 9. re.findall

以列表的形式返回能匹配的子串。

例子1：字符串a = "not 404 found 张三 99 深圳"，每个词中间是空格，用正则过滤掉英文和数字，最终输出"张三 深圳"。

```python
import re

a = "not 404 found 张三 99 深圳"
# 筛选数字或者字母
res = re.findall(r'\d+|[a-zA-Z]+', a)
str_list = a.split(' ')
for r in res:
    str_list.remove(r)
c = " ".join(str_list)
```

例子2：将以下网址提取出域名

```python
import re

# 提取出域名
s2 = """http://www.interoem.com/messageinfo.asp?id=35`
http://3995503.com/class/class09/news_show.asp?id=14
https://lib.wzmc.edu.cn/news/onews.asp?id=769
http://www.zy-ls.com/alfx.asp?newsid=377&id=6
https://www.fincm.com/newslist.asp?id=415"""
# [s]?表示0个或者1个s
# [\w\.\-]+: 表示多个字母或者数字或者.或者-，注意中括号只需要满足一个
pattern = r'http[s]?://[\w\.\-]+'
domain_names = re.findall(pattern, s2)
print(domain_names)
```

### 10. re.search

扫描整个字符串并返回第一个成功的匹配，如果没有匹配，就返回一个None

### 11. re.sub

将匹配到的数据进⾏替换

例子1："张明 98分"，将98替换为100

```python
import re

a = "张明 100分"
re.sub(r'\d+', "100", a)
```