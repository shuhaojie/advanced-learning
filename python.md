# # Python

## 一、 正则

### 1. 基本

正则表达式是用来匹配**字符串的**

- `\d`：匹配一个数字

- `\w`：匹配一个字母或数字
- `.`：匹配任意字符
- `\s`：匹配空格

```python
import re

re.match(r'00\d', '007')  # 匹配成功
re.match(r'00\d', '00A')  # 匹配失败
re.match(r'00\w', '00A')  # 匹配失败
re.match(r'00.', '00A')  # 匹配成功
```

### 2. 不定长字符

要匹配不定长的字符，可以采用如下形式：

- `*`表示任意个字符(包括0个)
- `+`表示至少一个字符
- `?`表示0个或1个字符
- `{n}`表示n个字符
- `{n,m}`表示n-m个字符

```python
import re

# 1. \d{3}表示匹配3个数字，例如'010'；
# 2. \s可以匹配一个空格，所以\s+表示至少有一个空格，例如匹配' '等；
# 3. \d{3,8}表示3-8个数字，例如'1234567'。
re.match(r'\d{3}\s+\d{3,8}', '003 2134')  # 匹配成功
```

### 3. 精准匹配`[]`

更精确地匹配，可以用`[]`表示范围，`[]`表示范围内的

````python
import re

# 匹配一个数字、字母(不论大小写)或者下划线
# 注意1: \_可以不要\
# 注意2: a-z不能写成a-Z，否则报错
re.match(r'[0-9a-zA-Z\_]', 'Z')  # 匹配成功
# 匹配至少由一个数字、字母(不论大小写)或者下划线组成的字符串
re.match(r'[0-9a-zA-Z\_]+', 'Z*')  # 匹配成功
````

### 4. 其他匹配符

- `｜`: 表示或，`A|B`表示匹配A或B

  ```python
  import re
  
  re.match(r'P|python', 'python')  # 匹配成功
  ```

- `^`：表示行的开头

  ```python
  import re
  re.match(r'^\d{3}\-\d{3,8}', '010-12345')
  ```

- `$`：表示行的结尾。例如`^py$`，整行匹配，只能匹配`'py'`

  ```
  import re
  re.match(r'^py$', 'py')
  ```

### 5. 分组

除了简单地判断是否匹配之外，正则表达式还有提取子串的强大功能。用`()`表示的就是要提取的分组（Group）。比如：

```python
import re
m = re.match(r'^(\d{3})-(\d{3,8})$', '010-12345')
m.group(0) # '010-12345'
m.group(1) # '010'
m.group(2) # '12345'
m.groups() # ('010', '12345')
```

`group(0)`永远是与整个正则表达式相匹配的字符串，`group(1)`、`group(2)`……表示第1、2、……个子串。

### 6. 贪婪匹配

正则匹配默认是贪婪匹配，也就是匹配尽可能多的字符

```python
import re
re.match(r'^(\d+)(0*)$', '102300').groups()  # ('102300', '')
```

由于前面的`\d+`会贪婪匹配，把所有的数字都匹配到，此时后面的`(0*)`就匹配不到东西了，也就是一个空字符串。此时可以采用非贪婪匹配，**可以加个`?`让`\d+`采用非贪婪匹配**

```python
import re
re.match(r'^(\d+?)(0*)$', '102300').groups()
```

### 7. re.compile

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

### 8. re.findall

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

### 9. re.search

扫描整个字符串并返回第一个成功的匹配，如果没有匹配，就返回一个None

### 10. re.sub

将匹配到的数据进⾏替换

例子1："张明 98分"，将98替换为100

```python
import re

a = "张明 100分"
re.sub(r'\d+', "100", a)
```