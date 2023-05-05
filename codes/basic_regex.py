import re

s = re.compile(fr'(?P<F_100375>^[一二三四五六七八九十零]+[、\.\s]+.*)', )
c = s.match('一、项目概况')

print(c.group('F_100375'))
