import re
m = "2017-11-21"
a = re.compile('-')
b = a.sub('/',m)
print b